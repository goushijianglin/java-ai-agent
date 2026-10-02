import { Link, Outlet, useNavigate } from 'react-router-dom';
import { useAuth } from '../auth.jsx';

export default function Layout() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const onLogout = async () => {
    await logout();
    navigate('/login', { replace: true });
  };

  return (
    <>
      <header className="header">
        <Link className="brand" to={user ? '/products' : '/login'}>Demo EC</Link>
        {user && (
          <div className="header-user">
            <span className="user-name">{user.displayName} さん</span>
            <button type="button" className="btn btn-link" onClick={onLogout}>ログアウト</button>
          </div>
        )}
      </header>
      <main className="container">
        <Outlet />
      </main>
    </>
  );
}
