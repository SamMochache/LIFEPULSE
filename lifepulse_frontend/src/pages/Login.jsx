import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import {
  container,
  card,
  heading,
  errorBox,
  input,
  button,
  footerText,
  footerLink,
} from "../styles/loginStyles"; // Adjust path if needed

const Login = () => {
  const { loginUser, user } = useAuth();
  const navigate = useNavigate();
  const [formData, setFormData] = useState({ username: "", password: "" });
  const [error, setError] = useState("");

  const handleChange = (e) =>
    setFormData({ ...formData, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    const success = await loginUser(formData.username, formData.password);
    if (success) {
      // Optional: Redirect based on role
      if (user?.role === "doctor") {
        navigate("/doctor");
      } else if (user?.role === "admin") {
        navigate("/admin");
      } else {
        navigate("/dashboard");
      }
    } else {
      setError("Invalid username or password");
    }
  };

  return (
    <div className={container}>
      <div className={card}>
        <h2 className={heading}>Login to LifePulse</h2>
        {error && <div className={errorBox}>{error}</div>}
        <form onSubmit={handleSubmit} className="space-y-4">
          <input
            type="text"
            name="username"
            value={formData.username}
            onChange={handleChange}
            placeholder="Username"
            className={input}
            required
          />
          <input
            type="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            placeholder="Password"
            className={input}
            required
          />
          <button type="submit" className={button}>
            Login
          </button>
        </form>
        <p className={footerText}>
          Don’t have an account?{" "}
          <span className={footerLink} onClick={() => navigate("/register")}>
            Register
          </span>
        </p>
      </div>
    </div>
  );
};

export default Login;
