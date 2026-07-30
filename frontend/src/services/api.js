import axios from "axios";

// Centralized Axios instance used by every service module.
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

export const TOKEN_STORAGE_KEY = "finance_platform_token";
const USER_STORAGE_KEY = "finance_platform_user";

// Request interceptor -- attaches the JWT issued at login, if we have one.
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem(TOKEN_STORAGE_KEY);
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor -- normalizes errors so every caller gets a plain
// string message instead of having to dig through the Axios error shape.
// A 401 means the token is missing/invalid/expired: clear the stale session
// so the next render sends the user back to the login screen instead of
// looping on broken requests.
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem(TOKEN_STORAGE_KEY);
      localStorage.removeItem(USER_STORAGE_KEY);
    }

    const message =
      error.response?.data?.error ||
      error.message ||
      "Something went wrong. Please try again.";
    return Promise.reject(new Error(message));
  }
);

export default api;
