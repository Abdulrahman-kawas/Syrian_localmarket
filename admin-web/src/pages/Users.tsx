import { useEffect, useState } from 'react';
import { api, type AdminUser } from '../api';

export function Users() {
  const [items, setItems] = useState<AdminUser[]>([]);
  const [q, setQ] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function load() {
    setLoading(true);
    setError(null);
    try {
      const query = q ? `?q=${encodeURIComponent(q)}` : '';
      setItems(await api.get<AdminUser[]>(`/admin/users${query}`));
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Failed to load');
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  async function toggleSuspend(u: AdminUser) {
    const notes = window.prompt(`Reason to ${u.is_suspended ? 'unsuspend' : 'suspend'}:`) ?? undefined;
    await api.put(`/admin/users/${u.id}/suspend`, { suspended: !u.is_suspended, notes });
    await load();
  }

  async function adjustReputation(u: AdminUser) {
    const raw = window.prompt('New reputation (0.00–5.00):', u.reputation_score);
    if (raw === null) return;
    const value = Number(raw);
    if (Number.isNaN(value) || value < 0 || value > 5) {
      alert('Enter a number between 0 and 5');
      return;
    }
    await api.put(`/admin/users/${u.id}/reputation`, { reputation_score: value });
    await load();
  }

  return (
    <section>
      <div className="page-head">
        <h2>Users</h2>
        <form
          onSubmit={(e) => {
            e.preventDefault();
            load();
          }}
        >
          <input
            placeholder="Search email or phone"
            value={q}
            onChange={(e) => setQ(e.target.value)}
          />
          <button type="submit">Search</button>
        </form>
      </div>
      {error && <div className="error">{error}</div>}
      {loading ? (
        <p className="muted">Loading…</p>
      ) : (
        <table className="table">
          <thead>
            <tr>
              <th>Phone</th>
              <th>Email</th>
              <th>Role</th>
              <th>Verified</th>
              <th>Reputation</th>
              <th>State</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {items.map((u) => (
              <tr key={u.id}>
                <td>{u.phone}</td>
                <td>{u.email ?? '—'}</td>
                <td>
                  <span className="tag">{u.role}</span>
                </td>
                <td>{u.verification_status}</td>
                <td>{u.reputation_score}</td>
                <td>
                  {u.is_suspended ? (
                    <span className="badge badge-suspended">suspended</span>
                  ) : (
                    <span className="badge badge-active">active</span>
                  )}
                </td>
                <td className="actions">
                  <button onClick={() => toggleSuspend(u)}>
                    {u.is_suspended ? 'Unsuspend' : 'Suspend'}
                  </button>
                  <button onClick={() => adjustReputation(u)}>Reputation</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </section>
  );
}
