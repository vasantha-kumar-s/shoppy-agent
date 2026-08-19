"""
AgentCart — API Integration Tests.
"""

import pytest


@pytest.mark.asyncio
async def test_health_api(client):
    """Test /api/health endpoint."""
    resp = await client.get("/api/health")
    assert resp.status_code == 200
    data = resp.json()
    assert "services" in data
    assert data["services"]["database"]["status"] == "online"


@pytest.mark.asyncio
async def test_list_products_api(client):
    """Test GET /api/products."""
    resp = await client.get("/api/products?limit=5")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) <= 5


@pytest.mark.asyncio
async def test_get_categories_api(client):
    """Test GET /api/products/categories."""
    resp = await client.get("/api/products/categories")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) >= 7


@pytest.mark.asyncio
async def test_get_product_detail_api(client):
    """Test GET /api/products/{id}."""
    resp = await client.get("/api/products/1")
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == 1
    assert "specifications" in data


@pytest.mark.asyncio
async def test_cart_api_flow(client):
    """Test /api/cart endpoints."""
    # 1. Add item
    add_resp = await client.post("/api/cart/items", json={"product_id": 1, "quantity": 1})
    assert add_resp.status_code == 200

    # 2. Get cart
    get_resp = await client.get("/api/cart")
    assert get_resp.status_code == 200
    data = get_resp.json()
    assert data["total_items"] >= 1

    # 3. Clear cart
    del_resp = await client.delete("/api/cart")
    assert del_resp.status_code == 200


@pytest.mark.asyncio
async def test_orders_api(client):
    """Test GET /api/orders."""
    resp = await client.get("/api/orders")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)
