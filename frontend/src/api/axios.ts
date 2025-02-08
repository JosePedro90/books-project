import axios from "axios";
import { refreshAccessToken } from "./auth";

export const API_BASE_URL = "http://localhost:8000"; //TODO: Make this an environment variable

const api = axios.create({
  baseURL: API_BASE_URL,
});

// Add request interceptor to inject access token
api.interceptors.request.use(
  (config) => {
    const accessToken = localStorage.getItem("access");
    if (accessToken) {
      config.headers.Authorization = `Bearer ${accessToken}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Add response interceptor to handle token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // If 401 and not a refresh request
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = localStorage.getItem("refresh");
        if (!refreshToken) throw new Error("No refresh token");

        const { access } = await refreshAccessToken(refreshToken);
        localStorage.setItem("access", access);

        // Retry original request with new token
        originalRequest.headers.Authorization = `Bearer ${access}`;
        return api(originalRequest);
      } catch (refreshError) {
        localStorage.removeItem("access");
        localStorage.removeItem("refresh");
        //TODO: Redirect to login, or not if using ProtectedRoute
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

export default api;
