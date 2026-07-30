import { useContext } from "react";
import { AuthContext } from "../context/AuthContext";

/** Access authentication state and actions from anywhere in the tree. */
export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}
