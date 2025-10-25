import { useState } from 'react'
import { SignedIn, SignedOut, useUser } from '@clerk/clerk-react'
import { Upload, Camera, AlertCircle } from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import { analyzeImage } from '../services/api'

export default function Analysis() {
  const { user } = useUser()
  const navigate = useNavigate()
  const [selectedFile, setSelectedFile] = useState(null)
  const [preview, setPreview] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [metadata, setMetadata] = useState({
    age: '',
    gender: '',
    location: '',
  })

  const handleFileSelect = (event) => {
    const file = event.target.files?.[0]
    if (file) {
      setSelectedFile(file)
      setError(null)

      const reader = new FileReader()
      reader.onloadend = () => {
        setPreview(reader.result)
      }
      reader.readAsDataURL(file)
    }
  }

  const handleMetadataChange = (field, value) => {
    setMetadata((prev) => ({
      ...prev,
      [field]: value,
    }))
  }

  const handleAnalyze = async () => {
    if (!selectedFile) {
      setError('Please select an image first')
      return
    }

    setLoading(true)
    setError(null)

    try {
      const result = await analyzeImage(selectedFile, metadata)
      
      // Store result and navigate to results page
      sessionStorage.setItem('analysisResult', JSON.stringify(result))
      navigate('/results')
    } catch (err) {
      setError(err.message || 'Analysis failed. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <SignedOut>
        <div className="text-center py-12">
          <AlertCircle className="w-16 h-16 text-yellow-500 mx-auto mb-4" />
          <h2 className="text-2xl font-bold mb-2">Authentication Required</h2>
          <p className="text-gray-600">
            Please sign in to use the analysis feature
          </p>
        </div>
      </SignedOut>

      <SignedIn>
        <div className="mb-8">
          <h1 className="text-3xl font-bold mb-2">Skin Lesion Analysis</h1>
          <p className="text-gray-600">
            Upload an image for AI-powered analysis with uncertainty
            quantification
          </p>
        </div>

        <div className="grid lg:grid-cols-2 gap-8">
          {/* Left Column: Upload */}
          <div>
            <div className="card">
              <h2 className="text-xl font-semibold mb-4">Image Upload</h2>

              {/* Upload Area */}
              <div
                className={`border-2 border-dashed rounded-lg p-8 text-center transition-colors ${
                  preview
                    ? 'border-primary-300 bg-primary-50'
                    : 'border-gray-300 hover:border-primary-400'
                }`}
              >
                {preview ? (
                  <div className="space-y-4">
                    <img
                      src={preview}
                      alt="Preview"
                      className="max-h-64 mx-auto rounded-lg"
                    />
                    <button
                      onClick={() => {
                        setPreview(null)
                        setSelectedFile(null)
                      }}
                      className="btn-secondary"
                    >
                      Remove Image
                    </button>
                  </div>
                ) : (
                  <div className="space-y-4">
                    <Upload className="w-12 h-12 text-gray-400 mx-auto" />
                    <div>
                      <label
                        htmlFor="file-upload"
                        className="btn-primary cursor-pointer inline-block"
                      >
                        Choose File
                      </label>
                      <input
                        id="file-upload"
                        type="file"
                        accept="image/*"
                        onChange={handleFileSelect}
                        className="hidden"
                      />
                    </div>
                    <p className="text-sm text-gray-500">
                      or drag and drop an image here
                    </p>
                  </div>
                )}
              </div>

              {/* Supported Formats */}
              <p className="text-xs text-gray-500 mt-2">
                Supported: JPG, PNG, JPEG (max 10MB)
              </p>
            </div>

            {/* Camera Capture (Optional) */}
            <div className="card mt-6">
              <h3 className="font-semibold mb-2 flex items-center">
                <Camera className="w-5 h-5 mr-2" />
                Or Use Camera
              </h3>
              <label
                htmlFor="camera-capture"
                className="btn-secondary cursor-pointer w-full block text-center"
              >
                Take Photo
              </label>
              <input
                id="camera-capture"
                type="file"
                accept="image/*"
                capture="environment"
                onChange={handleFileSelect}
                className="hidden"
              />
            </div>
          </div>

          {/* Right Column: Metadata */}
          <div>
            <div className="card">
              <h2 className="text-xl font-semibold mb-4">
                Patient Information (Optional)
              </h2>
              <p className="text-sm text-gray-600 mb-4">
                Providing this information helps improve prediction accuracy
              </p>

              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium mb-1">Age</label>
                  <input
                    type="number"
                    value={metadata.age}
                    onChange={(e) =>
                      handleMetadataChange('age', e.target.value)
                    }
                    placeholder="e.g., 45"
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium mb-1">
                    Gender
                  </label>
                  <select
                    value={metadata.gender}
                    onChange={(e) =>
                      handleMetadataChange('gender', e.target.value)
                    }
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  >
                    <option value="">Select...</option>
                    <option value="male">Male</option>
                    <option value="female">Female</option>
                    <option value="other">Other</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium mb-1">
                    Lesion Location
                  </label>
                  <input
                    type="text"
                    value={metadata.location}
                    onChange={(e) =>
                      handleMetadataChange('location', e.target.value)
                    }
                    placeholder="e.g., face, arm, back"
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  />
                </div>
              </div>
            </div>

            {/* Error Display */}
            {error && (
              <div className="mt-6 p-4 bg-red-50 border border-red-200 rounded-lg flex items-start">
                <AlertCircle className="w-5 h-5 text-red-600 mt-0.5 mr-2 flex-shrink-0" />
                <p className="text-sm text-red-800">{error}</p>
              </div>
            )}

            {/* Analyze Button */}
            <button
              onClick={handleAnalyze}
              disabled={!selectedFile || loading}
              className="btn-primary w-full mt-6 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? (
                <span className="flex items-center justify-center">
                  <svg
                    className="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                  >
                    <circle
                      className="opacity-25"
                      cx="12"
                      cy="12"
                      r="10"
                      stroke="currentColor"
                      strokeWidth="4"
                    ></circle>
                    <path
                      className="opacity-75"
                      fill="currentColor"
                      d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                    ></path>
                  </svg>
                  Analyzing...
                </span>
              ) : (
                'Analyze Image'
              )}
            </button>

            {/* Disclaimer */}
            <div className="mt-6 p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
              <p className="text-sm text-yellow-800">
                <strong>⚠️ Note:</strong> This tool is for informational
                purposes only and should not replace professional medical
                advice.
              </p>
            </div>
          </div>
        </div>
      </SignedIn>
    </div>
  )
}

