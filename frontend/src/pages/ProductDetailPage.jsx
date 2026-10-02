import { useEffect, useState } from 'react';
import { Link, Navigate, useNavigate, useParams } from 'react-router-dom';
import { api } from '../api.js';
import { useHandleAuthError } from '../auth.jsx';
import { yen } from '../format.js';
import Alert from '../components/Alert.jsx';

export default function ProductDetailPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const handleAuthError = useHandleAuthError();
  const [product, setProduct] = useState(null);
  const [loadError, setLoadError] = useState('');
  const [quantity, setQuantity] = useState('1');
  const [error, setError] = useState('');
  const [submitting, setSubmitting] = useState(false);

  const load = () =>
    api.getProduct(id)
      .then(setProduct)
      .catch((e) => { handleAuthError(e); setLoadError(e.message); });

  useEffect(() => {
    setProduct(null);
    setLoadError('');
    setError('');
    setQuantity('1');
    load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [id]);

  // 存在しない商品は一覧へ戻してエラー表示
  if (loadError) return <Navigate to="/products" replace state={{ error: loadError }} />;
  if (!product) return <p className="muted">読み込み中...</p>;

  const soldOut = product.stock < 1;

  const onSubmit = async (e) => {
    e.preventDefault();
    const qty = Number(quantity);
    if (!Number.isInteger(qty) || qty < 1) {
      setError('数量は1以上の整数で入力してください');
      return;
    }
    if (qty > product.stock) {
      setError(`在庫が不足しています（在庫: ${product.stock} 個 / ご希望: ${qty} 個）`);
      return;
    }
    setSubmitting(true);
    setError('');
    try {
      const { orderId } = await api.purchase(product.id, qty);
      navigate(`/purchase/complete?orderId=${orderId}`);
    } catch (err) {
      handleAuthError(err);
      setError(err.message);
      setSubmitting(false);
      load(); // 在庫数を最新化
    }
  };

  return (
    <>
      <p><Link to="/products">« 商品一覧へ戻る</Link></p>
      <div className="card detail">
        <img className="detail-image" src={product.imageUrl} alt={product.name} />
        <div className="detail-body">
          <div className="muted">商品ID: {product.id}</div>
          <h1>{product.name}</h1>
          <p className="price">{yen(product.price)}<small>（税込）</small></p>
          <p className="description">{product.description}</p>
          <p>
            在庫: <strong className={soldOut ? 'soldout' : ''}>{soldOut ? '在庫切れ' : `${product.stock} 個`}</strong>
          </p>
          <Alert messages={error} />
          <form className="purchase" onSubmit={onSubmit} noValidate>
            <label className="field">
              <span>数量</span>
              <input type="number" name="quantity" min="1" max={Math.max(product.stock, 1)} value={quantity}
                     disabled={soldOut} onChange={(e) => setQuantity(e.target.value)} />
            </label>
            <button type="submit" className="btn btn-primary" disabled={soldOut || submitting}>
              {submitting ? '処理中...' : '購入'}
            </button>
          </form>
        </div>
      </div>
    </>
  );
}
