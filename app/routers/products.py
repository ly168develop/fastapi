from fastapi import APIRouter, status, Depends, Query
from sqlalchemy.orm import Session

from app.schemas.products import ProductCreate, ProductUpdating, ProductListResponse, ProductDetailResponse
from app.services.user_service import require_role
from app.services.product_service import create_new_product, get_all_product, get_product_detail, update_product_all_field, update_product_part, delete_single_product
from app.database import DbSession

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

@router.get("/", dependencies=[
        Depends(require_role(["admin", "user"]))
    ],
    response_model=ProductListResponse
)
def get_product_list(
    db: DbSession, 
    limit: int = Query(default=10, ge=1, le=100), 
    page: int = Query(default=1, ge=1),
):
    products = get_all_product(db, limit, page)
    return products


@router.get("/{product_id}", dependencies=[
        Depends(require_role(["admin", "user"]))
    ],
    response_model=ProductDetailResponse
)
def get_single_product(product_id: int, db: DbSession):
    product_detail = get_product_detail(product_id, db)
    return product_detail


@router.post("/", 
    status_code=status.HTTP_201_CREATED, 
    dependencies=[
        Depends(require_role(["admin", "user"]))
    ],
    response_model=ProductDetailResponse
)
def create_product(product: ProductCreate, db: DbSession):
    product = create_new_product(product, db)
    return product


@router.put("/{product_id}", status_code=status.HTTP_200_OK, 
    dependencies=[
        Depends(require_role(["admin", "user"]))
    ],
    response_model=ProductDetailResponse
)
def update_product(product_id: int, product: ProductCreate, db: DbSession):
    product_updated = update_product_all_field(product_id, product, db)
    return product_updated

@router.patch("/{product_id}", status_code=status.HTTP_200_OK, 
    dependencies=[
        Depends(require_role(["admin", "user"]))
    ],
    response_model=ProductDetailResponse
)
def part_update_product(product_id: int, product: ProductUpdating, db: DbSession):
    product_updated = update_product_part(product_id, product, db)
    return product_updated

@router.delete("/{product_id}", status_code=status.HTTP_200_OK, 
    dependencies=[
        Depends(require_role(["admin", "user"]))
    ]
)
def delete_product(product_id: int, db: DbSession):
    product_deleted = delete_single_product(product_id, db)
    return product_deleted