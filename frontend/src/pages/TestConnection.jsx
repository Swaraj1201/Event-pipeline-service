import { useEffect, useState } from "react";
import apiClient from "../api/client";

const TestConnection = () => {
  const [status, setStatus] = useState("Checking...");

  useEffect(() => {
    apiClient
      .get("/health")
      .then(() => setStatus("Backend connected ✅"))
      .catch(() => setStatus("Backend connection failed ❌"));
  }, []);

  return <h2>{status}</h2>;
};

export default TestConnection;
