import { useAuth } from "../hooks/useAuth";

export default function Navbar({ onToggleSidebar }) {
  const { user, logout } = useAuth();

  return (
    <header className="navbar">
      <div className="navbar-left">
        <button
          type="button"
          className="navbar-menu-btn"
          onClick={onToggleSidebar}
          aria-label="Toggle navigation"
        >
          <span />
          <span />
          <span />
        </button>
        <span className="navbar-title">Personal Finance</span>
      </div>

      <div className="navbar-right">
        {user && <span className="navbar-username">{user.username}</span>}
        <button type="button" className="btn btn-ghost" onClick={logout}>
          Log out
        </button>
      </div>
    </header>
  );
}
