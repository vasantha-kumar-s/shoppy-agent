import { createFileRoute } from '@tanstack/react-router';
import React, { useEffect, useState } from 'react';
import { toast } from 'sonner';
import { mockCategories } from '@/shoppy/admin/mock-data';
import { adminApi, isLiveAdmin } from '@/shoppy/admin/admin-api';
import { getCategories } from '@/shoppy/services/api';
import { PageTitle, ActionMenu, CATEGORY_IMAGES } from '@/shoppy/admin/components';
import { EmptyState } from '@/shoppy/components/States';
import { confirmAction } from '@/shoppy/components/ConfirmDialog';
import { adminHead } from '@/shoppy/admin/head';

export const Route = createFileRoute('/admin/categories')({ head: adminHead('Categories'), component: Categories });
const slugify = s => s.toLowerCase().trim().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');

function Categories() {
  const [cats, setCats] = useState(mockCategories);
  const [counts, setCounts] = useState({});
  const [form, setForm] = useState({ id: null, name: '', description: '' });
  const [err, setErr] = useState('');

  useEffect(() => {
    getCategories().then(cs => {
      if (cs && cs.length > 0) setCats(cs);
    }).catch(() => {});

    adminApi.listProducts().then(ps => {
      setCounts(ps.reduce((a, p) => ({ ...a, [p.category]: (a[p.category] || 0) + 1 }), {}));
    }).catch(() => {});
  }, []);

  const save = e => {
    e.preventDefault();
    const name = form.name.trim(); if (!name) return setErr('Name is required');
    const slug = slugify(name);
    if (cats.some(c => c.slug === slug && c.id !== form.id)) return setErr('A category with this name already exists');
    if (form.id) setCats(cs => cs.map(c => c.id === form.id ? { ...c, name, slug: c.slug, description: form.description } : c));
    else setCats(cs => [...cs, { id: Date.now(), name, slug, description: form.description }]);
    toast.success(`${form.id ? 'Updated' : 'Added'} category`);
    setForm({ id: null, name: '', description: '' }); setErr('');
  };

  const remove = async c => {
    const n = counts[c.slug] || 0;
    if (!(await confirmAction({ title: `Delete “${c.name}”?`, description: n ? `${n} products use this category. They would need a new category.` : 'This category has no products.', confirmLabel: 'Delete', danger: true }))) return;
    setCats(cs => cs.filter(x => x.id !== c.id)); toast.success('Removed category');
  };

  return (
    <div>
      <PageTitle title="Categories" sub={isLiveAdmin() ? "Product categories in the store catalog" : "Organise how products are grouped"} />
      <div className="form-grid">
        <div>{cats.length === 0 ? <EmptyState icon="🏷️" title="No categories yet">Add your first category.</EmptyState> :
          <div className="table-wrap"><table className="data-table"><thead><tr><th>Category</th><th>Slug</th><th>Products</th><th aria-label="Actions" /></tr></thead><tbody>
            {cats.map(c => <tr key={c.id}><td><div style={{ display: 'flex', gap: 10, alignItems: 'center' }}>{CATEGORY_IMAGES[c.slug] ? <img className="thumb" src={CATEGORY_IMAGES[c.slug]} alt="" /> : <span className="thumb" />}<div><strong>{c.name}</strong><div style={{ fontSize: '.78rem', color: 'var(--text-muted)' }}>{c.description}</div></div></div></td><td><code>{c.slug}</code></td><td>{counts[c.slug] || 0}</td>
              <td><ActionMenu label={`Actions for ${c.name}`} items={[{ label: 'Edit', onClick: () => { setForm({ id: c.id, name: c.name, description: c.description || '' }); setErr(''); } }, { label: 'Delete', danger: true, onClick: () => remove(c) }]} /></td></tr>)}
          </tbody></table></div>}</div>
        <form className="card" onSubmit={save} noValidate>
          <h3 style={{ marginBottom: 12 }}>{form.id ? 'Edit category' : 'New category'}</h3>
          <div className={`field ${err ? 'invalid' : ''}`}><label htmlFor="c-name">Name *</label><input id="c-name" value={form.name} onChange={e => { setForm({ ...form, name: e.target.value }); setErr(''); }} />{err && <span className="err" role="alert">{err}</span>}</div>
          <div className="field"><label htmlFor="c-desc">Description</label><textarea id="c-desc" rows={3} value={form.description} onChange={e => setForm({ ...form, description: e.target.value })} /></div>
          <div style={{ display: 'flex', gap: 8 }}><button className="btn btn-primary">{form.id ? 'Save' : 'Add category'}</button>{form.id && <button type="button" className="btn btn-secondary" onClick={() => setForm({ id: null, name: '', description: '' })}>Cancel</button>}</div>
        </form>
      </div>
    </div>
  );
}
