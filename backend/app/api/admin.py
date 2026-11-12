"""
AgentCart — Admin API Endpoints.

Handles admin authentication, product catalog CRUD, stock adjustment,
order status oversight, customer metrics, and sales analytics.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.database.connection import get_db
from app.services.admin_service import AdminService
from app.schemas.admin import (
    AdminLoginRequest,
    AdminLoginResponse,
    AdminProductCreate,
    AdminProductUpdate,
    AdminStockUpdate,
    AdminCustomerOut,
    AdminOrderOut,
    AdminOrderStatusUpdate,
    AdminAnalyticsOut,
)
from app.schemas.product import ProductOut

router = APIRouter(prefix="/api/admin", tags=["Admin"])


def get_admin_service(db: AsyncSession = Depends(get_db)) -> AdminService:
    """Dependency providing AdminService instance."""
    return AdminService(db)


@router.post("/login", response_model=AdminLoginResponse)
async def admin_login(
    req: AdminLoginRequest,
    service: AdminService = Depends(get_admin_service),
):
    """Authenticate administrator credentials."""
    auth_data = await service.authenticate_admin(req.email, req.password)
    if not auth_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid admin credentials. Use admin@agentcart.local and admin123.",
        )
    return AdminLoginResponse(**auth_data)


@router.get("/products", response_model=List[ProductOut])
async def list_admin_products(
    service: AdminService = Depends(get_admin_service),
):
    """List products with full inventory detail for administration."""
    from app.services.product_service import ProductService
    ps = ProductService(service.db)
    return await ps.search_products(limit=100)


@router.post("/products", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
async def create_product(
    data: AdminProductCreate,
    service: AdminService = Depends(get_admin_service),
):
    """Add a new product with initial stock."""
    prod = await service.create_product(data)
    return prod


@router.put("/products/{product_id}", response_model=ProductOut)
async def update_product(
    product_id: int,
    data: AdminProductUpdate,
    service: AdminService = Depends(get_admin_service),
):
    """Update an existing product listing and stock."""
    updated = await service.update_product(product_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail=f"Product #{product_id} not found")
    return updated


@router.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: int,
    service: AdminService = Depends(get_admin_service),
):
    """Delete a product from the catalog."""
    deleted = await service.delete_product(product_id)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Product #{product_id} not found")
    return None


@router.patch("/products/{product_id}/stock")
async def adjust_stock(
    product_id: int,
    data: AdminStockUpdate,
    service: AdminService = Depends(get_admin_service),
):
    """Adjust real-time stock quantity for a product."""
    return await service.adjust_stock(product_id, data.stock)


@router.get("/orders", response_model=List[AdminOrderOut])
async def list_admin_orders(
    service: AdminService = Depends(get_admin_service),
):
    """Fetch all store orders across all users."""
    return await service.list_orders()


@router.patch("/orders/{order_id}/status")
async def update_order_status(
    order_id: int,
    data: AdminOrderStatusUpdate,
    service: AdminService = Depends(get_admin_service),
):
    """Update order fulfillment status."""
    res = await service.update_order_status(order_id, data.status)
    if not res:
        raise HTTPException(status_code=404, detail=f"Order #{order_id} not found")
    return res


@router.get("/customers", response_model=List[AdminCustomerOut])
async def list_admin_customers(
    service: AdminService = Depends(get_admin_service),
):
    """List customer directory with spend and order metrics."""
    return await service.list_customers()


@router.get("/analytics", response_model=AdminAnalyticsOut)
async def get_admin_analytics(
    service: AdminService = Depends(get_admin_service),
):
    """Calculate sales trends and revenue analytics."""
    return await service.get_analytics()

