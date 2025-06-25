import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import {
  container,
  form,
  heading,
  errorMessage,
  input,
  select,
  button,
  footerText,
  loginLink,
} from "../styles/registerStyles"; // adjust path if needed

const BASE_URL = import.meta.env.VITE_API_BASE_URL;


const Register = () => {
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
    confirmPassword: "",
    role: "user",
  });

  const [error, setError] = useState("");

  const handleChange = (e) => {
    setFormData((prev) => ({
      ...prev,
      [e.target.name]: e.target.value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    if (formData.password !== formData.confirmPassword) {
      setError("Passwords do not match");
      return;
    }

    try {
      const response = await axios.post(`${BASE_URL}/api/health/register/`, {
        username: formData.username,
        email: formData.email,
        password: formData.password,
        role: formData.role,
      });

      if (response.status === 201 || response.status === 200) {
        navigate("/login");
      }
    } catch (err) {
      console.error(err);
      setError("Registration failed. Check your input.");
    }
  };

  return (
    <div className={container}>
      <form onSubmit={handleSubmit} className={form}>
        <h2 className={heading}>Register</h2>

        {error && <div className={errorMessage}>{error}</div>}

        <input
          type="text"
          name="username"
          placeholder="Username"
          className={input}
          value={formData.username}
          onChange={handleChange}
          required
        />

        <input
          type="email"
          name="email"
          placeholder="Email"
          className={input}
          value={formData.email}
          onChange={handleChange}
          required
        />

        <input
          type="password"
          name="password"
          placeholder="Password"
          className={input}
          value={formData.password}
          onChange={handleChange}
          required
        />

        <input
          type="password"
          name="confirmPassword"
          placeholder="Confirm Password"
          className={input}
          value={formData.confirmPassword}
          onChange={handleChange}
          required
        />

        <select
          name="role"
          className={select}
          value={formData.role}
          onChange={handleChange}
        >
          <option value="user">User</option>
          <option value="doctor">Doctor</option>
        </select>

        <button type="submit" className={button}>
          Create Account
        </button>

        <p className={footerText}>
          Already have an account?{" "}
          <span className={loginLink} onClick={() => navigate("/login")}>
            Login
          </span>
        </p>
      </form>
    </div>
  );
};

export default Register;
