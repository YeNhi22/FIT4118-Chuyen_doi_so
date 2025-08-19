@echo off
echo ========================================
echo    THEM 10 LOAI HOP DONG
echo ========================================
echo.

echo [1/10] Them loai: Mua ban
curl -X POST http://localhost:8000/types -d "name=Mua ban&description=Hop dong mua ban hang hoa, san pham" -H "Content-Type: application/x-www-form-urlencoded"
echo.

echo [2/10] Them loai: Dich vu
curl -X POST http://localhost:8000/types -d "name=Dich vu&description=Hop dong cung cap dich vu" -H "Content-Type: application/x-www-form-urlencoded"
echo.

echo [3/10] Them loai: Lao dong
curl -X POST http://localhost:8000/types -d "name=Lao dong&description=Hop dong lao dong, thue muon nhan vien" -H "Content-Type: application/x-www-form-urlencoded"
echo.

echo [4/10] Them loai: Thue muon
curl -X POST http://localhost:8000/types -d "name=Thue muon&description=Hop dong thue mat bang, thiet bi" -H "Content-Type: application/x-www-form-urlencoded"
echo.

echo [5/10] Them loai: Hop tac
curl -X POST http://localhost:8000/types -d "name=Hop tac&description=Hop dong hop tac kinh doanh" -H "Content-Type: application/x-www-form-urlencoded"
echo.

echo [6/10] Them loai: Tu van
curl -X POST http://localhost:8000/types -d "name=Tu van&description=Hop dong tu van chuyen nghiep" -H "Content-Type: application/x-www-form-urlencoded"
echo.

echo [7/10] Them loai: Van chuyen
curl -X POST http://localhost:8000/types -d "name=Van chuyen&description=Hop dong van chuyen, logistics" -H "Content-Type: application/x-www-form-urlencoded"
echo.

echo [8/10] Them loai: Bao mat (NDA)
curl -X POST http://localhost:8000/types -d "name=Bao mat (NDA)&description=Thoa thuan bao mat thong tin" -H "Content-Type: application/x-www-form-urlencoded"
echo.

echo [9/10] Them loai: Bao hiem
curl -X POST http://localhost:8000/types -d "name=Bao hiem&description=Hop dong bao hiem" -H "Content-Type: application/x-www-form-urlencoded"
echo.

echo [10/10] Them loai: Khac
curl -X POST http://localhost:8000/types -d "name=Khac&description=Cac loai hop dong khac" -H "Content-Type: application/x-www-form-urlencoded"
echo.

echo ========================================
echo    HOAN THANH!
echo ========================================
echo Truy cap http://localhost:8000/types de xem ket qua
pause
