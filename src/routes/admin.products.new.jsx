import { createFileRoute } from '@tanstack/react-router';
import React from 'react';
import { toast } from 'sonner';
import { useNavigate } from '@/shoppy/navigation';
import { adminApi, isLiveAdmin } from '@/shoppy/admin/admin-api';
import { PageTitle } from '@/shoppy/admin/components';
import ProductForm from '@/shoppy/admin/ProductForm';
import { adminHead } from '@/shoppy/admin/head';

export const Route = createFileRoute('/admin/products/new')({ head: adminHead('Add product'), component: NewProduct });

function NewProduct() {
  const navigate = useNavigate();
  return (
    <div>
      <PageTitle title="Add product" sub="Create a new catalog listing" />
      <ProductForm submitLabel="Create product" onCancel={() => navigate('/admin/products')} onSubmit={async v => {
        await adminApi.createProduct(v);
        toast.success(isLiveAdmin() ? 'Saved to the store' : 'Product added to preview list (simulated — not saved to the store).');
        navigate('/admin/products');
      }} />
    </div>
  );
}
