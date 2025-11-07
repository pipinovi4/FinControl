export const API = process.env.NEXT_PUBLIC_API_URL ?? "";

export const api = (path: string) =>
  path.startsWith("/") ? `${API}${path}` : `${API}/${path}`;
