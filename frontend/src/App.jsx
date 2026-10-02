import { Navigate, Route, Routes } from 'react-router-dom';
import { AuthProvider, RequireAuth } from './auth.jsx';
import Layout from './components/Layout.jsx';
import LoginPage from './pages/LoginPage.jsx';
import ProductsPage from './pages/ProductsPage.jsx';
import ProductDetailPage from './pages/ProductDetailPage.jsx';
import PurchaseCompletePage from './pages/PurchaseCompletePage.jsx';

export default function App() {
  return (
    <AuthProvider>
      <Routes>
        <Route element={<Layout />}>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/products" element={<RequireAuth><ProductsPage /></RequireAuth>} />
          <Route path="/products/:id" element={<RequireAuth><ProductDetailPage /></RequireAuth>} />
          <Route path="/purchase/complete" element={<RequireAuth><PurchaseCompletePage /></RequireAuth>} />
          <Route path="*" element={<Navigate to="/products" replace />} />
        </Route>
      </Routes>
    </AuthProvider>
  );
}
