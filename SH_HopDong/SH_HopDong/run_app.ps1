# Số hóa Hợp đồng - Khởi động ứng dụng
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   Số hóa Hợp đồng - Khởi động ứng dụng" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Chuyển đến thư mục đúng
Set-Location "$PSScriptRoot\SH_HopDong"

Write-Host "[1/4] Kích hoạt virtual environment..." -ForegroundColor Yellow
& ".venv\Scripts\Activate.ps1"

Write-Host "[2/4] Kiểm tra thư mục uploads và outputs..." -ForegroundColor Yellow
if (!(Test-Path "uploads")) { New-Item -ItemType Directory -Name "uploads" }
if (!(Test-Path "outputs")) { New-Item -ItemType Directory -Name "outputs" }

Write-Host "[3/4] Kiểm tra dependencies..." -ForegroundColor Yellow
try {
    python -c "import fastapi, uvicorn, sqlalchemy, pytesseract" 2>$null
    Write-Host "✅ Dependencies đã sẵn sàng" -ForegroundColor Green
} catch {
    Write-Host "❌ Thiếu dependencies. Đang cài đặt..." -ForegroundColor Red
    pip install -r requirements.txt
}

Write-Host "[4/4] Khởi động ứng dụng..." -ForegroundColor Yellow
Write-Host ""
Write-Host "🌐 Ứng dụng sẽ chạy tại: http://localhost:8000" -ForegroundColor Green
Write-Host "📁 Upload page: http://localhost:8000/upload" -ForegroundColor Green
Write-Host "🔍 Search page: http://localhost:8000/search" -ForegroundColor Green
Write-Host ""
Write-Host "Nhấn Ctrl+C để dừng ứng dụng" -ForegroundColor Yellow
Write-Host ""

uvicorn app.main:app --reload --port 8000 --host 0.0.0.0
