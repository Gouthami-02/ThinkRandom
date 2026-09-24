import { BrowserRouter, Routes, Route } from "react-router-dom";

import Login from "./pages/Login";

import Dashboard from "./pages/Dashboard";
import RandomTopic from "./pages/RandomTopic";
import Practice from "./pages/Practice";
import History from "./pages/History";

function Register() {
  return <h1>ThinkRandom Register</h1>;
}


function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/random-topic" element={<RandomTopic />} /> 
        <Route path="/practice/:sessionId" element={<Practice />} />
        <Route path="/history" element={<History />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;