import React from "react";
import { useNavigate } from "react-router-dom";
import {
  container,
  card,
  heading,
  subtext,
  button,
} from "../styles/homeStyles"; // ✅ import reusable styles

const Home = () => {
  const navigate = useNavigate();

  return (
    <div className={container}>
      <div className={card}>
        <h1 className={heading}>🌿 LifePulse</h1>
        <p className={subtext}>Your Intelligent Health Companion</p>
        <button onClick={() => navigate("/register")} className={button}>
          Get Started
        </button>
      </div>
    </div>
  );
};

export default Home;
