# HƯỚNG DẪN THÊM 10 LOẠI HỢP ĐỒNG

## Cách dễ nhất (Khuyến nghị) 🎯

### Bước 1: Khởi động ứng dụng
1. Nhấp đúp vào file `run_app.bat`
2. Đợi ứng dụng khởi động (khoảng 30 giây)
3. Khi thấy dòng "Uvicorn running on http://0.0.0.0:8000" là đã sẵn sàng

### Bước 2: Chạy script tự động
1. Mở PowerShell hoặc Command Prompt
2. Chạy lệnh:
```bash
.venv\Scripts\python.exe add_10_contract_types.py
```

**HOẶC** nhấp đúp vào file `add_10_contract_types.py`

### Bước 3: Kiểm tra kết quả
- Truy cập: http://localhost:8000/types
- Bạn sẽ thấy 10 loại hợp đồng mới

---

## 10 Loại hợp đồng sẽ được thêm:

1. **Mua bán** - Hợp đồng mua bán hàng hóa, sản phẩm
2. **Dịch vụ** - Hợp đồng cung cấp dịch vụ  
3. **Lao động** - Hợp đồng lao động, thuê mướn nhân viên
4. **Thuê mướn** - Hợp đồng thuê mặt bằng, thiết bị
5. **Hợp tác** - Hợp đồng hợp tác kinh doanh
6. **Tư vấn** - Hợp đồng tư vấn chuyên nghiệp
7. **Vận chuyển** - Hợp đồng vận chuyển, logistics
8. **Bảo mật (NDA)** - Thỏa thuận bảo mật thông tin
9. **Bảo hiểm** - Hợp đồng bảo hiểm
10. **Khác** - Các loại hợp đồng khác

---

## Cách thủ công (Nếu script không hoạt động)

1. Khởi động ứng dụng bằng `run_app.bat`
2. Truy cập: http://localhost:8000/types
3. Nhấn nút "Thêm mới"
4. Nhập từng loại hợp đồng theo danh sách trên
5. Nhấn "Lưu" cho mỗi loại

---

## Lưu ý:
- Đảm bảo SQL Server đang chạy
- Đảm bảo database SH_HopDong tồn tại
- Nếu gặp lỗi, thử khởi động lại ứng dụng
