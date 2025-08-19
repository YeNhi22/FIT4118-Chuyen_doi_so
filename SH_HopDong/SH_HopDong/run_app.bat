@echo off
echo ========================================
echo    Số hóa Hợp đồng - Khởi động ứng dụng
echo ========================================
echo.

cd /d "%~dp0"

echo [1/4] Kích hoạt virtual environment...
call .venv\Scripts\activate.bat

echo [2/4] Kiểm tra thư mục uploads và outputs...
if not exist "uploads" mkdir uploads
if not exist "outputs" mkdir outputs

echo [3/4] Kiểm tra dependencies...
python -c "import fastapi, uvicorn, sqlalchemy, pytesseract" 2>nul
if errorlevel 1 (
    echo ❌ Thiếu dependencies. Đang cài đặt...
    pip install -r requirements.txt
) else (
    echo ✅ Dependencies đã sẵn sàng
)

echo [4/4] Khởi động ứng dụng...
echo.
echo 🌐 Ứng dụng sẽ chạy tại: http://localhost:8000
echo 📁 Upload page: http://localhost:8000/upload
echo 🔍 Search page: http://localhost:8000/search
echo.
echo Nhấn Ctrl+C để dừng ứng dụng
echo.

uvicorn app.main:app --reload --port 8000 --host 0.0.0.0

pause
