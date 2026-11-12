import { isOffline, OfflineState, ErrorState } from '@/shoppy/components/States';
import { confirmAction } from '@/shoppy/components/ConfirmDialog';
import { toast } from 'sonner';
import { createFileRoute } from '@tanstack/react-router';
import { useContext } from 'react';
import { CartContext } from '@/shoppy/cart-context';
import React, { useEffect, useState } from 'react';
import { Link, useNavigate } from '@/shoppy/navigation';
import { getCart, updateCartItem, removeFromCart, clearCart, createOrder } from '@/shoppy/services/api';

function CartPage({ onCartUpdate }) {
  const [cart, setCart] = useState(null);
  const [loading, setLoading] = useState(true);
  const [loadError, setLoadError] = useState('');
  const [placing, setPlacing] = useState(false);
  const navigate = useNavigate();

  const loadCart = async () => {
    try {
      const data = await getCart();
      setCart(data);
      if (onCartUpdate) onCartUpdate();
    } catch (err) {
      console.error('Failed to load cart:', err);
        setLoadError(err.message || 'Could not load your cart.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadCart();
  }, []);

  const handleUpdateQty = async (productId, newQty) => {
    try {
      await updateCartItem(productId, newQty);
      await loadCart();
    } catch (err) {
      toast.error(err.message || 'Failed to update quantity');
    }
  };

  const handleRemove = async (productId) => {
    try {
      await removeFromCart(productId);
      await loadCart();
    } catch (err) {
      toast.error(err.message || 'Failed to remove item');
    }
  };

  const handleClear = async () => {
    if (!(await confirmAction({ title: 'Clear your cart?', description: 'All items will be removed.', confirmLabel: 'Clear cart', danger: true }))) return;
    try {
      await clearCart();
      await loadCart();
    } catch (err) {
      toast.error(err.message || 'Failed to clear cart');
    }
  };

  const handlePlaceOrder = async () => {
    try {
      setPlacing(true);
      const res = await createOrder();
      if (onCartUpdate) onCartUpdate();
      toast.success(res.message || 'Order received by the store service', { description: res.order_number ? `Order ID: ${res.order_number}` : undefined });
      navigate('/orders');
    } catch (err) {
      toast.error(err.message || 'Failed to place order');
    } finally {
      setPlacing(false);
    }
  };

  if (isOffline()) return <OfflineState what="your cart" />;
  if (loadError) return <ErrorState message={loadError} onRetry={() => window.location.reload()} />;
  if (loading) {
    return (
      <div className="empty-state">
        <div className="loading-spinner"></div>
        <p style={{ marginTop: '12px' }}>Loading your cart...</p>
      </div>
    );
  }

  const items = cart?.items || [];

  return (
    <div>
      <div className="page-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end' }}>
        <div>
          <h2>Your Shopping Cart</h2>
          <p>{items.length === 0 ? 'Your cart is empty' : `${cart.total_items} items in your bag`}</p>
        </div>
        {items.length > 0 && (
          <button className="btn btn-danger btn-sm" onClick={handleClear}>
            Clear Cart
          </button>
        )}
      </div>

      {items.length === 0 ? (
        <div className="empty-state card">
          <div className="icon">🛒</div>
          <h3>Your cart is empty</h3>
          <p>Explore our wide selection of tech gear or talk to our AI assistant to find recommendations.</p>
          <div style={{ marginTop: '16px', display: 'flex', gap: '12px', justifyContent: 'center' }}>
            <Link to="/products" className="btn btn-primary">
              Browse Products
            </Link>
            <Link to="/assistant" className="btn btn-secondary">
              Ask AI Assistant
            </Link>
          </div>
        </div>
      ) : (
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))',
            gap: 'var(--space-2xl)',
            alignItems: 'start',
          }}
        >
          {/* Cart Items List */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-md)' }}>
            {items.map((item) => (
              <div
                key={item.id}
                className="card"
                style={{
                  display: 'flex',
                  gap: 'var(--space-md)',
                  alignItems: 'center',
                }}
              >
                <div
                  style={{
                    width: '60px',
                    height: '60px',
                    background: 'var(--bg-tertiary)',
                    borderRadius: 'var(--radius-md)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    fontSize: '1.8rem',
                  }}
                >
                  📦
                </div>

                <div style={{ flex: 1 }}>
                  <div
                    style={{
                      fontSize: '0.75rem',
                      color: 'var(--accent-primary)',
                      fontWeight: '600',
                      textTransform: 'uppercase',
                    }}
                  >
                    {item.product_brand}
                  </div>
                  <Link
                    to={`/products/${item.product_id}`}
                    style={{
                      fontWeight: '600',
                      color: 'var(--text-primary)',
                      fontSize: '1rem',
                    }}
                  >
                    {item.product_name}
                  </Link>
                  <div style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>
                    ₹{item.product_price.toLocaleString('en-IN')} each
                  </div>
                </div>

                {/* Quantity Controls */}
                <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                  <button
                    className="btn btn-secondary btn-icon"
                    style={{ width: '32px', height: '32px', fontSize: '1rem' }}
                    onClick={() => handleUpdateQty(item.product_id, item.quantity - 1)}
                    disabled={item.quantity <= 1}
                  >
                    -
                  </button>
                  <span style={{ fontWeight: '600', minWidth: '24px', textAlign: 'center' }}>
                    {item.quantity}
                  </span>
                  <button
                    className="btn btn-secondary btn-icon"
                    style={{ width: '32px', height: '32px', fontSize: '1rem' }}
                    onClick={() => handleUpdateQty(item.product_id, item.quantity + 1)}
                  >
                    +
                  </button>
                </div>

                {/* Subtotal */}
                <div style={{ textAlign: 'right', minWidth: '90px' }}>
                  <div style={{ fontWeight: '700', fontSize: '1.1rem' }}>
                    ₹{item.subtotal.toLocaleString('en-IN')}
                  </div>
                  <button
                    style={{
                      background: 'none',
                      color: 'var(--error)',
                      fontSize: '0.8rem',
                      textDecoration: 'underline',
                      marginTop: '4px',
                    }}
                    onClick={() => handleRemove(item.product_id)}
                  >
                    Remove
                  </button>
                </div>
              </div>
            ))}
          </div>

          {/* Order Summary Box */}
          <div className="card" style={{ padding: 'var(--space-xl)' }}>
            <h3 style={{ marginBottom: 'var(--space-lg)' }}>Order Summary</h3>

            <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-md)' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', color: 'var(--text-secondary)' }}>
                <span>Subtotal ({cart.total_items} items)</span>
                <span>₹{cart.total_amount.toLocaleString('en-IN')}</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', color: 'var(--text-secondary)' }}>
                <span>Shipping</span>
                <span style={{ color: 'var(--success)' }}>FREE</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', color: 'var(--text-secondary)' }}>
                <span>Simulated Taxes (18% GST)</span>
                <span>Included</span>
              </div>

              <div
                style={{
                  borderTop: '1px solid var(--border-color)',
                  paddingTop: 'var(--space-md)',
                  display: 'flex',
                  justifyContent: 'space-between',
                  fontSize: '1.3rem',
                  fontWeight: '800',
                }}
              >
                <span>Total</span>
                <span>₹{cart.total_amount.toLocaleString('en-IN')}</span>
              </div>

              <div
                className="badge badge-processing"
                style={{ alignSelf: 'flex-start', padding: '6px 12px', margin: '8px 0' }}
              >
                ℹ️ Simulated Checkout — No Real Charges
              </div>

              <button
                className="btn btn-primary"
                style={{ width: '100%', padding: '14px', fontSize: '1.05rem' }}
                disabled={placing}
                onClick={handlePlaceOrder}
              >
                {placing ? 'Placing Order...' : '🚀 Place Simulated Order'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export const Route = createFileRoute('/cart')({head: () => ({meta: [{title: 'AgentCart — Shopping cart'},{name:'description',content:'Shopping cart at AgentCart: smart shopping, product discovery, and comparison.'},{property:'og:title',content:'AgentCart — Shopping cart'},{property:'og:description',content:'Shopping cart at AgentCart: smart shopping, product discovery, and comparison.'},{property:'og:type',content:'website'},{name:'twitter:card',content:'summary_large_image'}]}), component: ImportedPage});
function ImportedPage() { const {refreshCart} = useContext(CartContext); return <CartPage onCartUpdate={refreshCart} />; }
