import { createFileRoute } from '@tanstack/react-router';
import React, { useEffect, useState } from 'react';
import { toast } from 'sonner';
import { useNavigate, useParams, Link } from '@/shoppy/navigation';
import { adminApi, isLiveAdmin } from '@/shoppy/admin/admin-api';
import { PageTitle } from '@/shoppy/admin/components';
import ProductForm from '@/shoppy/admin/ProductForm';
import { LoadingState, EmptyState } from '@/shoppy/components/States';
import { confirmAction } from '@/shoppy/components/ConfirmDialog';
import { adminHead } from '@/shoppy/admin/head';

export const Route = createFileRoute('/admin/products/$id')({ head: adminHead('Edit product'), component: EditProduct });

function EditProduct() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [p, setP] = useState(undefined);
  const [err, setErr] = useState('');
  useEffect(() => { adminApi.getProduct(id).then(setP).catch(e => setErr(e.message)); }, [id]);
  if (err) return <EmptyState icon="📦" title="Product not found" action={<Link to="/admin/products" className="btn btn-primary">Back to products</Link>}>{err}</EmptyState>;
  if (!p) return <LoadingState label="Loading product…" />;
  const del = async () => {
    if (!(await confirmAction({ title: 'Delete this product?', description: 'Simulated in preview mode — the store is not changed.', confirmLabel: 'Delete', danger: true }))) return;
    await adminApi.deleteProduct(p.id); toast.success(isLiveAdmin() ? 'Saved to the store' : 'Removed from preview (simulated)'); navigate('/admin/products');
  };
  return (
    <div>
      <PageTitle title={`Edit: ${p.name}`} sub={`SKU ${p.sku || '—'}`} actions={<button className="btn btn-danger btn-sm" onClick={del}>Delete</button>} />
      <ProductForm initial={{ ...p, price: String(p.price), original_price: String(p.original_price ?? ''), stock: String(p.stock) }} submitLabel="Save changes" onCancel={() => navigate('/admin/products')} onSubmit={async v => {
        await adminApi.updateProduct(p.id, v); toast.success(isLiveAdmin() ? 'Saved to the store' : 'Changes applied to preview (simulated — not saved to the store).'); navigate('/admin/products');
      }} />
    </div>
  );
}
