import { useEffect, useState } from 'react';
import { Link, useLocation, useSearchParams } from 'react-router-dom';
import { api } from '../api.js';
import { useHandleAuthError } from '../auth.jsx';
import { yen } from '../format.js';
import Alert from '../components/Alert.jsx';

const FIELDS = ['q', 'minPrice', 'maxPrice'];

export default function ProductsPage() {
  const [searchParams, setSearchParams] = useSearchParams();
  const location = useLocation();
  const handleAuthError = useHandleAuthError();
  const [form, setForm] = useState(() => Object.fromEntries(FIELDS.map((k) => [k, searchParams.get(k) ?? ''])));
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);
  // 他画面から渡されたエラー (例: 存在しない商品)
  const flashError = location.state?.error;

  // URL の検索条件が変わったら検索 (ブラウザの戻る/進むにも対応)
  useEffect(() => {
    const params = {};
    for (const k of [...FIELDS, 'page']) {
      const v = searchParams.get(k);
      if (v) params[k] = v;
    }
    setForm(Object.fromEntries(FIELDS.map((k) => [k, searchParams.get(k) ?? ''])));
    setLoading(true);
    let cancelled = false;
    api.searchProducts(params)
      .then((data) => { if (!cancelled) { setResult(data); setError(''); } })
      .catch((e) => { if (!cancelled) { handleAuthError(e); setResult(null); setError(e.message); } })
      .finally(() => { if (!cancelled) setLoading(false); });
    return () => { cancelled = true; };
  }, [searchParams, handleAuthError]);

  const toParams = (values, page) => {
    const p = {};
    for (const k of FIELDS) if (values[k]) p[k] = values[k];
    if (page > 1) p.page = String(page);
    return p;
  };

  const onSubmit = (e) => {
    e.preventDefault();
    setSearchParams(toParams(form, 1));
  };

  const current = Object.fromEntries(FIELDS.map((k) => [k, searchParams.get(k) ?? '']));
  const goPage = (page) => setSearchParams(toParams(current, page));

  return (
    <>
      <h1>商品検索</h1>
      <form className="search card" onSubmit={onSubmit}>
        <label className="field grow">
          <span>商品名</span>
          <input type="text" name="q" placeholder="部分一致" value={form.q}
                 onChange={(e) => setForm({ ...form, q: e.target.value })} />
        </label>
        <label className="field">
          <span>最低価格</span>
          <input type="number" name="minPrice" min="0" value={form.minPrice}
                 onChange={(e) => setForm({ ...form, minPrice: e.target.value })} />
        </label>
        <label className="field">
          <span>最高価格</span>
          <input type="number" name="maxPrice" min="0" value={form.maxPrice}
                 onChange={(e) => setForm({ ...form, maxPrice: e.target.value })} />
        </label>
        <div className="search-actions">
          <button type="submit" className="btn btn-primary">検索</button>
          <button type="button" className="btn" onClick={() => setSearchParams({})}>クリア</button>
        </div>
      </form>

      <Alert messages={[flashError, ...(result ? [] : error ? [error] : [])]} />

      {loading && !result && <p className="muted">読み込み中...</p>}

      {result && (
        <>
          <p className="muted">
            該当 {result.total} 件
            {result.total > 0 && `（${result.currentPage} / ${result.totalPages} ページ）`}
          </p>
          {result.products.length === 0 ? (
            <div className="card empty">該当する商品がありません</div>
          ) : (
            <table className="table">
              <thead>
                <tr>
                  <th className="num">ID</th>
                  <th></th>
                  <th>商品名</th>
                  <th className="num">価格</th>
                  <th className="num">在庫</th>
                  <th></th>
                </tr>
              </thead>
              <tbody>
                {result.products.map((p) => (
                  <tr key={p.id}>
                    <td className="num">{p.id}</td>
                    <td><img className="thumb" src={p.imageUrl} alt="" /></td>
                    <td>{p.name}</td>
                    <td className="num">{yen(p.price)}</td>
                    <td className={`num${p.stock === 0 ? ' soldout' : ''}`}>{p.stock === 0 ? '在庫切れ' : p.stock}</td>
                    <td><Link className="btn btn-small" to={`/products/${p.id}`}>詳細</Link></td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
          {result.totalPages > 1 && (
            <nav className="pager">
              <button type="button" className="btn" disabled={result.currentPage <= 1}
                      onClick={() => goPage(result.currentPage - 1)}>« 前へ</button>
              <span className="pager-info">{result.currentPage} / {result.totalPages}</span>
              <button type="button" className="btn btn-primary" disabled={result.currentPage >= result.totalPages}
                      onClick={() => goPage(result.currentPage + 1)}>次へ »</button>
            </nav>
          )}
        </>
      )}
    </>
  );
}
