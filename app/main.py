from fastapi import FastAPI

app = FastAPI()

from app.routers import users, products, orders, auth

app = FastAPI()

app.include_router(users.router)
app.include_router(products.router)
app.include_router(orders.router)
app.include_router(auth.router)
# @app.get("/users")
# def get_users():
#     return [
#         {"id": 1, "name": "Ly"},
#         {"id": 2, "name": "An"}
#     ]
    
# @app.get("/products/{product_id}")
# def get_products(product_id: int, category: str, limit: int = 10):
#     return {
#         "product_id": product_id,
#         "category": category,
#         "limit": limit
#     }


# class Product(BaseModel):
#     name: str = Field(min_length=3)
#     price: float = Field(gt=0)
#     quantity: int = Field(default=1, ge=0)


# @app.post("/products")
# def create_product(product: Product):
#     return {
#         "message": "Product created",
#         "product": product
#     }


# products = {
#     1: {"name": "Laptop", "price": 1200},
#     2: {"name": "Mouse", "price": 25}
# }

# @app.get("/products/{product_id}")
# def get_product(product_id: int):
#     if product_id not in products:
#         raise HTTPException(
#             status_code=404,
#             detail="Product not found"
#         )

#     return products[product_id]

# class userData():
#     def __init__(seft, name):
#         seft.name = name

#     @property
#     def name(seft):
#         return seft._name
#     @name.setter
#     def name (seft, name):
#         if name == "":
#             raise ValueError("ERORR")
#         else:
#             seft._name = name    
    
    
#     def getUser(seft):
#         return seft.name

# new_user = userData("Tran Ngoc Ly")

# print(new_user.name)

# new_user.name = "Tuyết Nhi"

# print(new_user.getUser())

    
# class ProductResponse(BaseModel):
#     id: int
#     name: str
#     price: float

# @app.get("/users/{user_id}", response_model=ProductResponse)
# def get_user(user_id: int):
#     if user_id <= 0:
#         raise HTTPException(
#             status_code=400,
#             detail="Invalid user ID"
#         )

#     if user_id != 1:
#         raise HTTPException(
#             status_code=404,
#             detail="User not found"
#         )

#     return {"id": 1, "name": "Ly", "price": 10.2}



# def check_role(role: str):
#     if role != "admin":
#         raise HTTPException(
#             status_code=403,
#             detail="Permission denied"
#         )

#     return role

# @app.get("/dashboard")
# def dashboard(role: str = Depends(check_role)):
#     return {"message": "Welcome Admin"}
