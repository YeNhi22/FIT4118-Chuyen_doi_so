<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>
    <h2 align="center">Hệ thống Số hóa và Quản lý Hợp đồng</h2>
    <p>
        Dự án được xây dựng bằng Python và FastAPI, nhằm thực hiện việc số hóa, phân tích và quản lý hợp đồng tự động sử dụng công nghệ OCR (Optical Character Recognition) và xử lý ngôn ngữ tự nhiên.
    </p>
    <h3>Chức năng của ứng dụng</h3>
    <ul>
      <li><strong>Số hóa hợp đồng tự động:</strong>
        <ul>
          <li>Tải lên file PDF, hình ảnh (PNG, JPG, JPEG, BMP, TIFF)</li>
          <li>Trích xuất văn bản bằng OCR với Tesseract</li>
          <li>Hỗ trợ đa ngôn ngữ (Tiếng Việt + Tiếng Anh)</li>
          <li>Xuất file Word (.docx) và văn bản (.txt)</li>
        </ul>
      </li>
      <li><strong>Phân tích và phân loại hợp đồng:</strong>
        <ul>
          <li>Tự động nhận diện loại hợp đồng (Mua bán, Lao động, Dịch vụ, Thuê, Hợp tác, Bảo mật)</li>
          <li>Trích xuất thông tin các bên tham gia</li>
          <li>Phát hiện ngày hiệu lực và ngày hết hạn</li>
          <li>Trích xuất giá trị hợp đồng và điều khoản quan trọng</li>
        </ul>
      </li>
      <li><strong>Quản lý dữ liệu toàn diện:</strong>
        <ul>
          <li>Lưu trữ và tìm kiếm hợp đồng</li>
          <li>Quản lý loại hợp đồng, đối tác, phòng ban</li>
          <li>Hệ thống nhãn (tags) và phân loại</li>
          <li>Báo cáo thống kê và theo dõi hết hạn</li>
        </ul>
      </li>
    </ul>
    <h3>Công nghệ OCR và xử lý văn bản</h3>
    <ul>
      <li><strong>OCR Engine:</strong> Tesseract với hỗ trợ tiếng Việt</li>
      <li><strong>Xử lý PDF:</strong> PyMuPDF (fitz) cho văn bản và hình ảnh</li>
      <li><strong>Xử lý hình ảnh:</strong> Pillow với tiền xử lý tự động</li>
      <li><strong>Phân tích văn bản:</strong> Regex patterns và NLP cơ bản</li>
      <li><strong>Xuất file:</strong> python-docx cho định dạng Word</li>
    </ul>
    <h3>Công nghệ phát triển</h3>
    <ul>
      <li>Python 3.x</li>
      <li>FastAPI</li>
      <li>SQLAlchemy</li>
      <li>Jinja2</li>
      <li>HTML5 + CSS3</li>
      <li>JavaScript</li>
      <li>Bootstrap</li>
      <li>SQLite/SQL Server</li>
    </ul>
    <h3>Cấu trúc dự án</h3>
    <ul>
      <li><code>app/main.py</code> - Ứng dụng FastAPI chính</li>
      <li><code>app/core/</code> - Thư viện xử lý cốt lõi:
        <ul>
          <li><code>ocr.py</code> - Xử lý OCR cho PDF và hình ảnh</li>
          <li><code>parser.py</code> - Phân tích và trích xuất thông tin hợp đồng</li>
          <li><code>config.py</code> - Cấu hình ứng dụng</li>
        </ul>
      </li>
      <li><code>app/db/</code> - Quản lý cơ sở dữ liệu:
        <ul>
          <li><code>models.py</code> - Định nghĩa bảng dữ liệu</li>
          <li><code>crud.py</code> - Các thao tác CRUD</li>
          <li><code>schemas.py</code> - Pydantic schemas</li>
        </ul>
      </li>
      <li><code>app/templates/</code> - Giao diện HTML</li>
      <li><code>app/static/</code> - Tài nguyên tĩnh</li>
      <li><code>uploads/</code> - Thư mục file tải lên</li>
      <li><code>outputs/</code> - Thư mục file đã xử lý</li>
    </ul>
    <h3>Hướng dẫn cài đặt</h3>
    <ol>
      <li>Clone repository:
        <pre><code>git clone https://github.com/YeNhi22/FIT4118-Chuyen_doi_so.git
cd contract-digitization</code></pre>
      </li>
      <li>Tạo môi trường ảo:
        <pre><code>python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac</code></pre>
      </li>
      <li>Cài đặt thư viện:
        <pre><code>pip install -r requirements.txt</code></pre>
      </li>
      <li>Cài đặt Tesseract OCR:
        <ul>
          <li>Windows: Tải từ <a href="https://github.com/UB-Mannheim/tesseract/wiki" target="_blank">GitHub Tesseract</a></li>
          <li>Linux: <code>sudo apt-get install tesseract-ocr tesseract-ocr-vie</code></li>
          <li>Mac: <code>brew install tesseract tesseract-lang</code></li>
        </ul>
      </li>
      <li>Chạy ứng dụng:
        <pre><code>.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000
</code></pre>
        hoặc
        <pre><code>run_app.bat  # Windows
run_app.ps1  # PowerShell</code></pre>
      </li>
      <li>Truy cập ứng dụng tại: <code>http://127.0.0.1:8000</code></li>
    </ol>
    <h3>Hướng dẫn sử dụng</h3>
    <ol>
      <li><strong>Tải lên hợp đồng:</strong>
        <ul>
          <li>Vào trang "Tải lên" từ menu chính</li>
          <li>Chọn loại hợp đồng</li>
          <li>Chọn file PDF hoặc hình ảnh hợp đồng</li>
          <li>Chọn ngôn ngữ OCR (Tiếng Việt + Tiếng Anh)</li>
          <li>Nhấn "Tải lên" để xử lý</li>
        </ul>
      </li>
      <li><strong>Xem kết quả:</strong>
        <ul>
          <li>Hệ thống tự động phân tích và phân loại</li>
          <li>Xem thông tin đã trích xuất</li>
          <li>Tải về file Word hoặc văn bản</li>
        </ul>
      </li>
      <li><strong>Quản lý hợp đồng:</strong>
        <ul>
          <li>Tìm kiếm theo nội dung, loại, đối tác</li>
          <li>Xem chi tiết và chỉnh sửa thông tin</li>
          <li>Theo dõi hợp đồng sắp hết hạn</li>
        </ul>
      </li>
    </ol>
    <h3>Tính năng nổi bật</h3>
    <ul>
      <li><strong>OCR chính xác cao:</strong> Hỗ trợ tiếng Việt với độ chính xác cao</li>
      <li><strong>Phân tích thông minh:</strong> Tự động nhận diện loại và trích xuất thông tin</li>
      <li><strong>Giao diện thân thiện:</strong> Responsive design, dễ sử dụng</li>
      <li><strong>Tìm kiếm mạnh mẽ:</strong> Full-text search với highlight</li>
      <li><strong>Báo cáo chi tiết:</strong> Thống kê và theo dõi trạng thái</li>
      <li><strong>Xuất đa định dạng:</strong> Word, Text, JSON</li>
    </ul>
    <h3>API Endpoints</h3>
    <ul>
      <li><code>GET /</code> - Trang chủ với thống kê</li>
      <li><code>POST /upload</code> - Tải lên và xử lý hợp đồng</li>
      <li><code>GET /search</code> - Tìm kiếm hợp đồng</li>
      <li><code>GET /detail/{id}</code> - Chi tiết hợp đồng</li>
      <li><code>GET /contract-types</code> - Quản lý loại hợp đồng</li>
      <li><code>GET /partners</code> - Quản lý đối tác</li>
      <li><code>GET /settings/ocr</code> - Cài đặt OCR</li>
    </ul>
    <h3>Cấu hình OCR</h3>
    <ul>
      <li><strong>Ngôn ngữ chính:</strong> vie+eng (Tiếng Việt + Tiếng Anh)</li>
      <li><strong>Chất lượng OCR:</strong> Balanced (Cân bằng tốc độ và độ chính xác)</li>
      <li><strong>Tiền xử lý:</strong> Tự động cải thiện chất lượng hình ảnh</li>
      <li><strong>Ngưỡng tin cậy:</strong> 70% (có thể điều chỉnh)</li>
      <li><strong>Timeout:</strong> 300 giây cho mỗi file</li>
    </ul>
    <h3>Yêu cầu hệ thống</h3>
    <ul>
      <li>Python 3.10+</li>
      <li>Tesseract OCR 4.0+</li>
      <li>RAM: Tối thiểu 4GB (khuyến nghị 8GB+)</li>
      <li>Ổ cứng: 2GB trống cho dữ liệu</li>
      <li>Trình duyệt: Chrome, Firefox, Safari, Edge</li>
    </ul>
    <h3>Thư viện chính</h3>
    <ul>
      <li><strong>FastAPI:</strong> Web framework hiện đại</li>
      <li><strong>SQLAlchemy:</strong> ORM cho cơ sở dữ liệu</li>
      <li><strong>Pytesseract:</strong> Python wrapper cho Tesseract</li>
      <li><strong>PyMuPDF:</strong> Xử lý file PDF</li>
      <li><strong>Pillow:</strong> Xử lý hình ảnh</li>
      <li><strong>python-docx:</strong> Tạo file Word</li>
    </ul>
    <h3>Lưu ý quan trọng</h3>
    <p><strong>⚠️ Quan trọng:</strong></p>
    <ul>
      <li>Đảm bảo Tesseract được cài đặt và cấu hình đúng đường dẫn</li>
      <li>File hình ảnh nên có độ phân giải cao (300 DPI+) để OCR chính xác</li>
      <li>Hỗ trợ file PDF có thể tìm kiếm và PDF scan</li>
      <li>Dữ liệu được lưu trong SQLite, có thể chuyển sang SQL Server</li>
      <li>Backup dữ liệu thường xuyên trong môi trường production</li>
    </ul>
    <h3>Giao diện ứng dụng</h3>
    <p><strong>Dashboard quản lý hợp đồng với OCR tự động:</strong></p>
    <div align="center">
      Contract Management Dashboard<br>
      <small>Giao diện quản lý hợp đồng thông minh</small>
    </div>
    <div align="center">
      <strong>Phát triển bởi:</strong><br>
      <em>Dự án Số hóa Hợp đồng</em><br>
      <em>Sử dụng công nghệ OCR và AI</em>
    </div>
</body>
</html>
