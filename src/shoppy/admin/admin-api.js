/**
 * Admin data client. Live sessions call the store service's REST endpoints;
 * preview sessions use the labelled in-memory mockAdmin (nothing is saved).
 *
 * Connected FastAPI endpoints:
 *   POST   /api/admin/login                  -> { access_token, role, name }
 *   GET    /api/products?limit=100           (existing)
 *   GET    /api/products/{id}                (existing)
 *   POST   /api/admin/products               (create product)
 *   PUT    /api/admin/products/{id}          (update product)
 *   DELETE /api/admin/products/{id}          (delete product)
 *   PATCH  /api/admin/products/{id}/stock    (adjust stock)
 *   GET    /api/admin/orders                 (all store orders)
 *   PATCH  /api/admin/orders/{id}/status     (update order status)
 *   GET    /api/admin/customers              (customer directory)
 *   GET    /api/admin/analytics              (sales analytics overview)
 */
import { API_BASE } from '../services/api';
import { getAdminSession } from './session';
import { mockAdmin, mockOrders, mockCustomers, mockSalesByMonth, mockCategories } from './mock-data';

export const isLiveAdmin = () => getAdminSession()?.mode === 'live';

async function call(path, options = {}) {
  if (!API_BASE) throw new Error('The store service is not connected.');
  const token = getAdminSession()?.token;
  const res = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers: { 'Content-Type': 'application/json', ...(token ? { Authorization: `Bearer ${token}` } : {}), ...options.headers },
  });
  if (res.status === 401 || res.status === 403) throw new Error('Your admin session is not allowed to do this. Sign in again.');
  if (res.status === 404 || res.status === 405) throw new Error(`The store service has no ${options.method || 'GET'} ${path.split('?')[0]} endpoint yet.`);
  if (!res.ok) { const e = await res.json().catch(() => ({})); throw new Error(typeof e.detail === 'string' ? e.detail : `Store service error ${res.status}`); }
  return res.status === 204 ? null : res.json().catch(() => null);
}

const toForm = p => ({
  ...p,
  category: typeof p.category === 'object' ? (p.category?.slug || p.category?.name || '') : (p.category_slug || p.category || ''),
  status: p.status || (p.is_active === false ? 'draft' : 'active'),
  stock: p.stock ?? p.inventory?.quantity ?? p.stock_quantity ?? 0,
  image_url: p.image_url || '',
});

const live = {
  async listProducts() { return (await call('/api/products?limit=100')).map(toForm); },
  async getProduct(id) { return toForm(await call(`/api/products/${id}`)); },
  async createProduct(data) { return toForm(await call('/api/admin/products', { method: 'POST', body: JSON.stringify(data) })); },
  async updateProduct(id, data) { return toForm(await call(`/api/admin/products/${id}`, { method: 'PUT', body: JSON.stringify(data) })); },
  async deleteProduct(id) { await call(`/api/admin/products/${id}`, { method: 'DELETE' }); },
  async adjustStock(id, stock) { await call(`/api/admin/products/${id}/stock`, { method: 'PATCH', body: JSON.stringify({ stock }) }); },
  async listOrders() { return await call('/api/admin/orders'); },
  async updateOrderStatus(id, status) { return await call(`/api/admin/orders/${id}/status`, { method: 'PATCH', body: JSON.stringify({ status }) }); },
  async listCustomers() { return await call('/api/admin/customers'); },
  async getAnalytics() { return await call('/api/admin/analytics'); },
};

const mockFallback = {
  ...mockAdmin,
  async listOrders() { return mockOrders; },
  async updateOrderStatus(id, status) { return { id, status }; },
  async listCustomers() { return mockCustomers; },
  async getAnalytics() {
    const valid = mockOrders.filter(o => o.status !== 'cancelled');
    const revenue = valid.reduce((a, o) => a + o.total, 0);
    return {
      revenue,
      orders: mockOrders.length,
      avg_order_value: Math.round(revenue / (valid.length || 1)),
      cancellation_rate: `${Math.round((1 - valid.length / mockOrders.length) * 100)}%`,
      sales_by_month: mockSalesByMonth,
      sales_by_category: mockCategories.map(c => [c.name, 100000]),
    };
  },
};

export const adminApi = new Proxy({}, { get: (_, k) => (isLiveAdmin() ? live : mockFallback)[k] });
