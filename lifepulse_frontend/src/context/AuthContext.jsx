import { createContext, useContext, useState, useEffect } from "react";
import { jwtDecode } from "jwt-decode";
import axios from "axios";

const AuthContext = createContext();
const BASE_URL = import.meta.env.VITE_API_BASE_URL;


export const AuthProvider = ({ children }) => {
  const [authTokens, setAuthTokens] = useState(() => {
    const storedTokens = localStorage.getItem("authTokens");
    return storedTokens ? JSON.parse(storedTokens) : null;
  });

  const [user, setUser] = useState(() => {
    const storedTokens = localStorage.getItem("authTokens");
    return storedTokens ? jwtDecode(JSON.parse(storedTokens).access) : null;
  });

  const [loading, setLoading] = useState(true);

  const loginUser = async (username, password) => {
    try {
      const response = await axios.post(`${BASE_URL}/api/token/`, {
        username,
        password,
      });

      if (response.status === 200) {
        const data = response.data;
        setAuthTokens(data);
        setUser(jwtDecode(data.access));
        localStorage.setItem("authTokens", JSON.stringify(data));
        return true;
      }
    } catch (error) {
      console.error("Login failed:", error);
      return false;
    }
  };

  const logoutUser = () => {
    setAuthTokens(null);
    setUser(null);
    localStorage.removeItem("authTokens");
  };

  const refreshToken = async () => {
    try {
      const response = await axios.post(`${BASE_URL}/api/token/refresh/`, {
        refresh: authTokens?.refresh,
      });

      if (response.status === 200) {
        const data = response.data;

        const updatedTokens = {
          access: data.access,
          refresh: authTokens.refresh,
        };

        setAuthTokens(updatedTokens);
        setUser(jwtDecode(data.access));
        localStorage.setItem("authTokens", JSON.stringify(updatedTokens));
      } else {
        logoutUser();
      }
    } catch (err) {
      console.error("Token refresh failed:", err);
      logoutUser();
    }
  };

  useEffect(() => {
    if (authTokens) {
      setUser(jwtDecode(authTokens.access));
    }
    setLoading(false);
  }, []);

  // ⏱ Background token refresh every 4.5 minutes (before 5 min token expiry)
  useEffect(() => {
    if (authTokens) {
      const interval = setInterval(() => {
        refreshToken();
      }, 1000 * 60 * 4.5); // 4.5 minutes

      return () => clearInterval(interval);
    }
  }, [authTokens]);

  const contextData = {
    user,
    authTokens,
    loginUser,
    logoutUser,
  };

  return (
    <AuthContext.Provider value={contextData}>
      {!loading && children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
