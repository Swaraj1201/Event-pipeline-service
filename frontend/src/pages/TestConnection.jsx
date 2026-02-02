import { useEffect, useState } from "react";
import apiClient from "../api/client";
import Loader from "../components/Loader";
import ErrorMessage from "../components/ErrorMessage";

const TestConnection = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    apiClient
      .get("/health")
      .then(() => setLoading(false))
      .catch(() => {
        setError("Backend unavailable");
        setLoading(false);
      });
  }, []);

  if (loading) return <Loader />;
  if (error) return <ErrorMessage message={error} />;

  return <h2>Backend connected ✅</h2>;
};

export default TestConnection;
