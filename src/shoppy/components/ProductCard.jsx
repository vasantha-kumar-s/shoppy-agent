import smartwatchesAsset from '../assets/smartwatches.jpg.asset.json';
import miceAsset from '../assets/mice.jpg.asset.json';
import keyboardsAsset from '../assets/keyboards.jpg.asset.json';
import monitorsAsset from '../assets/monitors.jpg.asset.json';
import headphonesAsset from '../assets/headphones.jpg.asset.json';
import smartphonesAsset from '../assets/smartphones.jpg.asset.json';
import laptopsAsset from '../assets/laptops.jpg.asset.json';
import React from 'react';
import { Link } from '../navigation';

const CATEGORY_IMAGES = {
  laptops: laptopsAsset.url,
  smartphones: smartphonesAsset.url,
  headphones: headphonesAsset.url,
  monitors: monitorsAsset.url,
  keyboards: keyboardsAsset.url,
  mice: miceAsset.url,
  smartwatches: smartwatchesAsset.url,
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
