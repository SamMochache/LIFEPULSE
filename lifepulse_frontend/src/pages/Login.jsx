// src/pages/Login.jsx
import React, { useState, useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import {
  container,
  card,
  heading,
  errorBox,
  successBox,
  input,
  button,
  footerText,
  footerLink,
} from "../styles/loginStyles";

const Login = () => {
  const { loginUser } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const [formData, setFormData] = useState({ username: "", password: "" });
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  useEffect(() => {
    if (location.search.includes("activated=true")) {
      setSuccess("✅ Your account has been successfully activated.");
    }
  }, [location.search]);

  const handleChange = (e) =>
    setFormData({ ...formData, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess("");

    const result = await loginUser(formData.username, formData.password);

    if (result.success) {
      const role = result.user.role;
      if (role === "doctor") {
        navigate("/doctor");
      } else if (role === "admin") {
        navigate("/admin");
      } else {
        navigate("/dashboard");
      }
    } else {
      setError(result.message);
    }
  };

  return (
    <div className={container}>
      <div className={card}>
        <h2 className={heading}>Login to LifePulse</h2>

        {success && <div className={successBox}>{success}</div>}
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
