import { FormEvent, useState } from 'react';
import { usePOSStore } from '../store/usePOSStore';

const RegisterView = () => {
  const { register, loading, error } = usePOSStore();
  const [displayName, setDisplayName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [status, setStatus] = useState('');

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    try {
      await register({ displayName, email, password });
      setStatus('Registration complete!');
    } catch (err) {
      setStatus((err as Error).message);
    }
  };

  return (
    <section className="card">
      <h2>Create Account</h2>
      <form className="form-grid" onSubmit={handleSubmit}>
        <label>
          Name
          <input value={displayName} onChange={(e) => setDisplayName(e.target.value)} required />
        </label>
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
          {loading ? 'Creating...' : 'Register'}
        </button>
        {(status || error) && <p className="status-pill warning">{status || error}</p>}
      </form>
    </section>
  );
};

export default RegisterView;
