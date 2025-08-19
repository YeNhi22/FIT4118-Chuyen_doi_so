@echo off
echo ========================================
echo    Cập nhật loại hợp đồng - SQL Server
echo ========================================
echo.

cd /d "%~dp0"

echo [1/2] Kiểm tra kết nối SQL Server...
sqlcmd -S localhost -d SH_HopDong -E -Q "SELECT COUNT(*) as 'Current Types' FROM contract_types"

if errorlevel 1 (
    echo ❌ Không thể kết nối đến SQL Server
    echo Vui lòng kiểm tra:
    echo - SQL Server đang chạy
    echo - Database SH_HopDong tồn tại
    echo - Windows Authentication được bật
    pause
    exit /b 1
)

echo.
echo [2/2] Chạy script cập nhật...
sqlcmd -S localhost -d SH_HopDong -E -i update_contract_types_sqlserver.sql

if errorlevel 1 (
    echo ❌ Lỗi khi chạy script cập nhật
) else (
    echo ✅ Cập nhật thành công!
)

echo.
pause
