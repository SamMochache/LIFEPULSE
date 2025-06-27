import React from "react";
import { useNavigate } from "react-router-dom";
import {
  container,
  card,
  heading,
  successBox,
  button,
} from "../styles/activateStyles"; // reuse styles

const CheckEmail = () => {
  const navigate = useNavigate();

  return (
    <div className={container}>
      <div className={card}>
        <h2 className={heading}>Verify Your Email</h2>
        <div className={successBox}>
          🎉 You're almost there! <br />
          We've sent a confirmation link to your email address. <br />
          Click the link to activate your account.
        </div>
        <button className={button} onClick={() => navigate("/login")}>
          Go to Login
        </button>
      </div>
    </div>
  );
};

export default CheckEmail;
