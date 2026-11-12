import React, { useEffect, useState } from 'react';
import { toast } from 'sonner';
import { mockCategories } from './mock-data';
import { CATEGORY_IMAGES } from './components';
import { SimulatedBadge } from '../components/States';
import { isLiveAdmin } from './admin-api';
import { confirmAction } from '../components/ConfirmDialog';

const EMPTY = { name: '', brand: '', sku: '', category: '', price: '', original_price: '', stock: '', status: 'draft', description: '', image_url: '' };

export function validateProduct(v) {
  const e = {};
  if (!v.name.trim()) e.name = 'Name is required';
  if (!v.brand.trim()) e.brand = 'Brand is required';
  if (!v.category) e.category = 'Choose a category';
  if (v.price === '' || Number(v.price) <= 0) e.price = 'Enter a price above 0';
  if (v.original_price !== '' && Number(v.original_price) < Number(v.price)) e.original_price = 'MRP must be at least the selling price';
  if (v.stock === '' || !Number.isInteger(Number(v.stock)) || Number(v.stock) < 0) e.stock = 'Enter a whole number, 0 or more';
  if (v.image_url && !/^https?:\/\/|^blob:/.test(v.image_url)) e.image_url = 'Use an http(s) image link';
  return e;
}

function F({ k, label, errors, children }) {
  return <div className={`field ${errors[k] ? 'invalid' : ''}`}><label htmlFor={`f-${k}`}>{label}</label>{children}{errors[k] && <span className="err" role="alert">{errors[k]}</span>}</div>;
}

export default function ProductForm({ initial, submitLabel, onSubmit, onCancel }) {
  const [v, setV] = useState({ ...EMPTY, ...(initial || {}) });
  const [errors, setErrors] = useState({});
  const [saving, setSaving] = useState(false);
  const [dirty, setDirty] = useState(false);
  const [imgBroken, setImgBroken] = useState(false);
  useEffect(() => setImgBroken(false), [v.image_url, v.category]);

  const set = k => e => { setV(s => ({ ...s, [k]: e.target.value })); setDirty(true); if (errors[k]) setErrors(x => ({ ...x, [k]: undefined })); };
  const onFile = e => {
    const f = e.target.files?.[0]; if (!f) return;
    if (!f.type.startsWith('image/')) return toast.error('Please choose an image file.');
    if (f.size > 5 * 1024 * 1024) return toast.error('Image must be under 5 MB.');
    setV(s => ({ ...s, image_url: URL.createObjectURL(f) })); setDirty(true);
    toast.info('Image previewed locally — it is not uploaded anywhere.');
  };
  const submit = async e => {
    e.preventDefault();
    const errs = validateProduct(v); setErrors(errs);
    if (Object.keys(errs).length) return toast.error('Please fix the highlighted fields.');
    setSaving(true);
    try { await onSubmit({ ...v, price: Number(v.price), original_price: v.original_price === '' ? Number(v.price) : Number(v.original_price), stock: Number(v.stock) }); setDirty(false); }
    catch (err) { toast.error(err.message || 'Could not save product.'); }
    finally { setSaving(false); }
  };
  const cancel = async () => { if (dirty && !(await confirmAction({ title: 'Discard changes?', description: 'Your edits will be lost.', confirmLabel: 'Discard', danger: true }))) return; onCancel(); };
  const preview = v.image_url || CATEGORY_IMAGES[v.category];

  return (
    <form onSubmit={submit} noValidate className="form-grid">
      <div className="card">
        <F errors={errors} k="name" label="Product name *"><input id="f-name" value={v.name} onChange={set('name')} placeholder="e.g. Lenovo IdeaPad Slim 5" /></F>
        <div className="field-row">
          <F errors={errors} k="brand" label="Brand *"><input id="f-brand" value={v.brand} onChange={set('brand')} /></F>
          <F errors={errors} k="sku" label="SKU"><input id="f-sku" value={v.sku} onChange={set('sku')} placeholder="Optional" /></F>
        </div>
        <div className="field-row">
          <F errors={errors} k="category" label="Category *"><select id="f-category" value={v.category} onChange={set('category')}><option value="">Select…</option>{mockCategories.map(c => <option key={c.slug} value={c.slug}>{c.name}</option>)}</select></F>
          <F errors={errors} k="status" label="Status"><select id="f-status" value={v.status} onChange={set('status')}><option value="draft">Draft</option><option value="active">Active</option></select></F>
        </div>
        <div className="field-row">
          <F errors={errors} k="price" label="Selling price (₹) *"><input id="f-price" type="number" min="0" inputMode="decimal" value={v.price} onChange={set('price')} /></F>
          <F errors={errors} k="original_price" label="MRP (₹)"><input id="f-original_price" type="number" min="0" value={v.original_price} onChange={set('original_price')} /></F>
        </div>
        <F errors={errors} k="stock" label="Stock quantity *"><input id="f-stock" type="number" min="0" step="1" value={v.stock} onChange={set('stock')} /></F>
        <F errors={errors} k="description" label="Description"><textarea id="f-description" rows={5} value={v.description} onChange={set('description')} /></F>
      </div>
      <div>
        <div className="card">
          <div className="field"><label>Image preview</label>
            <div className="img-preview">{preview && !imgBroken ? <img src={preview} alt="Product preview" onError={() => setImgBroken(true)} /> : <span>{imgBroken ? 'Image could not be loaded' : 'Pick a category or add an image'}</span>}</div>
          </div>
          <F errors={errors} k="image_url" label="Image link"><input id="f-image_url" value={v.image_url.startsWith('blob:') ? '' : v.image_url} onChange={set('image_url')} placeholder="https://…" /></F>
          <div className="field"><label htmlFor="f-file">Or choose a file</label><input id="f-file" type="file" accept="image/*" onChange={onFile} /></div>
          {v.image_url && <button type="button" className="btn btn-secondary btn-sm" onClick={() => { setV(s => ({ ...s, image_url: '' })); setDirty(true); }}>Remove image</button>}
        </div>
        <div className="card" style={{ marginTop: 16, display: 'flex', flexDirection: 'column', gap: 8 }}>
          {!isLiveAdmin() && <SimulatedBadge>Preview only — not saved to the store</SimulatedBadge>}
          <button type="submit" className="btn btn-primary" disabled={saving}>{saving ? 'Saving…' : submitLabel}</button>
          <button type="button" className="btn btn-secondary" onClick={cancel} disabled={saving}>Cancel</button>
        </div>
      </div>
    </form>
  );
}
