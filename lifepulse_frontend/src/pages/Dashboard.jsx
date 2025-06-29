import React, { useEffect, useState } from "react";
import { useAuth } from "../context/AuthContext";
import axios from "axios";
import {
  LineChart,
  Line,
  CartesianGrid,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from "recharts";
import { useNavigate } from "react-router-dom";
import CSVExport from "../components/CSVExport";
import { useSwipeable } from "react-swipeable";
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

const Dashboard = () => {
  const { user, authTokens } = useAuth();
  const [timelineData, setTimelineData] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [selectedChart, setSelectedChart] = useState("heart");
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
        setTimelineData(res.data);
      } catch (err) {
        console.error("Error fetching vitals", err);
      }
    };

    const fetchAlerts = async () => {
      try {
        const res = await axios.get(`${BASE_URL}/api/health/alerts/`, config);
        setAlerts(res.data);
      } catch (err) {
        console.error("Error fetching alerts", err);
      }
    };

    fetchVitals();
    fetchAlerts();
  }, []);

  const formatChartData = (data, key = "value") =>
    data
      .map((entry) => ({
        date: entry.date,
        value: parseFloat(entry[key]),
      }))
      .filter((d) => !isNaN(d.value));

  const latest = timelineData.slice(-1)[0] || {};

  const Card = ({ title, value, unit }) => (
    <div className={card}>
      <h4 className={cardTitle}>{title}</h4>
      <p className={cardValue}>
        {value} <span className={cardUnit}>{unit}</span>
      </p>
    </div>
  );

  const chartTabs = [
    { key: "heart", label: "Heart Rate" },
    { key: "bp", label: "Blood Pressure" },
    { key: "spo2", label: "SpO2" },
    { key: "sleep", label: "Sleep" },
    { key: "weight", label: "Weight" },
    { key: "temperature", label: "Body Temp" },
    { key: "sugar", label: "Blood Sugar" },
  ];

  const swipeHandlers = useSwipeable({
    onSwipedLeft: () => {
      const idx = chartTabs.findIndex((tab) => tab.key === selectedChart);
      if (idx < chartTabs.length - 1) setSelectedChart(chartTabs[idx + 1].key);
    },
    onSwipedRight: () => {
      const idx = chartTabs.findIndex((tab) => tab.key === selectedChart);
      if (idx > 0) setSelectedChart(chartTabs[idx - 1].key);
    },
  });

  const renderChart = () => {
    switch (selectedChart) {
      case "heart":
        return (
          <LineChart data={formatChartData(timelineData, "heart_rate")}>
            <Line type="monotone" dataKey="value" stroke="#ef4444" name="Heart Rate (bpm)" />
            <CartesianGrid stroke="#ccc" />
            <XAxis dataKey="date" />
            <YAxis />
            <Tooltip />
            <Legend />
          </LineChart>
        );

      case "bp":
        return (
          <LineChart
            data={timelineData
              .map((entry) => ({
                date: entry.date,
                systolic: parseFloat(entry.bp_systolic),
                diastolic: parseFloat(entry.bp_diastolic),
              }))
              .filter((d) => !isNaN(d.systolic) && !isNaN(d.diastolic))}
          >
            <Line type="monotone" dataKey="systolic" stroke="#10b981" name="Systolic (mmHg)" />
            <Line type="monotone" dataKey="diastolic" stroke="#6366f1" name="Diastolic (mmHg)" />
            <CartesianGrid stroke="#ccc" />
            <XAxis dataKey="date" />
            <YAxis />
            <Tooltip />
            <Legend />
          </LineChart>
        );

      case "spo2":
        return (
          <LineChart data={formatChartData(timelineData, "spo2")}>
            <Line type="monotone" dataKey="value" stroke="#3b82f6" name="SpO2 (%)" />
            <CartesianGrid stroke="#ccc" />
            <XAxis dataKey="date" />
            <YAxis />
            <Tooltip />
            <Legend />
          </LineChart>
        );

      case "sleep":
        return (
          <LineChart data={formatChartData(timelineData, "sleep_hours")}>
            <Line type="monotone" dataKey="value" stroke="#f59e0b" name="Sleep (hrs)" />
            <CartesianGrid stroke="#ccc" />
            <XAxis dataKey="date" />
            <YAxis />
            <Tooltip />
            <Legend />
          </LineChart>
        );

      case "weight":
        return (
          <LineChart data={formatChartData(timelineData, "weight")}>
            <Line type="monotone" dataKey="value" stroke="#a855f7" name="Weight (kg)" />
            <CartesianGrid stroke="#ccc" />
            <XAxis dataKey="date" />
            <YAxis />
            <Tooltip />
            <Legend />
          </LineChart>
        );

      case "temperature":
        return (
          <LineChart data={formatChartData(timelineData, "temperature")}>
            <Line type="monotone" dataKey="value" stroke="#f43f5e" name="Temperature (°C)" />
            <CartesianGrid stroke="#ccc" />
            <XAxis dataKey="date" />
            <YAxis />
            <Tooltip />
            <Legend />
          </LineChart>
        );

      case "sugar":
  return (
    <LineChart
      data={timelineData
        .map((entry) => ({
          date: entry.date,
          fasting: parseFloat(entry.blood_sugar),
          post_meal: parseFloat(entry.post_meal),
        }))
        .filter((d) => !isNaN(d.fasting) || !isNaN(d.post_meal))}
    >
      {!timelineData.every((d) => isNaN(d.blood_sugar)) && (
        <Line
          type="monotone"
          dataKey="fasting"
          stroke="#8b5cf6"
          name="Fasting (mg/dL)"
        />
      )}
      {!timelineData.every((d) => isNaN(d.post_meal)) && (
        <Line
          type="monotone"
          dataKey="post_meal"
          stroke="#ec4899"
          name="Post Meal (mg/dL)"
        />
      )}
      <CartesianGrid stroke="#ccc" />
      <XAxis dataKey="date" />
      <YAxis />
      <Tooltip />
      <Legend />
    </LineChart>
  );


      default:
        return null;
    }
  };

  return (
    <div className={container}>
      <div className={headerRow}>
        <h1 className={welcomeText}>Welcome, {user?.username || "User"} 👋</h1>
        <button onClick={() => navigate("/vitals")} className={addButton}>
          + Add Vital
        </button>
      </div>

      <div className={cardsGrid}>
        <Card title="Heart Rate" value={latest?.heart_rate ?? "--"} unit="bpm" />
        <Card
          title="Blood Pressure"
          value={
            latest?.bp_systolic && latest?.bp_diastolic
              ? `${latest.bp_systolic}/${latest.bp_diastolic}`
              : "--"
          }
          unit="mmHg"
        />
        <Card title="SpO2" value={latest?.spo2 ?? "--"} unit="%" />
        <Card title="Sleep" value={latest?.sleep_hours ?? "--"} unit="hrs" />
      </div>

      <div className={chartContainer}>
        <h2 className={sectionTitle}>Vitals Trend</h2>

        <div className="flex overflow-x-auto whitespace-nowrap border-b border-gray-300 mb-4 no-scrollbar">
          {chartTabs.map((tab) => (
            <div
              key={tab.key}
              onClick={() => setSelectedChart(tab.key)}
              className={`inline-block px-4 py-2 mr-2 rounded-t-lg cursor-pointer ${
                selectedChart === tab.key
                  ? "bg-white font-semibold border-t border-l border-r"
                  : "bg-gray-100"
              }`}
            >
              {tab.label}
            </div>
          ))}
        </div>

        <div {...swipeHandlers} className="w-full h-[300px]">
          <ResponsiveContainer width="100%" height="100%">
            {renderChart()}
          </ResponsiveContainer>
        </div>
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
