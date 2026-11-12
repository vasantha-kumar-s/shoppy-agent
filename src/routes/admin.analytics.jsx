import { createFileRoute } from '@tanstack/react-router';
import React, { useEffect, useState } from 'react';
import { mockOrders, mockSalesByMonth, mockCategories } from '@/shoppy/admin/mock-data';
import { adminApi, isLiveAdmin } from '@/shoppy/admin/admin-api';
import { PageTitle, Stat, MiniBars, inr } from '@/shoppy/admin/components';
import { LoadingState } from '@/shoppy/components/States';
import { adminHead } from '@/shoppy/admin/head';

export const Route = createFileRoute('/admin/analytics')({ head: adminHead('Analytics'), component: Analytics });

function Analytics() {
  const [products, setProducts] = useState(null);
  const [analytics, setAnalytics] = useState(null);
  const [range, setRange] = useState(6);

  useEffect(() => {
    adminApi.listProducts().then(setProducts).catch(() => setProducts([]));
    adminApi.getAnalytics().then(setAnalytics).catch(() => {});
  }, []);

  if (!products) return <LoadingState label="Loading analytics…" />;

  const valid = mockOrders.filter(o => o.status !== 'cancelled');
  const revenueTotal = analytics?.revenue ?? valid.reduce((a, o) => a + o.total, 0);
  const avgOrderVal = analytics?.avg_order_value ?? Math.round(revenueTotal / (valid.length || 1));
  const cancelRate = analytics?.cancellation_rate ?? `${Math.round((1 - valid.length / mockOrders.length) * 100)}%`;
  const salesData = (analytics?.sales_by_month || mockSalesByMonth).slice(-range);

  const byCat = analytics?.sales_by_category && analytics.sales_by_category.length > 0
    ? analytics.sales_by_category
    : mockCategories.map(c => [
        c.name,
        products.filter(p => p.category === c.slug).reduce((a, p) => a + p.price * Math.max(1, 20 - p.stock), 0)
      ]).sort((a, b) => b[1] - a[1]);

  const maxCat = byCat.length > 0 ? Math.max(...byCat.map(x => x[1]), 1) : 1;

  return (
    <div>
      <PageTitle
        title="Analytics"
        sub={isLiveAdmin() ? "Real-time store metrics from database" : "Sample trends — real reporting arrives with the store service"}
        actions={<select aria-label="Range" value={range} onChange={e => setRange(Number(e.target.value))}><option value={3}>Last 3 months</option><option value={6}>Last 6 months</option></select>}
      />
      <div className="stat-grid">
        <Stat label="Revenue" value={inr(revenueTotal)} />
        <Stat label="Avg order value" value={inr(avgOrderVal)} />
        <Stat label="Cancellation rate" value={cancelRate} />
      </div>
      <div className="form-grid">
        <div className="card"><h3>Monthly revenue</h3><MiniBars data={salesData} /></div>
        <div className="card">
          <h3 style={{ marginBottom: 12 }}>Revenue by category</h3>
          {byCat.map(([n, v]) => (
            <div key={n} style={{ marginBottom: 10 }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '.85rem' }}>
                <span>{n}</span>
                <span>{inr(v)}</span>
              </div>
              <div style={{ height: 6, background: 'var(--bg-tertiary)', borderRadius: 4 }}>
                <div style={{ width: `${Math.min(100, Math.max(5, (v / maxCat) * 100))}%`, height: '100%', background: 'var(--accent-gradient)', borderRadius: 4 }} />
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
