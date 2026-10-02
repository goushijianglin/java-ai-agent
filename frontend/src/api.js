// バックエンド (Spring Boot) の JSON API 呼び出し。セッション Cookie は同一オリジンなので自動送信される。

export class ApiError extends Error {
  constructor(status, message, body) {
    super(message);
    this.status = status;
    this.body = body;
  }
}

async function request(method, path, body) {
  const res = await fetch(path, {
    method,
    headers: {
      Accept: 'application/json',
      ...(body !== undefined && { 'Content-Type': 'application/json' }),
    },
    body: body !== undefined ? JSON.stringify(body) : undefined,
  });
  const data = await res.json().catch(() => null);
  if (!res.ok) {
    throw new ApiError(res.status, data?.message ?? `エラーが発生しました (${res.status})`, data);
  }
  return data;
}

export const api = {
  me: () => request('GET', '/api/me'),
  login: (username, password) => request('POST', '/api/login', { username, password }),
  logout: () => request('POST', '/api/logout'),
  searchProducts: (params) => request('GET', `/api/products?${new URLSearchParams(params)}`),
  getProduct: (id) => request('GET', `/api/products/${encodeURIComponent(id)}`),
  purchase: (productId, quantity) => request('POST', '/api/purchase', { productId, quantity }),
  getOrder: (orderId) => request('GET', `/api/orders/${encodeURIComponent(orderId)}`),
};
