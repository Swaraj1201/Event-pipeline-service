import { createContext, useContext, useState } from "react";

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [token, setToken] = useState(
    () => sessionStorage.getItem("token")
  );
  const [role, setRole] = useState(
    () => sessionStorage.getItem("role")
  );

  const login = (accessToken, userRole) => {
    sessionStorage.setItem("token", accessToken);
    sessionStorage.setItem("role", userRole);
    setToken(accessToken);
    setRole(userRole);
  };

  const logout = () => {
    sessionStorage.clear();
    setToken(null);
    setRole(null);
  };

  return (
    <AuthContext.Provider value={{ token, role, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
