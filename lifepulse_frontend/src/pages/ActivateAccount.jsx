import React, { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import axios from "axios";
import {
  container,
  card,
  heading,
  successBox,
  errorBox,
  button,
} from "../styles/activateStyles"; // reuse login styles

const BASE_URL = import.meta.env.VITE_API_BASE_URL;

const ActivateAccount = () => {
  const { uidb64, token } = useParams();
  const [status, setStatus] = useState("loading"); // loading, success, error

  useEffect(() => {
    const verify = async () => {
      try {
        await axios.get(`${BASE_URL}/api/activate/${uidb64}/${token}/`);
        setStatus("success");
      } catch (error) {
        setStatus("error");
      }
    };
    verify();
  }, [uidb64, token]);

  return (
    <div className={container}>
      <div className={card}>
        <h2 className={heading}>Account Activation</h2>
        {status === "loading" && <p>⏳ Verifying your account...</p>}

        {status === "success" && (
          <>
            <div className={successBox}>✅ Your account has been activated!</div>
            <Link to="/login">
              <button className={button}>Go to Login</button>
            </Link>
          </>
        )}

        {status === "error" && (
          <>
            <div className={errorBox}>
              ❌ Invalid or expired activation link.
            </div>
            <Link to="/register">
              <button className={button}>Register Again</button>
            </Link>
          </>
        )}
      </div>
    </div>
  );
};

export default ActivateAccount;
