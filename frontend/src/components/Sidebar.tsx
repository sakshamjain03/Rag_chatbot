import { useAuth } from "../context/AuthContext";
import "./Sidebar.css";

export default function Sidebar() {
  const { logout } = useAuth();

  return (
    <aside className="sidebar">
      <h2 className="logo">RAG Chat</h2>

      <nav>
        <button className="nav-btn">Chat</button>
        <button className="nav-btn" onClick={logout}>
          Logout
        </button>
      </nav>
    </aside>
  );
}
