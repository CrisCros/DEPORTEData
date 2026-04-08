import { createContext, useContext, useEffect, useState, type ReactNode } from 'react';

type AuthContextValue = {
  isAuthenticated: boolean;
  login: (username: string, password: string) => boolean;
  logout: () => void;
};

const AuthContext = createContext<AuthContextValue | null>(null);
const STORAGE_KEY = 'deportedata-admin-auth';

export function AuthProvider({ children }: { children: ReactNode }) {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    setIsAuthenticated(window.localStorage.getItem(STORAGE_KEY) === 'true');
  }, []);

  const value: AuthContextValue = {
    isAuthenticated,
    login: (username, password) => {
      const hasCredentials = username.trim().length > 0 && password.trim().length > 0;
      if (hasCredentials) {
        window.localStorage.setItem(STORAGE_KEY, 'true');
        setIsAuthenticated(true);
      }
      return hasCredentials;
    },
    logout: () => {
      window.localStorage.removeItem(STORAGE_KEY);
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
