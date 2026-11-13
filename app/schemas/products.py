from decimal import Decimal
from pydantic import BaseModel, Field, ConfigDict

class ProductCreate(BaseModel):
    name: str = Field(min_length=3)
    price: Decimal = Field(gt=0, max_digits=12, decimal_places=2)
    sale: Decimal = Field(default=Decimal("0"), ge=0, max_digits=12, decimal_places=2)
    quantity: int = Field(default=1, ge=0)
    description: str
    
class ProductUpdating(BaseModel):
    name: str = Field(default=None, min_length=3)
    price: Decimal = Field(default=None, gt=0, max_digits=12, decimal_places=2)
    sale: Decimal = Field(default=None, ge=0, max_digits=12, decimal_places=2)
    quantity: int = Field(default=None, ge=0)
    description: str = Field(default=None)

# RESPONSE
class ProductResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    price: Decimal
    sale: Decimal
    quantity: int
    description: str


class ProductDetailResponse(BaseModel):
    message: str
    data: ProductResponse


class ProductListResponse(BaseModel):
    message: str
    pagination: dict
    data: list[ProductResponse]
