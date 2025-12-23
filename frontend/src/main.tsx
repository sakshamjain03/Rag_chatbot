import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import App from "./App";
import { setAuthToken } from "./api/client";
import { AuthProvider } from "./context/AuthContext";
import "./index.css"

const token = localStorage.getItem("auth_token");
if (token) {
  setAuthToken(token);
}

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <AuthProvider>
      <App />
    </AuthProvider>
  </StrictMode>
);
