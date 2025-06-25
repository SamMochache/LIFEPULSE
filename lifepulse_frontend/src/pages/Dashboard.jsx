import React, { useEffect, useState } from "react";
import { useAuth } from "../context/AuthContext";
import axios from "axios";
import {
  LineChart, Line, CartesianGrid, XAxis, YAxis, Tooltip, ResponsiveContainer, Legend,
} from "recharts";
import { useNavigate } from "react-router-dom";
import CSVExport from "../components/CSVExport";
import {
  container,
  headerRow,
  welcomeText,
  addButton,
  cardsGrid,
  card,
  cardTitle,
  cardValue,
  cardUnit,
  chartContainer,
  alertsContainer,
  sectionTitle,
  alertItem,
} from "../styles/dashboardStyles";


const BASE_URL = import.meta.env.VITE_API_BASE_URL;

// ...imports stay the same

const Dashboard = () => {
  const { user, authTokens } = useAuth();
  const [vitals, setVitals] = useState({});
  const [alerts, setAlerts] = useState([]);
  const navigate = useNavigate();

  const config = {
    headers: {
      Authorization: `Bearer ${authTokens?.access}`,
    },
  };

  useEffect(() => {
    const fetchVitals = async () => {
      try {
        const res = await axios.get(`${BASE_URL}/api/health/timeline/`, config);
        setVitals(res.data);
      } catch (err) {
        console.error("Error fetching vitals", err);
      }
    };

    const fetchAlerts = async () => {
      try {
        const res = await axios.get(`${BASE_URL}/api/alerts/`, config);
        setAlerts(res.data);
      } catch (err) {
        console.error("Error fetching alerts", err);
      }
    };

    fetchVitals();
    fetchAlerts();
  }, []);

  const formatChartData = (data, key = "value") =>
    data.map((entry) => ({
      date: entry.date || entry.recorded_at?.split("T")[0],
      value: parseFloat(entry[key]),
      ...entry,
    }));

  const Card = ({ title, value, unit }) => (
    <div className={card}>
      <h4 className={cardTitle}>{title}</h4>
      <p className={cardValue}>
        {value} <span className={cardUnit}>{unit}</span>
      </p>
    </div>
  );

  return (
    <div className={container}>
      <div className={headerRow}>
        <h1 className={welcomeText}>
          Welcome, {user?.username || "User"} 👋
        </h1>
        <button onClick={() => navigate("/vitals")} className={addButton}>
          + Add Vital
        </button>
      </div>

      <div className={cardsGrid}>
        <Card title="Heart Rate" value={vitals?.heart_rate?.slice(-1)[0]?.bpm || "--"} unit="bpm" />
        <Card
          title="Blood Pressure"
          value={
            vitals?.blood_pressure?.slice(-1)[0]
              ? `${vitals?.blood_pressure?.slice(-1)[0].systolic}/${vitals?.blood_pressure?.slice(-1)[0].diastolic}`
              : "--"
          }
          unit="mmHg"
        />
        <Card title="SpO2" value={vitals?.spo2?.slice(-1)[0]?.value || "--"} unit="%" />
        <Card title="Sleep" value={vitals?.sleep?.slice(-1)[0]?.duration || "--"} unit="hrs" />
      </div>

      <div className={chartContainer}>
        <h2 className={sectionTitle}>Heart Rate Trend</h2>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={formatChartData(vitals?.heart_rate || [], "bpm")}>
            <Line type="monotone" dataKey="value" stroke="#ef4444" />
            <CartesianGrid stroke="#ccc" />
            <XAxis dataKey="date" />
            <YAxis domain={["auto", "auto"]} />
            <Tooltip />
            <Legend />
          </LineChart>
        </ResponsiveContainer>
      </div>

      <div className={alertsContainer}>
        <h2 className={sectionTitle}>Recent Alerts</h2>
        {alerts.length > 0 ? (
          <ul className="space-y-2">
            {alerts.map((alert, idx) => (
              <li key={idx} className={alertItem}>
                [{alert.vital_type.toUpperCase()}] {alert.message}
              </li>
            ))}
          </ul>
        ) : (
          <p className="text-gray-500 text-sm">No alerts to show.</p>
        )}
      </div>

      <CSVExport />
    </div>
  );
};

export default Dashboard;
