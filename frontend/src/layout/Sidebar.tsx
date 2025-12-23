import { useNavigate } from "react-router-dom";

export default function Sidebar() {
  const navigate = useNavigate();

  function logout() {
    localStorage.removeItem("auth_token");
    navigate("/login");
    window.location.reload();
  }

  return (
    <div className="w-64 bg-gray-900 text-white flex flex-col p-4">
      <h1 className="text-xl font-bold mb-6">FileChat RAG</h1>

      <button
        className="mb-2 text-left hover:bg-gray-800 p-2 rounded"
        onClick={() => navigate("/")}
      >
        Chat
      </button>

      <div className="mt-auto">
        <button
          onClick={logout}
          className="w-full bg-red-600 hover:bg-red-700 p-2 rounded"
        >
          Logout
        </button>
      </div>
    </div>
  );
}
