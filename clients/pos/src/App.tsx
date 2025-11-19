import { NavLink, Route, Routes } from 'react-router-dom';
import LoginView from './pages/LoginView';
import RegisterView from './pages/RegisterView';
import ProductSearchView from './pages/ProductSearchView';
import CartView from './pages/CartView';
import CheckoutView from './pages/CheckoutView';
import InventoryDashboard from './pages/InventoryDashboard';
import EndOfDayReports from './pages/EndOfDayReports';
import { usePOSStore } from './store/usePOSStore';

const App = () => {
  const { isAuthenticated, logout, currentUser } = usePOSStore();

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <h1>GoW POS</h1>
        {isAuthenticated && (
          <div style={{ marginBottom: '1rem', fontSize: '0.9rem', color: '#9ca3af' }}>
            <p>Signed in as</p>
            <strong>{currentUser?.displayName ?? currentUser?.email}</strong>
            <div>
              <button className="secondary" style={{ marginTop: '0.5rem' }} onClick={logout}>
                Sign out
              </button>
            </div>
          </div>
        )}
        <nav>
          <NavLink to="/login" className={({ isActive }) => (isActive ? 'active' : '')}>
            Login
          </NavLink>
          <NavLink to="/register" className={({ isActive }) => (isActive ? 'active' : '')}>
            Register
          </NavLink>
          <NavLink to="/products" className={({ isActive }) => (isActive ? 'active' : '')}>
            Product Search
          </NavLink>
          <NavLink to="/cart" className={({ isActive }) => (isActive ? 'active' : '')}>
            Cart
          </NavLink>
          <NavLink to="/checkout" className={({ isActive }) => (isActive ? 'active' : '')}>
            Checkout
          </NavLink>
          <NavLink to="/inventory" className={({ isActive }) => (isActive ? 'active' : '')}>
            Inventory
          </NavLink>
          <NavLink to="/reports" className={({ isActive }) => (isActive ? 'active' : '')}>
            EOD Reports
          </NavLink>
        </nav>
      </aside>
      <main className="content">
        <Routes>
          <Route path="/" element={<ProductSearchView />} />
          <Route path="/login" element={<LoginView />} />
          <Route path="/register" element={<RegisterView />} />
          <Route path="/products" element={<ProductSearchView />} />
          <Route path="/cart" element={<CartView />} />
          <Route path="/checkout" element={<CheckoutView />} />
          <Route path="/inventory" element={<InventoryDashboard />} />
          <Route path="/reports" element={<EndOfDayReports />} />
        </Routes>
      </main>
    </div>
  );
};

export default App;
