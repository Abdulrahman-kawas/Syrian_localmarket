import { useEffect, useState } from 'react';
import { api, type Complaint } from '../api';

export function Complaints() {
  const [items, setItems] = useState<Complaint[]>([]);
  const [status, setStatus] = useState<string>('pending');
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function load() {
    setLoading(true);
    setError(null);
    try {
      const q = status ? `?status=${status}` : '';
      setItems(await api.get<Complaint[]>(`/admin/complaints${q}`));
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Failed to load');
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [status]);

  async function resolve(id: string, newStatus: string) {
    const notes = window.prompt('Admin notes (optional):') ?? undefined;
    await api.put(`/admin/complaints/${id}/resolve`, { status: newStatus, admin_notes: notes });
    await load();
  }

  return (
    <section>
      <div className="page-head">
        <h2>Complaints Queue</h2>
        <select value={status} onChange={(e) => setStatus(e.target.value)}>
          <option value="">All</option>
          <option value="pending">Pending</option>
          <option value="reviewed">Reviewed</option>
          <option value="resolved">Resolved</option>
        </select>
      </div>
      {error && <div className="error">{error}</div>}
      {loading ? (
        <p className="muted">Loading…</p>
      ) : items.length === 0 ? (
        <p className="muted">No complaints.</p>
      ) : (
        <table className="table">
          <thead>
            <tr>
              <th>Created</th>
              <th>Target</th>
              <th>Reason</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {items.map((c) => (
              <tr key={c.id}>
                <td>{new Date(c.created_at).toLocaleString()}</td>
                <td>
                  <span className="tag">{c.target_type}</span>
                  <code>{c.target_id.slice(0, 8)}</code>
                </td>
                <td className="reason">{c.reason}</td>
                <td>
                  <span className={`badge badge-${c.status}`}>{c.status}</span>
                </td>
                <td className="actions">
                  <button onClick={() => resolve(c.id, 'reviewed')}>Reviewed</button>
                  <button onClick={() => resolve(c.id, 'resolved')}>Resolve</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </section>
  );
}
