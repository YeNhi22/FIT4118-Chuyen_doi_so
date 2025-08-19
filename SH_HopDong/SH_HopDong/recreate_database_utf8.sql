-- Xóa và tạo lại database với encoding UTF-8
USE master;

-- Drop database nếu tồn tại
IF EXISTS (SELECT name FROM sys.databases WHERE name = 'SH_HopDong')
BEGIN
    ALTER DATABASE SH_HopDong SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
    DROP DATABASE SH_HopDong;
END

-- Tạo database mới với collation Vietnamese_CI_AS
CREATE DATABASE SH_HopDong
COLLATE Vietnamese_CI_AS;

-- Sử dụng database mới
USE SH_HopDong;

-- Kiểm tra collation
SELECT name, collation_name FROM sys.databases WHERE name = 'SH_HopDong';

-- Tạo tables với NVARCHAR (Unicode support)
CREATE TABLE contract_types (
    id INT IDENTITY(1,1) PRIMARY KEY,
    name NVARCHAR(100) NOT NULL UNIQUE,
    description NVARCHAR(MAX) NULL,
    created_at DATETIMEOFFSET NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE partners (
    id INT IDENTITY(1,1) PRIMARY KEY,
    name NVARCHAR(255) NOT NULL UNIQUE,
    partner_type NVARCHAR(50) NOT NULL,
    tax_id NVARCHAR(50) NULL,
    address NVARCHAR(MAX) NULL,
    phone NVARCHAR(50) NULL,
    email NVARCHAR(255) NULL,
    contact_person NVARCHAR(255) NULL,
    notes NVARCHAR(MAX) NULL,
    created_at DATETIMEOFFSET NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE departments (
    id INT IDENTITY(1,1) PRIMARY KEY,
    name NVARCHAR(100) NOT NULL UNIQUE,
    description NVARCHAR(MAX) NULL,
    created_at DATETIMEOFFSET NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE tags (
    id INT IDENTITY(1,1) PRIMARY KEY,
    name NVARCHAR(50) NOT NULL UNIQUE,
    color NVARCHAR(20) NULL,
    created_at DATETIMEOFFSET NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE contracts (
    id INT IDENTITY(1,1) PRIMARY KEY,
    original_filename NVARCHAR(255) NOT NULL,
    original_path NVARCHAR(MAX) NOT NULL,
    text_path NVARCHAR(MAX) NOT NULL,
    docx_path NVARCHAR(MAX) NOT NULL,
    parsed_json NVARCHAR(MAX) NULL,
    created_at DATETIMEOFFSET NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status NVARCHAR(32) NOT NULL,
    expiration_date DATETIMEOFFSET NULL
);

-- Tạo indexes
CREATE INDEX ix_contract_types_id ON contract_types (id);
CREATE INDEX ix_partners_id ON partners (id);
CREATE INDEX ix_departments_id ON departments (id);
CREATE INDEX ix_tags_id ON tags (id);
CREATE INDEX ix_contracts_id ON contracts (id);

-- Kiểm tra tables đã tạo
SELECT name FROM sys.tables;

-- Kiểm tra collation của các cột
SELECT 
    t.name AS TableName,
    c.name AS ColumnName,
    c.collation_name,
    TYPE_NAME(c.user_type_id) AS DataType
FROM sys.columns c
INNER JOIN sys.tables t ON c.object_id = t.object_id
ORDER BY t.name, c.name;
