from fastapi import APIRouter

router = APIRouter(prefix="/orders")

@router.get("/")
def get_orders():
    return [{"id": 100, "order_name": "Nước hoa"}]

@router.get("/{order_id}")
def get_order(order_id: int):
    return {"id": order_id}