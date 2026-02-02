import axios from "axios";

const apiClient = axios.create({
  baseURL: "http://localhost:8000/api/v1",
  headers: { "Content-Type": "application/json" },
});

apiClient.interceptors.request.use((config) => {
  const token = sessionStorage.getItem("token");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (!error.response) {
      // Network error - let components handle it gracefully
      // Don't show alert for login endpoint
      const isLoginEndpoint = error.config?.url?.includes("/auth/login");
      if (!isLoginEndpoint) {
        alert("Network error. Please try again.");
      }
      return Promise.reject(error);
    }

    const { status, config } = error.response;
    const isLoginEndpoint = config?.url?.includes("/auth/login");

    // Don't handle 401 on login endpoint - let the component handle it
    if (status === 401 && !isLoginEndpoint) {
      sessionStorage.clear();
      window.location.href = "/login";
    }

    // Don't show alerts for login endpoint errors - let component handle them
    if (isLoginEndpoint) {
      return Promise.reject(error);
    }

    if (status === 403) {
      alert("You do not have permission to perform this action.");
    }

    if (status === 429) {
      alert("Too many requests. Please slow down.");
    }

    return Promise.reject(error);
  }
);

export default apiClient;
