import { createFileRoute } from '@tanstack/react-router';
import React, { useMemo, useState, useEffect } from 'react';
import { toast } from 'sonner';
import { mockOrders } from '@/shoppy/admin/mock-data';
import { adminApi, isLiveAdmin } from '@/shoppy/admin/admin-api';
import { PageTitle, Pager, StatusBadge, ActionMenu, inr } from '@/shoppy/admin/components';
import { EmptyState } from '@/shoppy/components/States';
import { confirmAction } from '@/shoppy/components/ConfirmDialog';
import { adminHead } from '@/shoppy/admin/head';

export const Route = createFileRoute('/admin/orders')({ head: adminHead('Orders'), component: Orders });
const PER = 10; const FLOW = ['confirmed', 'processing', 'shipped', 'delivered'];

function Orders() {
  const [orders, setOrders] = useState(mockOrders);
  const [q, setQ] = useState(''); const [status, setStatus] = useState(''); const [page, setPage] = useState(1); const [open, setOpen] = useState(null);

  useEffect(() => {
    adminApi.listOrders().then(data => {
      if (data && data.length > 0) setOrders(data);
    }).catch(() => {});
  }, []);

  const list = useMemo(() => orders.filter(o => (!status || o.status === status) && (o.order_number + o.customer).toLowerCase().includes(q.toLowerCase())), [orders, q, status]);

  const setSt = async (o, s) => {
    try {
      if (isLiveAdmin()) await adminApi.updateOrderStatus(o.id, s);
      setOrders(x => x.map(i => i.id === o.id ? { ...i, status: s } : i));
      toast.success(isLiveAdmin() ? `${o.order_number} marked ${s} (saved to store)` : `${o.order_number} marked ${s} (simulated)`);
    } catch (e) {
      toast.error(e.message || 'Failed to update order status');
    }
  };

  const cancel = async o => {
    if (await confirmAction({
      title: `Cancel ${o.order_number}?`,
      description: isLiveAdmin() ? 'This will update the order status to cancelled in the store database.' : 'Simulated only. No refund or notification is sent.',
      confirmLabel: 'Cancel order',
      cancelLabel: 'Keep',
      danger: true
    })) {
      await setSt(o, 'cancelled');
    }
  };

  const pages = Math.ceil(list.length / PER), rows = list.slice((page - 1) * PER, page * PER);

  return (
    <div>
      <PageTitle title="Orders" sub={isLiveAdmin() ? "Live customer orders from store database" : "Sample orders for previewing the workflow"} />
      <div className="toolbar"><input className="search-input" type="search" aria-label="Search orders" placeholder="Search order number or customer…" value={q} onChange={e => { setQ(e.target.value); setPage(1); }} />
        <select aria-label="Status" value={status} onChange={e => { setStatus(e.target.value); setPage(1); }}><option value="">All statuses</option>{[...FLOW, 'cancelled'].map(s => <option key={s} value={s}>{s}</option>)}</select></div>
      {list.length === 0 ? <EmptyState icon="🧾" title="No orders match">Try another search.</EmptyState> : <>
        <div className="table-wrap"><table className="data-table"><thead><tr><th>Order</th><th>Date</th><th>Customer</th><th>Items</th><th>Total</th><th>Status</th><th aria-label="Actions" /></tr></thead><tbody>
          {rows.map(o => { const next = FLOW[FLOW.indexOf(o.status) + 1]; return <React.Fragment key={o.id}><tr>
            <td><button className="btn btn-secondary btn-sm" aria-expanded={open === o.id} onClick={() => setOpen(open === o.id ? null : o.id)}>{o.order_number}</button></td><td>{o.date}</td><td>{o.customer}</td><td>{o.items}</td><td>{inr(o.total)}</td><td><StatusBadge status={o.status} /></td>
            <td><ActionMenu label={`Actions for ${o.order_number}`} items={[...(next ? [{ label: `Mark ${next}`, onClick: () => setSt(o, next) }] : []), { label: open === o.id ? 'Hide details' : 'View details', onClick: () => setOpen(open === o.id ? null : o.id) }, ...(o.status !== 'cancelled' && o.status !== 'delivered' ? [{ label: 'Cancel order', danger: true, onClick: () => cancel(o) }] : [])]} /></td></tr>
            {open === o.id && <tr><td colSpan={7} style={{ background: 'var(--bg-tertiary)' }}><strong>Timeline:</strong> {FLOW.map(s => <span key={s} style={{ marginRight: 12, opacity: FLOW.indexOf(s) <= FLOW.indexOf(o.status) ? 1 : 0.4 }}>{FLOW.indexOf(s) <= FLOW.indexOf(o.status) ? '●' : '○'} {s}</span>)}{o.status === 'cancelled' && <span style={{ color: 'var(--error)' }}>● cancelled</span>}</td></tr>}
          </React.Fragment>; })}
        </tbody></table></div>
        <Pager page={page} pages={pages} total={list.length} onPage={setPage} /></>}
    </div>
  );
}
