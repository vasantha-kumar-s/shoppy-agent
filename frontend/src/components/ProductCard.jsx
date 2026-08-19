import React from 'react';
import { Link } from 'react-router-dom';

const CATEGORY_IMAGES = {
  laptops: 'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=300&h=200&fit=crop',
  smartphones: 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=300&h=200&fit=crop',
  headphones: 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=300&h=200&fit=crop',
  monitors: 'https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=300&h=200&fit=crop',
  keyboards: 'https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=300&h=200&fit=crop',
  mice: 'https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=300&h=200&fit=crop',
  smartwatches: 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=300&h=200&fit=crop',
};

export default function ProductCard({ product, onAddToCart, adding }) {
  const stock = product.inventory?.quantity ?? 0;
  const isOutOfStock = stock <= 0;
  const isLowStock = stock > 0 && stock < 15;
  const categorySlug = product.category?.name?.toLowerCase() || product.category?.slug || '';
  const imageUrl = CATEGORY_IMAGES[categorySlug] || CATEGORY_IMAGES.laptops;

  return (
    <div className="product-card">
      <div className="product-card-image" style={{ background: '#f5f3ee' }}>
        <img
          src={imageUrl}
          alt={product.name}
          style={{
            width: '100%',
            height: '100%',
            objectFit: 'cover',
            opacity: 0.85,
            transition: 'opacity 0.3s ease, transform 0.3s ease',
          }}
          onMouseOver={(e) => { e.target.style.opacity = '1'; e.target.style.transform = 'scale(1.05)'; }}
          onMouseOut={(e) => { e.target.style.opacity = '0.85'; e.target.style.transform = 'scale(1)'; }}
          onError={(e) => { e.target.style.display = 'none'; }}
          loading="lazy"
        />
      </div>
      <div className="product-card-body">
        <div className="product-card-brand">{product.brand}</div>
        <Link to={`/products/${product.id}`} className="product-card-name">
          {product.name}
        </Link>
        <div className="product-card-price">
          <span className="currency">₹</span>
          {product.price.toLocaleString('en-IN')}
        </div>

        <div className="product-card-meta">
          <div className="product-rating">
            ★ {product.rating.toFixed(1)}
          </div>
          <span
            className={`product-stock ${
              isOutOfStock ? 'out-of-stock' : isLowStock ? 'low-stock' : 'in-stock'
            }`}
          >
            {isOutOfStock ? 'Sold Out' : isLowStock ? `Only ${stock} left` : 'In Stock'}
          </span>
        </div>

        <div style={{ marginTop: '14px', display: 'flex', gap: '8px' }}>
          <button
            className="btn btn-primary btn-sm"
            style={{ flex: 1 }}
            disabled={isOutOfStock || adding}
            onClick={() => onAddToCart && onAddToCart(product.id)}
          >
            {adding ? 'Adding...' : isOutOfStock ? 'Sold Out' : 'Add to Cart'}
          </button>
          <Link
            to={`/products/${product.id}`}
            className="btn btn-secondary btn-sm"
          >
            Details
          </Link>
        </div>
      </div>
    </div>
  );
}
