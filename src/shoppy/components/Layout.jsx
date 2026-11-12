import React, {useState, useEffect} from 'react';
import {getCart, API_BASE, loadApiBase, getApiSetting} from '../services/api';
import ConnectionDialog from './ConnectionDialog';
import { LoadingState } from './States';
import {CartContext} from '../cart-context';
import { NavLink } from '../navigation';
import HealthIndicator from './HealthIndicator';
import { useRouterState } from '@tanstack/react-router';
import { getAdminSession } from '../admin/session';

export default function Layout({ children }) {
  const [cartCount, setCartCount] = useState(0);
  const [open, setOpen] = useState(false);
  const [isAdmin, setIsAdmin] = useState(false);
  const [ready, setReady] = useState(false);
  const [connOpen, setConnOpen] = useState(false);
  useEffect(() => { loadApiBase(); setReady(true); const o = () => setConnOpen(true); window.addEventListener('shoppy-open-connection', o); return () => window.removeEventListener('shoppy-open-connection', o); }, []);
  const pathname = useRouterState({ select: s => s.location.pathname });
  useEffect(() => { const on = () => setIsAdmin(!!getAdminSession()); on(); window.addEventListener('agentcart-admin', on); return () => window.removeEventListener('agentcart-admin', on); }, []);
  useEffect(() => { setOpen(false); }, [pathname]);
  const refreshCart = async () => { try { const data = await getCart(); setCartCount(data?.total_items || 0); } catch {} };
  useEffect(() => { if (ready) refreshCart(); }, [ready]);
  useEffect(() => { if (!open) return; const close = e => {if(e.key === 'Escape') setOpen(false);}; window.addEventListener('keydown', close); return () => window.removeEventListener('keydown', close); }, [open]);
  const dialog = connOpen && <ConnectionDialog onClose={() => setConnOpen(false)} />;
  if (!ready) return <div style={{padding:48}}><LoadingState label="Loading store…" /></div>;
  if (pathname.startsWith('/admin')) return <CartContext.Provider value={{refreshCart}}>{children}{dialog}</CartContext.Provider>;
  return (
    <CartContext.Provider value={{refreshCart}}><div className="app-layout">
<button className="mobile-menu btn btn-secondary" aria-label="Toggle navigation" aria-expanded={open} onClick={() => setOpen(!open)}>{open ? '✕' : '☰'}</button>
      {open && <div className="nav-backdrop" onClick={() => setOpen(false)} />}
      <aside className={`sidebar ${open ? "open" : ""}`} onClick={e => {if(e.target.closest("a")) setOpen(false);}}>
        <div className="sidebar-logo">
          <div className="logo-icon">🛒</div>
          <div>
            <h1>AgentCart</h1>
            <p style={{ fontSize: '0.68rem', color: 'var(--text-muted)', fontWeight: 500 }}>
              Smart Shopping
            </p>
          </div>
        </div>

        <nav className="sidebar-nav">
          <NavLink
            to="/"
            className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}
            end
          >
            <span className="nav-icon">🏠</span> Home
          </NavLink>
          <NavLink
            to="/assistant"
            className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}
          >
            <span className="nav-icon">💬</span> Assistant
          </NavLink>
          <NavLink
            to="/products"
            className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}
          >
            <span className="nav-icon">📦</span> Products
          </NavLink>
          <NavLink
            to="/cart"
            className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}
          >
            <span className="nav-icon">🛒</span> Cart
            {cartCount > 0 && (
              <span
                style={{
                  marginLeft: 'auto',
                  background: 'var(--accent-gradient)',
                  color: '#fff',
                  borderRadius: '8px',
                  padding: '1px 7px',
                  fontSize: '0.7rem',
                  fontWeight: 'bold',
                }}
              >
                {cartCount}
              </span>
            )}
          </NavLink>
          <NavLink
            to="/orders"
            className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}
          >
            <span className="nav-icon">📋</span> Orders
          </NavLink>
          <NavLink
            to="/compare"
            className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}
          >
            <span className="nav-icon">⚖️</span> Compare
          </NavLink>
          <NavLink to={isAdmin ? '/admin' : '/admin/login'} className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
            <span className="nav-icon">🛠️</span> {isAdmin ? 'Admin dashboard' : 'Staff sign-in'}
          </NavLink>
        </nav>

        <div
          style={{
            padding: '16px 20px',
            borderTop: '1px solid var(--border-color)',
            display: 'flex',
            flexDirection: 'column',
            gap: '8px',
          }}
        >
          <div
            style={{
              fontSize: '0.68rem',
              color: 'var(--text-muted)',
              fontWeight: '600',
              textTransform: 'uppercase',
              letterSpacing: '0.08em',
            }}
          >
            Services
          </div>
          <HealthIndicator />
          <button className="btn btn-secondary btn-sm" onClick={() => setConnOpen(true)}>{API_BASE ? '🔌 Connected · change' : '🔌 Connect store'}</button>
        </div>
      </aside>

      <main className="main-content">
        {!API_BASE && (<div role="status" className="card" style={{marginBottom:"var(--space-lg)",borderLeft:"4px solid var(--warning, #f59e0b)",display:"flex",gap:"12px",alignItems:"flex-start"}}><span aria-hidden="true">⚠️</span><div><strong>Shopping services are offline</strong><p style={{margin:"4px 0 0",color:"var(--text-muted)",fontSize:"0.9rem"}}>Products, cart, orders, and the assistant will show data once the store service is connected.</p><button className="btn btn-primary btn-sm" style={{marginTop:10}} onClick={() => setConnOpen(true)}>Connect your service</button></div></div>)}
        {children}
      </main>
      {dialog}
    </div></CartContext.Provider>
  );
}
