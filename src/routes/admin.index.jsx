import { createFileRoute } from '@tanstack/react-router';
import React, { useEffect, useState } from 'react';
import { Link } from '@/shoppy/navigation';
import { mockOrders, mockSalesByMonth } from '@/shoppy/admin/mock-data';
import { adminApi, isLiveAdmin } from '@/shoppy/admin/admin-api';
import { PageTitle, StatusBadge, inr, Stat, MiniBars } from '@/shoppy/admin/components';
import { LoadingState } from '@/shoppy/components/States';
import { adminHead } from '@/shoppy/admin/head';

export const Route = createFileRoute('/admin/')({ head: adminHead('Overview'), component: Overview });

function Overview() {
  const [products, setProducts] = useState(null);
  const [orders, setOrders] = useState(mockOrders);

  useEffect(() => {
    adminApi.listProducts().then(setProducts).catch(() => setProducts([]));
    adminApi.listOrders().then(data => {
      if (data && data.length > 0) setOrders(data);
    }).catch(() => {});
  }, []);

  if (!products) return <LoadingState label="Loading overview…" />;
  const revenue = orders.filter(o => o.status !== 'cancelled').reduce((a, o) => a + o.total, 0);
  const low = products.filter(p => p.stock > 0 && p.stock < 5).length, out = products.filter(p => p.stock === 0).length;

  return (
    <div>
      <PageTitle
        title="Overview"
        sub={isLiveAdmin() ? "Store dashboard connected to backend database" : "A snapshot of your store (sample figures)"}
        actions={<Link to="/admin/products/new" className="btn btn-primary">+ Add product</Link>}
      />
      <div className="stat-grid">
        <Stat label={isLiveAdmin() ? "Revenue" : "Revenue (sample)"} value={inr(revenue)} delta="+8% vs last month" />
        <Stat label="Orders" value={orders.length} />
        <Stat label="Products" value={products.length} />
        <Stat label="Low / out of stock" value={`${low} / ${out}`} />
      </div>
      <div className="form-grid">
        <div className="card"><h3 style={{ marginBottom: 12 }}>Recent orders</h3>
          <div className="table-wrap"><table className="data-table"><thead><tr><th>Order</th><th>Customer</th><th>Total</th><th>Status</th></tr></thead>
            <tbody>{orders.slice(0, 6).map(o => <tr key={o.id}><td>{o.order_number}</td><td>{o.customer}</td><td>{inr(o.total)}</td><td><StatusBadge status={o.status} /></td></tr>)}</tbody></table></div>
          <Link to="/admin/orders" className="btn btn-secondary btn-sm" style={{ marginTop: 12 }}>View all orders</Link>
        </div>
        <div className="card"><h3>Sales trend</h3><MiniBars data={mockSalesByMonth} /></div>
      </div>
    </div>
  );
}
