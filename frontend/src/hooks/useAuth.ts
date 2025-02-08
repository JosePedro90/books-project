import { useState, useEffect } from "react";

const useAuth = () => {
  const [accessToken, setAccessToken] = useState<string | null>(null);
  const [refreshToken, setRefreshToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true); // Add isLoading state

  useEffect(() => {
    const loadTokens = async () => {
      try {
        const access = localStorage.getItem("access");
        const refresh = localStorage.getItem("refresh");
        if (access && refresh) {
          setAccessToken(access);
          setRefreshToken(refresh);
        }
      } finally {
        setIsLoading(false);
      }
    };

    loadTokens();
  }, []);

  const saveTokens = (access: string, refresh: string) => {
    localStorage.setItem("access", access);
    localStorage.setItem("refresh", refresh);
    setAccessToken(access);
    setRefreshToken(refresh);
  };

  const logout = () => {
    localStorage.removeItem("access");
    localStorage.removeItem("refresh");
    setAccessToken(null);
    setRefreshToken(null);
  };

  return { accessToken, refreshToken, saveTokens, logout, isLoading }; // Return isLoading
};

export default useAuth;
