import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import apiClient from "../api/client";
import { useAuth } from "../context/AuthContext";
import ErrorMessage from "../components/ErrorMessage";

const Login = () => {
  const { login, token } = useAuth();
  const navigate = useNavigate();
  
  // Redirect if already logged in
  useEffect(() => {
    if (token) {
      navigate("/");
    }
  }, [token, navigate]);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      const res = await apiClient.post("/auth/login", {
        username,
        password,
      });
      // Decode JWT to extract role from token payload
      const tokenParts = res.data.access_token.split(".");
      const payload = JSON.parse(atob(tokenParts[1]));
      const userRole = payload.role || "unknown";
      login(res.data.access_token, userRole);
      // Navigate to home page after successful login
      navigate("/");
    } catch (err) {
      // Handle network errors and API errors gracefully
      if (!err.response) {
        setError("Network error. Please check if the backend server is running.");
      } else if (err.response.status === 401) {
        setError("Invalid username or password");
      } else {
        setError(err.response?.data?.detail || "An error occurred. Please try again.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Login</h2>
      {error && <ErrorMessage message={error} />}
      <input
        placeholder="Username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        disabled={loading}
      />
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        disabled={loading}
      />
      <button type="submit" disabled={loading}>
        {loading ? "Logging in..." : "Login"}
      </button>
    </form>
  );
};

export default Login;
