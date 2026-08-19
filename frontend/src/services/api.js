/**
 * AgentCart — API Service
 * Centralized API client for all backend communication.
 */

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000';

async function request(path, options = {}) {
  const url = `${API_BASE}${path}`;
  const config = {
    headers: {
      'Content-Type': 'application/json',
      'X-User-ID': '1', // Demo user
      ...options.headers,
    },
    ...options,
  };

  // Don't set Content-Type for FormData
  if (config.body instanceof FormData) {
    delete config.headers['Content-Type'];
  }

  const response = await fetch(url, config);

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: response.statusText }));
    throw new Error(error.detail || `API Error: ${response.status}`);
  }

  // Handle audio responses
  if (response.headers.get('content-type')?.includes('audio')) {
    return response.blob();
  }

  return response.json();
}

// --- Products ---
export async function getProducts(params = {}) {
  const query = new URLSearchParams();
  Object.entries(params).forEach(([key, value]) => {
    if (value !== null && value !== undefined && value !== '') {
      query.set(key, value);
    }
  });
  return request(`/api/products?${query.toString()}`);
}

export async function getProduct(id) {
  return request(`/api/products/${id}`);
}

export async function getCategories() {
  return request('/api/products/categories');
}

export async function compareProducts(productIds) {
  return request('/api/products/compare', {
    method: 'POST',
    body: JSON.stringify(productIds),
  });
}

export async function checkStock(productId, quantity = 1) {
  return request(`/api/products/${productId}/stock?quantity=${quantity}`);
}

// --- Cart ---
export async function getCart() {
  return request('/api/cart');
}

export async function addToCart(productId, quantity = 1) {
  return request('/api/cart/items', {
    method: 'POST',
    body: JSON.stringify({ product_id: productId, quantity }),
  });
}

export async function updateCartItem(productId, quantity) {
  return request(`/api/cart/items/${productId}`, {
    method: 'PUT',
    body: JSON.stringify({ quantity }),
  });
}

export async function removeFromCart(productId) {
  return request(`/api/cart/items/${productId}`, { method: 'DELETE' });
}

export async function clearCart() {
  return request('/api/cart', { method: 'DELETE' });
}

// --- Orders ---
export async function createOrder(shippingAddressId = null) {
  return request('/api/orders', {
    method: 'POST',
    body: JSON.stringify({ shipping_address_id: shippingAddressId }),
  });
}

export async function getOrders() {
  return request('/api/orders');
}

export async function getOrder(orderId) {
  return request(`/api/orders/${orderId}`);
}

// --- Chat & Conversation Sessions ---
export async function sendMessage(message, conversationId = null) {
  return request('/api/chat', {
    method: 'POST',
    body: JSON.stringify({
      message,
      user_id: 1,
      conversation_id: conversationId,
    }),
  });
}

export async function getConversations() {
  return request('/api/conversations');
}

export async function createConversation() {
  return request('/api/conversations', { method: 'POST' });
}

export async function getConversationMessages(conversationId) {
  return request(`/api/conversations/${conversationId}/messages`);
}

export async function deleteConversation(conversationId) {
  return request(`/api/conversations/${conversationId}`, { method: 'DELETE' });
}

// --- Voice ---
export async function transcribeAudio(audioBlob) {
  const formData = new FormData();
  formData.append('audio', audioBlob, 'recording.webm');
  return request('/api/voice/transcribe', {
    method: 'POST',
    body: formData,
  });
}

export async function synthesizeSpeech(text) {
  return request('/api/voice/speak', {
    method: 'POST',
    body: JSON.stringify({ text }),
  });
}

// --- Health ---
export async function getHealth() {
  return request('/api/health');
}
