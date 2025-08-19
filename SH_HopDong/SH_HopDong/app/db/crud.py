from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from datetime import datetime, timedelta

from app.db import models
from app.db import schemas


def create_contract(db: Session, contract_in: schemas.ContractCreate) -> models.Contract:
    contract = models.Contract(
        original_filename=contract_in.original_filename,
        original_path=contract_in.original_path,
        text_path=contract_in.text_path,
        docx_path=contract_in.docx_path,
        parsed_json=contract_in.parsed_json,
        status=contract_in.status or "pending",
        expiration_date=contract_in.expiration_date,
        contract_type_id=contract_in.contract_type_id,
    )
    db.add(contract)
    db.commit()
    db.refresh(contract)
    return contract


def get_contract(db: Session, contract_id: int) -> Optional[models.Contract]:
    return db.query(models.Contract).filter(models.Contract.id == contract_id).first()


def count_contracts(db: Session) -> int:
    return db.query(models.Contract).count()


def get_contract_types(db: Session) -> List[models.ContractType]:
    """Get all contract types"""
    return db.query(models.ContractType).order_by(models.ContractType.name).all()


def get_contract_type(db: Session, contract_type_id: int) -> Optional[models.ContractType]:
    """Get a specific contract type by ID"""
    return db.query(models.ContractType).filter(models.ContractType.id == contract_type_id).first()


def list_contracts(db: Session, skip: int = 0, limit: int = 50, q: Optional[str] = None) -> List[models.Contract]:
    query = db.query(models.Contract).options(joinedload(models.Contract.contract_type))
    if q:
        like = f"%{q}%"
        query = query.filter(models.Contract.original_filename.ilike(like))
    return (
        query.order_by(models.Contract.id.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def delete_contract(db: Session, contract_id: int) -> bool:
    obj = db.query(models.Contract).filter(models.Contract.id == contract_id).first()
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True


def count_pending_contracts(db: Session) -> int:
    return db.query(models.Contract).filter(models.Contract.status == "pending").count()

def count_processed_contracts(db: Session) -> int:
    return db.query(models.Contract).filter(models.Contract.status == "processed").count()

def count_expiring_contracts(db: Session, days: int = 30) -> int:
    now = datetime.now()
    soon = now + timedelta(days=days)
    return db.query(models.Contract).filter(
        models.Contract.status == "processed",
        models.Contract.expiration_date != None,
        models.Contract.expiration_date >= now,
        models.Contract.expiration_date <= soon
    ).count() 

# ContractType CRUD

def create_contract_type(db: Session, obj_in: schemas.ContractTypeCreate) -> models.ContractType:
    obj = models.ContractType(**obj_in.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def get_contract_type(db: Session, id: int) -> Optional[models.ContractType]:
    return db.query(models.ContractType).filter(models.ContractType.id == id).first()

def list_contract_types(db: Session) -> List[models.ContractType]:
    return db.query(models.ContractType).order_by(models.ContractType.id.desc()).all()

def update_contract_type(db: Session, id: int, obj_in: schemas.ContractTypeCreate) -> Optional[models.ContractType]:
    obj = get_contract_type(db, id)
    if not obj:
        return None
    for k, v in obj_in.dict().items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj

def delete_contract_type(db: Session, id: int) -> bool:
    obj = get_contract_type(db, id)
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True

# Partner CRUD

def create_partner(db: Session, obj_in: schemas.PartnerCreate) -> models.Partner:
    obj = models.Partner(**obj_in.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def get_partner(db: Session, id: int) -> Optional[models.Partner]:
    return db.query(models.Partner).filter(models.Partner.id == id).first()

def list_partners(db: Session) -> List[models.Partner]:
    return db.query(models.Partner).order_by(models.Partner.id.desc()).all()

def update_partner(db: Session, id: int, obj_in: schemas.PartnerCreate) -> Optional[models.Partner]:
    obj = get_partner(db, id)
    if not obj:
        return None
    for k, v in obj_in.dict().items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj

def delete_partner(db: Session, id: int) -> bool:
    obj = get_partner(db, id)
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True

# Department CRUD

def create_department(db: Session, obj_in: schemas.DepartmentCreate) -> models.Department:
    obj = models.Department(**obj_in.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def get_department(db: Session, id: int) -> Optional[models.Department]:
    return db.query(models.Department).filter(models.Department.id == id).first()

def list_departments(db: Session) -> List[models.Department]:
    return db.query(models.Department).order_by(models.Department.id.desc()).all()

def update_department(db: Session, id: int, obj_in: schemas.DepartmentCreate) -> Optional[models.Department]:
    obj = get_department(db, id)
    if not obj:
        return None
    for k, v in obj_in.dict().items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj

def delete_department(db: Session, id: int) -> bool:
    obj = get_department(db, id)
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True

# Tag CRUD

def create_tag(db: Session, obj_in: schemas.TagCreate) -> models.Tag:
    obj = models.Tag(**obj_in.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def get_tag(db: Session, id: int) -> Optional[models.Tag]:
    return db.query(models.Tag).filter(models.Tag.id == id).first()

def list_tags(db: Session) -> List[models.Tag]:
    return db.query(models.Tag).order_by(models.Tag.id.desc()).all()

def update_tag(db: Session, id: int, obj_in: schemas.TagCreate) -> Optional[models.Tag]:
    obj = get_tag(db, id)
    if not obj:
        return None
    for k, v in obj_in.dict().items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj

def delete_tag(db: Session, id: int) -> bool:
    obj = get_tag(db, id)
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True 