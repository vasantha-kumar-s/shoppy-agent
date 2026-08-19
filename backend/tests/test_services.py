"""
AgentCart — Service Layer Unit Tests.
"""

import pytest
from app.services.product_service import ProductService
from app.services.cart_service import CartService
from app.services.order_service import OrderService
from app.rag.retriever import PolicyRetriever


@pytest.mark.asyncio
async def test_search_products(db_session):
    """Test product search by keyword and category."""
    service = ProductService(db_session)
    products = await service.search_products(query="Sony")
    assert len(products) > 0
    assert any("Sony" in p.brand for p in products)


@pytest.mark.asyncio
async def test_filter_products_by_price(db_session):
    """Test filtering products by price range."""
    service = ProductService(db_session)
    products = await service.search_products(max_price=10000.0)
    for p in products:
        assert p.price <= 10000.0


@pytest.mark.asyncio
async def test_compare_products(db_session):
    """Test side-by-side product comparison."""
    service = ProductService(db_session)
    all_prods = await service.search_products(limit=2)
    ids = [p.id for p in all_prods]

    res = await service.compare_products(ids)
    assert len(res["products"]) == 2
    assert len(res["comparison_fields"]) > 0


@pytest.mark.asyncio
async def test_check_stock(db_session):
    """Test stock checking service."""
    service = ProductService(db_session)
    all_prods = await service.search_products(limit=1)
    p = all_prods[0]

    stock_info = await service.check_stock(p.id, quantity=1)
    assert stock_info["product_id"] == p.id
    assert stock_info["available_quantity"] > 0
    assert stock_info["in_stock"] is True


@pytest.mark.asyncio
async def test_cart_operations(db_session):
    """Test full cart lifecycle: add, view, update, remove, clear."""
    service = CartService(db_session)
    prod_service = ProductService(db_session)

    products = await prod_service.search_products(limit=1)
    p = products[0]

    # Clear first
    await service.clear_cart(user_id=1)
    await db_session.commit()

    # 1. Add to cart
    add_res = await service.add_to_cart(user_id=1, product_id=p.id, quantity=2)
    assert add_res.get("success") is True
    await db_session.commit()

    # 2. View cart
    cart = await service.get_cart(user_id=1)
    assert cart["total_items"] == 2
    assert len(cart["items"]) == 1

    # 3. Update quantity
    upd_res = await service.update_quantity(user_id=1, product_id=p.id, quantity=1)
    assert upd_res.get("success") is True
    await db_session.commit()

    # 4. View cart again
    cart = await service.get_cart(user_id=1)
    assert cart["total_items"] == 1

    # 5. Remove item
    rem_res = await service.remove_from_cart(user_id=1, product_id=p.id)
    assert rem_res.get("success") is True
    await db_session.commit()

    # 6. Clear
    await service.clear_cart(user_id=1)
    await db_session.commit()
    cart = await service.get_cart(user_id=1)
    assert cart["total_items"] == 0


@pytest.mark.asyncio
async def test_order_creation_flow(db_session):
    """Test simulated checkout order flow."""
    cart_service = CartService(db_session)
    prod_service = ProductService(db_session)
    order_service = OrderService(db_session)

    # Add 1 item
    products = await prod_service.search_products(limit=1)
    p = products[0]
    await cart_service.add_to_cart(user_id=1, product_id=p.id, quantity=1)
    await db_session.commit()

    # Create simulated order
    order_res = await order_service.create_order(user_id=1)
    assert order_res.get("success") is True
    assert "AC" in order_res["order_number"]
    await db_session.commit()

    # Verify cart is empty after order
    cart = await cart_service.get_cart(user_id=1)
    assert cart["total_items"] == 0

    # Verify order history
    history = await order_service.get_order_history(user_id=1)
    assert len(history) > 0


@pytest.mark.asyncio
async def test_policy_retriever(db_session):
    """Test RAG policy retriever."""
    retriever = PolicyRetriever(db_session)
    docs = await retriever.retrieve("return policy for laptop", top_k=2)
    assert len(docs) > 0
    assert any("return" in d["title"].lower() or "return" in d["content"].lower() for d in docs)
