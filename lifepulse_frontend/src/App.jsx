// src/App.jsx
import { Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import Register from "./pages/Register";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import VitalsForm from "./pages/VitalsForm";
import ActivateAccount from "./pages/ActivateAccount";




function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/register" element={<Register />} />
      <Route path="/login" element={<Login />} />
      <Route path="/dashboard" element={<Dashboard/>} />
      <Route path="/vitals" element={<VitalsForm />} />
      <Route path="/activate/:uidb64/:token" element={<ActivateAccount />} />
    
    </Routes>
  );
}

export default App;
