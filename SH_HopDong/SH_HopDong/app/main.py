import os
import uuid
from datetime import datetime, timedelta
from typing import Optional, List

from fastapi import FastAPI, Request, UploadFile, File, Form, HTTPException, Depends, Query
from fastapi.responses import RedirectResponse, FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.ocr import extract_text_from_pdf, extract_text_from_image
from app.core.parser import parse_contract_text
from app.db.base import Base, engine, get_db
from app.db import crud, schemas
from app.db import models  # ensure models are imported

from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_
from docx import Document
import orjson
import html
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
UPLOAD_DIR = os.path.join(PROJECT_ROOT, 'uploads')
OUTPUT_DIR = os.path.join(PROJECT_ROOT, 'outputs')

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

app = FastAPI(
    title="Số hóa hợp đồng",
    openapi_tags=[
        {"name": "contracts", "description": "Quản lý hợp đồng"},
        {"name": "types", "description": "Quản lý loại hợp đồng"},
        {"name": "partners", "description": "Quản lý đối tác"},
        {"name": "departments", "description": "Quản lý phòng ban"},
        {"name": "tags", "description": "Quản lý nhãn"},
    ]
)

# Cấu hình CORS và encoding
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware để thêm UTF-8 headers
@app.middleware("http")
async def add_utf8_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["Content-Type"] = "text/html; charset=utf-8"
    return response

app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, 'static')), name="static")
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, 'templates'))

# Cấu hình templates để sử dụng UTF-8
templates.env.globals.update({
    'charset': 'utf-8'
})

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


@app.get("/")
def index(request: Request, q: Optional[str] = Query(default=None), db: Session = Depends(get_db)):
    total = crud.count_contracts(db)
    processed = crud.count_processed_contracts(db)
    pending = crud.count_pending_contracts(db)
    expiring = crud.count_expiring_contracts(db)
    stats = {"total": total, "processed": processed, "pending": pending, "expiring": expiring}
    print(f"DEBUG - Stats: {stats}")  # Debug log
    contracts = crud.list_contracts(db=db, limit=20, q=q)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "contracts": contracts,
        "stats": stats,
        "q": q or ""
    })

@app.get("/test/{contract_id}")
def test_route(contract_id: int):
    """Test route"""
    print(f"TEST - Contract ID: {contract_id}")
    return {"message": f"Test route for contract {contract_id}"}

@app.get("/search")
def search_page(request: Request):
    """Trang tải lên hợp đồng (đã thay đổi từ trang tìm kiếm)"""
    return templates.TemplateResponse("search.html", {
        "request": request
    })


@app.get("/api/contract-types")
def get_contract_types(db: Session = Depends(get_db)):
    """API endpoint to get all contract types"""
    contract_types = crud.get_contract_types(db)
    result = []
    for ct in contract_types:
        result.append({
            "id": ct.id,
            "name": ct.name or "",
            "description": ct.description or ""
        })
    return result

@app.get("/api/contracts")
def get_contracts(contract_type_id: Optional[int] = None, db: Session = Depends(get_db)):
    """API endpoint to get contracts by type"""
    try:
        query = db.query(models.Contract).options(joinedload(models.Contract.contract_type))

        if contract_type_id:
            query = query.filter(models.Contract.contract_type_id == contract_type_id)

        contracts = query.order_by(models.Contract.created_at.desc()).all()

        result = []
        for contract in contracts:
            result.append({
                "id": contract.id,
                "original_filename": contract.original_filename,
                "created_at": contract.created_at.isoformat(),
                "status": contract.status,
                "contract_type_name": contract.contract_type.name if contract.contract_type else None
            })

        return result
    except Exception as e:
        print(f"Error getting contracts: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get contracts")

@app.get("/api/search-in-contract")
def search_in_contract(contract_id: int, q: str, db: Session = Depends(get_db)):
    """API endpoint to search within a specific contract"""
    try:
        contract = crud.get_contract(db, contract_id)
        if not contract:
            raise HTTPException(status_code=404, detail="Contract not found")

        # Read contract text content
        text_content = ""
        if contract.text_path and os.path.exists(contract.text_path):
            with open(contract.text_path, 'r', encoding='utf-8') as f:
                text_content = f.read()

        # Search for matches
        matches = []
        if text_content and q:
            import re

            # Split text into sentences/paragraphs for better context
            sentences = re.split(r'[.!?]\s+|\n\s*\n', text_content)

            for i, sentence in enumerate(sentences):
                if q.lower() in sentence.lower():
                    # Calculate confidence based on exact match vs partial match
                    confidence = 1.0 if q.lower() == sentence.lower().strip() else 0.8

                    # Add some context around the match
                    start_idx = max(0, i - 1)
                    end_idx = min(len(sentences), i + 2)
                    context = ' '.join(sentences[start_idx:end_idx]).strip()

                    matches.append({
                        "text": context,
                        "page": (i // 10) + 1,  # Rough page estimation
                        "confidence": confidence
                    })

        return {
            "contract": {
                "id": contract.id,
                "original_filename": contract.original_filename,
                "created_at": contract.created_at.isoformat(),
                "contract_type_name": contract.contract_type.name if contract.contract_type else None
            },
            "search_term": q,
            "matches": matches[:20]  # Limit to 20 matches
        }

    except Exception as e:
        print(f"Error searching in contract: {str(e)}")
        raise HTTPException(status_code=500, detail="Search failed")

@app.get("/find")
def find_page(
    request: Request,
    q: Optional[str] = Query(default=None),
    type: Optional[str] = Query(default=None),
    id: Optional[int] = Query(default=None),
    db: Session = Depends(get_db)
):
    """Trang tìm kiếm hợp đồng (route mới)"""
    # Không lọc theo tên file bằng q; lấy tất cả rồi tìm trong nội dung
    contracts = crud.list_contracts(db=db, limit=1000, q=None)
    results: List[dict] = []
    q_norm = (q or "").strip()

    for c in contracts:
        pj = c.parsed_json or {}
        if type and pj.get("type") != type:
            continue
        snippet = ""
        found = False
        if q_norm:
            txt = ""
            try:
                if c.text_path and os.path.exists(c.text_path):
                    with open(c.text_path, "r", encoding="utf-8") as f:
                        txt = f.read()
            except Exception:
                txt = ""
            if txt:
                pattern = re.compile(re.escape(q_norm), re.IGNORECASE)
                m = pattern.search(txt)
                if m:
                    found = True
                    start = max(0, m.start() - 80)
                    end = min(len(txt), m.end() + 80)
                    piece = txt[start:end]
                    # Chỉ hiển thị đoạn trích không highlight ở danh sách kết quả
                    snippet = ("..." if start > 0 else "") + html.escape(piece) + ("..." if end < len(txt) else "")
        else:
            found = True  # không có từ khóa thì luôn hiện

        if found:
            results.append({
                "id": c.id,
                "original_filename": c.original_filename,
                "snippet": snippet,
                "type": pj.get("type"),
                "type_label": pj.get("type_label"),
            })

    preview_text = None
    preview_contract = None
    if id:
        c = crud.get_contract(db, id)
        if c:
            pj = c.parsed_json or {}
            if not type or pj.get("type") == type:
                preview_contract = c
                try:
                    with open(c.text_path, "r", encoding="utf-8") as f:
                        raw = f.read()
                    text_html = html.escape(raw)
                    if q_norm:
                        pattern = re.compile(re.escape(q_norm), re.IGNORECASE)
                        text_html = pattern.sub(lambda mm: f"<mark>{html.escape(mm.group(0))}</mark>", text_html)
                    preview_text = text_html
                except Exception:
                    preview_text = ""

    # Sử dụng template tìm kiếm riêng (có thể tạo find.html sau)
    return templates.TemplateResponse("find.html", {
        "request": request,
        "results": results,
        "q": q_norm,
        "type": type,
        "selected_id": id,
        "preview_text": preview_text,
        "preview_contract": preview_contract,
    })


@app.get("/contracts/{contract_id}")
def contract_detail(contract_id: int, request: Request, db: Session = Depends(get_db)):
    try:
        print(f"DEBUG - Accessing contract detail for ID: {contract_id}")

        # Get contract with contract_type relationship
        contract = db.query(models.Contract).options(joinedload(models.Contract.contract_type)).filter(models.Contract.id == contract_id).first()
        if not contract:
            print(f"DEBUG - Contract {contract_id} not found")
            raise HTTPException(status_code=404, detail="Không tìm thấy hợp đồng")

        print(f"DEBUG - Contract found: {contract.original_filename}")

        parsed = contract.parsed_json or {}
        parties = parsed.get("parties", {})

        print(f"DEBUG - Parsed data: {parsed}")
        print(f"DEBUG - Parties: {parties}")

        try:
            parties_json = orjson.dumps(parsed.get("parties", {}), option=orjson.OPT_INDENT_2).decode("utf-8")
            signatures_json = orjson.dumps(parsed.get("signatures", {}), option=orjson.OPT_INDENT_2).decode("utf-8")
        except Exception as json_error:
            print(f"DEBUG - JSON error: {json_error}")
            parties_json = "{}"
            signatures_json = "{}"

        # Read contract text content
        contract_text = ""
        try:
            if contract.text_path and os.path.exists(contract.text_path):
                with open(contract.text_path, "r", encoding="utf-8") as f:
                    contract_text = f.read()
                print(f"DEBUG - Contract text loaded, length: {len(contract_text)}")
            else:
                print(f"DEBUG - Text file not found: {contract.text_path}")
        except Exception as text_error:
            print(f"DEBUG - Error reading text file: {text_error}")
            contract_text = ""

        print("DEBUG - About to render template")

        return templates.TemplateResponse("detail.html", {
            "request": request,
            "contract": contract,
            "parsed": parsed,
            "parties": parties,
            "parties_json": parties_json,
            "signatures_json": signatures_json,
            "contract_text": contract_text,
        })
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in contract_detail: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Lỗi server: {str(e)}")


@app.post("/contracts/{contract_id}/delete")
def delete_contract(contract_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_contract(db, contract_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Không tìm thấy hợp đồng")
    return RedirectResponse(url="/", status_code=303)


# Đã loại bỏ route chỉnh sửa hợp đồng


@app.post("/upload")
async def upload_file(
    request: Request,
    files: List[UploadFile] = File(...),
    lang: str = Form("vie+eng"),
    contract_type_id: Optional[int] = Form(default=None),
    db: Session = Depends(get_db),
):

    if not files:
        raise HTTPException(status_code=400, detail="Vui lòng chọn tệp")

    try:
        # contract_type_id đã được truyền trực tiếp từ form
        last_contract = None
        for file in files:
            original_filename = file.filename or "uploaded"
            ext = os.path.splitext(original_filename)[1].lower()
            
            # Kiểm tra định dạng file
            if ext not in [".pdf", ".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff"]:
                continue  # Bỏ qua file không hợp lệ
            
            uid = uuid.uuid4().hex
            saved_name = f"{uid}{ext}"
            saved_path = os.path.join(UPLOAD_DIR, saved_name)
            
            # Lưu file gốc
            with open(saved_path, "wb") as f_out:
                f_out.write(await file.read())
            
            # Xử lý OCR
            try:
                if ext in [".pdf"]:
                    text = extract_text_from_pdf(saved_path, lang=lang)
                elif ext in [".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff"]:
                    text = extract_text_from_image(saved_path, lang=lang)
                else:
                    text = ""
            except Exception as e:
                print(f"OCR Error for {original_filename}: {str(e)}")
                text = f"Lỗi OCR: {str(e)}"
            
            # Tạo file txt
            txt_path = os.path.join(OUTPUT_DIR, f"{uid}.txt")
            with open(txt_path, "w", encoding="utf-8") as f_txt:
                f_txt.write(text)
            
            # Tạo file docx
            docx_path = os.path.join(OUTPUT_DIR, f"{uid}.docx")
            document = Document()
            document.add_paragraph(text)
            document.save(docx_path)
            
            # Parse contract
            try:
                parsed = parse_contract_text(text)
            except Exception as e:
                print(f"Parse Error for {original_filename}: {str(e)}")
                parsed = {"title": original_filename, "content": text}
            
            if contract_type_id:
                try:
                    # Get contract type from database
                    contract_type_obj = crud.get_contract_type(db, contract_type_id)
                    if contract_type_obj:
                        parsed["type"] = str(contract_type_id)
                        parsed["type_label"] = contract_type_obj.name
                        parsed["type_description"] = contract_type_obj.description
                except Exception as e:
                    print(f"Error getting contract type {contract_type_id}: {str(e)}")
                    parsed["type"] = str(contract_type_id)
                    parsed["type_label"] = f"Contract Type {contract_type_id}"
            
            # Tạo contract trong database
            contract_in = schemas.ContractCreate(
                original_filename=original_filename,
                original_path=saved_path,
                text_path=txt_path,
                docx_path=docx_path,
                parsed_json=parsed,
                status="processed",  # Đổi thành processed ngay
                expiration_date=None,
                contract_type_id=contract_type_id
            )
            
            if parsed.get("expiration_date"):
                try:
                    from dateutil import parser as date_parser
                    contract_in.expiration_date = date_parser.parse(parsed["expiration_date"])
                except Exception:
                    contract_in.expiration_date = None
            
            contract = crud.create_contract(db, contract_in)
            db.commit()
            db.refresh(contract)
            last_contract = contract
            print(f"DEBUG - Created contract: {contract.id}, status: {contract.status}")  # Debug log
            
    except Exception as e:
        print(f"Upload Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Lỗi khi tải lên: {str(e)}")
    # Sau khi upload thành công, chuyển về trang chủ để thấy thống kê cập nhật
    print("DEBUG - Redirecting to home page")  # Debug log
    return RedirectResponse(url="/", status_code=303)


# Route download cũ - đã được thay thế bằng route mới bên dưới
# @app.get("/download/{contract_id}/{kind}")
# def download_file(contract_id: int, kind: str, db: Session = Depends(get_db)):
#     contract = crud.get_contract(db, contract_id)
#     if not contract:
#         raise HTTPException(status_code=404, detail="Không tìm thấy hợp đồng")

#     if kind == "txt":
#         path = contract.text_path
#     elif kind == "docx":
#         path = contract.docx_path
#     elif kind == "original":
#         path = contract.original_path
#     else:
#         raise HTTPException(status_code=400, detail="Loại tệp không hợp lệ")

#     if not path or not os.path.exists(path):
#         raise HTTPException(status_code=404, detail="Tệp không tồn tại")

#     filename = os.path.basename(path)
#     return FileResponse(path=path, filename=filename)


@app.get("/types")
def contract_type_list(request: Request, db: Session = Depends(get_db)):
    types = crud.list_contract_types(db)
    return templates.TemplateResponse("contract_types.html", {"request": request, "types": types})



@app.get("/api/search")
def api_search(
    q: Optional[str] = None,
    contract_type_id: Optional[int] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    status: Optional[str] = None,
    sort: str = "created_at_desc",
    page: int = 1,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """API endpoint for searching contracts"""
    try:
        # Build query
        query = db.query(models.Contract)

        # Apply filters
        if q:
            query = query.filter(
                or_(
                    models.Contract.original_filename.ilike(f"%{q}%"),
                    models.Contract.extracted_text.ilike(f"%{q}%")
                )
            )

        if contract_type_id:
            query = query.filter(models.Contract.contract_type_id == contract_type_id)

        if status:
            query = query.filter(models.Contract.status == status)

        # Apply sorting
        if sort == "created_at_desc":
            query = query.order_by(models.Contract.created_at.desc())
        elif sort == "created_at_asc":
            query = query.order_by(models.Contract.created_at.asc())
        elif sort == "filename_asc":
            query = query.order_by(models.Contract.original_filename.asc())
        elif sort == "filename_desc":
            query = query.order_by(models.Contract.original_filename.desc())

        # Get total count
        total = query.count()

        # Apply pagination
        offset = (page - 1) * limit
        contracts = query.offset(offset).limit(limit).all()

        # Format response
        contracts_data = []
        for contract in contracts:
            contract_data = {
                "id": contract.id,
                "original_filename": contract.original_filename,
                "status": contract.status,
                "created_at": contract.created_at.isoformat() if contract.created_at else None,
                "extracted_text": contract.extracted_text[:200] if contract.extracted_text else None,
                "contract_type": None
            }

            # Add contract type info if available
            if contract.contract_type_id:
                contract_type = crud.get_contract_type(db, contract.contract_type_id)
                if contract_type:
                    contract_data["contract_type"] = {
                        "id": contract_type.id,
                        "name": contract_type.name,
                        "description": contract_type.description
                    }

            contracts_data.append(contract_data)

        return {
            "contracts": contracts_data,
            "total": total,
            "page": page,
            "limit": limit,
            "total_pages": (total + limit - 1) // limit
        }

    except Exception as e:
        print(f"Search error: {str(e)}")
        raise HTTPException(status_code=500, detail="Search failed")

@app.get("/api/search")
def api_search(
    q: Optional[str] = None,
    contract_type_id: Optional[int] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    status: Optional[str] = None,
    sort: str = "created_at_desc",
    page: int = 1,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """API endpoint for searching contracts"""
    try:
        # Build query
        query = db.query(models.Contract)

        # Apply filters
        if q:
            query = query.filter(
                or_(
                    models.Contract.original_filename.ilike(f"%{q}%"),
                    models.Contract.extracted_text.ilike(f"%{q}%")
                )
            )

        if contract_type_id:
            query = query.filter(models.Contract.contract_type_id == contract_type_id)

        if date_from:
            try:
                date_from_obj = datetime.strptime(date_from, "%Y-%m-%d")
                query = query.filter(models.Contract.created_at >= date_from_obj)
            except ValueError:
                pass

        if date_to:
            try:
                date_to_obj = datetime.strptime(date_to, "%Y-%m-%d")
                # Add one day to include the entire day
                date_to_obj = date_to_obj.replace(hour=23, minute=59, second=59)
                query = query.filter(models.Contract.created_at <= date_to_obj)
            except ValueError:
                pass

        if status:
            query = query.filter(models.Contract.status == status)

        # Apply sorting
        if sort == "created_at_desc":
            query = query.order_by(models.Contract.created_at.desc())
        elif sort == "created_at_asc":
            query = query.order_by(models.Contract.created_at.asc())
        elif sort == "filename_asc":
            query = query.order_by(models.Contract.original_filename.asc())
        elif sort == "filename_desc":
            query = query.order_by(models.Contract.original_filename.desc())

        # Get total count
        total = query.count()

        # Apply pagination
        offset = (page - 1) * limit
        contracts = query.offset(offset).limit(limit).all()

        # Format response
        contracts_data = []
        for contract in contracts:
            contract_data = {
                "id": contract.id,
                "original_filename": contract.original_filename,
                "status": contract.status,
                "created_at": contract.created_at.isoformat() if contract.created_at else None,
                "extracted_text": contract.extracted_text[:200] if contract.extracted_text else None,
                "contract_type": None
            }

            # Add contract type info if available
            if contract.contract_type_id:
                contract_type = crud.get_contract_type(db, contract.contract_type_id)
                if contract_type:
                    contract_data["contract_type"] = {
                        "id": contract_type.id,
                        "name": contract_type.name,
                        "description": contract_type.description
                    }

            contracts_data.append(contract_data)

        return {
            "contracts": contracts_data,
            "total": total,
            "page": page,
            "limit": limit,
            "total_pages": (total + limit - 1) // limit
        }

    except Exception as e:
        print(f"Search error: {str(e)}")
        raise HTTPException(status_code=500, detail="Search failed")

@app.post("/types")
def contract_type_create(request: Request, name: str = Form(...), description: str = Form(""), db: Session = Depends(get_db)):
    crud.create_contract_type(db, schemas.ContractTypeCreate(name=name, description=description))
    return RedirectResponse(url="/types", status_code=303)

@app.post("/types/{type_id}/delete")
def contract_type_delete(type_id: int, db: Session = Depends(get_db)):
    crud.delete_contract_type(db, type_id)
    return RedirectResponse(url="/types", status_code=303)

@app.get("/categories")
def categories_page(request: Request):
    return templates.TemplateResponse("categories.html", {"request": request})

# Đối tác
@app.get("/partners")
def partner_list(request: Request, db: Session = Depends(get_db)):
    partners = crud.list_partners(db)
    return templates.TemplateResponse("partners.html", {"request": request, "partners": partners})

@app.post("/partners")
def partner_create(
    request: Request, 
    name: str = Form(...), 
    partner_type: str = Form(...),
    tax_id: str = Form(""),
    address: str = Form(""),
    phone: str = Form(""),
    email: str = Form(""),
    contact_person: str = Form(""),
    notes: str = Form(""),
    db: Session = Depends(get_db)
):
    partner_data = schemas.PartnerCreate(
        name=name,
        partner_type=partner_type,
        tax_id=tax_id if tax_id else None,
        address=address if address else None,
        phone=phone if phone else None,
        email=email if email else None,
        contact_person=contact_person if contact_person else None,
        notes=notes if notes else None
    )
    crud.create_partner(db, partner_data)
    return RedirectResponse(url="/partners", status_code=303)

@app.post("/partners/{partner_id}/delete")
def partner_delete(partner_id: int, db: Session = Depends(get_db)):
    crud.delete_partner(db, partner_id)
    return RedirectResponse(url="/partners", status_code=303)

# Phòng ban
@app.get("/departments")
def department_list(request: Request, db: Session = Depends(get_db)):
    departments = crud.list_departments(db)
    return templates.TemplateResponse("departments.html", {"request": request, "departments": departments})

@app.post("/departments")
def department_create(request: Request, name: str = Form(...), description: str = Form(""), db: Session = Depends(get_db)):
    crud.create_department(db, schemas.DepartmentCreate(name=name, description=description))
    return RedirectResponse(url="/departments", status_code=303)

@app.post("/departments/{department_id}/delete")
def department_delete(department_id: int, db: Session = Depends(get_db)):
    crud.delete_department(db, department_id)
    return RedirectResponse(url="/departments", status_code=303)

# Thẻ tag
@app.get("/tags")
def tag_list(request: Request, db: Session = Depends(get_db)):
    tags = crud.list_tags(db)
    return templates.TemplateResponse("tags.html", {"request": request, "tags": tags})

@app.post("/tags")
def tag_create(request: Request, name: str = Form(...), color: str = Form(""), db: Session = Depends(get_db)):
    crud.create_tag(db, schemas.TagCreate(name=name, color=color))
    return RedirectResponse(url="/tags", status_code=303)

@app.post("/tags/{tag_id}/delete")
def tag_delete(tag_id: int, db: Session = Depends(get_db)):
    crud.delete_tag(db, tag_id)
    return RedirectResponse(url="/tags", status_code=303) 

# Báo cáo
@app.get("/reports/contract-stats")
def contract_stats_report(request: Request, db: Session = Depends(get_db)):
    # TODO: Implement actual statistics calculation
    contract_stats = [
        {"type": "Lao động", "count": 15, "percentage": 30.0, "avg_value": "500 triệu"},
        {"type": "Dịch vụ", "count": 25, "percentage": 50.0, "avg_value": "200 triệu"},
        {"type": "Mua bán", "count": 10, "percentage": 20.0, "avg_value": "1 tỷ"}
    ]
    
    type_labels = ["Lao động", "Dịch vụ", "Mua bán"]
    type_data = [15, 25, 10]
    status_labels = ["Đã xử lý", "Chờ xử lý", "Hết hạn", "Khác"]
    status_data = [35, 10, 3, 2]
    dept_labels = ["Kinh doanh", "Nhân sự", "Kế toán", "Kỹ thuật"]
    dept_data = [20, 15, 10, 5]
    
    return templates.TemplateResponse("reports/contract_stats.html", {
        "request": request,
        "contract_stats": contract_stats,
        "type_labels": type_labels,
        "type_data": type_data,
        "status_labels": status_labels,
        "status_data": status_data,
        "dept_labels": dept_labels,
        "dept_data": dept_data
    })

@app.get("/reports/expiring")
def expiring_report(request: Request, db: Session = Depends(get_db)):
    # TODO: Implement actual expiring contracts calculation
    expiring_contracts = [
        {
            "id": 1,
            "original_filename": "hop_dong_abc.pdf",
            "partner_name": "Công ty ABC",
            "expiration_date": datetime.now() + timedelta(days=25),
            "days_left": 25,
            "status": "processed"
        },
        {
            "id": 2,
            "original_filename": "hop_dong_xyz.pdf",
            "partner_name": "Công ty XYZ",
            "expiration_date": datetime.now() + timedelta(days=45),
            "days_left": 45,
            "status": "processed"
        }
    ]
    
    return templates.TemplateResponse("reports/expiring.html", {
        "request": request,
        "expiring_contracts": expiring_contracts,
        "urgent_count": 1,
        "warning_count": 1,
        "info_count": 0
    })

@app.get("/reports/legal-risk")
def legal_risk_report(request: Request, db: Session = Depends(get_db)):
    # TODO: Implement actual legal risk analysis
    legal_risks = [
        {
            "contract_id": 1,
            "contract_name": "hop_dong_abc.pdf",
            "partner_name": "Công ty ABC",
            "risk_level": "high",
            "risk_level_display": "Cao",
            "risk_clauses": [
                {"type": "Thanh toán", "description": "Điều khoản thanh toán không rõ ràng"},
                {"type": "Bảo mật", "description": "Thiếu điều khoản bảo mật thông tin"}
            ],
            "recommendation": "Cần rà soát và bổ sung điều khoản"
        }
    ]
    
    risk_summary = {
        "payment": [
            {"description": "Điều khoản thanh toán không rõ ràng", "count": 5, "risk_color": "danger"},
            {"description": "Thiếu điều khoản phạt", "count": 3, "risk_color": "warning"}
        ],
        "confidentiality": [
            {"description": "Thiếu điều khoản bảo mật", "count": 8, "risk_color": "danger"},
            {"description": "Điều khoản bảo mật yếu", "count": 2, "risk_color": "warning"}
        ]
    }
    
    return templates.TemplateResponse("reports/legal_risk.html", {
        "request": request,
        "legal_risks": legal_risks,
        "risk_summary": risk_summary,
        "high_risk_count": 5,
        "medium_risk_count": 3,
        "low_risk_count": 2,
        "safe_count": 40
    })

@app.get("/reports/history")
def history_report(request: Request, db: Session = Depends(get_db)):
    # TODO: Implement actual change history
    changes = [
        {
            "id": 1,
            "timestamp": datetime.now() - timedelta(hours=2),
            "user_name": "admin",
            "contract_id": 1,
            "contract_name": "hop_dong_abc.pdf",
            "change_type": "content",
            "change_type_display": "Nội dung",
            "description": "Cập nhật điều khoản thanh toán",
            "old_value": "Thanh toán 30 ngày",
            "new_value": "Thanh toán 45 ngày"
        }
    ]
    
    return templates.TemplateResponse("reports/history.html", {
        "request": request,
        "changes": changes,
        "total_changes": 25,
        "contracts_modified": 15,
        "active_users": 8,
        "recent_changes": 5,
        "users": [{"id": 1, "name": "admin"}],
        "page": 1,
        "total_pages": 1
    }) 

# Cài đặt hệ thống
@app.get("/settings/users")
def user_management(request: Request, db: Session = Depends(get_db)):
    # TODO: Implement actual user management
    users = [
        {
            "id": 1,
            "username": "admin",
            "full_name": "Quản trị viên",
            "email": "admin@company.com",
            "role": "admin",
            "role_display": "Quản trị viên",
            "is_active": True,
            "permissions": ["view_contracts", "edit_contracts", "manage_users", "system_settings"]
        },
        {
            "id": 2,
            "username": "manager",
            "full_name": "Người quản lý",
            "email": "manager@company.com",
            "role": "manager",
            "role_display": "Quản lý",
            "is_active": True,
            "permissions": ["view_contracts", "edit_contracts", "view_reports"]
        }
    ]
    
    departments = [
        {"id": 1, "name": "Kinh doanh"},
        {"id": 2, "name": "Nhân sự"},
        {"id": 3, "name": "Kế toán"}
    ]
    
    return templates.TemplateResponse("settings/users.html", {
        "request": request,
        "users": users,
        "departments": departments
    })

@app.get("/settings/ocr")
def ocr_settings(request: Request, db: Session = Depends(get_db)):
    # TODO: Implement actual OCR settings
    ocr_config = {
        "primary_language": "vie+eng",
        "secondary_language": "",
        "ocr_quality": "balanced",
        "image_processing": "basic",
        "enable_preprocessing": True,
        "enable_postprocessing": True,
        "enable_confidence_check": True,
        "enable_auto_correction": False,
        "confidence_threshold": 70,
        "timeout_seconds": 300
    }
    
    ocr_stats = {
        "today_processed": 25,
        "today_success": 23,
        "today_failed": 2,
        "month_total": 450,
        "month_success_rate": 95.6,
        "avg_processing_time": 2.3,
        "accuracy_rate": 92.8
    }
    
    return templates.TemplateResponse("settings/ocr.html", {
        "request": request,
        "ocr_config": ocr_config,
        "ocr_stats": ocr_stats
    })

@app.get("/settings/automation")
def automation_settings(request: Request, db: Session = Depends(get_db)):
    # TODO: Implement actual automation settings
    auto_rules = [
        {
            "id": 1,
            "name": "Tự động phân loại hợp đồng lao động",
            "description": "Phân loại hợp đồng có từ khóa 'lao động', 'nhân viên', 'công nhân'",
            "conditions": [
                {"field": "contract_type", "operator": "contains", "value": "lao động"}
            ],
            "actions": [
                {"type": "set_contract_type", "value": "Lao động"}
            ],
            "is_active": True
        }
    ]
    
    auto_tag_config = {
        "expiring_contracts": True,
        "high_value_contracts": True,
        "confidential_contracts": False,
        "renewal_contracts": True
    }
    
    automation_stats = {
        "today_rules_executed": 15,
        "today_contracts_processed": 45,
        "today_tags_applied": 23,
        "month_total_rules": 120,
        "month_efficiency": 94.2
    }
    
    return templates.TemplateResponse("settings/automation.html", {
        "request": request,
        "auto_rules": auto_rules,
        "auto_tag_config": auto_tag_config,
        "automation_stats": automation_stats
    })

@app.get("/settings/backup")
def backup_settings(request: Request, db: Session = Depends(get_db)):
    # TODO: Implement actual backup settings
    backup_config = {
        "frequency": "daily",
        "time": "02:00",
        "retention_days": 30,
        "compression": "gzip",
        "data_types": ["contracts", "database", "settings"],
        "notification_email": "admin@company.com",
        "enable_auto_backup": True
    }
    
    backup_history = [
        {
            "timestamp": datetime.now() - timedelta(hours=2),
            "type": "auto",
            "size_mb": 1250,
            "status": "success",
            "duration_seconds": 45,
            "filename": "backup_20241201_020000.zip"
        }
    ]
    
    backup_stats = {
        "today_backups": 1,
        "today_success": 1,
        "today_failed": 0,
        "month_total": 30,
        "month_total_size_gb": 37.5,
        "month_success_rate": 100.0,
        "disk_usage_percent": 65,
        "disk_used_gb": 650,
        "disk_total_gb": 1000
    }
    
    backup_info = {
        "last_backup_time": "01/12/2024 02:00",
        "next_backup_time": "02/12/2024 02:00",
        "storage_path": "D:/backups/contracts",
        "free_space_gb": 350
    }
    
    return templates.TemplateResponse("settings/backup.html", {
        "request": request,
        "backup_config": backup_config,
        "backup_history": backup_history,
        "backup_stats": backup_stats,
        "backup_info": backup_info
    })

@app.get("/settings/system-log")
def system_log(request: Request, db: Session = Depends(get_db)):
    # TODO: Implement actual system log
    system_logs = [
        {
            "id": 1,
            "timestamp": datetime.now() - timedelta(minutes=30),
            "level": "INFO",
            "module": "contract",
            "user_name": "admin",
            "action": "Tải lên hợp đồng mới",
            "details": "Hợp đồng ABC đã được tải lên thành công",
            "ip_address": "192.168.1.100"
        },
        {
            "id": 2,
            "timestamp": datetime.now() - timedelta(hours=1),
            "level": "WARNING",
            "module": "ocr",
            "user_name": "system",
            "action": "OCR xử lý chậm",
            "details": "Thời gian xử lý OCR vượt quá 10 giây",
            "ip_address": "N/A"
        }
    ]
    
    system_stats = {
        "total_logs": 1250,
        "info_logs": 980,
        "warning_logs": 200,
        "error_logs": 70
    }
    
    module_stats = [
        {"name": "Hợp đồng", "total": 450, "info": 400, "warning": 40, "error": 10},
        {"name": "Người dùng", "total": 200, "info": 180, "warning": 15, "error": 5},
        {"name": "OCR", "total": 300, "info": 250, "warning": 35, "error": 15},
        {"name": "Hệ thống", "total": 200, "info": 100, "warning": 80, "error": 20},
        {"name": "Sao lưu", "total": 100, "info": 50, "warning": 30, "error": 20}
    ]
    
    recent_activities = [
        {
            "timestamp": datetime.now() - timedelta(minutes=5),
            "level": "INFO",
            "action": "Đăng nhập thành công",
            "user_name": "manager"
        },
        {
            "timestamp": datetime.now() - timedelta(minutes=15),
            "level": "INFO",
            "action": "Cập nhật hợp đồng",
            "user_name": "admin"
        }
    ]
    
    return templates.TemplateResponse("settings/system_log.html", {
        "request": request,
        "system_logs": system_logs,
        "system_stats": system_stats,
        "module_stats": module_stats,
        "recent_activities": recent_activities,
        "page": 1,
        "total_pages": 1
    }) 

@app.get("/contract-types")
def contract_types_page(request: Request, db: Session = Depends(get_db)):
    """Trang quản lý loại hợp đồng"""
    contract_types = crud.list_contract_types(db)
    return templates.TemplateResponse("contract_types.html", {
        "request": request,
        "contract_types": contract_types
    })

@app.get("/partners")
def partners_page(request: Request, db: Session = Depends(get_db)):
    """Trang quản lý đối tác"""
    partners = crud.list_partners(db)
    return templates.TemplateResponse("partners.html", {
        "request": request,
        "partners": partners
    })

@app.get("/departments")
def departments_page(request: Request, db: Session = Depends(get_db)):
    """Trang quản lý phòng ban"""
    departments = crud.list_departments(db)
    return templates.TemplateResponse("departments.html", {
        "request": request,
        "departments": departments
    })

@app.get("/tags")
def tags_page(request: Request, db: Session = Depends(get_db)):
    """Trang quản lý thẻ tag"""
    tags = crud.list_tags(db)
    return templates.TemplateResponse("tags.html", {
        "request": request,
        "tags": tags
    })

@app.get("/upload")
def upload_page(request: Request):
    """Trang tải lên hợp đồng"""
    return templates.TemplateResponse("upload.html", {
        "request": request
    })



@app.post("/detail/{contract_id}/delete")
def delete_contract_detail(contract_id: int, db: Session = Depends(get_db)):
    """Xóa hợp đồng từ trang chi tiết"""
    ok = crud.delete_contract(db, contract_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Hợp đồng không tồn tại")
    return RedirectResponse(url="/search", status_code=303)

@app.post("/contracts/{contract_id}/delete")
def delete_contract(contract_id: int, db: Session = Depends(get_db)):
    """Xóa hợp đồng từ trang danh sách"""
    ok = crud.delete_contract(db, contract_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Hợp đồng không tồn tại")
    return RedirectResponse(url="/search", status_code=303)

@app.get("/download/{contract_id}/{format}")
def download_contract(contract_id: int, format: str, db: Session = Depends(get_db)):
    """Tải xuống hợp đồng theo định dạng"""
    contract = crud.get_contract(db, contract_id)
    if not contract:
        raise HTTPException(status_code=404, detail="Hợp đồng không tồn tại")
    
    if format == "txt":
        file_path = contract.text_path
        media_type = "text/plain"
        filename = f"{contract.original_filename}.txt"
    elif format == "docx":
        file_path = contract.docx_path
        media_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        filename = f"{contract.original_filename}.docx"
    elif format == "original":
        # Tải file gốc từ thư mục uploads
        file_path = contract.original_path
        # Xác định media type dựa trên extension
        if contract.original_filename.lower().endswith('.pdf'):
            media_type = "application/pdf"
        elif contract.original_filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            media_type = "image/png" if contract.original_filename.lower().endswith('.png') else "image/jpeg"
        else:
            media_type = "application/octet-stream"
        filename = contract.original_filename
    else:
        raise HTTPException(status_code=400, detail="Định dạng không được hỗ trợ")
    
    if not file_path or not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File không tồn tại")
    
    return FileResponse(
        path=file_path,
        media_type=media_type,
        filename=filename
    ) 