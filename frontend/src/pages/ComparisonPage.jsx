import React, { useEffect, useState } from 'react';
import { useSearchParams, Link } from 'react-router-dom';
import { compareProducts, getProducts, addToCart } from '../services/api';

export default function ComparisonPage({ onCartUpdate }) {
  const [searchParams, setSearchParams] = useSearchParams();
  const [availableProducts, setAvailableProducts] = useState([]);
  const [comparison, setComparison] = useState(null);
  const [selectedIds, setSelectedIds] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    async function loadCatalog() {
      try {
        const data = await getProducts({ limit: 50 });
        setAvailableProducts(data);

        // Pre-select from URL if present
        const urlIds = searchParams.get('ids');
        if (urlIds) {
          const parsed = urlIds.split(',').map((id) => parseInt(id)).filter(Boolean);
          if (parsed.length >= 2) {
            setSelectedIds(parsed);
          }
        }
      } catch (err) {
        console.error('Failed to load products for comparison:', err);
      }
    }
    loadCatalog();
  }, []);

  useEffect(() => {
    if (selectedIds.length >= 2) {
      async function runComparison() {
        setLoading(true);
        try {
          const res = await compareProducts(selectedIds);
          setComparison(res);
          setSearchParams({ ids: selectedIds.join(',') });
        } catch (err) {
          console.error('Comparison error:', err);
        } finally {
          setLoading(false);
        }
      }
      runComparison();
    } else {
      setComparison(null);
    }
  }, [selectedIds]);

  const toggleSelect = (id) => {
    if (selectedIds.includes(id)) {
      setSelectedIds(selectedIds.filter((item) => item !== id));
    } else {
      if (selectedIds.length >= 4) {
        alert('You can compare a maximum of 4 products at once.');
        return;
      }
      setSelectedIds([...selectedIds, id]);
    }
  };

  const handleAddToCart = async (id) => {
    try {
      await addToCart(id, 1);
      if (onCartUpdate) onCartUpdate();
      alert('Product added to cart!');
    } catch (err) {
      alert(err.message || 'Failed to add to cart');
    }
  };

  return (
    <div>
      <div className="page-header">
        <h2>Product Comparison</h2>
        <p>Compare technical specifications, prices, and features side by side</p>
      </div>

      {/* Product Selector Bar */}
      <div className="card" style={{ marginBottom: 'var(--space-xl)' }}>
        <h4 style={{ marginBottom: 'var(--space-sm)' }}>
          Select 2 to 4 products to compare ({selectedIds.length} selected):
        </h4>
        <div
          style={{
            display: 'flex',
            gap: 'var(--space-sm)',
            flexWrap: 'wrap',
            maxHeight: '160px',
            overflowY: 'auto',
            padding: '4px',
          }}
        >
          {availableProducts.map((p) => {
            const isSelected = selectedIds.includes(p.id);
            return (
              <button
                key={p.id}
                type="button"
                className={`btn btn-sm ${isSelected ? 'btn-primary' : 'btn-secondary'}`}
                onClick={() => toggleSelect(p.id)}
                style={{ fontSize: '0.8rem' }}
              >
                {isSelected ? '✓ ' : '+ '} {p.name} (₹{p.price.toLocaleString('en-IN')})
              </button>
            );
          })}
        </div>
      </div>

      {/* Comparison View */}
      {loading ? (
        <div className="empty-state">
          <div className="loading-spinner"></div>
          <p style={{ marginTop: '12px' }}>Generating comparison...</p>
        </div>
      ) : comparison?.products?.length >= 2 ? (
        <div style={{ overflowX: 'auto' }}>
          <table
            style={{
              width: '100%',
              borderCollapse: 'collapse',
              background: 'var(--bg-card)',
              borderRadius: 'var(--radius-lg)',
              overflow: 'hidden',
              border: '1px solid var(--border-color)',
            }}
          >
            <thead>
              <tr style={{ background: 'var(--bg-tertiary)', borderBottom: '1px solid var(--border-color)' }}>
                <th style={{ padding: 'var(--space-md)', textAlign: 'left', minWidth: '160px' }}>
                  Feature
                </th>
                {comparison.products.map((p) => (
                  <th
                    key={p.id}
                    style={{
                      padding: 'var(--space-md)',
                      textAlign: 'center',
                      minWidth: '220px',
                    }}
                  >
                    <Link
                      to={`/products/${p.id}`}
                      style={{ fontSize: '1.05rem', fontWeight: '700', color: 'var(--text-primary)' }}
                    >
                      {p.name}
                    </Link>
                    <div style={{ fontSize: '0.8rem', color: 'var(--accent-primary)', marginTop: '2px' }}>
                      {p.brand}
                    </div>
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {/* Price */}
              <tr style={{ borderBottom: '1px solid var(--border-color)' }}>
                <td style={{ padding: 'var(--space-md)', fontWeight: '600', color: 'var(--text-secondary)' }}>
                  Price
                </td>
                {comparison.products.map((p) => (
                  <td key={p.id} style={{ padding: 'var(--space-md)', textAlign: 'center', fontWeight: '700', fontSize: '1.2rem' }}>
                    ₹{p.price.toLocaleString('en-IN')}
                  </td>
                ))}
              </tr>

              {/* Rating */}
              <tr style={{ borderBottom: '1px solid var(--border-color)' }}>
                <td style={{ padding: 'var(--space-md)', fontWeight: '600', color: 'var(--text-secondary)' }}>
                  Customer Rating
                </td>
                {comparison.products.map((p) => (
                  <td key={p.id} style={{ padding: 'var(--space-md)', textAlign: 'center', color: 'var(--warning)' }}>
                    ⭐ {p.rating?.toFixed(1)} / 5.0
                  </td>
                ))}
              </tr>

              {/* Stock */}
              <tr style={{ borderBottom: '1px solid var(--border-color)' }}>
                <td style={{ padding: 'var(--space-md)', fontWeight: '600', color: 'var(--text-secondary)' }}>
                  Availability
                </td>
                {comparison.products.map((p) => (
                  <td key={p.id} style={{ padding: 'var(--space-md)', textAlign: 'center' }}>
                    <span className={`product-stock ${p.stock > 0 ? 'in-stock' : 'out-of-stock'}`}>
                      {p.stock > 0 ? `${p.stock} in stock` : 'Out of Stock'}
                    </span>
                  </td>
                ))}
              </tr>

              {/* Warranty */}
              <tr style={{ borderBottom: '1px solid var(--border-color)' }}>
                <td style={{ padding: 'var(--space-md)', fontWeight: '600', color: 'var(--text-secondary)' }}>
                  Warranty
                </td>
                {comparison.products.map((p) => (
                  <td key={p.id} style={{ padding: 'var(--space-md)', textAlign: 'center' }}>
                    {p.warranty || 'Standard'}
                  </td>
                ))}
              </tr>

              {/* Specs Rows */}
              {comparison.comparison_fields?.map((field) => (
                <tr key={field} style={{ borderBottom: '1px solid var(--border-color)' }}>
                  <td
                    style={{
                      padding: 'var(--space-md)',
                      fontWeight: '600',
                      color: 'var(--text-secondary)',
                      textTransform: 'capitalize',
                    }}
                  >
                    {field.replace(/_/g, ' ')}
                  </td>
                  {comparison.products.map((p) => (
                    <td key={p.id} style={{ padding: 'var(--space-md)', textAlign: 'center' }}>
                      {p.specifications?.[field] ?? '—'}
                    </td>
                  ))}
                </tr>
              ))}

              {/* Action row */}
              <tr>
                <td style={{ padding: 'var(--space-md)' }}></td>
                {comparison.products.map((p) => (
                  <td key={p.id} style={{ padding: 'var(--space-md)', textAlign: 'center' }}>
                    <button
                      className="btn btn-primary btn-sm"
                      style={{ width: '100%' }}
                      disabled={p.stock <= 0}
                      onClick={() => handleAddToCart(p.id)}
                    >
                      {p.stock > 0 ? 'Add to Cart' : 'Out of Stock'}
                    </button>
                  </td>
                ))}
              </tr>
            </tbody>
          </table>
        </div>
      ) : (
        <div className="empty-state card">
          <div className="icon">⚖️</div>
          <h3>Select products above to begin comparison</h3>
          <p>Pick at least 2 items to inspect specifications and value side by side.</p>
        </div>
      )}
    </div>
  );
}
