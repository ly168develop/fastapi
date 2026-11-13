# Hướng dẫn dùng Alembic từ đầu trong dự án FastAPI

> Áp dụng cho **FastAPI + SQLAlchemy 2.x + PostgreSQL + Psycopg 3**, chạy trên Windows/PowerShell.
>
> **Khuyến nghị:** Dự án mới nên quản lý cấu trúc bảng bằng **Alembic ngay từ đầu**. Không cần gọi `Base.metadata.create_all()` khi đã dùng migration.

## 1. Alembic để làm gì?

- **SQLAlchemy Model:** Mô tả bảng/cột bằng Python.
- **Alembic Migration:** Ghi lại các thay đổi schema để tạo hoặc cập nhật bảng trong PostgreSQL.
- **`upgrade head`:** Áp dụng migration lên Database.
- **`downgrade -1`:** Lùi một revision (cẩn thận: có thể mất dữ liệu).

> Sửa Model **không** đồng nghĩa với việc Database tự thay đổi. Sau khi sửa Model, cần tạo, **kiểm tra** và chạy migration.

## 2. Cài đặt thư viện

Mở Terminal tại **thư mục gốc dự án** (nơi có `app/`):

```powershell
# Nếu đã có .venv
.\.venv\Scripts\Activate.ps1

python -m pip install "fastapi[standard]" sqlalchemy "psycopg[binary]" python-dotenv alembic
python -m pip freeze > requirements.txt
```

PostgreSQL cần chạy sẵn và Database (ví dụ `fastapi_db`) đã được tạo. **Alembic tạo bảng, không tự tạo Database PostgreSQL.**

## 3. Cấu trúc thư mục tham khảo

```text
fastAPI/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── product.py
│   ├── schemas/
│   ├── routers/
│   └── services/
├── alembic/
│   ├── env.py
│   └── versions/
├── alembic.ini
├── .env
├── .gitignore
└── requirements.txt
```

## 4. Cấu hình Database

**`.env`** (ví dụ; thay bằng giá trị của bạn):

```dotenv
DB_USER=postgres
DB_PASSWORD="your_password@here"
DB_HOST=localhost
DB_PORT=5432
DB_NAME=fastapi_db
```

**`app/database.py`**:

```python
import os
from dotenv import load_dotenv
from sqlalchemy import URL, create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

load_dotenv()

DATABASE_URL = URL.create(
    drivername="postgresql+psycopg",
    username=os.environ["DB_USER"],
    password=os.environ["DB_PASSWORD"],
    host=os.getenv("DB_HOST", "localhost"),
    port=int(os.getenv("DB_PORT", "5432")),
    database=os.environ["DB_NAME"],
)

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass

def get_db():
    with SessionLocal() as db:
        yield db
```

Dùng `URL.create()` giúp mật khẩu chứa `@`, `#`, `%`... không cần URL-encode thủ công.

**`.gitignore`** tối thiểu:

```gitignore
.venv/
.env
__pycache__/
*.pyc
.pytest_cache/
```

> Không đưa mật khẩu thật vào `alembic.ini`, source code hoặc Git.

## 5. Tạo SQLAlchemy Model đầu tiên

**`app/models/product.py`**:

```python
from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base

class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, default=1)
```

> `default=1` là mặc định do SQLAlchemy áp dụng khi insert qua ORM; nếu muốn mặc định ở mức Database, tìm hiểu thêm `server_default`.

## 6. Khởi tạo Alembic (chỉ một lần cho mỗi project)

```powershell
python -m alembic init alembic
```

Trong **`alembic/env.py`**, thêm import (trước phần `target_metadata`):

```python
from app.database import Base, engine
from app.models.product import Product  # Phải import Model để đăng ký metadata
```

Đổi:

```python
target_metadata = None
```

thành:

```python
target_metadata = Base.metadata
```

Trong hàm `run_migrations_online()`, thay đoạn tạo `connectable` từ `engine_from_config(...)` bằng:

```python
connectable = engine
```

Giữ nguyên đoạn `with connectable.connect() as connection:`, `context.configure(...)` và `context.run_migrations()` mà Alembic đã tạo.

**Chú ý:** Nếu có nhiều Model, phải import **tất cả** Model trước khi autogenerate, nếu không Alembic có thể hiểu nhầm bảng hiện có là bảng cần xóa.

Kiểm tra import tại thư mục gốc:

```powershell
python -c "from app.models.product import Product; print(Product.__tablename__)"
```

Kết quả: `products`.

## 7. Tạo bảng lần đầu bằng migration (dự án mới, DB chưa có bảng ứng dụng)

**Không chạy `create_all()` trước bước này.**

```powershell
# Tạo migration đầu tiên từ ORM Model
python -m alembic revision --autogenerate -m "create products table"
```

Mở file mới trong `alembic/versions/` và kiểm tra có lệnh kiểu `op.create_table("products", ...)` trong `upgrade()`.

```powershell
# Thực sự tạo bảng trong PostgreSQL
python -m alembic upgrade head

# Xem revision hiện tại
python -m alembic current
```

Mở pgAdmin → Database `fastapi_db` → Schemas → public → Tables → Refresh, bạn sẽ thấy bảng `products`.

## 8. Thêm hoặc sửa cột sau này

Ví dụ muốn thêm `description` vào class `Product`:

```python
description: Mapped[str | None] = mapped_column(String(500), nullable=True)
```

Chạy lần lượt:

```powershell
python -m alembic revision --autogenerate -m "add product description"
```

**Mở file migration mới và đọc `upgrade()` / `downgrade()` trước khi chạy.** Dự kiến có:

```python
op.add_column(
    "products",
    sa.Column("description", sa.String(length=500), nullable=True),
)
```

Nếu đúng mới chạy:

```powershell
python -m alembic upgrade head
```

**Lưu ý với cột `NOT NULL`:** Nếu bảng đã có dữ liệu, thường cần thêm cột nullable hoặc có `server_default`, cập nhật dữ liệu cũ, rồi mới đặt `NOT NULL`; không nên thêm cột bắt buộc một cách tùy tiện.

## 9. Lệnh thường dùng

| Lệnh | Công dụng |
|---|---|
| `python -m alembic init alembic` | Khởi tạo Alembic **một lần** |
| `python -m alembic revision --autogenerate -m "..."` | Sinh migration từ thay đổi Model |
| `python -m alembic upgrade head` | Áp dụng migration mới nhất |
| `python -m alembic current` | Xem revision hiện tại của Database |
| `python -m alembic history` | Xem lịch sử migration |
| `python -m alembic downgrade -1` | Lùi một revision, cần kiểm tra rủi ro |

## 10. Trường hợp đã tạo bảng bằng `create_all()` trước khi dùng Alembic

Không áp dụng lại migration `create_table` lên bảng đã tồn tại. Quy trình an toàn với dự án học hiện tại:

1. Đảm bảo SQLAlchemy Models khớp với các bảng đang có trong Database.
2. Khởi tạo Alembic và cấu hình `target_metadata`/`engine`.
3. Chạy `revision --autogenerate -m "baseline"` **trước khi sửa thêm Model**.
4. Kiểm tra file baseline: nếu cấu trúc khớp hoàn toàn thì `upgrade()` và `downgrade()` không cần thao tác schema (có thể là `pass`). Nếu xuất hiện `create_table`, `drop_table` hoặc thay đổi bất ngờ, **dừng lại** và kiểm tra.
5. Khi đã xác nhận baseline không gây thay đổi schema, chạy `upgrade head` để ghi nhận revision.
6. Từ đây về sau, chỉ thay đổi schema bằng các migration tiếp theo.

**Không xóa bảng hoặc Database đang chứa dữ liệu thật chỉ để chạy lại migration.**

## 11. Các lỗi thường gặp

- **`ModuleNotFoundError: No module named 'app.models.product'`**: kiểm tra tên file `product.py`/`products.py`, `__init__.py`, import và thư mục đang chạy lệnh.
- **`Target database is not up to date`**: kiểm tra `python -m alembic current`, `history`, và áp dụng migration còn thiếu trước khi tạo migration mới.
- **Migration trống dù đã sửa Model**: bảo đảm Model được import vào `alembic/env.py` (trực tiếp hoặc qua `app.models`).
- **Bị sinh `drop_table` ngoài ý muốn**: có thể Model chưa được import hoặc đang kết nối nhầm Database; **không chạy `upgrade`** trước khi tìm nguyên nhân.
- **Không kết nối PostgreSQL**: kiểm tra `.env`, tên Database, port `5432`, service PostgreSQL và interpreter `.venv`.

## 12. Quy trình ghi nhớ

```text
Tạo/Sửa SQLAlchemy Model
          ↓
revision --autogenerate
          ↓
KIỂM TRA file migration
          ↓
upgrade head
          ↓
Kiểm tra kết quả trong pgAdmin
```

> **Nguyên tắc:** Model mô tả trạng thái mong muốn; Alembic Migration là lịch sử thay đổi schema; PostgreSQL là nơi lưu dữ liệu thực tế. Với dự án mới, dùng Alembic từ đầu và không trộn lẫn với `create_all()`.
