import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { 
  User, 
  Calendar, 
  Activity, 
  FileText, 
  LogOut, 
  Eye, 
  Download,
  AlertCircle,
  CheckCircle,
  Clock,
  MapPin,
  Heart,
  TrendingUp,
  BarChart3,
  Shield,
  Camera,
  Upload,
  History,
  Settings,
  Grid3X3,
  Stethoscope,
  ArrowRight
} from 'lucide-react'

export default function PatientDashboard() {
  const navigate = useNavigate()
  const [patient, setPatient] = useState(null)
  const [analyses, setAnalyses] = useState([])
  const [stats, setStats] = useState({})
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    // Check if patient is logged in
    const patientData = localStorage.getItem('patient')
    if (!patientData) {
      navigate('/patient-login')
      return
    }

    setPatient(JSON.parse(patientData))
    fetchPatientData()
  }, [navigate])

  const fetchPatientData = async () => {
    try {
      setLoading(true)
      setError('')
      
      // Fetch analyses and stats
      const [analysesRes, statsRes] = await Promise.all([
        fetch('http://localhost:5001/api/history', {
          credentials: 'include'
        }),
        fetch('http://localhost:5001/api/history/stats', {
          credentials: 'include'
        })
      ])

      if (analysesRes.ok) {
        const analysesData = await analysesRes.json()
        setAnalyses(analysesData.analyses || [])
      } else {
        console.error('Failed to fetch analyses:', analysesRes.status)
      }

      if (statsRes.ok) {
        const statsData = await statsRes.json()
        setStats(statsData.stats || {})
      } else {
        console.error('Failed to fetch stats:', statsRes.status)
      }
    } catch (err) {
      console.error('Error fetching patient data:', err)
      setError('Failed to load data. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const handleLogout = async () => {
    try {
      await fetch('http://localhost:5001/api/patient/logout', {
        method: 'POST',
        credentials: 'include'
      })
    } catch (err) {
      console.error('Logout error:', err)
    } finally {
      localStorage.removeItem('patient')
      localStorage.removeItem('userType')
      navigate('/patient-login')
    }
  }

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  const getRiskColor = (diagnosis) => {
    const risk = diagnosis.toLowerCase()
    if (risk.includes('malignant') || risk.includes('cancer') || risk.includes('melanoma')) return 'text-red-600 bg-red-50'
    if (risk.includes('suspicious')) return 'text-yellow-600 bg-yellow-50'
    if (risk.includes('benign') || risk.includes('nevi')) return 'text-green-600 bg-green-50'
    return 'text-gray-600 bg-gray-50'
  }

  const getDiagnosisCount = (diagnosis) => {
    return analyses.filter(a => a.diagnosis === diagnosis).length
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading your dashboard...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50 flex">
      {/* Sidebar */}
      <div className="w-64 bg-blue-900 text-white flex flex-col">
        {/* Logo */}
        <div className="p-6 border-b border-blue-800">
          <div className="flex items-center">
            <div className="w-8 h-8 bg-white/20 rounded-lg flex items-center justify-center mr-3">
              <Heart className="w-5 h-5" />
            </div>
            <div>
              <h1 className="text-lg font-bold">SkinCare AI</h1>
              <p className="text-xs text-blue-200">Detection System</p>
            </div>
          </div>
        </div>

        {/* Navigation */}
        <nav className="flex-1 p-4">
          <div className="space-y-2">
            <div className="flex items-center px-3 py-2 bg-blue-800 rounded-lg opacity-50 cursor-not-allowed">
              <Grid3X3 className="w-5 h-5 mr-3" />
              <span className="font-medium">Dashboard</span>
              <div className="w-2 h-2 bg-blue-300 rounded-full ml-auto"></div>
            </div>
            <div className="flex items-center px-3 py-2 text-blue-200 opacity-50 cursor-not-allowed">
              <Stethoscope className="w-5 h-5 mr-3" />
              <span>New Analysis</span>
            </div>
            <div className="flex items-center px-3 py-2 text-blue-200 hover:bg-blue-800 rounded-lg cursor-pointer">
              <History className="w-5 h-5 mr-3" />
              <span>History</span>
            </div>
          </div>
        </nav>

        {/* Bottom Navigation */}
        <div className="p-4 border-t border-blue-800">
          <div className="space-y-2">
            <div className="flex items-center px-3 py-2 text-blue-200 hover:bg-blue-800 rounded-lg cursor-pointer">
              <Settings className="w-5 h-5 mr-3" />
              <span>Settings</span>
            </div>
            <div 
              onClick={handleLogout}
              className="flex items-center px-3 py-2 text-blue-200 hover:bg-blue-800 rounded-lg cursor-pointer"
            >
              <LogOut className="w-5 h-5 mr-3" />
              <span>Logout</span>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <header className="bg-white shadow-sm border-b px-8 py-6">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Dashboard Overview</h1>
              <p className="text-gray-600 mt-1">Welcome back! Here's your summary.</p>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-sm text-gray-600">
                Welcome, {patient?.full_name || patient?.name}
              </span>
              <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                <User className="w-5 h-5 text-blue-600" />
              </div>
            </div>
          </div>
        </header>

        {/* Main Content Area */}
        <div className="flex-1 p-8">
          {error && (
            <div className="mb-6 rounded-md bg-red-50 p-4">
              <div className="flex">
                <AlertCircle className="h-5 w-5 text-red-400" />
                <div className="ml-3">
                  <h3 className="text-sm font-medium text-red-800">{error}</h3>
                </div>
              </div>
            </div>
          )}

          {/* Stats Cards */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-100">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">Total Analyses</p>
                  <p className="text-3xl font-bold text-gray-900 mt-2">{stats.total_analyses || 0}</p>
                </div>
                <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                  <Activity className="w-6 h-6 text-blue-600" />
                </div>
              </div>
            </div>

            <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-100">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">Avg Confidence</p>
                  <p className="text-3xl font-bold text-green-600 mt-2">{stats.avg_confidence || 0}%</p>
                </div>
                <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
                  <CheckCircle className="w-6 h-6 text-green-600" />
                </div>
              </div>
            </div>

            <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-100">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">This Week</p>
                  <p className="text-3xl font-bold text-orange-600 mt-2">{analyses.filter(a => {
                    const weekAgo = new Date()
                    weekAgo.setDate(weekAgo.getDate() - 7)
                    return new Date(a.created_at) > weekAgo
                  }).length}</p>
                  <p className="text-xs text-gray-500 mt-1 flex items-center">
                    <TrendingUp className="w-3 h-3 mr-1" />
                    Recent analyses
                  </p>
                </div>
                <div className="w-12 h-12 bg-orange-100 rounded-lg flex items-center justify-center">
                  <Clock className="w-6 h-6 text-orange-600" />
                </div>
              </div>
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Left Column - Diagnosis Distribution */}
            <div className="lg:col-span-2">
              <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-100 mb-8">
                <div className="flex items-center justify-between mb-6">
                  <h2 className="text-lg font-semibold text-gray-900">Diagnosis Distribution</h2>
                  <BarChart3 className="w-5 h-5 text-gray-400" />
                </div>
                
                {analyses.length > 0 ? (
                  <div className="space-y-4">
                    {['Melanocytic nevi', 'Melanoma', 'Basal cell carcinoma', 'Squamous cell carcinoma'].map((diagnosis) => {
                      const count = getDiagnosisCount(diagnosis)
                      const percentage = analyses.length > 0 ? (count / analyses.length) * 100 : 0
                      
                      return count > 0 ? (
                        <div key={diagnosis} className="flex items-center justify-between">
                          <div className="flex-1">
                            <div className="flex items-center justify-between mb-1">
                              <span className="text-sm font-medium text-gray-700">{diagnosis}</span>
                              <span className="text-sm text-gray-500">{count} cases</span>
                            </div>
                            <div className="w-full bg-gray-200 rounded-full h-2">
                              <div 
                                className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                                style={{ width: `${percentage}%` }}
                              ></div>
                            </div>
                          </div>
                        </div>
                      ) : null
                    })}
                  </div>
                ) : (
                  <div className="text-center py-8">
                    <BarChart3 className="w-12 h-12 text-gray-300 mx-auto mb-4" />
                    <p className="text-gray-500">No data available</p>
                  </div>
                )}
              </div>

              {/* Recent Analyses Table */}
              <div className="bg-white rounded-xl shadow-sm border border-gray-100">
                <div className="px-6 py-4 border-b border-gray-100">
                  <div className="flex items-center justify-between">
                    <h2 className="text-lg font-semibold text-gray-900">Recent Analyses</h2>
                    <button 
                      onClick={() => navigate('/patient-history')}
                      className="text-blue-600 hover:text-blue-700 text-sm font-medium flex items-center"
                    >
                      View All <ArrowRight className="w-4 h-4 ml-1" />
                    </button>
                  </div>
                </div>
                
                {analyses.length === 0 ? (
                  <div className="p-8 text-center">
                    <Activity className="h-12 w-12 text-gray-300 mx-auto mb-4" />
                    <h3 className="text-lg font-medium text-gray-900 mb-2">No analyses found</h3>
                    <p className="text-gray-600 mb-4">Your analysis history will appear here when a doctor performs an analysis linked to your email address</p>
                    <p className="text-sm text-gray-500">Contact your healthcare provider to have your skin analysis performed</p>
                  </div>
                ) : (
                  <div className="divide-y divide-gray-100">
                    {analyses.slice(0, 5).map((analysis) => (
                      <div key={analysis.id} className="p-6 hover:bg-gray-50 transition-colors">
                        <div className="flex items-center justify-between">
                          <div className="flex-1">
                            <div className="flex items-center space-x-3 mb-2">
                              <h3 className="text-sm font-medium text-gray-900">
                                {analysis.patient_name}
                              </h3>
                              <span className="text-sm text-gray-500">
                                {analysis.age} yrs, {analysis.gender}
                              </span>
                            </div>
                            <div className="flex items-center space-x-3">
                              <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getRiskColor(analysis.diagnosis)}`}>
                                {analysis.diagnosis}
                              </span>
                              <span className="text-sm text-gray-500">
                                {analysis.confidence}%
                              </span>
                              <span className="text-sm text-gray-500">
                                {formatDate(analysis.created_at)}
                              </span>
                            </div>
                          </div>
                          <div className="flex items-center space-x-2">
                            <button
                              onClick={() => navigate(`/analysis-detail/${analysis.id}`)}
                              className="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
                              title="View Details"
                            >
                              <Eye className="h-4 w-4" />
                            </button>
                            {analysis.report_path && (
                              <a
                                href={`http://localhost:5001${analysis.report_path}`}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
                                title="Download Report"
                              >
                                <Download className="h-4 w-4" />
                              </a>
                            )}
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>

            {/* Right Column */}
            <div className="space-y-6">
              {/* Quick Actions */}
              <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-100">
                <h2 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h2>
                <div className="space-y-3">
                  <button className="w-full flex items-center justify-center px-4 py-3 bg-gray-300 text-gray-500 rounded-lg cursor-not-allowed opacity-50" disabled>
                    <Upload className="w-5 h-5 mr-2" />
                    Upload Image
                  </button>
                  <button className="w-full flex items-center justify-center px-4 py-3 bg-gray-300 text-gray-500 rounded-lg cursor-not-allowed opacity-50" disabled>
                    <Camera className="w-5 h-5 mr-2" />
                    Use Camera
                  </button>
                  <button 
                    onClick={() => navigate('/patient-history')}
                    className="w-full flex items-center justify-center px-4 py-3 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors"
                  >
                    <History className="w-5 h-5 mr-2" />
                    View History
                  </button>
                </div>
              </div>

              {/* High Risk Cases */}
              <div className="bg-white rounded-xl shadow-sm p-6 border border-red-200">
                <div className="flex items-center mb-4">
                  <AlertCircle className="w-5 h-5 text-red-600 mr-2" />
                  <h2 className="text-lg font-semibold text-gray-900">High Risk Cases</h2>
                </div>
                <p className="text-2xl font-bold text-red-600 mb-2">
                  {analyses.filter(a => a.diagnosis.toLowerCase().includes('melanoma') || a.diagnosis.toLowerCase().includes('malignant')).length} melanoma cases detected
                </p>
                <button className="text-red-600 hover:text-red-700 text-sm font-medium flex items-center">
                  Review Cases <ArrowRight className="w-4 h-4 ml-1" />
                </button>
              </div>

              {/* System Status */}
              <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-100">
                <h2 className="text-lg font-semibold text-gray-900 mb-4">System Status</h2>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">AI Model</span>
                  <div className="flex items-center">
                    <div className="w-2 h-2 bg-green-500 rounded-full mr-2"></div>
                    <span className="text-sm font-medium text-green-600">Active</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}