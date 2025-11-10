import { useState } from 'react';
import { authService } from '../lib/auth';

export default function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [msg, setMsg] = useState('');

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await authService.login(username, password);
      setMsg('Logged in!');
      window.location.href = '/';
    } catch (e) {
      setMsg('Login failed');
    }
  };

  return (
    <form onSubmit={onSubmit} style={{ maxWidth: 320, margin: '80px auto' }}>
      <h3>Login</h3>
      <input placeholder="Username" value={username} onChange={e=>setUsername(e.target.value)} />
      <input placeholder="Password" type="password" value={password} onChange={e=>setPassword(e.target.value)} />
      <button type="submit">Login</button>
      <div>{msg}</div>
    </form>
  );
}