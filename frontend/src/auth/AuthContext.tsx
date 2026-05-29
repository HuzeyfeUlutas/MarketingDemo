import { createContext, ReactNode, useContext, useEffect, useState } from "react";

import { getMe, login as loginRequest } from "../api/auth";
import { User } from "../types";
import { tokenStorage } from "./tokenStorage";

interface AuthContextValue {
  user: User | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  isAdmin: boolean;
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  // Uygulama açılışında, token varsa kullanıcıyı yükle.
  useEffect(() => {
    if (!tokenStorage.getAccess()) {
      setLoading(false);
      return;
    }
    getMe()
      .then(setUser)
      .catch(() => tokenStorage.clear())
      .finally(() => setLoading(false));
  }, []);

  const login = async (email: string, password: string) => {
    const tokens = await loginRequest(email, password);
    tokenStorage.set(tokens.access_token, tokens.refresh_token);
    setUser(await getMe());
  };

  const logout = () => {
    tokenStorage.clear();
    setUser(null);
  };

  return (
    <AuthContext.Provider
      value={{ user, loading, login, logout, isAdmin: user?.role === "admin" }}
    >
      {children}
    </AuthContext.Provider>
  );
}

// eslint-disable-next-line react-refresh/only-export-components
export function useAuth(): AuthContextValue {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth, AuthProvider içinde kullanılmalıdır");
  return ctx;
}
