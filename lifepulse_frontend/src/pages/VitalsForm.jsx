import React, { useState } from "react";
import axios from "axios";
import { useAuth } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";
import {
  container,
  form,
  formTitle,
  select,
  input,
  submitButton,
  message,
} from "../styles/vitalsForm";

const BASE_URL = import.meta.env.VITE_API_BASE_URL;

const VITAL_OPTIONS = [
  "heart_rate",
  "blood_pressure",
  "blood_sugar",
  "spo2",
  "body_temperature",
  "sleep",
  "weight",
];

const API_ENDPOINTS = {
  heart_rate: "heartrate",
  blood_pressure: "bloodpressure",
  blood_sugar: "bloodsugar",
  spo2: "spo2",
  body_temperature: "temperature",
  sleep: "sleep",
  weight: "weight",
};

const VitalsForm = () => {
  const { authTokens } = useAuth();
  const navigate = useNavigate();
  const [vitalType, setVitalType] = useState("");
  const [formData, setFormData] = useState({});
  const [msg, setMsg] = useState("");

  const config = {
    headers: {
      Authorization: `Bearer ${authTokens?.access}`,
    },
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const endpoint = `${BASE_URL}/api/health/${API_ENDPOINTS[vitalType]}/`;
      await axios.post(endpoint, formData, config);
      setMsg("✅ Vital submitted successfully!");
      setFormData({});
      setTimeout(() => navigate("/dashboard"), 1200);
    } catch (err) {
      console.error(err);
      setMsg("❌ Error submitting vital. Check inputs or try again.");
    }
  };

  const handleChange = (e) =>
    setFormData({ ...formData, [e.target.name]: e.target.value });

  const renderFields = () => {
  switch (vitalType) {
    case "heart_rate":
      return (
        <>
          <input
            type="date"
            name="date"
            value={formData.date || ""}
            onChange={handleChange}
            required
            className={input}
          />
          <input
            type="number"
            name="resting_hr"
            value={formData.resting_hr || ""}
            onChange={handleChange}
            placeholder="Resting HR"
            required
            className={input}
          />
          <input
            type="number"
            name="high_hr"
            value={formData.high_hr || ""}
            onChange={handleChange}
            placeholder="High HR"
            required
            className={input}
          />
          <input
            type="number"
            name="low_hr"
            value={formData.low_hr || ""}
            onChange={handleChange}
            placeholder="Low HR"
            required
            className={input}
          />
        </>
      );

    case "blood_pressure":
      return (
        <>
          <input
            type="date"
            name="date"
            value={formData.date || ""}
            onChange={handleChange}
            required
            className={input}
          />
          <input
            type="number"
            name="systolic"
            value={formData.systolic || ""}
            onChange={handleChange}
            placeholder="Systolic"
            required
            className={input}
          />
          <input
            type="number"
            name="diastolic"
            value={formData.diastolic || ""}
            onChange={handleChange}
            placeholder="Diastolic"
            required
            className={input}
          />
          <input
            type="number"
            name="pulse"
            value={formData.pulse || ""}
            onChange={handleChange}
            placeholder="Pulse"
            required
            className={input}
          />
        </>
      );

    case "blood_sugar":
      return (
        <>
          <input
            type="date"
            name="date"
            value={formData.date || ""}
            onChange={handleChange}
            required
            className={input}
          />
          <input
            type="number"
            name="fasting"
            value={formData.fasting || ""}
            onChange={handleChange}
            placeholder="Fasting"
            required
            className={input}
          />
          <input
            type="number"
            name="post_meal"
            value={formData.post_meal || ""}
            onChange={handleChange}
            placeholder="Post Meal"
            required
            className={input}
          />
        </>
      );

    case "spo2":
  return (
    <>
      <input
        type="date"
        name="date"
        value={formData.date || ""}
        onChange={handleChange}
        required
        className={input}
      />
      <input
        type="number"
        name="spo2"
        value={formData.spo2 || ""}
        onChange={handleChange}
        placeholder="SpO₂ (%)"
        required
        className={input}
      />
    </>
  );


    case "body_temperature":
  return (
    <>
      <input
        type="date"
        name="date"
        value={formData.date || ""}
        onChange={handleChange}
        required
        className={input}
      />
      <input
        type="number"
        name="temperature"
        value={formData.temperature || ""}
        onChange={handleChange}
        placeholder="Temperature (°C)"
        required
        className={input}
      />
    </>
  );


    case "sleep":
      return (
        <>
          <input
            type="date"
            name="date"
            value={formData.date || ""}
            onChange={handleChange}
            required
            className={input}
          />
          <input
            type="number"
            name="hours_slept"
            value={formData.hours_slept || ""}
            onChange={handleChange}
            placeholder="Hours Slept"
            required
            className={input}
          />
          <select
            name="sleep_quality"
            value={formData.sleep_quality || ""}
            onChange={handleChange}
            required
            className={input}
          >
            <option value="">-- Sleep Quality --</option>
            <option value="poor">Poor</option>
            <option value="average">Average</option>
            <option value="good">Good</option>
          </select>
        </>
      );

    case "weight":
      return (
        <>
          <input
            type="date"
            name="date"
            value={formData.date || ""}
            onChange={handleChange}
            required
            className={input}
          />
          <input
            type="number"
            name="weight_kg"
            value={formData.weight_kg || ""}
            onChange={handleChange}
            placeholder="Weight (kg)"
            required
            className={input}
          />
        </>
      );

    default:
      return null;
  }
};


  return (
    <div className={container}>
      <form onSubmit={handleSubmit} className={form}>
        <h2 className={formTitle}>Add New Vital</h2>

        <select
          name="vitalType"
          value={vitalType}
          onChange={(e) => {
            setFormData({});
            setVitalType(e.target.value);
            setMsg("");
          }}
          required
          className={select}
        >
          <option value="">-- Select Vital Type --</option>
          {VITAL_OPTIONS.map((v) => (
            <option key={v} value={v}>
              {v.replace("_", " ").toUpperCase()}
            </option>
          ))}
        </select>

        {renderFields()}

        <button type="submit" className={submitButton}>
          Submit
        </button>

        {msg && <p className={message}>{msg}</p>}
      </form>
    </div>
  );
};

export default VitalsForm;
