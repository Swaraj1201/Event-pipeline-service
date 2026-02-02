import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import apiClient from "../api/client";
import { useAuth } from "../context/AuthContext";

const TestConnection = () => {
  const { token, logout } = useAuth();
  const navigate = useNavigate();
  const [status, setStatus] = useState("Checking...");

  useEffect(() => {
    if (!token) {
      navigate("/login");
      return;
    }
    apiClient
      .get("/health")
      .then(() => setStatus("Backend connected ✅"))
      .catch(() => setStatus("Backend connection failed ❌"));
  }, [token, navigate]);

  return (
    <div>
      <h2>{status}</h2>
      <button onClick={logout}>Logout</button>
    </div>
  );
};

export default TestConnection;
