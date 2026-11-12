import { createFileRoute } from '@tanstack/react-router';
import React, { useMemo, useState, useEffect } from 'react';
import { toast } from 'sonner';
import { mockCustomers } from '@/shoppy/admin/mock-data';
import { adminApi, isLiveAdmin } from '@/shoppy/admin/admin-api';
import { PageTitle, Pager, ActionMenu, inr } from '@/shoppy/admin/components';
import { EmptyState } from '@/shoppy/components/States';
import { adminHead } from '@/shoppy/admin/head';

export const Route = createFileRoute('/admin/customers')({ head: adminHead('Customers'), component: Customers });
const PER = 8;

function Customers() {
  const [customers, setCustomers] = useState(mockCustomers);
  const [q, setQ] = useState(''); const [sort, setSort] = useState('spent'); const [page, setPage] = useState(1);

  useEffect(() => {
    adminApi.listCustomers().then(data => {
      if (data && data.length > 0) setCustomers(data);
    }).catch(() => {});
  }, []);

  const list = useMemo(() => customers.filter(c => (c.name + c.email + (c.city || '')).toLowerCase().includes(q.toLowerCase())).sort((a, b) => sort === 'name' ? a.name.localeCompare(b.name) : b[sort] - a[sort]), [customers, q, sort]);
  const pages = Math.ceil(list.length / PER), rows = list.slice((page - 1) * PER, page * PER);
  const copy = async c => { try { await navigator.clipboard.writeText(c.email); toast.success('Email copied'); } catch { toast.error('Could not copy email'); } };

  return (
    <div>
      <PageTitle title="Customers" sub={isLiveAdmin() ? "Registered customers and spend metrics" : "Sample customer accounts"} />
      <div className="toolbar"><input className="search-input" type="search" aria-label="Search customers" placeholder="Search name, email or city…" value={q} onChange={e => { setQ(e.target.value); setPage(1); }} />
        <select aria-label="Sort" value={sort} onChange={e => setSort(e.target.value)}><option value="spent">Top spend</option><option value="orders">Most orders</option><option value="name">Name</option></select></div>
      {list.length === 0 ? <EmptyState icon="👥" title="No customers match" /> : <>
        <div className="table-wrap"><table className="data-table"><thead><tr><th>Customer</th><th>City</th><th>Orders</th><th>Total spent</th><th>Joined</th><th aria-label="Actions" /></tr></thead><tbody>
          {rows.map(c => <tr key={c.id}><td><strong>{c.name}</strong><div style={{ fontSize: '.78rem', color: 'var(--text-muted)' }}>{c.email}</div></td><td>{c.city}</td><td>{c.orders}</td><td>{inr(c.spent)}</td><td>{c.joined}</td>
            <td><ActionMenu label={`Actions for ${c.name}`} items={[{ label: 'Copy email', onClick: () => copy(c) }, { label: 'Send message', onClick: () => toast.info('Customer messaging is queued.') }]} /></td></tr>)}
        </tbody></table></div>
        <Pager page={page} pages={pages} total={list.length} onPage={setPage} /></>}
    </div>
  );
}
