// src/contexts/AuthContext.jsx
import React, { createContext, useContext, useState, useEffect } from "react";
import axios from "axios";

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [tokens, setTokens] = useState(null);
  const [user, setUser] = useState(null);

  // 1. Настраиваем interceptor один раз
  useEffect(() => {
    const reqInterceptor = axios.interceptors.request.use((config) => {
      if (tokens?.access) {
        config.headers.Authorization = `Bearer ${tokens.access}`;
      }
      return config;
    });
    return () => axios.interceptors.request.eject(reqInterceptor);
  }, [tokens]);

  // 2. Функция логина — сохраняет токены + подгружает профиль
  const loginWithTokens = async ({ access, refresh }) => {
    setTokens({ access, refresh });
    try {
      const { data: me } = await axios.get("/api/auth/users/me/");
      setUser(me);
    } catch {
      setUser(null);
    }
  };

  // 3. Функция выхода
  const logout = () => {
    setTokens(null);
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, tokens, loginWithTokens, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
};
