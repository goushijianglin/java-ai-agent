import { useEffect, useState } from 'react';
import { Link, Navigate, useSearchParams } from 'react-router-dom';
import { api } from '../api.js';
import { useHandleAuthError } from '../auth.jsx';
import { yen } from '../format.js';

export default function PurchaseCompletePage() {
  const [searchParams] = useSearchParams();
  const orderId = searchParams.get('orderId') ?? '';
  const handleAuthError = useHandleAuthError();
  const [order, setOrder] = useState(null);
  const [error, setError] = useState('');

  useEffect(() => {
    api.getOrder(orderId)
      .then(setOrder)
      .catch((e) => { handleAuthError(e); setError(e.message); });
  }, [orderId, handleAuthError]);

  if (error) return <Navigate to="/products" replace state={{ error }} />;
  if (!order) return <p className="muted">読み込み中...</p>;

  return (
    <div className="card complete">
      <h1>ご購入ありがとうございました</h1>
      <dl className="summary">
        <dt>注文番号</dt><dd>{order.orderId}</dd>
        <dt>注文日時</dt><dd>{order.createdAt}</dd>
        <dt>商品名</dt><dd>{order.productName}</dd>
        <dt>単価</dt><dd>{yen(order.unitPrice)}</dd>
        <dt>数量</dt><dd>{order.quantity}</dd>
        <dt>合計金額</dt><dd className="total">{yen(order.totalPrice)}</dd>
      </dl>
      <Link className="btn btn-primary" to="/products">買い物を続ける</Link>
    </div>
  );
}
