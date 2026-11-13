# Hướng dẫn khởi tạo và chạy dự án FastAPI

## 1. Yêu cầu môi trường

- Python 3.14 (bản ổn định)
- Visual Studio Code
- VS Code Python Extension
- Pip (Python Package Manager)

Kiểm tra phiên bản Python:

```powershell
py -3.14 --version
```

## 2. Khởi tạo Project

Tạo thư mục dự án và di chuyển vào thư mục:

```powershell
mkdir fastapi-project
cd fastapi-project
```

Tạo Virtual Environment:

```powershell
py -3.14 -m venv .venv
```

Kích hoạt môi trường:

```powershell
.\.venv\Scripts\Activate.ps1
```

Khi kích hoạt thành công, Terminal hiển thị `(.venv)`.

## 3. Cài đặt thư viện

Cập nhật pip:

```powershell
python -m pip install --upgrade pip
```

Cài FastAPI:

```powershell
python -m pip install "fastapi[standard]"
```

Xuất danh sách thư viện vào `requirements.txt`:

```powershell
python -m pip freeze > requirements.txt
```

Khi clone dự án từ GitHub, có thể cài lại các thư viện bằng lệnh:

```powershell
python -m pip install -r requirements.txt
```

## 4. Cấu trúc thư mục

```text
fastapi-project/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── users.py
│   │   └── products.py
│   ├── schemas/
│   ├── models/
│   └── services/
├── tests/
├── .venv/
├── .gitignore
└── requirements.txt
```

Chức năng:

- `main.py`: Khởi tạo ứng dụng FastAPI và đăng ký Routers.
- `routers/`: Quản lý các API Endpoint.
- `schemas/`: Định nghĩa Pydantic Models để kiểm tra dữ liệu.
- `models/`: Định nghĩa các Models làm việc với Database.
- `services/`: Xử lý Business Logic.
- `tests/`: Chứa các bài kiểm thử.

## 5. Tạo API đầu tiên

File `app/main.py`:

```python
from fastapi import FastAPI

app = FastAPI(
    title="My FastAPI Project",
    version="1.0.0"
)

@app.get("/")
def home():
    return {"message": "FastAPI is running"}
```

## 6. Chạy Project

Mở Terminal tại thư mục gốc `fastapi-project`.

Kích hoạt Virtual Environment (nếu chưa kích hoạt):

```powershell
.\.venv\Scripts\Activate.ps1
```

Khởi động Server:

```powershell

py -m uvicorn app.main:app --reload --port 8000
```

Trong đó:

- `app.main`: File `app/main.py`.
- `:app`: Biến ứng dụng FastAPI.
- `--reload`: Tự động reload khi sửa code, chỉ dùng khi phát triển.
- `--port 8000`: Cổng chạy Backend.

Các đường dẫn sau hoạt động khi Server đang chạy:

| Chức năng | URL |
|---|---|
| API Home | http://127.0.0.1:8000/ |
| Swagger UI | http://127.0.0.1:8000/docs |
| ReDoc | http://127.0.0.1:8000/redoc |
| OpenAPI JSON | http://127.0.0.1:8000/openapi.json |

Dừng Server bằng `Ctrl + C`.

## 7. Cấu hình Git

Tạo file `.gitignore`:

```gitignore
.venv/
__pycache__/
*.pyc
.env
.pytest_cache/
.vscode/
```

Không đưa thư mục `.venv` hoặc file `.env` chứa thông tin bí mật lên GitHub.

## 8. Các lệnh thường dùng

| Lệnh | Chức năng |
|---|---|
| `py -3.14 -m venv .venv` | Tạo môi trường ảo |
| `.\.venv\Scripts\Activate.ps1` | Kích hoạt môi trường |
| `python -m pip install package` | Cài thư viện |
| `python -m pip list` | Xem thư viện đã cài |
| `python -m pip freeze > requirements.txt` | Xuất danh sách dependencies |
| `python -m pip install -r requirements.txt` | Cài dependencies từ file |
| `python -m uvicorn app.main:app --reload` | Chạy FastAPI tại port 8000 |
| `deactivate` | Thoát môi trường ảo |

**Lưu ý:** Trong VS Code, hãy chọn Python Interpreter tại `.venv\Scripts\python.exe` để bảo đảm các package được nhận diện đúng.