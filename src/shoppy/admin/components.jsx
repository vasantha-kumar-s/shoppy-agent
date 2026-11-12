import React, { useEffect, useRef, useState } from 'react';
import { Link, NavLink, useNavigate } from '../navigation';
import { getAdminSession, signOutAdmin } from './session';
import { MOCK_NOTICE } from './mock-data';
import { confirmAction } from '../components/ConfirmDialog';
import laptops from '../assets/laptops.jpg.asset.json';
import smartphones from '../assets/smartphones.jpg.asset.json';
import headphones from '../assets/headphones.jpg.asset.json';
import monitors from '../assets/monitors.jpg.asset.json';
import keyboards from '../assets/keyboards.jpg.asset.json';
import mice from '../assets/mice.jpg.asset.json';
import smartwatches from '../assets/smartwatches.jpg.asset.json';

export const CATEGORY_IMAGES = { laptops: laptops.url, smartphones: smartphones.url, headphones: headphones.url, monitors: monitors.url, keyboards: keyboards.url, mice: mice.url, smartwatches: smartwatches.url };
export const productImage = p => p.image_url || CATEGORY_IMAGES[p.category] || '';
export const inr = n => '₹' + Number(n || 0).toLocaleString('en-IN');

const NAV = [
  ['/admin', '📊', 'Overview', ['admin', 'staff'], true],
  ['/admin/products', '📦', 'Products', ['admin', 'staff']],
  ['/admin/categories', '🏷️', 'Categories', ['admin']],
  ['/admin/inventory', '📋', 'Inventory', ['admin', 'staff']],
  ['/admin/orders', '🧾', 'Orders', ['admin', 'staff']],
  ['/admin/customers', '👥', 'Customers', ['admin']],
  ['/admin/analytics', '📈', 'Analytics', ['admin']],
];

export function useAdminSession() {
  const [s, setS] = useState(() => getAdminSession());
  useEffect(() => { const on = () => setS(getAdminSession()); window.addEventListener('agentcart-admin', on); return () => window.removeEventListener('agentcart-admin', on); }, []);
  return s;
}

export function AdminShell({ session, children }) {
  const [open, setOpen] = useState(false);
  const navigate = useNavigate();
  useEffect(() => { if (!open) return; const k = e => e.key === 'Escape' && setOpen(false); window.addEventListener('keydown', k); return () => window.removeEventListener('keydown', k); }, [open]);
  const logout = async () => {
    if (!(await confirmAction({ title: 'Sign out of admin?', confirmLabel: 'Sign out' }))) return;
    signOutAdmin(); navigate('/admin/login');
  };
  return (
    <div className="app-layout">
      <button className="mobile-menu btn btn-secondary" aria-label="Toggle admin navigation" aria-expanded={open} onClick={() => setOpen(!open)}>{open ? '✕' : '☰'}</button>
      {open && <div className="nav-backdrop" onClick={() => setOpen(false)} />}
      <aside className={`sidebar ${open ? 'open' : ''}`} onClick={e => { if (e.target.closest('a')) setOpen(false); }}>
        <div className="sidebar-logo"><div className="logo-icon">🛠️</div><div><h1>AgentCart</h1><p style={{ fontSize: '0.68rem', color: 'var(--text-muted)', fontWeight: 500 }}>Admin · {session.role}</p></div></div>
        <nav className="sidebar-nav">
          {NAV.filter(n => n[3].includes(session.role)).map(([to, icon, label, , end]) => (
            <NavLink key={to} to={to} end={end} className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}><span className="nav-icon">{icon}</span> {label}</NavLink>
          ))}
        </nav>
        <div style={{ padding: '16px 20px', borderTop: '1px solid var(--border-color)', display: 'flex', flexDirection: 'column', gap: 8 }}>
          <Link to="/" className="nav-link" style={{ padding: '8px 0' }}><span className="nav-icon">🏠</span> View storefront</Link>
          <button className="btn btn-secondary btn-sm" onClick={logout}>Sign out</button>
        </div>
      </aside>
      <main className="main-content">
        {session.mode === 'preview' && <div className="sim-banner" role="status"><span aria-hidden>🧪</span><span><strong>Preview mode.</strong> {MOCK_NOTICE}</span></div>}
        {session.mode === 'live' && /\/admin\/(orders|customers|analytics|categories)|^\/admin\/?$/.test(window.location.pathname) && <div className="sim-banner" role="status"><span aria-hidden>🧪</span><span>Products and stock use your store. Orders, customers, categories and charts here are still sample data until your service adds admin endpoints for them.</span></div>}
        {children}
      </main>
    </div>
  );
}

export function PageTitle({ title, sub, actions }) {
  return <div className="admin-topbar"><div className="page-header" style={{ marginBottom: 0, minWidth: 0 }}><h2>{title}</h2>{sub && <p>{sub}</p>}</div>{actions && <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>{actions}</div>}</div>;
}

export function ActionMenu({ items, label = 'Actions' }) {
  const [open, setOpen] = useState(false);
  const ref = useRef(null);
  useEffect(() => { if (!open) return; const c = e => { if (!ref.current?.contains(e.target)) setOpen(false); }; const k = e => e.key === 'Escape' && setOpen(false); document.addEventListener('mousedown', c); window.addEventListener('keydown', k); return () => { document.removeEventListener('mousedown', c); window.removeEventListener('keydown', k); }; }, [open]);
  return (
    <div className="menu" ref={ref}>
      <button className="btn btn-secondary btn-sm" aria-haspopup="menu" aria-expanded={open} aria-label={label} onClick={() => setOpen(!open)}>⋯</button>
      {open && <div className="menu-list" role="menu">{items.map(it => <button key={it.label} role="menuitem" className={it.danger ? 'danger' : ''} onClick={() => { setOpen(false); it.onClick(); }}>{it.label}</button>)}</div>}
    </div>
  );
}

export function Pager({ page, pages, total, onPage }) {
  return <div className="pager"><span>{total} result{total === 1 ? '' : 's'} · page {page} of {Math.max(pages, 1)}</span><div style={{ display: 'flex', gap: 6 }}><button className="btn btn-secondary btn-sm" disabled={page <= 1} onClick={() => onPage(page - 1)}>← Prev</button><button className="btn btn-secondary btn-sm" disabled={page >= pages} onClick={() => onPage(page + 1)}>Next →</button></div></div>;
}

export function StatusBadge({ status }) {
  const map = { active: 'badge-delivered', draft: 'badge-processing', confirmed: 'badge-confirmed', processing: 'badge-processing', shipped: 'badge-shipped', delivered: 'badge-delivered', cancelled: 'badge-cancelled' };
  return <span className={`badge ${map[status] || 'badge-cancelled'}`}>{status}</span>;
}

export function Stat({ label, value, delta }) { return <div className="card stat-card"><div className="label">{label}</div><div className="value">{value}</div>{delta && <div className="delta">{delta}</div>}</div>; }
export function MiniBars({ data }) {
  const max = Math.max(...data.map(d => d[1]));
  return <div className="bar-chart" role="img" aria-label="Monthly sales bar chart">{data.map(([m, v]) => <div className="bar" key={m} title={inr(v)}><span className="fill" style={{ height: `${(v / max) * 85}%` }} />{m}</div>)}</div>;
}
