import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Login from './pages/Login'
import Register from './pages/Register'
import Dashboard from './pages/Dashboard'
import DashboardNew from './pages/DashboardNew'
import AnalysisNew from './pages/AnalysisNew'
import History from './pages/History'
import Settings from './pages/Settings'
import PatientLogin from './pages/PatientLogin'
import PatientRegister from './pages/PatientRegister'
import PatientDashboard from './pages/PatientDashboard'
import PatientHistory from './pages/PatientHistory'
import AnalysisDetail from './pages/AnalysisDetail'

function App() {
  return (
    <Router future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
      <div className="min-h-screen">
        <Routes>
          {/* Admin Routes */}
          <Route path="/" element={<Login />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/dashboard-old" element={<Dashboard />} />
          <Route path="/dashboard" element={<DashboardNew />} />
          <Route path="/analysis" element={<AnalysisNew />} />
          <Route path="/analysis-detail/:id" element={<AnalysisDetail />} />
          <Route path="/history" element={<History />} />
          <Route path="/analytics" element={<DashboardNew />} />
          <Route path="/patients" element={<History />} />
          <Route path="/settings" element={<Settings />} />
          
          {/* Patient Routes */}
          <Route path="/patient-login" element={<PatientLogin />} />
          <Route path="/patient-register" element={<PatientRegister />} />
          <Route path="/patient-dashboard" element={<PatientDashboard />} />
          <Route path="/patient-history" element={<PatientHistory />} />
          <Route path="/patient-settings" element={<Settings />} />
        </Routes>
      </div>
    </Router>
  )
}

export default App

