import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Login from './pages/Login'
import Register from './pages/Register'
import Dashboard from './pages/Dashboard'
import DashboardNew from './pages/DashboardNew'
import AnalysisNew from './pages/AnalysisNew'
import History from './pages/History'
import Settings from './pages/Settings'

function App() {
  return (
    <Router>
      <div className="min-h-screen">
        <Routes>
          <Route path="/" element={<Login />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/dashboard-old" element={<Dashboard />} />
          <Route path="/dashboard" element={<DashboardNew />} />
          <Route path="/analysis" element={<AnalysisNew />} />
          <Route path="/history" element={<History />} />
          <Route path="/analytics" element={<DashboardNew />} />
          <Route path="/patients" element={<History />} />
          <Route path="/settings" element={<Settings />} />
        </Routes>
      </div>
    </Router>
  )
}

export default App

