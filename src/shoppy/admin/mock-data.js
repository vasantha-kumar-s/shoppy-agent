/**
 * PREVIEW MOCK DATA — admin dashboard only.
 * Nothing here comes from or is written to the Shoppy store service.
 * Replace each function with a real call in services/admin-api.js once FastAPI admin endpoints exist.
 */
export const MOCK_NOTICE = 'Preview data — changes are simulated and are not saved.';

export const mockCategories = [
  { id: 1, name: 'Laptops', slug: 'laptops', description: 'Portable computers for work and play' },
  { id: 2, name: 'Smartphones', slug: 'smartphones', description: 'Latest Android and iOS phones' },
  { id: 3, name: 'Headphones', slug: 'headphones', description: 'Wired and wireless audio' },
  { id: 4, name: 'Monitors', slug: 'monitors', description: 'Displays for every desk' },
  { id: 5, name: 'Keyboards', slug: 'keyboards', description: 'Mechanical and membrane keyboards' },
  { id: 6, name: 'Mice', slug: 'mice', description: 'Precision pointing devices' },
  { id: 7, name: 'Smartwatches', slug: 'smartwatches', description: 'Wearables and fitness trackers' },
];

const brands = { laptops: ['Lenovo', 'Dell', 'HP', 'ASUS'], smartphones: ['Samsung', 'OnePlus', 'Xiaomi', 'Apple'], headphones: ['Sony', 'boAt', 'JBL'], monitors: ['LG', 'Samsung', 'BenQ'], keyboards: ['Logitech', 'Keychron', 'Redragon'], mice: ['Logitech', 'Razer'], smartwatches: ['Noise', 'Amazfit', 'Samsung'] };
const basePrice = { laptops: 62000, smartphones: 28000, headphones: 4500, monitors: 16000, keyboards: 3800, mice: 1600, smartwatches: 5200 };

let products = [];
let pid = 1;
mockCategories.forEach((c, ci) => {
  brands[c.slug].forEach((b, bi) => {
    for (let k = 0; k < 2; k++) {
      const price = Math.round(basePrice[c.slug] * (0.7 + ((bi * 2 + k) % 5) * 0.15) / 10) * 10;
      products.push({
        id: pid, name: `${b} ${c.name.replace(/s$/, '')} ${['Pro', 'Lite', 'Max', 'Air'][(bi + k) % 4]} ${(ci + 1) * 10 + k}`,
        brand: b, category: c.slug, price, original_price: Math.round(price * 1.15),
        stock: (pid * 7) % 40, rating: Math.round((3.6 + ((pid * 3) % 14) / 10) * 10) / 10,
        status: pid % 9 === 0 ? 'draft' : 'active', description: `Preview listing for a ${b} ${c.name.toLowerCase().replace(/s$/, '')}.`, image_url: '', sku: `SKU-${String(pid).padStart(4, '0')}`,
      });
      pid++;
    }
  });
});

export const mockCustomers = ['Aarav Sharma', 'Diya Patel', 'Rohan Iyer', 'Meera Nair', 'Kabir Singh', 'Ananya Rao', 'Vihaan Gupta', 'Isha Reddy', 'Arjun Menon', 'Sara Khan', 'Dev Joshi', 'Nisha Verma']
  .map((name, i) => ({ id: i + 1, name, email: `${name.split(' ')[0].toLowerCase()}@example.com`, city: ['Bangalore', 'Mumbai', 'Chennai', 'Delhi', 'Pune', 'Hyderabad'][i % 6], orders: (i * 3) % 9 + 1, spent: ((i * 3) % 9 + 1) * (8000 + i * 1300), joined: `2026-0${(i % 9) + 1}-1${i % 9}` }));

const statuses = ['confirmed', 'processing', 'shipped', 'delivered', 'cancelled'];
export const mockOrders = Array.from({ length: 24 }, (_, i) => ({
  id: i + 1, order_number: `PRV-${1040 + i}`, customer: mockCustomers[i % mockCustomers.length].name,
  items: (i % 3) + 1, total: 2500 + ((i * 7919) % 90000), status: statuses[i % 5], date: `2026-10-${String((i % 28) + 1).padStart(2, '0')}`,
}));

export const mockSalesByMonth = [['May', 182000], ['Jun', 214000], ['Jul', 198000], ['Aug', 256000], ['Sep', 289000], ['Oct', 312000]];

const delay = (ms = 350) => new Promise(r => setTimeout(r, ms));
const clone = v => JSON.parse(JSON.stringify(v));

export const mockAdmin = {
  async listProducts() { await delay(); return clone(products); },
  async getProduct(id) { await delay(); const p = products.find(x => x.id === Number(id)); if (!p) throw new Error('Product not found in preview data.'); return clone(p); },
  async createProduct(data) { await delay(500); const p = { ...data, id: pid++ }; products = [p, ...products]; return clone(p); },
  async updateProduct(id, data) { await delay(500); products = products.map(p => p.id === Number(id) ? { ...p, ...data, id: p.id } : p); return clone(products.find(p => p.id === Number(id))); },
  async deleteProduct(id) { await delay(300); products = products.filter(p => p.id !== Number(id)); },
  async adjustStock(id, stock) { await delay(250); products = products.map(p => p.id === Number(id) ? { ...p, stock } : p); },
};
