import api, { TOKEN_STORAGE_KEY } from "./api";

const USER_STORAGE_KEY = "finance_platform_user";

/**
 * Register a new user.
 * Returns { success, user } or { success: false, error }.
 * Note: registration does NOT log the user in automatically (matches
 * RegisterPage's flow of redirecting to /login afterwards), so we don't
 * persist the token here even though the backend issues one.
 */
export async function register(email, username, password, confirmPassword) {
  try {
    const response = await api.post("/auth/register", {
      email,
      username,
      password,
      confirm_password: confirmPassword,
    });
    return { success: true, user: response.data.user };
  } catch (error) {
    return { success: false, error: error.message };
  }
}

/**
 * Log in a user, persist the user + JWT to localStorage.
 * Returns { success, user } or { success: false, error }.
 */
export async function login(email, password) {
  try {
    const response = await api.post("/auth/login", { email, password });
    const user = response.data.user;
    localStorage.setItem(USER_STORAGE_KEY, JSON.stringify(user));
    if (user.token) {
      localStorage.setItem(TOKEN_STORAGE_KEY, user.token);
    }
    return { success: true, user };
  } catch (error) {
    return { success: false, error: error.message };
  }
}

/** Remove the persisted user + token, ending the session locally. */
export function logout() {
  localStorage.removeItem(USER_STORAGE_KEY);
  localStorage.removeItem(TOKEN_STORAGE_KEY);
}

/** Read the persisted user (if any) from localStorage. */
export function getStoredUser() {
  const raw = localStorage.getItem(USER_STORAGE_KEY);
  if (!raw) return null;
  try {
    return JSON.parse(raw);
  } catch {
    return null;
  }
}

/** Read the persisted JWT (if any) from localStorage. */
export function getToken() {
  return localStorage.getItem(TOKEN_STORAGE_KEY);
}
