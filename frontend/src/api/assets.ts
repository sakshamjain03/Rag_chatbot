import { api } from "./client";

export const deleteAsset = (id: string) => api.delete(`/assets/${id}/`);
export const renameAsset = (id: string, name: string) =>
  api.patch(`/assets/${id}/update/`, { original_name: name });
