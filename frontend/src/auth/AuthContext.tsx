import { createContext, useContext, useEffect, useState, type ReactNode } from 'react';
import { authApi } from '../services/api';

type AuthContextValue = {
  isAuthenticated: boolean;
  login: (username: string, password: string) => Promise<boolean>;
  logout: () => void;
};

const AuthContext = createContext<AuthContextValue | null>(null);
const STORAGE_AUTH_KEY = 'deportedata-admin-auth';
const STORAGE_TOKEN_KEY = 'deportedata-admin-token';

export function AuthProvider({ children }: { children: ReactNode }) {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    const hasAuthFlag = window.localStorage.getItem(STORAGE_AUTH_KEY) === 'true';
    const hasToken = Boolean(window.localStorage.getItem(STORAGE_TOKEN_KEY));
    setIsAuthenticated(hasAuthFlag && hasToken);
  }, []);

  const value: AuthContextValue = {
    isAuthenticated,
    login: async (username, password) => {
      const hasCredentials = username.trim().length > 0 && password.trim().length > 0;
      if (!hasCredentials) {
        return false;
      }

      const response = await authApi.login(username.trim(), password);
      window.localStorage.setItem(STORAGE_AUTH_KEY, 'true');
      window.localStorage.setItem(STORAGE_TOKEN_KEY, response.token);
      setIsAuthenticated(true);
      return true;
    },
    logout: () => {
      window.localStorage.removeItem(STORAGE_AUTH_KEY);
      window.localStorage.removeItem(STORAGE_TOKEN_KEY);
      setIsAuthenticated(false);
    },
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);

  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }

  return context;
}
