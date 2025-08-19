# PowerShell script để cập nhật loại hợp đồng
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   Cập nhật loại hợp đồng - SQL Server" -ForegroundColor Cyan  
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Cấu hình kết nối
$Server = "localhost"
$Database = "SH_HopDong"

Write-Host "[1/3] Kiểm tra kết nối SQL Server..." -ForegroundColor Yellow

try {
    # Test connection
    $connectionString = "Server=$Server;Database=$Database;Integrated Security=true;"
    $connection = New-Object System.Data.SqlClient.SqlConnection($connectionString)
    $connection.Open()
    
    # Check current types count
    $command = $connection.CreateCommand()
    $command.CommandText = "SELECT COUNT(*) FROM contract_types"
    $currentCount = $command.ExecuteScalar()
    
    Write-Host "✅ Kết nối thành công! Hiện có $currentCount loại hợp đồng" -ForegroundColor Green
    $connection.Close()
    
} catch {
    Write-Host "❌ Không thể kết nối đến SQL Server: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "Vui lòng kiểm tra:" -ForegroundColor Yellow
    Write-Host "- SQL Server đang chạy" -ForegroundColor Yellow
    Write-Host "- Database SH_HopDong tồn tại" -ForegroundColor Yellow
    Write-Host "- Windows Authentication được bật" -ForegroundColor Yellow
    Read-Host "Nhấn Enter để thoát"
    exit 1
}

Write-Host ""
Write-Host "[2/3] Xóa dữ liệu cũ..." -ForegroundColor Yellow

try {
    $connection = New-Object System.Data.SqlClient.SqlConnection($connectionString)
    $connection.Open()
    
    # Delete old data
    $command = $connection.CreateCommand()
    $command.CommandText = "DELETE FROM contract_types"
    $deletedRows = $command.ExecuteNonQuery()
    
    # Reset identity
    $command.CommandText = "DBCC CHECKIDENT ('contract_types', RESEED, 0)"
    $command.ExecuteNonQuery()
    
    Write-Host "✅ Đã xóa $deletedRows loại hợp đồng cũ" -ForegroundColor Green
    $connection.Close()
    
} catch {
    Write-Host "❌ Lỗi khi xóa dữ liệu cũ: $($_.Exception.Message)" -ForegroundColor Red
    Read-Host "Nhấn Enter để thoát"
    exit 1
}

Write-Host ""
Write-Host "[3/3] Thêm loại hợp đồng mới..." -ForegroundColor Yellow

# Danh sach loai hop dong moi
$contractTypes = @(
    @("Mua ban", "Hop dong mua ban hang hoa, san pham, dich vu"),
    @("Cung cap", "Hop dong cung cap nguyen vat lieu, thiet bi"),
    @("Phan phoi", "Hop dong phan phoi, dai ly ban hang"),
    @("Gia cong", "Hop dong gia cong san xuat, che tao"),
    @("Van chuyen", "Hop dong van chuyen, logistics"),
    @("Dich vu", "Hop dong cung cap dich vu chuyen nghiep"),
    @("Tu van", "Hop dong tu van, ho tro ky thuat"),
    @("Bao tri", "Hop dong bao tri, sua chua thiet bi"),
    @("Thiet ke", "Hop dong thiet ke, sang tao noi dung"),
    @("Marketing", "Hop dong quang cao, marketing, truyen thong"),
    @("IT/Phan mem", "Hop dong phat trien phan mem, IT"),
    @("Lao dong", "Hop dong lao dong, thue muon nhan vien"),
    @("Thuc tap", "Hop dong thuc tap sinh"),
    @("Cong tac vien", "Hop dong cong tac vien, freelancer"),
    @("Dao tao", "Hop dong dao tao, giang day"),
    @("Thue mat bang", "Hop dong thue van phong, mat bang kinh doanh"),
    @("Thue nha", "Hop dong thue nha o, can ho"),
    @("Thue kho", "Hop dong thue kho bai, nha xuong"),
    @("Mua ban BDS", "Hop dong mua ban bat dong san"),
    @("Vay von", "Hop dong vay von, tin dung"),
    @("Bao lanh", "Hop dong bao lanh, dam bao"),
    @("Bao hiem", "Hop dong bao hiem cac loai"),
    @("Dau tu", "Hop dong dau tu, gop von"),
    @("Hop tac", "Hop dong hop tac kinh doanh, lien doanh"),
    @("Lien ket", "Hop dong lien ket chien luoc"),
    @("Nhuong quyen", "Hop dong nhuong quyen thuong mai (franchise)"),
    @("Doi tac", "Thoa thuan doi tac, partnership"),
    @("Bao mat (NDA)", "Thoa thuan bao mat thong tin"),
    @("Ban quyen", "Hop dong chuyen nhuong ban quyen, so huu tri tue"),
    @("Giay phep", "Hop dong cap phep su dung"),
    @("Phap ly", "Hop dong dich vu phap ly, luat su"),
    @("Nguyen tac/Khung", "Hop dong khung, thoa thuan nguyen tac"),
    @("Ghi nho (MOU)", "Bien ban ghi nho, thoa thuan so bo"),
    @("Y dinh (LOI)", "Thu y dinh, letter of intent"),
    @("Sua doi/Phu luc", "Phu luc sua doi hop dong"),
    @("Xuat khau", "Hop dong xuat khau hang hoa"),
    @("Nhap khau", "Hop dong nhap khau hang hoa"),
    @("Thuong mai quoc te", "Hop dong thuong mai quoc te"),
    @("Khac", "Cac loai hop dong khac")
)

try {
    $connection = New-Object System.Data.SqlClient.SqlConnection($connectionString)
    $connection.Open()
    
    $insertedCount = 0
    foreach ($type in $contractTypes) {
        $command = $connection.CreateCommand()
        $command.CommandText = "INSERT INTO contract_types (name, description, created_at) VALUES (@name, @description, @created_at)"
        $command.Parameters.AddWithValue("@name", $type[0])
        $command.Parameters.AddWithValue("@description", $type[1])
        $command.Parameters.AddWithValue("@created_at", (Get-Date))
        $command.ExecuteNonQuery()
        $insertedCount++
        Write-Host "✅ Đã tạo: $($type[0])" -ForegroundColor Green
    }
    
    $connection.Close()
    
    Write-Host ""
    Write-Host "🎉 Đã tạo thành công $insertedCount loại hợp đồng mới!" -ForegroundColor Green
    
} catch {
    Write-Host "❌ Lỗi khi thêm dữ liệu mới: $($_.Exception.Message)" -ForegroundColor Red
    Read-Host "Nhấn Enter để thoát"
    exit 1
}

Write-Host ""
Write-Host "✅ Hoàn thành cập nhật loại hợp đồng!" -ForegroundColor Green
Read-Host "Nhấn Enter để thoát"
