#!/usr/bin/env python3
"""
Script để cập nhật danh sách loại hợp đồng
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.db.database import SessionLocal
from app.db.models import ContractType

def update_contract_types():
    """Cập nhật danh sách loại hợp đồng"""
    print("🚀 Bắt đầu cập nhật loại hợp đồng...")
    
    new_types = [
        {"name": "Mua bán", "description": "Hợp đồng mua bán hàng hóa, sản phẩm"},
        {"name": "Dịch vụ", "description": "Hợp đồng cung cấp dịch vụ"},
        {"name": "Lao động", "description": "Hợp đồng lao động, thuê mướn nhân viên"},
        {"name": "Thuê mướn", "description": "Hợp đồng thuê mặt bằng, thiết bị"},
        {"name": "Hợp tác", "description": "Hợp đồng hợp tác kinh doanh"},
        {"name": "Tư vấn", "description": "Hợp đồng tư vấn chuyên nghiệp"},
        {"name": "Vận chuyển", "description": "Hợp đồng vận chuyển, logistics"},
        {"name": "Bảo mật (NDA)", "description": "Thỏa thuận bảo mật thông tin"},
        {"name": "Bảo hiểm", "description": "Hợp đồng bảo hiểm"},
        {"name": "Khác", "description": "Các loại hợp đồng khác"},
    ]
    
    db = SessionLocal()
    try:
        # Xóa tất cả contract types cũ
        print("Đang xóa contract types cũ...")
        db.query(ContractType).delete()
        db.commit()
        print("✅ Đã xóa contract types cũ")
        
        # Tạo contract types mới
        print("Đang tạo contract types mới...")
        for type_data in new_types:
            contract_type = ContractType(
                name=type_data["name"],
                description=type_data["description"]
            )
            db.add(contract_type)
            print(f"Đã tạo loại hợp đồng: {type_data['name']}")
        
        db.commit()
        print(f"✅ Đã tạo thành công {len(new_types)} loại hợp đồng mới!")
        
    except Exception as e:
        print(f"❌ Lỗi khi cập nhật contract types: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    try:
        print("📋 Script bắt đầu chạy...")
        update_contract_types()
        print("🎉 Hoàn thành!")
    except Exception as e:
        print(f"💥 Lỗi: {e}")
        import traceback
        traceback.print_exc()
