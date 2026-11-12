import { createFileRoute, Navigate } from '@tanstack/react-router';
import React, { useState } from 'react';
import { toast } from 'sonner';
import { useNavigate, Link } from '@/shoppy/navigation';
import { signInAdmin, startPreviewSession } from '@/shoppy/admin/session';
import { useAdminSession } from '@/shoppy/admin/components';
import { API_BASE } from '@/shoppy/services/api';
import { adminHead } from '@/shoppy/admin/head';

export const Route = createFileRoute('/admin/login')({ head: adminHead('Sign in', 'Sign in to the AgentCart admin dashboard.'), component: AdminLogin });

function AdminLogin() {
  const session = useAdminSession();
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [busy, setBusy] = useState(false);
  if (session) return <Navigate to="/admin" replace />;

  const submit = async e => {
    e.preventDefault(); setError('');
    if (!/^\S+@\S+\.\S+$/.test(email)) return setError('Enter a valid email address.');
    if (password.length < 6) return setError('Password must be at least 6 characters.');
    setBusy(true);
    try { await signInAdmin(email, password); toast.success('Signed in'); navigate('/admin'); }
    catch (err) { setError(err.message); }
    finally { setBusy(false); }
  };
  const preview = () => { startPreviewSession(); toast.info('Preview mode — all admin data is simulated.'); navigate('/admin'); };

  return (
    <div className="login-wrap">
      <div className="card login-card">
        <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 16 }}><div className="logo-icon" style={{ width: 40, height: 40, borderRadius: 10, display: 'grid', placeItems: 'center', background: 'var(--accent-gradient)' }}>🛠️</div><div><h2 style={{ fontSize: '1.2rem' }}>AgentCart Admin</h2><p style={{ color: 'var(--text-muted)', fontSize: '.85rem' }}>Staff sign-in</p></div></div>
        {!API_BASE && <div className="sim-banner" role="status">Real sign-in is unavailable until the store service is connected. <button type="button" className="btn btn-primary btn-sm" onClick={() => window.dispatchEvent(new Event('shoppy-open-connection'))}>Connect store</button></div>}
        <form onSubmit={submit} noValidate>
          <div className="field"><label htmlFor="a-email">Email</label><input id="a-email" type="email" autoComplete="username" value={email} onChange={e => setEmail(e.target.value)} /></div>
          <div className="field"><label htmlFor="a-pass">Password</label><input id="a-pass" type="password" autoComplete="current-password" value={password} onChange={e => setPassword(e.target.value)} /></div>
          {error && <p role="alert" style={{ color: 'var(--error)', fontSize: '.85rem', marginBottom: 12 }}>{error}</p>}
          <button className="btn btn-primary" style={{ width: '100%' }} disabled={busy}>{busy ? 'Signing in…' : 'Sign in'}</button>
        </form>
        <div style={{ borderTop: '1px solid var(--border-color)', margin: '20px 0 14px' }} />
        <button className="btn btn-secondary" style={{ width: '100%' }} onClick={preview}>Explore in preview mode</button>
        <p style={{ fontSize: '.78rem', color: 'var(--text-muted)', marginTop: 8, textAlign: 'center' }}>Preview mode uses sample data. Nothing you change is saved.</p>
        <p style={{ textAlign: 'center', marginTop: 12, fontSize: '.85rem' }}><Link to="/">← Back to store</Link></p>
      </div>
    </div>
  );
}
