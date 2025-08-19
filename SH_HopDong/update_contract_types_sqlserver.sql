-- Script để cập nhật danh sách loại hợp đồng cho SQL Server
-- Sử dụng database SH_HopDong
USE SH_HopDong;
GO

-- Xóa tất cả contract types cũ
DELETE FROM contract_types;
GO

-- Reset identity seed
DBCC CHECKIDENT ('contract_types', RESEED, 0);
GO

-- Thêm các loại hợp đồng mới
INSERT INTO contract_types (name, description, created_at) VALUES 
-- Hợp đồng kinh doanh cơ bản
(N'Mua bán', N'Hợp đồng mua bán hàng hóa, sản phẩm, dịch vụ', GETDATE()),
(N'Cung cấp', N'Hợp đồng cung cấp nguyên vật liệu, thiết bị', GETDATE()),
(N'Phân phối', N'Hợp đồng phân phối, đại lý bán hàng', GETDATE()),
(N'Gia công', N'Hợp đồng gia công sản xuất, chế tạo', GETDATE()),
(N'Vận chuyển', N'Hợp đồng vận chuyển, logistics', GETDATE()),

-- Hợp đồng dịch vụ
(N'Dịch vụ', N'Hợp đồng cung cấp dịch vụ chuyên nghiệp', GETDATE()),
(N'Tư vấn', N'Hợp đồng tư vấn, hỗ trợ kỹ thuật', GETDATE()),
(N'Bảo trì', N'Hợp đồng bảo trì, sửa chữa thiết bị', GETDATE()),
(N'Thiết kế', N'Hợp đồng thiết kế, sáng tạo nội dung', GETDATE()),
(N'Marketing', N'Hợp đồng quảng cáo, marketing, truyền thông', GETDATE()),
(N'IT/Phần mềm', N'Hợp đồng phát triển phần mềm, IT', GETDATE()),

-- Hợp đồng lao động và nhân sự
(N'Lao động', N'Hợp đồng lao động, thuê mướn nhân viên', GETDATE()),
(N'Thực tập', N'Hợp đồng thực tập sinh', GETDATE()),
(N'Cộng tác viên', N'Hợp đồng cộng tác viên, freelancer', GETDATE()),
(N'Đào tạo', N'Hợp đồng đào tạo, giảng dạy', GETDATE()),

-- Hợp đồng bất động sản
(N'Thuê mặt bằng', N'Hợp đồng thuê văn phòng, mặt bằng kinh doanh', GETDATE()),
(N'Thuê nhà', N'Hợp đồng thuê nhà ở, căn hộ', GETDATE()),
(N'Thuê kho', N'Hợp đồng thuê kho bãi, nhà xưởng', GETDATE()),
(N'Mua bán BĐS', N'Hợp đồng mua bán bất động sản', GETDATE()),

-- Hợp đồng tài chính
(N'Vay vốn', N'Hợp đồng vay vốn, tín dụng', GETDATE()),
(N'Bảo lãnh', N'Hợp đồng bảo lãnh, đảm bảo', GETDATE()),
(N'Bảo hiểm', N'Hợp đồng bảo hiểm các loại', GETDATE()),
(N'Đầu tư', N'Hợp đồng đầu tư, góp vốn', GETDATE()),

-- Hợp đồng hợp tác
(N'Hợp tác', N'Hợp đồng hợp tác kinh doanh, liên doanh', GETDATE()),
(N'Liên kết', N'Hợp đồng liên kết chiến lược', GETDATE()),
(N'Nhượng quyền', N'Hợp đồng nhượng quyền thương mại (franchise)', GETDATE()),
(N'Đối tác', N'Thỏa thuận đối tác, partnership', GETDATE()),

-- Hợp đồng pháp lý và bảo mật
(N'Bảo mật (NDA)', N'Thỏa thuận bảo mật thông tin', GETDATE()),
(N'Bản quyền', N'Hợp đồng chuyển nhượng bản quyền, sở hữu trí tuệ', GETDATE()),
(N'Giấy phép', N'Hợp đồng cấp phép sử dụng', GETDATE()),
(N'Pháp lý', N'Hợp đồng dịch vụ pháp lý, luật sư', GETDATE()),

-- Hợp đồng khung và đặc biệt
(N'Nguyên tắc/Khung', N'Hợp đồng khung, thỏa thuận nguyên tắc', GETDATE()),
(N'Ghi nhớ (MOU)', N'Biên bản ghi nhớ, thỏa thuận sơ bộ', GETDATE()),
(N'Ý định (LOI)', N'Thư ý định, letter of intent', GETDATE()),
(N'Sửa đổi/Phụ lục', N'Phụ lục sửa đổi hợp đồng', GETDATE()),

-- Hợp đồng xuất nhập khẩu
(N'Xuất khẩu', N'Hợp đồng xuất khẩu hàng hóa', GETDATE()),
(N'Nhập khẩu', N'Hợp đồng nhập khẩu hàng hóa', GETDATE()),
(N'Thương mại quốc tế', N'Hợp đồng thương mại quốc tế', GETDATE()),

-- Loại khác
(N'Khác', N'Các loại hợp đồng khác', GETDATE());
GO

-- Hiển thị kết quả
PRINT 'Đã cập nhật thành công các loại hợp đồng!';
SELECT COUNT(*) as 'Tổng số loại hợp đồng' FROM contract_types;
SELECT id, name, description FROM contract_types ORDER BY id;
GO
