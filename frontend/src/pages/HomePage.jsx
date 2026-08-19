import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { getProducts, getCategories, addToCart } from '../services/api';
import ProductCard from '../components/ProductCard';

const HERO_FEATURES = [
  { icon: '🔍', title: 'Smart Search', desc: 'Natural language product discovery' },
  { icon: '🎙️', title: 'Voice Input', desc: 'Speak to search and shop' },
  { icon: '📊', title: 'Compare', desc: 'Side-by-side spec analysis' },
  { icon: '🛡️', title: 'Policy Q&A', desc: 'Instant return & warranty answers' },
];

export default function HomePage({ onCartUpdate }) {
  const [featured, setFeatured] = useState([]);
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [addingId, setAddingId] = useState(null);

  useEffect(() => {
    async function loadData() {
      try {
        const [prods, cats] = await Promise.all([
          getProducts({ limit: 6 }),
          getCategories(),
        ]);
        setFeatured(prods);
        setCategories(cats);
      } catch (err) {
        console.error('Failed to load home page data:', err);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  const handleAddToCart = async (productId) => {
    try {
      setAddingId(productId);
      await addToCart(productId, 1);
      if (onCartUpdate) onCartUpdate();
    } catch (err) {
      alert(err.message || 'Failed to add to cart');
    } finally {
      setAddingId(null);
    }
  };

  const CATEGORY_ICONS = {
    laptops: '💻', smartphones: '📱', headphones: '🎧',
    monitors: '🖥️', keyboards: '⌨️', mice: '🖱️', smartwatches: '⌚',
  };

  return (
    <div>
      {/* Hero Section */}
      <section
        style={{
          padding: '40px 36px',
          background: 'linear-gradient(135deg, #1b1b1f 0%, #2a2520 100%)',
          borderRadius: 'var(--radius-xl)',
          marginBottom: 'var(--space-2xl)',
          position: 'relative',
          overflow: 'hidden',
          color: 'white',
        }}
      >
        <div style={{ maxWidth: '560px', position: 'relative', zIndex: 2 }}>
          <div
            style={{
              display: 'inline-block',
              padding: '4px 14px',
              borderRadius: 'var(--radius-full)',
              background: 'rgba(180, 130, 60, 0.15)',
              color: '#d4a054',
              fontSize: '0.75rem',
              fontWeight: '600',
              marginBottom: '16px',
              letterSpacing: '0.03em',
            }}
          >
            Powered by Local AI
          </div>
          <h1
            style={{
              fontSize: '2.2rem',
              fontWeight: '800',
              lineHeight: 1.2,
              marginBottom: '14px',
              letterSpacing: '-0.03em',
            }}
          >
            Your personal
            <br />
            shopping assistant
          </h1>
          <p
            style={{
              fontSize: '1rem',
              color: 'rgba(255,255,255,0.6)',
              marginBottom: '28px',
              lineHeight: 1.6,
            }}
          >
            Search, compare, and shop with natural language.
            Voice-enabled, privacy-first — everything runs locally.
          </p>

          <div style={{ display: 'flex', gap: '10px', flexWrap: 'wrap' }}>
            <Link
              to="/assistant"
              className="btn btn-primary"
              style={{ padding: '12px 28px', fontSize: '0.92rem' }}
            >
              Start Shopping →
            </Link>
            <Link
              to="/products"
              className="btn"
              style={{
                padding: '12px 28px',
                background: 'rgba(255,255,255,0.08)',
                color: 'white',
                border: '1px solid rgba(255,255,255,0.12)',
                fontSize: '0.92rem',
              }}
            >
              Browse Catalog
            </Link>
          </div>
        </div>

        {/* Feature pills */}
        <div
          style={{
            display: 'flex',
            gap: '12px',
            marginTop: '32px',
            flexWrap: 'wrap',
          }}
        >
          {HERO_FEATURES.map((f) => (
            <div
              key={f.title}
              style={{
                padding: '8px 16px',
                background: 'rgba(255,255,255,0.05)',
                border: '1px solid rgba(255,255,255,0.08)',
                borderRadius: 'var(--radius-md)',
                display: 'flex',
                alignItems: 'center',
                gap: '8px',
                fontSize: '0.8rem',
              }}
            >
              <span>{f.icon}</span>
              <div>
                <div style={{ fontWeight: '600', color: 'rgba(255,255,255,0.9)' }}>{f.title}</div>
                <div style={{ fontSize: '0.72rem', color: 'rgba(255,255,255,0.4)' }}>{f.desc}</div>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Categories Grid */}
      <section style={{ marginBottom: 'var(--space-2xl)' }}>
        <div className="page-header">
          <h2>Shop by Category</h2>
          <p>Browse our curated electronics collection</p>
        </div>
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(130px, 1fr))',
            gap: 'var(--space-md)',
          }}
        >
          {categories.map((cat) => (
            <Link
              key={cat.id}
              to={`/products?category=${cat.slug}`}
              className="card"
              style={{
                textAlign: 'center',
                padding: '20px 14px',
                textDecoration: 'none',
                cursor: 'pointer',
              }}
            >
              <div style={{ fontSize: '1.8rem', marginBottom: '6px' }}>
                {CATEGORY_ICONS[cat.slug] || '📦'}
              </div>
              <div style={{ fontWeight: '600', fontSize: '0.85rem', color: 'var(--text-primary)' }}>
                {cat.name}
              </div>
            </Link>
          ))}
        </div>
      </section>

      {/* Featured Products */}
      <section>
        <div className="page-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end' }}>
          <div>
            <h2>Popular Products</h2>
            <p>Top-rated items loved by customers</p>
          </div>
          <Link to="/products" className="btn btn-secondary btn-sm">
            View All →
          </Link>
        </div>

        {loading ? (
          <div className="empty-state">
            <div className="loading-spinner"></div>
            <p style={{ marginTop: '12px' }}>Loading products...</p>
          </div>
        ) : (
          <div className="product-grid">
            {featured.map((product) => (
              <ProductCard
                key={product.id}
                product={product}
                onAddToCart={handleAddToCart}
                adding={addingId === product.id}
              />
            ))}
          </div>
        )}
      </section>
    </div>
  );
}
