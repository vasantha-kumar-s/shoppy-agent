import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { getOrders } from '../services/api';

export default function OrdersPage() {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchOrders() {
      try {
        const data = await getOrders();
        setOrders(data);
      } catch (err) {
        console.error('Failed to fetch orders:', err);
      } finally {
        setLoading(false);
      }
    }
    fetchOrders();
  }, []);

  const getStatusBadge = (status) => {
    switch (status?.toLowerCase()) {
      case 'confirmed': return 'badge-confirmed';
      case 'processing': return 'badge-processing';
      case 'shipped': return 'badge-shipped';
      case 'delivered': return 'badge-delivered';
      default: return 'badge-cancelled';
    }
  };

  if (loading) {
    return (
      <div className="empty-state">
        <div className="loading-spinner"></div>
        <p style={{ marginTop: '12px' }}>Loading order history...</p>
      </div>
    );
  }

  return (
    <div>
      <div className="page-header">
        <h2>Order History</h2>
        <p>Review simulated orders placed through the store or AI assistant</p>
      </div>

      {orders.length === 0 ? (
        <div className="empty-state card">
          <div className="icon">📦</div>
          <h3>No orders placed yet</h3>
          <p>Once you purchase items using the cart or the voice AI agent, they'll appear here.</p>
          <Link to="/products" className="btn btn-primary" style={{ marginTop: '16px' }}>
            Start Shopping
          </Link>
        </div>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-lg)' }}>
          {orders.map((order) => (
            <div key={order.order_id} className="card">
              <div
                style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                  paddingBottom: 'var(--space-md)',
                  borderBottom: '1px solid var(--border-color)',
                  marginBottom: 'var(--space-md)',
                  flexWrap: 'wrap',
                  gap: 'var(--space-sm)',
                }}
              >
                <div>
                  <span style={{ fontWeight: '700', fontSize: '1.1rem' }}>
                    Order #{order.order_number}
                  </span>
                  <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                    Placed on {order.created_at ? new Date(order.created_at).toLocaleDateString('en-IN', {
                      year: 'numeric',
                      month: 'short',
                      day: 'numeric',
                      hour: '2-digit',
                      minute: '2-digit'
                    }) : 'Recent'}
                  </div>
                </div>

                <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-md)' }}>
                  <span className={`badge ${getStatusBadge(order.status)}`}>
                    {order.status}
                  </span>
                  <div style={{ fontSize: '1.2rem', fontWeight: '800' }}>
                    ₹{order.total_amount.toLocaleString('en-IN')}
                  </div>
                </div>
              </div>

              {/* Items Breakdown */}
              <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-sm)' }}>
                {order.items?.map((item, idx) => (
                  <div
                    key={idx}
                    style={{
                      display: 'flex',
                      justifyContent: 'space-between',
                      alignItems: 'center',
                      fontSize: '0.9rem',
                    }}
                  >
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                      <span>🏷️</span>
                      <Link to={`/products/${item.product_id}`} style={{ color: 'var(--text-primary)' }}>
                        {item.product_name}
                      </Link>
                      <span style={{ color: 'var(--text-muted)' }}>x {item.quantity}</span>
                    </div>
                    <div style={{ fontWeight: '600' }}>
                      ₹{item.subtotal?.toLocaleString('en-IN')}
                    </div>
                  </div>
                ))}
              </div>

              {/* Shipping Address */}
              {order.shipping_address && (
                <div
                  style={{
                    marginTop: 'var(--space-md)',
                    paddingTop: 'var(--space-md)',
                    borderTop: '1px solid var(--border-color)',
                    fontSize: '0.85rem',
                    color: 'var(--text-secondary)',
                  }}
                >
                  📍 <strong>Shipping Address:</strong> {order.shipping_address}
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
