import { useEffect, useState } from 'react';
import { api, type AdminActionRow } from '../api';

export function Audit() {
  const [items, setItems] = useState<AdminActionRow[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    (async () => {
      setLoading(true);
      try {
        setItems(await api.get<AdminActionRow[]>('/admin/actions'));
      } catch (e) {
        setError(e instanceof Error ? e.message : 'Failed to load');
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  return (
    <section>
      <div className="page-head">
        <h2>Admin Action Audit Log</h2>
      </div>
      {error && <div className="error">{error}</div>}
      {loading ? (
        <p className="muted">Loading…</p>
      ) : items.length === 0 ? (
        <p className="muted">No actions recorded yet.</p>
      ) : (
        <table className="table">
          <thead>
            <tr>
              <th>When</th>
              <th>Action</th>
              <th>Target</th>
              <th>Notes</th>
            </tr>
          </thead>
          <tbody>
            {items.map((a) => (
              <tr key={a.id}>
                <td>{new Date(a.created_at).toLocaleString()}</td>
                <td>
                  <span className="tag">{a.action_type}</span>
                </td>
                <td>
                  <span className="muted">{a.target_type}</span> <code>{a.target_id.slice(0, 8)}</code>
                </td>
                <td>{a.notes ?? '—'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </section>
  );
}
