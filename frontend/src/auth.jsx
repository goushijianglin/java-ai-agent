import { createContext, useCallback, useContext, useEffect, useState } from 'react';
import { Navigate } from 'react-router-dom';
import { api } from './api.js';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  // undefined: 確認中 / null: 未ログイン / object: ログインユーザ
  const [user, setUser] = useState(undefined);

  useEffect(() => {
    api.me().then(setUser).catch(() => setUser(null));
  }, []);

  const login = useCallback(async (username, password) => {
    setUser(await api.login(username, password));
  }, []);

  const logout = useCallback(async () => {
    try {
      await api.logout();
    } finally {
      setUser(null);
    }
  }, []);

  return (
    <AuthContext.Provider value={{ user, setUser, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}

/** ログイン必須の画面。未ログインなら /login へ */
export function RequireAuth({ children }) {
  const { user } = useAuth();
  if (user === undefined) return <p className="muted container">読み込み中...</p>;
  if (user === null) return <Navigate to="/login" replace />;
  return children;
}

/** API が 401 を返したら (セッション切れ) ログアウト状態にする */
export function useHandleAuthError() {
  const { setUser } = useAuth();
  return useCallback(
    (e) => {
      if (e?.status === 401) setUser(null);
    },
    [setUser],
  );
}
