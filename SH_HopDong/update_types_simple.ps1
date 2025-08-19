# Simple PowerShell script to update contract types
Write-Host "Updating contract types..." -ForegroundColor Green

# Connection string
$Server = "localhost"
$Database = "SH_HopDong"
$connectionString = "Server=$Server;Database=$Database;Integrated Security=true;"

try {
    # Create connection
    $connection = New-Object System.Data.SqlClient.SqlConnection($connectionString)
    $connection.Open()
    Write-Host "Connected to database successfully!" -ForegroundColor Green
    
    # Delete old data
    $command = $connection.CreateCommand()
    $command.CommandText = "DELETE FROM contract_types"
    $deletedRows = $command.ExecuteNonQuery()
    Write-Host "Deleted $deletedRows old contract types" -ForegroundColor Yellow
    
    # Reset identity
    $command.CommandText = "DBCC CHECKIDENT ('contract_types', RESEED, 0)"
    $command.ExecuteNonQuery()
    
    # Insert new data
    $insertSQL = "INSERT INTO contract_types (name, description, created_at) VALUES (@name, @description, @created_at)"
    
    $types = @(
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
    
    $count = 0
    foreach ($type in $types) {
        $command = $connection.CreateCommand()
        $command.CommandText = $insertSQL
        $command.Parameters.Clear()
        $command.Parameters.AddWithValue("@name", $type[0])
        $command.Parameters.AddWithValue("@description", $type[1])
        $command.Parameters.AddWithValue("@created_at", (Get-Date))
        $command.ExecuteNonQuery()
        $count++
        Write-Host "Added: $($type[0])" -ForegroundColor Green
    }
    
    Write-Host "Successfully added $count contract types!" -ForegroundColor Green
    $connection.Close()
    
} catch {
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "Done!" -ForegroundColor Green
