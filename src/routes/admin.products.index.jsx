import { createFileRoute } from '@tanstack/react-router';
import React, { useEffect, useMemo, useState } from 'react';
import { toast } from 'sonner';
import { Link, useNavigate } from '@/shoppy/navigation';
import { mockCategories } from '@/shoppy/admin/mock-data';
import { adminApi, isLiveAdmin } from '@/shoppy/admin/admin-api';
import { PageTitle, ActionMenu, Pager, StatusBadge, inr, productImage } from '@/shoppy/admin/components';
import { LoadingState, ErrorState, EmptyState } from '@/shoppy/components/States';
import { confirmAction } from '@/shoppy/components/ConfirmDialog';
import { adminHead } from '@/shoppy/admin/head';

export const Route = createFileRoute('/admin/products/')({ head: adminHead('Products'), component: ProductsAdmin });
const PER = 10;

function ProductsAdmin() {
  const navigate = useNavigate();
  const [items, setItems] = useState(null);
  const [error, setError] = useState('');
  const [q, setQ] = useState(''); const [cat, setCat] = useState(''); const [status, setStatus] = useState(''); const [stock, setStock] = useState('');
  const [sort, setSort] = useState('name'); const [page, setPage] = useState(1); const [sel, setSel] = useState([]);
  const load = () => { setError(''); setItems(null); adminApi.listProducts().then(setItems).catch(e => setError(e.message)); };
  useEffect(load, []);
  useEffect(() => setPage(1), [q, cat, status, stock, sort]);

  const filtered = useMemo(() => {
    if (!items) return [];
    const t = q.trim().toLowerCase();
    return items.filter(p => (!t || [p.name, p.brand, p.sku].join(' ').toLowerCase().includes(t)) && (!cat || p.category === cat) && (!status || p.status === status)
      && (!stock || (stock === 'out' ? p.stock === 0 : stock === 'low' ? p.stock > 0 && p.stock < 5 : p.stock >= 5)))
      .sort((a, b) => sort === 'price' ? a.price - b.price : sort === '-price' ? b.price - a.price : sort === 'stock' ? a.stock - b.stock : a.name.localeCompare(b.name));
  }, [items, q, cat, status, stock, sort]);
  const pages = Math.ceil(filtered.length / PER); const rows = filtered.slice((page - 1) * PER, page * PER);
  const reset = () => { setQ(''); setCat(''); setStatus(''); setStock(''); };

  const remove = async ids => {
    if (!(await confirmAction({ title: ids.length > 1 ? `Delete ${ids.length} products?` : 'Delete this product?', description: 'This is simulated in preview mode — the store catalog is not changed.', confirmLabel: 'Delete', danger: true }))) return;
    await Promise.all(ids.map(id => adminApi.deleteProduct(id)));
    setItems(x => x.filter(p => !ids.includes(p.id))); setSel([]);
    toast.success(isLiveAdmin() ? 'Saved to the store' : `Removed from preview (simulated)`);
  };
  const toggleStatus = async p => {
    const next = p.status === 'active' ? 'draft' : 'active';
    await adminApi.updateProduct(p.id, { status: next });
    setItems(x => x.map(i => i.id === p.id ? { ...i, status: next } : i)); toast.success(isLiveAdmin() ? 'Saved to the store' : `Marked ${next} (simulated)`);
  };
  const duplicate = async p => { const c = await adminApi.createProduct({ ...p, name: p.name + ' (copy)', status: 'draft' }); setItems(x => [c, ...x]); toast.success(isLiveAdmin() ? 'Saved to the store' : 'Duplicated as draft (simulated)'); };

  return (
    <div>
      <PageTitle title="Products" sub="Manage catalog listings" actions={<Link to="/admin/products/new" className="btn btn-primary">+ Add product</Link>} />
      <div className="toolbar">
        <input className="search-input" type="search" aria-label="Search products" placeholder="Search name, brand or SKU…" value={q} onChange={e => setQ(e.target.value)} />
        <select aria-label="Category" value={cat} onChange={e => setCat(e.target.value)}><option value="">All categories</option>{mockCategories.map(c => <option key={c.slug} value={c.slug}>{c.name}</option>)}</select>
        <select aria-label="Status" value={status} onChange={e => setStatus(e.target.value)}><option value="">Any status</option><option value="active">Active</option><option value="draft">Draft</option></select>
        <select aria-label="Stock" value={stock} onChange={e => setStock(e.target.value)}><option value="">Any stock</option><option value="in">In stock</option><option value="low">Low (&lt;5)</option><option value="out">Out of stock</option></select>
        <select aria-label="Sort" value={sort} onChange={e => setSort(e.target.value)}><option value="name">Name A–Z</option><option value="price">Price ↑</option><option value="-price">Price ↓</option><option value="stock">Stock ↑</option></select>
      </div>
      {sel.length > 0 && <div className="sim-banner"><strong>{sel.length} selected</strong><button className="btn btn-danger btn-sm" onClick={() => remove(sel)}>Delete selected</button><button className="btn btn-secondary btn-sm" onClick={() => setSel([])}>Clear</button></div>}
      {error ? <ErrorState message={error} onRetry={load} /> : !items ? <LoadingState label="Loading products…" /> : filtered.length === 0 ? (
        <EmptyState icon="🔍" title="No products match" action={<button className="btn btn-secondary" onClick={reset}>Clear filters</button>}>Try a different search or filter.</EmptyState>
      ) : (
        <>
          <div className="table-wrap"><table className="data-table">
            <thead><tr><th><input type="checkbox" aria-label="Select page" checked={rows.every(r => sel.includes(r.id))} onChange={e => setSel(e.target.checked ? [...new Set([...sel, ...rows.map(r => r.id)])] : sel.filter(id => !rows.some(r => r.id === id)))} /></th><th>Product</th><th>Category</th><th>Price</th><th>Stock</th><th>Status</th><th aria-label="Actions" /></tr></thead>
            <tbody>{rows.map(p => (
              <tr key={p.id}>
                <td><input type="checkbox" aria-label={`Select ${p.name}`} checked={sel.includes(p.id)} onChange={e => setSel(e.target.checked ? [...sel, p.id] : sel.filter(i => i !== p.id))} /></td>
                <td><div style={{ display: 'flex', gap: 10, alignItems: 'center', minWidth: 0 }}><img className="thumb" src={productImage(p)} alt="" loading="lazy" /><div style={{ minWidth: 0 }}><Link to={`/admin/products/${p.id}`} style={{ fontWeight: 600, color: 'var(--text-primary)' }}>{p.name}</Link><div style={{ fontSize: '.78rem', color: 'var(--text-muted)' }}>{p.brand} · {p.sku}</div></div></div></td>
                <td style={{ textTransform: 'capitalize' }}>{p.category}</td><td>{inr(p.price)}</td>
                <td className={p.stock === 0 ? 'stock-out' : p.stock < 5 ? 'stock-low' : ''}>{p.stock}</td>
                <td><StatusBadge status={p.status} /></td>
                <td><ActionMenu label={`Actions for ${p.name}`} items={[{ label: 'Edit', onClick: () => navigate(`/admin/products/${p.id}`) }, { label: p.status === 'active' ? 'Unpublish' : 'Publish', onClick: () => toggleStatus(p) }, { label: 'Duplicate', onClick: () => duplicate(p) }, { label: 'Delete', danger: true, onClick: () => remove([p.id]) }]} /></td>
              </tr>))}</tbody>
          </table></div>
          <Pager page={page} pages={pages} total={filtered.length} onPage={setPage} />
        </>
      )}
    </div>
  );
}
