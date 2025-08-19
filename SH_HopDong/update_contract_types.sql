-- Script để cập nhật danh sách loại hợp đồng
-- Xóa tất cả contract types cũ
DELETE FROM contract_types;

-- Thêm các loại hợp đồng mới
INSERT INTO contract_types (name, description) VALUES 
-- Hợp đồng kinh doanh cơ bản
('Mua bán', 'Hợp đồng mua bán hàng hóa, sản phẩm, dịch vụ'),
('Cung cấp', 'Hợp đồng cung cấp nguyên vật liệu, thiết bị'),
('Phân phối', 'Hợp đồng phân phối, đại lý bán hàng'),
('Gia công', 'Hợp đồng gia công sản xuất, chế tạo'),
('Vận chuyển', 'Hợp đồng vận chuyển, logistics'),

-- Hợp đồng dịch vụ
('Dịch vụ', 'Hợp đồng cung cấp dịch vụ chuyên nghiệp'),
('Tư vấn', 'Hợp đồng tư vấn, hỗ trợ kỹ thuật'),
('Bảo trì', 'Hợp đồng bảo trì, sửa chữa thiết bị'),
('Thiết kế', 'Hợp đồng thiết kế, sáng tạo nội dung'),
('Marketing', 'Hợp đồng quảng cáo, marketing, truyền thông'),
('IT/Phần mềm', 'Hợp đồng phát triển phần mềm, IT'),

-- Hợp đồng lao động và nhân sự
('Lao động', 'Hợp đồng lao động, thuê mướn nhân viên'),
('Thực tập', 'Hợp đồng thực tập sinh'),
('Cộng tác viên', 'Hợp đồng cộng tác viên, freelancer'),
('Đào tạo', 'Hợp đồng đào tạo, giảng dạy'),

-- Hợp đồng bất động sản
('Thuê mặt bằng', 'Hợp đồng thuê văn phòng, mặt bằng kinh doanh'),
('Thuê nhà', 'Hợp đồng thuê nhà ở, căn hộ'),
('Thuê kho', 'Hợp đồng thuê kho bãi, nhà xưởng'),
('Mua bán BĐS', 'Hợp đồng mua bán bất động sản'),

-- Hợp đồng tài chính
('Vay vốn', 'Hợp đồng vay vốn, tín dụng'),
('Bảo lãnh', 'Hợp đồng bảo lãnh, đảm bảo'),
('Bảo hiểm', 'Hợp đồng bảo hiểm các loại'),
('Đầu tư', 'Hợp đồng đầu tư, góp vốn'),

-- Hợp đồng hợp tác
('Hợp tác', 'Hợp đồng hợp tác kinh doanh, liên doanh'),
('Liên kết', 'Hợp đồng liên kết chiến lược'),
('Nhượng quyền', 'Hợp đồng nhượng quyền thương mại (franchise)'),
('Đối tác', 'Thỏa thuận đối tác, partnership'),

-- Hợp đồng pháp lý và bảo mật
('Bảo mật (NDA)', 'Thỏa thuận bảo mật thông tin'),
('Bản quyền', 'Hợp đồng chuyển nhượng bản quyền, sở hữu trí tuệ'),
('Giấy phép', 'Hợp đồng cấp phép sử dụng'),
('Pháp lý', 'Hợp đồng dịch vụ pháp lý, luật sư'),

-- Hợp đồng khung và đặc biệt
('Nguyên tắc/Khung', 'Hợp đồng khung, thỏa thuận nguyên tắc'),
('Ghi nhớ (MOU)', 'Biên bản ghi nhớ, thỏa thuận sơ bộ'),
('Ý định (LOI)', 'Thư ý định, letter of intent'),
('Sửa đổi/Phụ lục', 'Phụ lục sửa đổi hợp đồng'),

-- Hợp đồng xuất nhập khẩu
('Xuất khẩu', 'Hợp đồng xuất khẩu hàng hóa'),
('Nhập khẩu', 'Hợp đồng nhập khẩu hàng hóa'),
('Thương mại quốc tế', 'Hợp đồng thương mại quốc tế'),

-- Loại khác
('Khác', 'Các loại hợp đồng khác');

-- Hiển thị kết quả
SELECT COUNT(*) as 'Tổng số loại hợp đồng' FROM contract_types;
SELECT id, name, description FROM contract_types ORDER BY id;
