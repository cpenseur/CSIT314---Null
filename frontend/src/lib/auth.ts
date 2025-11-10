
import api from "../lib/api";

export const authService = {
  async login(username: string, password: string) {
    const { data } = await api.post('/auth/login/', { username, password });
    localStorage.setItem('access', data.access);
    localStorage.setItem('refresh', data.refresh);
    return data;
  },
  logout() {
    localStorage.removeItem('access');
    localStorage.removeItem('refresh');
  },
};