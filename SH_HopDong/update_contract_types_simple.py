#!/usr/bin/env python3
"""
Script đơn giản để cập nhật danh sách loại hợp đồng cho SQL Server
"""

import pyodbc
import os
from datetime import datetime

def update_contract_types():
    """Cập nhật danh sách loại hợp đồng"""
    print("🚀 Bắt đầu cập nhật loại hợp đồng...")
    
    # Cấu hình kết nối SQL Server
    server = os.getenv("SQLSERVER_SERVER", "localhost")
    database = os.getenv("SQLSERVER_DATABASE", "SH_HopDong")
    username = os.getenv("SQLSERVER_USERNAME", "")
    password = os.getenv("SQLSERVER_PASSWORD", "")
    driver = os.getenv("SQLSERVER_DRIVER", "ODBC Driver 17 for SQL Server")
    
    # Tạo connection string
    if username and password:
        # SQL Authentication
        conn_str = f"DRIVER={{{driver}}};SERVER={server};DATABASE={database};UID={username};PWD={password};CHARSET=UTF8;"
    else:
        # Windows Authentication
        conn_str = f"DRIVER={{{driver}}};SERVER={server};DATABASE={database};Trusted_Connection=yes;CHARSET=UTF8;"
    
    print(f"📡 Kết nối đến: {server}/{database}")
    
    new_types = [
        # Hợp đồng kinh doanh cơ bản
        ("Mua bán", "Hợp đồng mua bán hàng hóa, sản phẩm, dịch vụ"),
        ("Cung cấp", "Hợp đồng cung cấp nguyên vật liệu, thiết bị"),
        ("Phân phối", "Hợp đồng phân phối, đại lý bán hàng"),
        ("Gia công", "Hợp đồng gia công sản xuất, chế tạo"),
        ("Vận chuyển", "Hợp đồng vận chuyển, logistics"),
        
        # Hợp đồng dịch vụ
        ("Dịch vụ", "Hợp đồng cung cấp dịch vụ chuyên nghiệp"),
        ("Tư vấn", "Hợp đồng tư vấn, hỗ trợ kỹ thuật"),
        ("Bảo trì", "Hợp đồng bảo trì, sửa chữa thiết bị"),
        ("Thiết kế", "Hợp đồng thiết kế, sáng tạo nội dung"),
        ("Marketing", "Hợp đồng quảng cáo, marketing, truyền thông"),
        ("IT/Phần mềm", "Hợp đồng phát triển phần mềm, IT"),
        
        # Hợp đồng lao động và nhân sự
        ("Lao động", "Hợp đồng lao động, thuê mướn nhân viên"),
        ("Thực tập", "Hợp đồng thực tập sinh"),
        ("Cộng tác viên", "Hợp đồng cộng tác viên, freelancer"),
        ("Đào tạo", "Hợp đồng đào tạo, giảng dạy"),
        
        # Hợp đồng bất động sản
        ("Thuê mặt bằng", "Hợp đồng thuê văn phòng, mặt bằng kinh doanh"),
        ("Thuê nhà", "Hợp đồng thuê nhà ở, căn hộ"),
        ("Thuê kho", "Hợp đồng thuê kho bãi, nhà xưởng"),
        ("Mua bán BĐS", "Hợp đồng mua bán bất động sản"),
        
        # Hợp đồng tài chính
        ("Vay vốn", "Hợp đồng vay vốn, tín dụng"),
        ("Bảo lãnh", "Hợp đồng bảo lãnh, đảm bảo"),
        ("Bảo hiểm", "Hợp đồng bảo hiểm các loại"),
        ("Đầu tư", "Hợp đồng đầu tư, góp vốn"),
        
        # Hợp đồng hợp tác
        ("Hợp tác", "Hợp đồng hợp tác kinh doanh, liên doanh"),
        ("Liên kết", "Hợp đồng liên kết chiến lược"),
        ("Nhượng quyền", "Hợp đồng nhượng quyền thương mại (franchise)"),
        ("Đối tác", "Thỏa thuận đối tác, partnership"),
        
        # Hợp đồng pháp lý và bảo mật
        ("Bảo mật (NDA)", "Thỏa thuận bảo mật thông tin"),
        ("Bản quyền", "Hợp đồng chuyển nhượng bản quyền, sở hữu trí tuệ"),
        ("Giấy phép", "Hợp đồng cấp phép sử dụng"),
        ("Pháp lý", "Hợp đồng dịch vụ pháp lý, luật sư"),
        
        # Hợp đồng khung và đặc biệt
        ("Nguyên tắc/Khung", "Hợp đồng khung, thỏa thuận nguyên tắc"),
        ("Ghi nhớ (MOU)", "Biên bản ghi nhớ, thỏa thuận sơ bộ"),
        ("Ý định (LOI)", "Thư ý định, letter of intent"),
        ("Sửa đổi/Phụ lục", "Phụ lục sửa đổi hợp đồng"),
        
        # Hợp đồng xuất nhập khẩu
        ("Xuất khẩu", "Hợp đồng xuất khẩu hàng hóa"),
        ("Nhập khẩu", "Hợp đồng nhập khẩu hàng hóa"),
        ("Thương mại quốc tế", "Hợp đồng thương mại quốc tế"),
        
        # Loại khác
        ("Khác", "Các loại hợp đồng khác"),
    ]
    
    try:
        # Kết nối database
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        
        # Xóa tất cả contract types cũ
        print("🗑️ Đang xóa contract types cũ...")
        cursor.execute("DELETE FROM contract_types")
        conn.commit()
        print("✅ Đã xóa contract types cũ")
        
        # Reset identity seed
        cursor.execute("DBCC CHECKIDENT ('contract_types', RESEED, 0)")
        conn.commit()
        
        # Tạo contract types mới
        print("📝 Đang tạo contract types mới...")
        for name, description in new_types:
            cursor.execute(
                "INSERT INTO contract_types (name, description, created_at) VALUES (?, ?, ?)",
                (name, description, datetime.now())
            )
            print(f"✅ Đã tạo loại hợp đồng: {name}")
        
        conn.commit()
        
        # Kiểm tra kết quả
        cursor.execute("SELECT COUNT(*) FROM contract_types")
        count = cursor.fetchone()[0]
        print(f"🎉 Đã tạo thành công {count} loại hợp đồng mới!")
        
        # Hiển thị danh sách
        print("\n📋 Danh sách loại hợp đồng:")
        cursor.execute("SELECT id, name, description FROM contract_types ORDER BY id")
        for row in cursor.fetchall():
            print(f"  {row[0]}: {row[1]} - {row[2]}")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Lỗi khi cập nhật contract types: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    try:
        print("📋 Script bắt đầu chạy...")
        update_contract_types()
        print("🎉 Hoàn thành!")
    except Exception as e:
        print(f"💥 Lỗi: {e}")
        import traceback
        traceback.print_exc()
