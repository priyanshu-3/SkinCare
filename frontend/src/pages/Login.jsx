import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'

export default function Login() {
  const navigate = useNavigate()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      const response = await fetch('http://localhost:5001/api/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email,
          password,
        }),
        credentials: 'include',
      })

      const result = await response.json()

      if (response.ok && result.success) {
        navigate('/dashboard')
      } else {
        setError(result.error || 'Invalid email or password')
      }
    } catch (err) {
      setError('Login failed. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center p-5 bg-gradient-to-br from-[#667eea] to-[#764ba2]">
      <div className="w-full max-w-[480px]">
        <div className="bg-white rounded-3xl shadow-2xl overflow-hidden animate-slide-in">
          {/* Header */}
          <div className="bg-gradient-to-r from-blue-600 to-purple-600 px-8 py-10 text-center text-white">
            <div className="w-20 h-20 bg-white/20 backdrop-blur-md rounded-2xl flex items-center justify-center mx-auto mb-5">
              <i className="fas fa-microscope text-4xl"></i>
            </div>
            <h1 className="text-3xl font-bold mb-2">Welcome Back</h1>
            <p className="text-sm opacity-95">Sign in to access AI-powered skin cancer detection</p>
            <div className="flex gap-2 justify-center flex-wrap mt-4">
              <span className="bg-white/20 backdrop-blur-md px-3 py-1 rounded-full text-xs">
                <i className="fas fa-brain"></i> AI-Powered
              </span>
              <span className="bg-white/20 backdrop-blur-md px-3 py-1 rounded-full text-xs">
                <i className="fas fa-shield-alt"></i> Secure
              </span>
              <span className="bg-white/20 backdrop-blur-md px-3 py-1 rounded-full text-xs">
                <i className="fas fa-chart-line"></i> Accurate
              </span>
            </div>
          </div>

          {/* Body */}
          <div className="p-10">
            {error && (
              <div className="bg-red-50 border-l-4 border-red-600 text-red-900 p-4 rounded-xl mb-5 animate-slide-down">
                <i className="fas fa-exclamation-circle mr-2"></i>
                {error}
              </div>
            )}

            <form onSubmit={handleSubmit}>
              <div className="mb-5">
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Email Address
                </label>
                <div className="relative">
                  <i className="fas fa-envelope absolute left-4 top-1/2 -translate-y-1/2 text-gray-400"></i>
                  <input
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className="w-full h-13 pl-12 pr-4 py-3 border-2 border-gray-200 rounded-xl focus:border-blue-600 focus:ring-4 focus:ring-blue-100 transition-all"
                    placeholder="your.email@example.com"
                    required
                    autoFocus
                  />
                </div>
              </div>

              <div className="mb-5">
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Password
                </label>
                <div className="relative">
                  <i className="fas fa-lock absolute left-4 top-1/2 -translate-y-1/2 text-gray-400"></i>
                  <input
                    type={showPassword ? 'text' : 'password'}
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className="w-full h-13 pl-12 pr-12 py-3 border-2 border-gray-200 rounded-xl focus:border-blue-600 focus:ring-4 focus:ring-blue-100 transition-all"
                    placeholder="Enter your password"
                    required
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-4 top-1/2 -translate-y-1/2 text-gray-400 hover:text-blue-600 transition-colors"
                  >
                    <i className={`fas fa-${showPassword ? 'eye-slash' : 'eye'}`}></i>
                  </button>
                </div>
              </div>

              <button
                type="submit"
                disabled={loading}
                className="w-full h-13 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-xl font-semibold text-base mt-3 hover:-translate-y-0.5 hover:shadow-lg hover:shadow-blue-500/40 active:translate-y-0 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {loading ? (
                  <span>
                    <i className="fas fa-spinner fa-spin mr-2"></i>
                    Signing In...
                  </span>
                ) : (
                  <span>
                    <i className="fas fa-sign-in-alt mr-2"></i>
                    Sign In
                  </span>
                )}
              </button>
            </form>

            <div className="text-center mt-6 pt-6 border-t border-gray-200 text-gray-600 text-sm">
              Don't have an account?{' '}
              <Link
                to="/register"
                className="text-blue-600 font-semibold hover:text-blue-800 hover:underline transition-colors"
              >
                Create one now
              </Link>
            </div>

            <div className="text-center mt-4 text-gray-600 text-sm">
              Are you a patient?{' '}
              <Link
                to="/patient-login"
                className="text-green-600 font-semibold hover:text-green-800 hover:underline transition-colors"
              >
                Patient Login
              </Link>
            </div>

            {/* Demo Credentials */}
            <div className="mt-6 p-4 bg-blue-50 rounded-lg border border-blue-200">
              <h3 className="text-sm font-semibold text-gray-900 mb-3 text-center">Demo Credentials:</h3>
              <div className="space-y-2">
                <div 
                  className="flex items-center justify-between p-3 bg-white rounded-lg border border-blue-200 cursor-pointer hover:bg-blue-50 transition-colors"
                  onClick={() => {
                    setEmail('priyanshu@gmail.com')
                    setPassword('admin123')
                  }}
                >
                  <div className="flex items-center space-x-3">
                    <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                      <i className="fas fa-user-md text-blue-600"></i>
                    </div>
                    <div>
                      <p className="text-sm font-medium text-gray-900">Admin User</p>
                      <p className="text-xs text-gray-500">priyanshu@gmail.com</p>
                    </div>
                  </div>
                  <div className="text-right">
                    <p className="text-xs text-gray-500">Password:</p>
                    <p className="text-sm font-mono text-gray-700">admin123</p>
                  </div>
                </div>

                <div 
                  className="flex items-center justify-between p-3 bg-white rounded-lg border border-blue-200 cursor-pointer hover:bg-blue-50 transition-colors"
                  onClick={() => {
                    setEmail('doctor@test.com')
                    setPassword('doctor123')
                  }}
                >
                  <div className="flex items-center space-x-3">
                    <div className="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center">
                      <i className="fas fa-microscope text-green-600"></i>
                    </div>
                    <div>
                      <p className="text-sm font-medium text-gray-900">Test Doctor</p>
                      <p className="text-xs text-gray-500">doctor@test.com</p>
                    </div>
                  </div>
                  <div className="text-right">
                    <p className="text-xs text-gray-500">Password:</p>
                    <p className="text-sm font-mono text-gray-700">doctor123</p>
                  </div>
                </div>
              </div>
              <p className="text-xs text-gray-500 text-center mt-3">
                Click on any credential to auto-fill the form
              </p>
            </div>
          </div>
        </div>

        <div className="text-center mt-5 text-white text-xs">
          <i className="fas fa-shield-alt mr-1"></i>
          Your data is encrypted and secure
        </div>
      </div>

    </div>
  )
}

