"""
Script đơn giản để thêm 10 loại hợp đồng phổ biến
"""
import requests
import time

# Danh sách 10 loại hợp đồng phổ biến
contract_types = [
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

def add_contract_types():
    """Thêm loại hợp đồng qua web API"""
    base_url = "http://localhost:8000"
    
    print("🚀 Bắt đầu thêm 10 loại hợp đồng...")
    
    success = 0
    for i, contract_type in enumerate(contract_types, 1):
        try:
            print(f"[{i}/10] Đang thêm: {contract_type['name']}")
            
            response = requests.post(
                f"{base_url}/types",
                data={
                    "name": contract_type["name"],
                    "description": contract_type["description"]
                },
                timeout=10
            )
            
            if response.status_code in [200, 303]:
                print(f"✅ Thành công: {contract_type['name']}")
                success += 1
            else:
                print(f"❌ Lỗi: {contract_type['name']} - Status: {response.status_code}")
                
            time.sleep(0.5)  # Nghỉ 0.5 giây giữa các request
            
        except Exception as e:
            print(f"❌ Lỗi khi thêm {contract_type['name']}: {e}")
    
    print(f"\n🎉 Hoàn thành! Đã thêm thành công {success}/10 loại hợp đồng")
    return success

if __name__ == "__main__":
    print("=" * 50)
    print("   THÊM 10 LOẠI HỢP ĐỒNG PHỔ BIẾN")
    print("=" * 50)
    
    # Kiểm tra ứng dụng có đang chạy không
    try:
        response = requests.get("http://localhost:8000/types", timeout=5)
        print("✅ Ứng dụng đang chạy tại http://localhost:8000")
        
        # Thêm loại hợp đồng
        success_count = add_contract_types()
        
        if success_count == 10:
            print("\n🎊 Tất cả loại hợp đồng đã được thêm thành công!")
            print("📋 Bạn có thể xem danh sách tại: http://localhost:8000/types")
        else:
            print(f"\n⚠️  Chỉ thêm được {success_count}/10 loại hợp đồng")
            
    except requests.exceptions.RequestException:
        print("❌ Không thể kết nối đến ứng dụng!")
        print("📝 Vui lòng:")
        print("   1. Chạy file run_app.bat để khởi động ứng dụng")
        print("   2. Đợi ứng dụng khởi động hoàn tất")
        print("   3. Chạy lại script này")
        
    input("\nNhấn Enter để thoát...")
