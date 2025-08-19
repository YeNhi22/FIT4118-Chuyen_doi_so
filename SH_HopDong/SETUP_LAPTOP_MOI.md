# HƯỚNG DẪN SETUP DỰ ÁN TRÊN LAPTOP MỚI

## 📋 YÊU CẦU HỆ THỐNG

### 1. Cài đặt Python 3.10+
```bash
# Tải từ: https://www.python.org/downloads/
# Hoặc dùng winget:
winget install Python.Python.3.10
```

### 2. Cài đặt SQL Server
```bash
# SQL Server Express (miễn phí):
# Tải từ: https://www.microsoft.com/en-us/sql-server/sql-server-downloads

# Hoặc SQL Server Developer Edition
# Tải từ: https://www.microsoft.com/en-us/sql-server/sql-server-downloads
```

### 3. Cài đặt SQL Server Management Studio (SSMS)
```bash
# Tải từ: https://docs.microsoft.com/en-us/sql/ssms/download-sql-server-management-studio-ssms
```

### 4. Cài đặt Git
```bash
# Tải từ: https://git-scm.com/download/win
# Hoặc dùng winget:
winget install Git.Git
```

### 5. Cài đặt Tesseract OCR
```bash
# Tải từ: https://github.com/UB-Mannheim/tesseract/wiki
# Cài vào: C:\Program Files\Tesseract-OCR\
```

## 🚀 SETUP DỰ ÁN

### Bước 1: Clone dự án
```bash
# Tạo thư mục làm việc
mkdir D:\Projects
cd D:\Projects

# Clone dự án (thay YOUR_REPO_URL bằng URL thực tế)
git clone YOUR_REPO_URL SH_HopDong
cd SH_HopDong
```

### Bước 2: Tạo Virtual Environment
```bash
# Tạo virtual environment
python -m venv .venv

# Kích hoạt virtual environment
.venv\Scripts\activate

# Upgrade pip
python -m pip install --upgrade pip
```

### Bước 3: Cài đặt Dependencies
```bash
# Cài đặt các package cần thiết
pip install -r requirements.txt

# Nếu thiếu pyodbc:
pip install pyodbc

# Nếu thiếu requests:
pip install requests
```

### Bước 4: Setup SQL Server Database

#### 4.1. Tạo Database
```sql
-- Mở SSMS, kết nối đến SQL Server
-- Chạy các lệnh sau:

CREATE DATABASE SH_HopDong;
GO

USE SH_HopDong;
GO
```

#### 4.2. Tạo Tables
```sql
-- Tạo bảng contract_types
CREATE TABLE contract_types (
    id INT IDENTITY(1,1) PRIMARY KEY,
    name NVARCHAR(100) NOT NULL UNIQUE,
    description NVARCHAR(MAX),
    created_at DATETIME2 DEFAULT GETDATE()
);

-- Tạo bảng contracts
CREATE TABLE contracts (
    id INT IDENTITY(1,1) PRIMARY KEY,
    original_filename NVARCHAR(255) NOT NULL,
    original_path NVARCHAR(MAX) NOT NULL,
    text_path NVARCHAR(MAX) NOT NULL,
    docx_path NVARCHAR(MAX) NOT NULL,
    parsed_json NVARCHAR(MAX),
    created_at DATETIME2 DEFAULT GETDATE(),
    status NVARCHAR(32) DEFAULT 'pending',
    expiration_date DATETIME2,
    contract_type_id INT,
    FOREIGN KEY (contract_type_id) REFERENCES contract_types(id)
);

-- Tạo các bảng khác (partners, departments, tags)
CREATE TABLE partners (
    id INT IDENTITY(1,1) PRIMARY KEY,
    name NVARCHAR(255) NOT NULL,
    partner_type NVARCHAR(50) DEFAULT N'Khách hàng',
    tax_id NVARCHAR(50),
    address NVARCHAR(MAX),
    phone NVARCHAR(20),
    email NVARCHAR(100),
    contact_person NVARCHAR(100),
    notes NVARCHAR(MAX),
    created_at DATETIME2 DEFAULT GETDATE()
);

CREATE TABLE departments (
    id INT IDENTITY(1,1) PRIMARY KEY,
    name NVARCHAR(100) NOT NULL,
    description NVARCHAR(MAX),
    created_at DATETIME2 DEFAULT GETDATE()
);

CREATE TABLE tags (
    id INT IDENTITY(1,1) PRIMARY KEY,
    name NVARCHAR(50) NOT NULL,
    color NVARCHAR(7),
    created_at DATETIME2 DEFAULT GETDATE()
);
```

### Bước 5: Cấu hình Environment

#### 5.1. Tạo file .env (tùy chọn)
```bash
# Tạo file .env trong thư mục gốc
echo DATABASE_TYPE=sqlserver > .env
echo SQLSERVER_SERVER=localhost >> .env
echo SQLSERVER_DATABASE=SH_HopDong >> .env
echo TESSERACT_PATH=C:\Program Files\Tesseract-OCR\tesseract.exe >> .env
```

### Bước 6: Tạo thư mục cần thiết
```bash
# Tạo các thư mục cần thiết
mkdir uploads
mkdir outputs
```

### Bước 7: Test kết nối
```bash
# Test Python và packages
python -c "import fastapi, uvicorn, sqlalchemy, pytesseract; print('All packages OK')"

# Test kết nối SQL Server
python -c "import pyodbc; conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=SH_HopDong;Trusted_Connection=yes'); print('SQL Server connection OK'); conn.close()"
```

## 🎯 CHẠY ỨNG DỤNG

### Cách 1: Sử dụng batch file
```bash
# Chạy file batch
run_app.bat
```

### Cách 2: Chạy thủ công
```bash
# Kích hoạt virtual environment
.venv\Scripts\activate

# Chạy ứng dụng
uvicorn app.main:app --reload --port 8000 --host 0.0.0.0
```

### Cách 3: Sử dụng PowerShell
```powershell
# Chạy file PowerShell
.\run_app.ps1
```

## 🔧 THÊM DỮ LIỆU MẪU

### Thêm loại hợp đồng
```bash
# Sau khi ứng dụng chạy, truy cập:
# http://localhost:8000/types
# Hoặc chạy script:
python add_10_contract_types.py
```

## 📝 KIỂM TRA

1. **Truy cập ứng dụng:** http://localhost:8000
2. **Trang upload:** http://localhost:8000/upload
3. **Quản lý loại hợp đồng:** http://localhost:8000/types
4. **Tìm kiếm:** http://localhost:8000/search

## ⚠️ XỬ LÝ LỖI THƯỜNG GẶP

### Lỗi kết nối SQL Server:
```bash
# Kiểm tra SQL Server đang chạy:
services.msc
# Tìm "SQL Server" và đảm bảo đang chạy

# Kiểm tra Windows Authentication:
# Trong SSMS: Security > Logins > Thêm Windows user
```

### Lỗi Tesseract:
```bash
# Kiểm tra đường dẫn Tesseract:
"C:\Program Files\Tesseract-OCR\tesseract.exe" --version
```

### Lỗi Python packages:
```bash
# Cài lại packages:
pip install --force-reinstall -r requirements.txt
```

## 🎉 HOÀN THÀNH!

Sau khi hoàn thành các bước trên, bạn sẽ có:
- ✅ Ứng dụng chạy tại http://localhost:8000
- ✅ Database SQL Server hoạt động
- ✅ Có thể upload và xử lý hợp đồng
- ✅ Quản lý loại hợp đồng
- ✅ Tìm kiếm hợp đồng
