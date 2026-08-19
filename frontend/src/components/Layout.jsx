import React from 'react';
import { NavLink, Outlet } from 'react-router-dom';
import HealthIndicator from './HealthIndicator';

export default function Layout({ cartCount = 0 }) {
  return (
    <div className="app-layout">
      <aside className="sidebar">
        <div className="sidebar-logo">
          <div className="logo-icon">🛒</div>
          <div>
            <h1>AgentCart</h1>
            <p style={{ fontSize: '0.68rem', color: 'rgba(255,255,255,0.35)', fontWeight: 500 }}>
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
        </nav>

        <div
          style={{
            padding: '16px 20px',
            borderTop: '1px solid rgba(255,255,255,0.06)',
            display: 'flex',
            flexDirection: 'column',
            gap: '8px',
          }}
        >
          <div
            style={{
              fontSize: '0.68rem',
              color: 'rgba(255,255,255,0.3)',
              fontWeight: '600',
              textTransform: 'uppercase',
              letterSpacing: '0.08em',
            }}
          >
            Services
          </div>
          <HealthIndicator />
        </div>
      </aside>

      <main className="main-content">
        <Outlet />
      </main>
    </div>
  );
}
