"""
Script to add contract types via web interface
"""
import requests
import json

# Base URL of the application
BASE_URL = "http://localhost:8000"

# List of new contract types
contract_types = [
    {"name": "Mua bán", "description": "Hợp đồng mua bán hàng hóa, sản phẩm, dịch vụ"},
    {"name": "Cung cấp", "description": "Hợp đồng cung cấp nguyên vật liệu, thiết bị"},
    {"name": "Phân phối", "description": "Hợp đồng phân phối, đại lý bán hàng"},
    {"name": "Gia công", "description": "Hợp đồng gia công sản xuất, chế tạo"},
    {"name": "Vận chuyển", "description": "Hợp đồng vận chuyển, logistics"},
    {"name": "Dịch vụ", "description": "Hợp đồng cung cấp dịch vụ chuyên nghiệp"},
    {"name": "Tư vấn", "description": "Hợp đồng tư vấn, hỗ trợ kỹ thuật"},
    {"name": "Bảo trì", "description": "Hợp đồng bảo trì, sửa chữa thiết bị"},
    {"name": "Thiết kế", "description": "Hợp đồng thiết kế, sáng tạo nội dung"},
    {"name": "Marketing", "description": "Hợp đồng quảng cáo, marketing, truyền thông"},
    {"name": "IT/Phần mềm", "description": "Hợp đồng phát triển phần mềm, IT"},
    {"name": "Lao động", "description": "Hợp đồng lao động, thuê mướn nhân viên"},
    {"name": "Thực tập", "description": "Hợp đồng thực tập sinh"},
    {"name": "Cộng tác viên", "description": "Hợp đồng cộng tác viên, freelancer"},
    {"name": "Đào tạo", "description": "Hợp đồng đào tạo, giảng dạy"},
    {"name": "Thuê mặt bằng", "description": "Hợp đồng thuê văn phòng, mặt bằng kinh doanh"},
    {"name": "Thuê nhà", "description": "Hợp đồng thuê nhà ở, căn hộ"},
    {"name": "Thuê kho", "description": "Hợp đồng thuê kho bãi, nhà xưởng"},
    {"name": "Mua bán BĐS", "description": "Hợp đồng mua bán bất động sản"},
    {"name": "Vay vốn", "description": "Hợp đồng vay vốn, tín dụng"},
    {"name": "Bảo lãnh", "description": "Hợp đồng bảo lãnh, đảm bảo"},
    {"name": "Bảo hiểm", "description": "Hợp đồng bảo hiểm các loại"},
    {"name": "Đầu tư", "description": "Hợp đồng đầu tư, góp vốn"},
    {"name": "Hợp tác", "description": "Hợp đồng hợp tác kinh doanh, liên doanh"},
    {"name": "Liên kết", "description": "Hợp đồng liên kết chiến lược"},
    {"name": "Nhượng quyền", "description": "Hợp đồng nhượng quyền thương mại (franchise)"},
    {"name": "Đối tác", "description": "Thỏa thuận đối tác, partnership"},
    {"name": "Bảo mật (NDA)", "description": "Thỏa thuận bảo mật thông tin"},
    {"name": "Bản quyền", "description": "Hợp đồng chuyển nhượng bản quyền, sở hữu trí tuệ"},
    {"name": "Giấy phép", "description": "Hợp đồng cấp phép sử dụng"},
    {"name": "Pháp lý", "description": "Hợp đồng dịch vụ pháp lý, luật sư"},
    {"name": "Nguyên tắc/Khung", "description": "Hợp đồng khung, thỏa thuận nguyên tắc"},
    {"name": "Ghi nhớ (MOU)", "description": "Biên bản ghi nhớ, thỏa thuận sơ bộ"},
    {"name": "Ý định (LOI)", "description": "Thư ý định, letter of intent"},
    {"name": "Sửa đổi/Phụ lục", "description": "Phụ lục sửa đổi hợp đồng"},
    {"name": "Xuất khẩu", "description": "Hợp đồng xuất khẩu hàng hóa"},
    {"name": "Nhập khẩu", "description": "Hợp đồng nhập khẩu hàng hóa"},
    {"name": "Thương mại quốc tế", "description": "Hợp đồng thương mại quốc tế"},
    {"name": "Khác", "description": "Các loại hợp đồng khác"},
]

def add_contract_types():
    """Add contract types via web interface"""
    print("🚀 Bắt đầu thêm loại hợp đồng...")
    
    success_count = 0
    error_count = 0
    
    for contract_type in contract_types:
        try:
            # Send POST request to add contract type
            response = requests.post(
                f"{BASE_URL}/types",
                data={
                    "name": contract_type["name"],
                    "description": contract_type["description"]
                },
                allow_redirects=False
            )
            
            if response.status_code in [200, 303]:  # 303 is redirect after successful POST
                print(f"✅ Đã thêm: {contract_type['name']}")
                success_count += 1
            else:
                print(f"❌ Lỗi khi thêm {contract_type['name']}: {response.status_code}")
                error_count += 1
                
        except Exception as e:
            print(f"❌ Lỗi khi thêm {contract_type['name']}: {e}")
            error_count += 1
    
    print(f"\n🎉 Hoàn thành! Thành công: {success_count}, Lỗi: {error_count}")

if __name__ == "__main__":
    print("📋 Script bắt đầu chạy...")
    print("⚠️  Đảm bảo ứng dụng đang chạy tại http://localhost:8000")
    
    try:
        # Test if application is running
        response = requests.get(f"{BASE_URL}/types", timeout=5)
        if response.status_code == 200:
            print("✅ Ứng dụng đang chạy")
            add_contract_types()
        else:
            print("❌ Ứng dụng không phản hồi đúng cách")
    except requests.exceptions.RequestException as e:
        print(f"❌ Không thể kết nối đến ứng dụng: {e}")
        print("Vui lòng khởi động ứng dụng trước khi chạy script này")
