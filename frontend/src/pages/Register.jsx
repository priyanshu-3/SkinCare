import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'

export default function Register() {
  const navigate = useNavigate()
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
  })
  const [showPassword, setShowPassword] = useState(false)
  const [passwordStrength, setPasswordStrength] = useState(0)
  const [strengthText, setStrengthText] = useState('Use 8+ characters with a mix of letters and numbers')
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const [loading, setLoading] = useState(false)

  const checkPasswordStrength = (password) => {
    let strength = 0
    if (password.length >= 8) strength++
    if (password.match(/[a-z]/) && password.match(/[A-Z]/)) strength++
    if (password.match(/[0-9]/)) strength++
    if (password.match(/[^a-zA-Z0-9]/)) strength++

    setPasswordStrength(strength)

    if (strength === 0) {
      setStrengthText('Weak password')
    } else if (strength <= 2) {
      setStrengthText('Weak - Add more characters')
    } else if (strength === 3) {
      setStrengthText('Medium - Could be stronger')
    } else {
      setStrengthText('Strong password!')
    }
  }

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData((prev) => ({ ...prev, [name]: value }))

    if (name === 'password') {
      checkPasswordStrength(value)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setSuccess('')
    setLoading(true)

    try {
      const response = await fetch('http://localhost:5001/api/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
        credentials: 'include',
      })

      const result = await response.json()

      if (response.ok && result.success) {
        setSuccess('Registration successful! Redirecting to login...')
        setTimeout(() => navigate('/login'), 2000)
      } else {
        setError(result.error || 'Registration failed. Please try again.')
      }
    } catch (err) {
      setError('Registration failed. Please check your connection and try again.')
    } finally {
      setLoading(false)
    }
  }

  const getStrengthClass = () => {
    if (passwordStrength === 0) return 'w-0'
    if (passwordStrength <= 2) return 'w-1/3 bg-red-500'
    if (passwordStrength === 3) return 'w-2/3 bg-orange-500'
    return 'w-full bg-green-500'
  }

  const getStrengthColor = () => {
    if (passwordStrength === 0 || passwordStrength <= 2) return 'text-red-500'
    if (passwordStrength === 3) return 'text-orange-500'
    return 'text-green-500'
  }

  return (
    <div className="min-h-screen flex items-center justify-center p-5 bg-gradient-to-br from-[#667eea] to-[#764ba2]">
      <div className="w-full max-w-[480px]">
        <div className="bg-white rounded-3xl shadow-2xl overflow-hidden animate-slide-in">
          {/* Header */}
          <div className="bg-gradient-to-r from-blue-600 to-purple-600 px-8 py-10 text-center text-white">
            <div className="w-20 h-20 bg-white/20 backdrop-blur-md rounded-2xl flex items-center justify-center mx-auto mb-5">
              <i className="fas fa-user-plus text-4xl"></i>
            </div>
            <h1 className="text-3xl font-bold mb-2">Create Account</h1>
            <p className="text-sm opacity-95">Join us to access advanced AI skin cancer detection</p>
            <div className="flex gap-2 justify-center flex-wrap mt-4">
              <span className="bg-white/20 backdrop-blur-md px-3 py-1 rounded-full text-xs">
                <i className="fas fa-shield-check"></i> Free to Use
              </span>
              <span className="bg-white/20 backdrop-blur-md px-3 py-1 rounded-full text-xs">
                <i className="fas fa-lock"></i> Private
              </span>
              <span className="bg-white/20 backdrop-blur-md px-3 py-1 rounded-full text-xs">
                <i className="fas fa-bolt"></i> Fast
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

            {success && (
              <div className="bg-green-50 border-l-4 border-green-600 text-green-900 p-4 rounded-xl mb-5 animate-slide-down">
                <i className="fas fa-check-circle mr-2"></i>
                {success}
              </div>
            )}

            {/* Benefits */}
            <div className="bg-gray-50 p-5 rounded-xl mb-5">
              <h6 className="text-xs font-bold text-gray-700 mb-3 uppercase tracking-wide">
                What You'll Get
              </h6>
              <div className="space-y-2">
                <div className="flex items-center gap-2 text-sm text-gray-600">
                  <i className="fas fa-check-circle text-blue-600"></i>
                  <span>AI-powered skin lesion analysis</span>
                </div>
                <div className="flex items-center gap-2 text-sm text-gray-600">
                  <i className="fas fa-check-circle text-blue-600"></i>
                  <span>Explainable AI visualizations</span>
                </div>
                <div className="flex items-center gap-2 text-sm text-gray-600">
                  <i className="fas fa-check-circle text-blue-600"></i>
                  <span>Instant results with confidence scores</span>
                </div>
              </div>
            </div>

            <form onSubmit={handleSubmit}>
              <div className="mb-5">
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Full Name
                </label>
                <div className="relative">
                  <i className="fas fa-user absolute left-4 top-1/2 -translate-y-1/2 text-gray-400"></i>
                  <input
                    type="text"
                    name="name"
                    value={formData.name}
                    onChange={handleChange}
                    className="w-full h-13 pl-12 pr-4 py-3 border-2 border-gray-200 rounded-xl focus:border-blue-600 focus:ring-4 focus:ring-blue-100 transition-all"
                    placeholder="John Doe"
                    required
                    autoFocus
                  />
                </div>
              </div>

              <div className="mb-5">
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Email Address
                </label>
                <div className="relative">
                  <i className="fas fa-envelope absolute left-4 top-1/2 -translate-y-1/2 text-gray-400"></i>
                  <input
                    type="email"
                    name="email"
                    value={formData.email}
                    onChange={handleChange}
                    className="w-full h-13 pl-12 pr-4 py-3 border-2 border-gray-200 rounded-xl focus:border-blue-600 focus:ring-4 focus:ring-blue-100 transition-all"
                    placeholder="your.email@example.com"
                    required
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
                    name="password"
                    value={formData.password}
                    onChange={handleChange}
                    className="w-full h-13 pl-12 pr-12 py-3 border-2 border-gray-200 rounded-xl focus:border-blue-600 focus:ring-4 focus:ring-blue-100 transition-all"
                    placeholder="Create a strong password"
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
                
                {/* Password Strength Bar */}
                <div className="h-1 bg-gray-200 rounded-full mt-2 overflow-hidden">
                  <div
                    className={`h-full transition-all duration-300 ${getStrengthClass()}`}
                  ></div>
                </div>
                <p className={`text-xs mt-1 ${getStrengthColor()}`}>
                  {strengthText}
                </p>
              </div>

              <button
                type="submit"
                disabled={loading}
                className="w-full h-13 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-xl font-semibold text-base mt-3 hover:-translate-y-0.5 hover:shadow-lg hover:shadow-blue-500/40 active:translate-y-0 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {loading ? (
                  <span>
                    <i className="fas fa-spinner fa-spin mr-2"></i>
                    Creating Account...
                  </span>
                ) : (
                  <span>
                    <i className="fas fa-user-plus mr-2"></i>
                    Create Account
                  </span>
                )}
              </button>
            </form>

            <div className="text-center mt-6 pt-6 border-t border-gray-200 text-gray-600 text-sm">
              Already have an account?{' '}
              <Link
                to="/login"
                className="text-blue-600 font-semibold hover:text-blue-800 hover:underline transition-colors"
              >
                Sign in here
              </Link>
            </div>
          </div>
        </div>

        <div className="text-center mt-5 text-white text-xs">
          <i className="fas fa-info-circle mr-1"></i>
          By signing up, you agree to our Terms of Service
        </div>
      </div>

      <style jsx>{`
        @keyframes slide-in {
          from {
            opacity: 0;
            transform: translateY(20px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
        @keyframes slide-down {
          from {
            opacity: 0;
            transform: translateY(-10px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
        .animate-slide-in {
          animation: slide-in 0.5s ease-out;
        }
        .animate-slide-down {
          animation: slide-down 0.3s ease-out;
        }
      `}</style>
    </div>
  )
}

