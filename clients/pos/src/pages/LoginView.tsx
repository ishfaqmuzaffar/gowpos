import { FormEvent, useState } from 'react';
import { usePOSStore } from '../store/usePOSStore';

const LoginView = () => {
  const { login, loading, error, isAuthenticated } = usePOSStore();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [status, setStatus] = useState('');

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setStatus('');
    try {
      await login(email, password);
      setStatus('Logged in successfully');
    } catch (err) {
      setStatus((err as Error).message);
    }
  };

  return (
    <section className="card">
      <h2>Sign In</h2>
      {isAuthenticated && <p className="status-pill success">You are already signed in.</p>}
      <form className="form-grid" onSubmit={handleSubmit}>
        <label>
          Email
          <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
        </label>
        <label>
          Password
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </label>
        <button className="primary" type="submit" disabled={loading}>
          {loading ? 'Signing in…' : 'Sign In'}
        </button>
        {(status || error) && <p className="status-pill warning">{status || error}</p>}
      </form>
    </section>
  );
};

export default LoginView;
