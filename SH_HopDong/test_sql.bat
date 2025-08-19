@echo off
echo Testing SQL Server connection...
sqlcmd -S localhost -d SH_HopDong -E -Q "SELECT COUNT(*) as CurrentTypes FROM contract_types"
pause
