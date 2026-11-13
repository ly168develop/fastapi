from fastapi import HTTPException
from math import ceil
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models.product_model import Product
from app.schemas.products import ProductCreate, ProductUpdating

def get_all_product(db: Session, limit: int, page: int):
    
    offset = (page - 1) * limit
    
    total = db.scalar(
        select(func.count()).select_from(Product)
    )

    products = db.scalars(
        select(Product)
        .order_by(Product.id)
        .offset(offset)
        .limit(limit)
    ).all()
    
    return {
        "message": "Get data successfully",
        "pagination": {
            "total": total,
            "page": page,
            "limit": limit,
            "total_pages": ceil(total / limit)
        },
        "data": products
    }
    
def get_product_detail(product_id: int, db: Session):
    product_detail = db.get(Product, product_id)
    
    if product_detail is None : 
        raise HTTPException(
            status_code=404,
            detail="Product is not found"
        )
    
    return {
        "message": "Get product detail successfully",
        "data": product_detail
    }

def create_new_product(product: ProductCreate, db: Session):
    existing = db.scalar(
        select(Product).where(
            (Product.name == product.name)
        )
    )
    
    if existing is not None:
        raise HTTPException(
            status_code=409,
            detail="Product already exists"
        )
        
    new_product = Product(
        name = product.name,
        price = product.price,
        sale = product.sale,
        quantity = product.quantity,
        description = product.description
    )
    
    db.add(new_product)
    
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Product violates a database constraint"
        )
        
    db.refresh(new_product)
    
    return {
        "message": "Product created successfully",
        "data": new_product
    }
    
def update_product_all_field(
    product_id: int, 
    product: ProductCreate, 
    db: Session
):
    product_updated = db.get(Product, product_id)
    
    if product_updated is None : 
        raise HTTPException(
            status_code=404,
            detail="Product is not found"
        )
    
    product_updated.name = product.name
    product_updated.price = product.price
    product_updated.sale = product.sale
    product_updated.quantity = product.quantity
    product_updated.description = product.description
    
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Product violates a database constraint"
        )
        
    db.refresh(product_updated)
    
    return {
        "message": "Update product successfully",
        "data": product_updated
    }
    
def update_product_part(product_id: int, product: ProductUpdating, db: Session):
    product_updated = db.get(Product, product_id)
        
    if product_updated is None : 
        raise HTTPException(
            status_code=404,
            detail="Product is not found"
        )
        
    update_data = product.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(product_updated, field, value)
    
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Product violates a database constraint"
        )
        
    db.refresh(product_updated)
        
    return {
        "message": "Update product successfully",
        "data": product_updated
    }

def delete_single_product(product_id: int, db: Session):
    product_updated = db.get(Product, product_id)
    if product_updated is None : 
        raise HTTPException(
            status_code=404,
            detail="Product is not found"
        )
    db.delete(product_updated)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Product violates a database constraint"
        )
    
    return {
        "message": "Product deleted successfully",
    }
