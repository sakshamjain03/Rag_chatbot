import { api } from "./client";

export const loginUser = async (email: string, password: string) => {
  const res = await api.post("/auth/login/", { email, password });
  return res.data; // { token }
};

export const registerUser = async (email: string, password: string) => {
  const res = await api.post("/auth/register/", { email, password });
  return res.data; // { token }
};
