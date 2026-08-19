import React, { useEffect, useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import { getProducts, getCategories, addToCart } from '../services/api';
import ProductCard from '../components/ProductCard';

export default function ProductsPage({ onCartUpdate }) {
  const [searchParams, setSearchParams] = useSearchParams();
  const [products, setProducts] = useState([]);
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [addingId, setAddingId] = useState(null);

  // Filter state from query params
  const query = searchParams.get('query') || '';
  const category = searchParams.get('category') || '';
  const maxPrice = searchParams.get('max_price') || '';
  const minRating = searchParams.get('min_rating') || '';

  useEffect(() => {
    async function loadCategories() {
      try {
        const cats = await getCategories();
        setCategories(cats);
      } catch (err) {
        console.error('Failed to load categories:', err);
      }
    }
    loadCategories();
  }, []);

  useEffect(() => {
    async function fetchFilteredProducts() {
      setLoading(true);
      try {
        const data = await getProducts({
          query,
          category,
          max_price: maxPrice ? parseFloat(maxPrice) : null,
          min_rating: minRating ? parseFloat(minRating) : null,
          limit: 50,
        });
        setProducts(data);
      } catch (err) {
        console.error('Failed to fetch products:', err);
      } finally {
        setLoading(false);
      }
    }
    fetchFilteredProducts();
  }, [query, category, maxPrice, minRating]);

  const updateParam = (key, value) => {
    const nextParams = new URLSearchParams(searchParams);
    if (value) {
      nextParams.set(key, value);
    } else {
      nextParams.delete(key);
    }
    setSearchParams(nextParams);
  };

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

  return (
    <div>
      <div className="page-header">
        <h2>Browse Products</h2>
        <p>Find the perfect gear with real-time stock and dynamic filtering</p>
      </div>

      {/* Filter Bar */}
      <div
        className="card"
        style={{
          marginBottom: 'var(--space-xl)',
          display: 'flex',
          gap: 'var(--space-md)',
          flexWrap: 'wrap',
          alignItems: 'center',
        }}
      >
        {/* Search */}
        <div style={{ flex: '1 1 200px' }}>
          <input
            type="text"
            className="search-input"
            style={{ width: '100%' }}
            placeholder="🔍 Search laptops, brands, specs..."
            value={query}
            onChange={(e) => updateParam('query', e.target.value)}
          />
        </div>

        {/* Category */}
        <div>
          <select
            value={category}
            onChange={(e) => updateParam('category', e.target.value)}
          >
            <option value="">All Categories</option>
            {categories.map((cat) => (
              <option key={cat.id} value={cat.slug}>
                {cat.name}
              </option>
            ))}
          </select>
        </div>

        {/* Max Price */}
        <div>
          <select
            value={maxPrice}
            onChange={(e) => updateParam('max_price', e.target.value)}
          >
            <option value="">Any Price</option>
            <option value="5000">Under ₹5,000</option>
            <option value="15000">Under ₹15,000</option>
            <option value="35000">Under ₹35,000</option>
            <option value="50000">Under ₹50,000</option>
            <option value="80000">Under ₹80,000</option>
          </select>
        </div>

        {/* Min Rating */}
        <div>
          <select
            value={minRating}
            onChange={(e) => updateParam('min_rating', e.target.value)}
          >
            <option value="">Any Rating</option>
            <option value="4.0">⭐ 4.0 & above</option>
            <option value="4.5">⭐ 4.5 & above</option>
          </select>
        </div>

        {/* Reset button */}
        {(query || category || maxPrice || minRating) && (
          <button
            className="btn btn-secondary btn-sm"
            onClick={() => setSearchParams({})}
          >
            Reset Filters
          </button>
        )}
      </div>

      {/* Product List */}
      {loading ? (
        <div className="empty-state">
          <div className="loading-spinner"></div>
          <p style={{ marginTop: '12px' }}>Loading catalog...</p>
        </div>
      ) : products.length === 0 ? (
        <div className="empty-state card">
          <div className="icon">🔍</div>
          <h3>No products found</h3>
          <p>Try broadening your search terms or clearing your filters.</p>
          <button
            className="btn btn-primary"
            style={{ marginTop: '16px' }}
            onClick={() => setSearchParams({})}
          >
            Clear Filters
          </button>
        </div>
      ) : (
        <>
          <div
            style={{
              marginBottom: 'var(--space-md)',
              color: 'var(--text-muted)',
              fontSize: '0.9rem',
            }}
          >
            Showing {products.length} products
          </div>
          <div className="product-grid">
            {products.map((product) => (
              <ProductCard
                key={product.id}
                product={product}
                onAddToCart={handleAddToCart}
                adding={addingId === product.id}
              />
            ))}
          </div>
        </>
      )}
    </div>
  );
}
