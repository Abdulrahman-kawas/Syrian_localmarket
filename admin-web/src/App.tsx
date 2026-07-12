import { Navigate, Route, Routes, NavLink } from 'react-router-dom';
import { useAuth } from './auth';
import { Login } from './pages/Login';
import { Complaints } from './pages/Complaints';
import { Users } from './pages/Users';
import { Audit } from './pages/Audit';
import type { ReactNode } from 'react';

function RequireAuth({ children }: { children: ReactNode }) {
  const { isAuthed } = useAuth();
  return isAuthed ? <>{children}</> : <Navigate to="/login" replace />;
}

function Shell({ children }: { children: ReactNode }) {
  const { logout } = useAuth();
  return (
    <div className="shell">
      <header className="topbar">
        <span className="brand">LocalMarket Admin</span>
        <nav>
          <NavLink to="/complaints">Complaints</NavLink>
          <NavLink to="/users">Users</NavLink>
          <NavLink to="/audit">Audit Log</NavLink>
        </nav>
        <button className="linkbtn" onClick={logout}>
          Sign out
        </button>
      </header>
      <main className="content">{children}</main>
    </div>
  );
}

export function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route
        path="/complaints"
        element={
          <RequireAuth>
            <Shell>
              <Complaints />
            </Shell>
          </RequireAuth>
        }
      />
      <Route
        path="/users"
        element={
          <RequireAuth>
            <Shell>
              <Users />
            </Shell>
          </RequireAuth>
        }
      />
      <Route
        path="/audit"
        element={
          <RequireAuth>
            <Shell>
              <Audit />
            </Shell>
          </RequireAuth>
        }
      />
      <Route path="*" element={<Navigate to="/complaints" replace />} />
    </Routes>
  );
}
