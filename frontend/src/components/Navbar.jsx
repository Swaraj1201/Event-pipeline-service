import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

const Navbar = () => {
  const { role, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <nav>
      <span>Role: {role}</span>
      <button onClick={handleLogout}>Logout</button>
    </nav>
  );
};

export default Navbar;
