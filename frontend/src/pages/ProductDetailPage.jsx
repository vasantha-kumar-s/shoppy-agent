import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { getProduct, addToCart } from '../services/api';

const CATEGORY_IMAGES = {
  laptops: 'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=600&h=400&fit=crop',
  smartphones: 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=600&h=400&fit=crop',
  headphones: 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=600&h=400&fit=crop',
  monitors: 'https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=600&h=400&fit=crop',
  keyboards: 'https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=600&h=400&fit=crop',
  mice: 'https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=600&h=400&fit=crop',
  smartwatches: 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=600&h=400&fit=crop',
};

export default function ProductDetailPage({ onCartUpdate }) {
  const { id } = useParams();
  const [product, setProduct] = useState(null);
  const [quantity, setQuantity] = useState(1);
  const [loading, setLoading] = useState(true);
  const [adding, setAdding] = useState(false);
  const [notification, setNotification] = useState(null);

  useEffect(() => {
    async function loadProduct() {
      try {
        const data = await getProduct(id);
        setProduct(data);
      } catch (err) {
        console.error('Failed to load product:', err);
      } finally {
        setLoading(false);
      }
    }
    loadProduct();
  }, [id]);

  const handleAddToCart = async () => {
    try {
      setAdding(true);
      await addToCart(product.id, quantity);
      if (onCartUpdate) onCartUpdate();
      setNotification(`Added ${quantity}× "${product.name}" to your cart!`);
      setTimeout(() => setNotification(null), 4000);
    } catch (err) {
      alert(err.message || 'Could not add to cart');
    } finally {
      setAdding(false);
    }
  };

  if (loading) {
    return (
      <div className="empty-state">
        <div className="loading-spinner"></div>
        <p style={{ marginTop: '12px' }}>Loading product...</p>
      </div>
    );
  }

  if (!product) {
    return (
      <div className="empty-state card">
        <div className="icon">❌</div>
        <h3>Product Not Found</h3>
        <p>This product doesn't exist or has been removed.</p>
        <Link to="/products" className="btn btn-primary" style={{ marginTop: '16px' }}>
          Back to Catalog
        </Link>
      </div>
    );
  }

  const stock = product.inventory?.quantity ?? 0;
  const isOutOfStock = stock <= 0;
  const categorySlug = product.category?.slug || '';
  const imageUrl = CATEGORY_IMAGES[categorySlug] || CATEGORY_IMAGES.laptops;

  return (
    <div>
      <div style={{ marginBottom: 'var(--space-md)' }}>
        <Link to="/products" style={{ color: 'var(--text-secondary)', fontSize: '0.88rem' }}>
          ← Back to Products
        </Link>
      </div>

      {notification && (
        <div
          className="card"
          style={{
            background: 'var(--success-bg)',
            borderColor: 'var(--success)',
            color: 'var(--success)',
            marginBottom: 'var(--space-lg)',
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
          }}
        >
          <span>✓ {notification}</span>
          <Link to="/cart" className="btn btn-primary btn-sm">
            View Cart
          </Link>
        </div>
      )}

      <div
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))',
          gap: 'var(--space-2xl)',
          marginBottom: 'var(--space-2xl)',
        }}
      >
        {/* Product Image */}
        <div
          className="card"
          style={{
            minHeight: '340px',
            padding: 0,
            overflow: 'hidden',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            background: '#f5f3ee',
          }}
        >
          <img
            src={imageUrl}
            alt={product.name}
            style={{
              width: '100%',
              height: '100%',
              objectFit: 'cover',
              minHeight: '340px',
            }}
            onError={(e) => { e.target.style.display = 'none'; }}
          />
        </div>

        {/* Info Column */}
        <div style={{ display: 'flex', flexDirection: 'column' }}>
          <div
            style={{
              display: 'inline-block',
              alignSelf: 'flex-start',
              padding: '3px 12px',
              borderRadius: 'var(--radius-full)',
              background: 'rgba(180, 130, 60, 0.08)',
              color: 'var(--accent-primary)',
              fontSize: '0.72rem',
              fontWeight: '700',
              textTransform: 'uppercase',
              letterSpacing: '0.06em',
              marginBottom: '10px',
            }}
          >
            {product.brand}
          </div>
          <h1 style={{ fontSize: '1.7rem', fontWeight: '700', marginBottom: '10px', letterSpacing: '-0.02em' }}>
            {product.name}
          </h1>

          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: 'var(--space-md)',
              marginBottom: 'var(--space-md)',
            }}
          >
            <div className="product-rating" style={{ fontSize: '1rem' }}>
              ★ {product.rating.toFixed(1)}
            </div>
            <span
              className={`product-stock ${
                isOutOfStock ? 'out-of-stock' : stock < 15 ? 'low-stock' : 'in-stock'
              }`}
            >
              {isOutOfStock ? 'Out of Stock' : `${stock} available`}
            </span>
          </div>

          <div
            style={{
              fontSize: '1.8rem',
              fontWeight: '800',
              color: 'var(--text-primary)',
              marginBottom: 'var(--space-lg)',
              letterSpacing: '-0.02em',
            }}
          >
            <span style={{ fontSize: '1rem', color: 'var(--text-secondary)', fontWeight: '500' }}>₹</span>
            {product.price.toLocaleString('en-IN')}
          </div>

          <p
            style={{
              color: 'var(--text-secondary)',
              lineHeight: 1.7,
              marginBottom: 'var(--space-xl)',
              fontSize: '0.92rem',
            }}
          >
            {product.description}
          </p>

          {/* Action Row */}
          <div
            style={{
              display: 'flex',
              gap: 'var(--space-md)',
              alignItems: 'center',
              marginBottom: 'var(--space-xl)',
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <label style={{ fontSize: '0.88rem', color: 'var(--text-secondary)' }}>
                Qty:
              </label>
              <select
                value={quantity}
                onChange={(e) => setQuantity(parseInt(e.target.value))}
                disabled={isOutOfStock}
                style={{ width: '70px' }}
              >
                {[...Array(Math.min(stock || 1, 10)).keys()].map((n) => (
                  <option key={n + 1} value={n + 1}>
                    {n + 1}
                  </option>
                ))}
              </select>
            </div>

            <button
              className="btn btn-primary"
              style={{ flex: 1, padding: '12px 24px' }}
              disabled={isOutOfStock || adding}
              onClick={handleAddToCart}
            >
              {adding ? 'Adding...' : isOutOfStock ? 'Out of Stock' : 'Add to Cart'}
            </button>
          </div>

          {/* Warranty Info */}
          {product.warranty && (
            <div
              className="card"
              style={{
                padding: 'var(--space-md)',
                display: 'flex',
                alignItems: 'center',
                gap: 'var(--space-sm)',
                fontSize: '0.88rem',
                color: 'var(--text-secondary)',
              }}
            >
              <span>🛡️</span>
              <span>
                <strong>Warranty:</strong> {product.warranty}
              </span>
            </div>
          )}
        </div>
      </div>

      {/* Specifications Table */}
      {product.specifications && Object.keys(product.specifications).length > 0 && (
        <section className="card" style={{ marginBottom: 'var(--space-2xl)' }}>
          <h3 style={{ marginBottom: 'var(--space-md)', fontSize: '1.15rem', fontWeight: '700' }}>
            Specifications
          </h3>
          <div
            style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))',
              gap: '12px',
            }}
          >
            {Object.entries(product.specifications).map(([key, value]) => (
              <div
                key={key}
                style={{
                  background: 'var(--bg-tertiary)',
                  padding: '14px 16px',
                  borderRadius: 'var(--radius-md)',
                }}
              >
                <div
                  style={{
                    fontSize: '0.7rem',
                    textTransform: 'uppercase',
                    color: 'var(--accent-primary)',
                    fontWeight: '700',
                    letterSpacing: '0.06em',
                    marginBottom: '3px',
                  }}
                >
                  {key.replace(/_/g, ' ')}
                </div>
                <div style={{ color: 'var(--text-primary)', fontWeight: '500', fontSize: '0.92rem' }}>
                  {typeof value === 'object' ? JSON.stringify(value) : String(value)}
                </div>
              </div>
            ))}
          </div>
        </section>
      )}
    </div>
  );
}
