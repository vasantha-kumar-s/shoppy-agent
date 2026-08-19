import React, { useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import HomePage from './pages/HomePage';
import ProductsPage from './pages/ProductsPage';
import ProductDetailPage from './pages/ProductDetailPage';
import CartPage from './pages/CartPage';
import OrdersPage from './pages/OrdersPage';
import ComparisonPage from './pages/ComparisonPage';
import AssistantPage from './pages/AssistantPage';
import { getCart } from './services/api';

export default function App() {
  const [cartCount, setCartCount] = useState(0);

  const refreshCart = async () => {
    try {
      const data = await getCart();
      setCartCount(data?.total_items || 0);
    } catch {
      // Backend might be offline during initial boot
    }
  };

  useEffect(() => {
    refreshCart();
  }, []);

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout cartCount={cartCount} />}>
          <Route index element={<HomePage onCartUpdate={refreshCart} />} />
          <Route path="products" element={<ProductsPage onCartUpdate={refreshCart} />} />
          <Route path="products/:id" element={<ProductDetailPage onCartUpdate={refreshCart} />} />
          <Route path="cart" element={<CartPage onCartUpdate={refreshCart} />} />
          <Route path="orders" element={<OrdersPage />} />
          <Route path="compare" element={<ComparisonPage onCartUpdate={refreshCart} />} />
          <Route path="assistant" element={<AssistantPage onCartUpdate={refreshCart} />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
