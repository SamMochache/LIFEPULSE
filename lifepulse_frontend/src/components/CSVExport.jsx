import React from "react";
import { useAuth } from "../context/AuthContext";
import axios from "axios";
import {
  container,
  title,
  grid,
  button,
} from "../styles/csvExport";

const BASE_URL = import.meta.env.VITE_API_BASE_URL;

const EXPORT_TYPES = [
  { type: "heart_rate", label: "Heart Rate" },
  { type: "blood_pressure", label: "Blood Pressure" },
  { type: "blood_sugar", label: "Blood Sugar" },
  { type: "sleep", label: "Sleep" },
  { type: "steps", label: "Steps" },
  { type: "weight", label: "Weight" },
  { type: "spo2", label: "SpO₂" },
  { type: "body_temperature", label: "Body Temp" },
];

const CSVExport = () => {
  const { authTokens } = useAuth();

  const handleExport = async (type) => {
    try {
      const response = await axios.get(`${BASE_URL}/api/export/${type}/`, {
        headers: {
          Authorization: `Bearer ${authTokens.access}`,
        },
        responseType: "blob",
      });

      const blob = new Blob([response.data], { type: "text/csv" });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", `${type}_export_${Date.now()}.csv`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (error) {
      console.error("Failed to export CSV:", error);
      alert("Export failed. Please try again.");
    }
  };

  return (
    <div className={container}>
      <h3 className={title}>📥 Export Your Vitals</h3>
      <div className={grid}>
        {EXPORT_TYPES.map(({ type, label }) => (
          <button
            key={type}
            onClick={() => handleExport(type)}
            className={button}
          >
            {label}
          </button>
        ))}
      </div>
    </div>
  );
};

export default CSVExport;
