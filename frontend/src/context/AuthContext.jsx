import { createContext, useEffect, useState } from "react";
import * as authService from "../services/auth";

export const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  // Restore session from localStorage on first load
  useEffect(() => {
    const storedUser = authService.getStoredUser();
    setUser(storedUser);
    setIsLoading(false);
  }, []);

  async function login(email, password) {
    const result = await authService.login(email, password);
    if (result.success) {
      setUser(result.user);
    }
    return result;
  }

  async function register(email, username, password, confirmPassword) {
    return authService.register(email, username, password, confirmPassword);
  }

  function logout() {
    authService.logout();
    setUser(null);
  }

  const value = {
    user,
    isAuthenticated: Boolean(user),
    isLoading,
    login,
    register,
    logout,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
