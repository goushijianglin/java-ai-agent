import { useState } from 'react';
import { Navigate, useNavigate } from 'react-router-dom';
import { useAuth } from '../auth.jsx';
import Alert from '../components/Alert.jsx';

export default function LoginPage() {
  const { user, login } = useAuth();
  const navigate = useNavigate();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [submitting, setSubmitting] = useState(false);

  if (user) return <Navigate to="/products" replace />;

  const onSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    setError('');
    try {
      await login(username, password);
      navigate('/products', { replace: true });
    } catch (err) {
      setError(err.message);
      setSubmitting(false);
    }
  };

  return (
    <div className="card login-card">
      <h1>ログイン</h1>
      <Alert messages={error} />
      <form onSubmit={onSubmit}>
        <label className="field">
          <span>ユーザ名</span>
          <input type="text" name="username" value={username} required autoFocus autoComplete="username"
                 onChange={(e) => setUsername(e.target.value)} />
        </label>
        <label className="field">
          <span>パスワード</span>
          <input type="password" name="password" value={password} required autoComplete="current-password"
                 onChange={(e) => setPassword(e.target.value)} />
        </label>
        <button type="submit" className="btn btn-primary btn-block" disabled={submitting}>
          {submitting ? 'ログイン中...' : 'ログイン'}
        </button>
      </form>
      <p className="hint">デモユーザ: demo / demo</p>
    </div>
  );
}
