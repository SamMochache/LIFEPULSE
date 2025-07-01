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
  { type: "temperature", label: "Body Temp" },
];

const ReportExport = () => {
  const { authTokens } = useAuth();

  const config = {
    headers: {
      Authorization: `Bearer ${authTokens.access}`,
    },
    responseType: "blob",
  };

  const handleExportCSV = async (type) => {
    try {
      const response = await axios.get(`${BASE_URL}/api/health/export/?vital=${type}`, config);
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
      alert("CSV export failed. Please try again.");
    }
  };

  const handleExportPDF = async () => {
    try {
      const response = await axios.get(`${BASE_URL}/api/health/export/pdf/`, config);
      const blob = new Blob([response.data], { type: "application/pdf" });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", `health_report_${Date.now()}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (error) {
      console.error("Failed to export PDF:", error);
      alert("PDF export failed. Please try again.");
    }
  };

  return (
    <div className={container}>
      <h3 className={title}>📥 Export Your Vitals</h3>
      <div className={grid}>
        {EXPORT_TYPES.map(({ type, label }) => (
          <button key={type} onClick={() => handleExportCSV(type)} className={button}>
            {label} (CSV)
          </button>
        ))}
        <button onClick={handleExportPDF} className={`${button} bg-orange-600 text-white`}>
          📄 Full PDF Report
        </button>
      </div>
    </div>
  );
};

export default ReportExport;
