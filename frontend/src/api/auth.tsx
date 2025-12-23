import { api, setAuthToken } from "./client";

export async function login(username: string, password: string) {
  const res = await api.post("/auth/login/", { username, password });
  setAuthToken(res.data.token);
  return res.data;
}

export async function register(username: string, password: string) {
  const res = await api.post("/auth/register/", { username, password });
  setAuthToken(res.data.token);
  return res.data;
}

export function logout() {
  setAuthToken(null);
}
