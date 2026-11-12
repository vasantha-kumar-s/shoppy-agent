import { createFileRoute } from '@tanstack/react-router';
import React, { useEffect, useMemo, useState } from 'react';
import { toast } from 'sonner';
import { adminApi, isLiveAdmin } from '@/shoppy/admin/admin-api';
import { PageTitle, Pager, productImage, Stat } from '@/shoppy/admin/components';
import { LoadingState, EmptyState } from '@/shoppy/components/States';
import { adminHead } from '@/shoppy/admin/head';

export const Route = createFileRoute('/admin/inventory')({ head: adminHead('Inventory'), component: Inventory });
const PER = 12;

function Inventory() {
  const [items, setItems] = useState(null);
  const [draft, setDraft] = useState({});
  const [filter, setFilter] = useState('all'); const [q, setQ] = useState(''); const [page, setPage] = useState(1);
  useEffect(() => { adminApi.listProducts().then(setItems); }, []);
  useEffect(() => setPage(1), [filter, q]);
  const list = useMemo(() => (items || []).filter(p => (filter === 'all' || (filter === 'out' ? p.stock === 0 : p.stock > 0 && p.stock < 5)) && p.name.toLowerCase().includes(q.toLowerCase())).sort((a, b) => a.stock - b.stock), [items, filter, q]);
  if (!items) return <LoadingState label="Loading inventory…" />;
  const save = async p => {
    const v = Number(draft[p.id]);
    if (!Number.isInteger(v) || v < 0) return toast.error('Stock must be a whole number, 0 or more.');
    await adminApi.adjustStock(p.id, v);
    setItems(x => x.map(i => i.id === p.id ? { ...i, stock: v } : i)); setDraft(d => { const n = { ...d }; delete n[p.id]; return n; });
    toast.success(isLiveAdmin() ? 'Saved to the store' : `Stock for ${p.name} set to ${v} (simulated)`);
  };
  const pages = Math.ceil(list.length / PER), rows = list.slice((page - 1) * PER, page * PER);
  return (
    <div>
      <PageTitle title="Inventory" sub="Track and adjust stock levels" />
      <div className="stat-grid"><Stat label="Total units" value={items.reduce((a, p) => a + p.stock, 0)} /><Stat label="Low stock (<5)" value={items.filter(p => p.stock > 0 && p.stock < 5).length} /><Stat label="Out of stock" value={items.filter(p => p.stock === 0).length} /></div>
      <div className="toolbar"><input className="search-input" type="search" aria-label="Search inventory" placeholder="Search products…" value={q} onChange={e => setQ(e.target.value)} />
        <select aria-label="Stock filter" value={filter} onChange={e => setFilter(e.target.value)}><option value="all">All items</option><option value="low">Low stock</option><option value="out">Out of stock</option></select></div>
      {list.length === 0 ? <EmptyState icon="✅" title="Nothing here">No items match this filter.</EmptyState> : <>
        <div className="table-wrap"><table className="data-table"><thead><tr><th>Product</th><th>SKU</th><th>Current</th><th>Set stock</th></tr></thead><tbody>
          {rows.map(p => <tr key={p.id}><td><div style={{ display: 'flex', gap: 10, alignItems: 'center' }}><img className="thumb" src={productImage(p)} alt="" loading="lazy" />{p.name}</div></td><td>{p.sku}</td>
            <td className={p.stock === 0 ? 'stock-out' : p.stock < 5 ? 'stock-low' : ''}>{p.stock === 0 ? 'Out' : p.stock}</td>
            <td><div style={{ display: 'flex', gap: 6 }}>
              <button className="btn btn-secondary btn-sm" aria-label="Decrease" onClick={() => setDraft(d => ({ ...d, [p.id]: Math.max(0, Number(d[p.id] ?? p.stock) - 1) }))}>−</button>
              <input type="number" min="0" aria-label={`Stock for ${p.name}`} style={{ width: 70, padding: '4px 8px', border: '1px solid var(--border-color)', borderRadius: 6 }} value={draft[p.id] ?? p.stock} onChange={e => setDraft(d => ({ ...d, [p.id]: e.target.value }))} />
              <button className="btn btn-secondary btn-sm" aria-label="Increase" onClick={() => setDraft(d => ({ ...d, [p.id]: Number(d[p.id] ?? p.stock) + 1 }))}>+</button>
              <button className="btn btn-primary btn-sm" disabled={draft[p.id] === undefined || Number(draft[p.id]) === p.stock} onClick={() => save(p)}>Save</button>
            </div></td></tr>)}
        </tbody></table></div>
        <Pager page={page} pages={pages} total={list.length} onPage={setPage} /></>}
    </div>
  );
}
