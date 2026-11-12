import React from 'react';
import { API_BASE } from '../services/api';

export const isOffline = () => !API_BASE;

export function LoadingState({ label = 'Loading…' }) {
  return <div className="empty-state" role="status" aria-live="polite"><div className="loading-spinner" /><p style={{ marginTop: 12 }}>{label}</p></div>;
}
export function OfflineState({ what = 'this page' }) {
  return (
    <div className="empty-state card state-offline" role="status">
      <div className="icon">🔌</div>
      <h3>Store service not connected</h3>
      <p>We can't load {what} until the Shoppy store service is connected. Nothing is wrong with your device.</p>
    </div>
  );
}
export function ErrorState({ message, onRetry }) {
  return (
    <div className="empty-state card state-error" role="alert">
      <div className="icon">⚠️</div>
      <h3>Something went wrong</h3>
      <p>{message || 'The request failed. Please try again.'}</p>
      {onRetry && <button className="btn btn-primary" style={{ marginTop: 16 }} onClick={onRetry}>Try again</button>}
    </div>
  );
}
export function EmptyState({ icon = '📭', title, children, action }) {
  return <div className="empty-state card"><div className="icon">{icon}</div><h3>{title}</h3>{children && <p>{children}</p>}{action && <div style={{ marginTop: 16 }}>{action}</div>}</div>;
}
/** Picks offline / error / loading in one place. Returns null when content should render. */
export function StatusGate({ loading, error, what, onRetry, loadingLabel }) {
  if (isOffline()) return <OfflineState what={what} />;
  if (loading) return <LoadingState label={loadingLabel} />;
  if (error) return <ErrorState message={error} onRetry={onRetry} />;
  return null;
}
export function SimulatedBadge({ children = 'Simulated' }) {
  return <span className="sim-badge" title="This is preview data. Nothing is saved.">{children}</span>;
}
