import { useState, useRef, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import Sidebar from '../components/Sidebar'
import { Upload, Camera, User, MapPin, Calendar, X, Loader, CheckCircle, AlertCircle } from 'lucide-react'

export default function AnalysisNew() {
  const navigate = useNavigate()
  const [collapsed, setCollapsed] = useState(false)
  const [selectedFile, setSelectedFile] = useState(null)
  const [preview, setPreview] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [success, setSuccess] = useState(false)
  const [activeTab, setActiveTab] = useState('upload')
  const [cameraActive, setCameraActive] = useState(false)
  const [stream, setStream] = useState(null)
  
  const fileInputRef = useRef(null)
  const videoRef = useRef(null)
  const canvasRef = useRef(null)

  const [patientInfo, setPatientInfo] = useState({
    name: '',
    age: '',
    gender: '',
    location: ''
  })

  // Handle video stream setup
  useEffect(() => {
    if (stream && videoRef.current && !videoRef.current.srcObject) {
      videoRef.current.srcObject = stream
    }
  }, [stream])

  // Cleanup camera on unmount
  useEffect(() => {
    return () => {
      if (stream) {
        stream.getTracks().forEach((track) => track.stop())
      }
    }
  }, [stream])

  const handleFileSelect = (file) => {
    if (!file.type.startsWith('image/')) {
      setError('Please select an image file')
      return
    }

    setSelectedFile(file)
    setError(null)
    const reader = new FileReader()
    reader.onloadend = () => {
      setPreview(reader.result)
    }
    reader.readAsDataURL(file)
  }

  const handleDrop = (e) => {
    e.preventDefault()
    const files = e.dataTransfer.files
    if (files.length > 0) {
      handleFileSelect(files[0])
    }
  }

  const startCamera = async () => {
    try {
      setError(null)
      // Request camera permission and get stream
      const mediaStream = await navigator.mediaDevices.getUserMedia({
        video: { 
          width: { ideal: 1280 },
          height: { ideal: 720 },
          facingMode: 'environment' // Use back camera on mobile if available
        }
      })
      
      setStream(mediaStream)
      setCameraActive(true)
      
      // Set video source after a short delay to ensure video element is rendered
      setTimeout(() => {
        if (videoRef.current && mediaStream) {
          videoRef.current.srcObject = mediaStream
        }
      }, 100)
    } catch (err) {
      console.error('Camera error:', err)
      let errorMessage = 'Unable to access camera. '
      
      if (err.name === 'NotAllowedError' || err.name === 'PermissionDeniedError') {
        errorMessage += 'Please grant camera permissions in your browser settings.'
      } else if (err.name === 'NotFoundError' || err.name === 'DevicesNotFoundError') {
        errorMessage += 'No camera found on this device.'
      } else if (err.name === 'NotReadableError' || err.name === 'TrackStartError') {
        errorMessage += 'Camera is already in use by another application.'
      } else {
        errorMessage += err.message
      }
      
      setError(errorMessage)
      setCameraActive(false)
    }
  }

  const stopCamera = () => {
    if (stream) {
      stream.getTracks().forEach((track) => track.stop())
      setStream(null)
      setCameraActive(false)
    }
  }

  const captureImage = () => {
    const video = videoRef.current
    const canvas = canvasRef.current
    if (video && canvas) {
      const ctx = canvas.getContext('2d')
      canvas.width = video.videoWidth
      canvas.height = video.videoHeight
      ctx.drawImage(video, 0, 0)
      canvas.toBlob((blob) => {
        const file = new File([blob], 'captured.jpg', { type: 'image/jpeg' })
        handleFileSelect(file)
        stopCamera()
      }, 'image/jpeg', 0.8)
    }
  }

  const handleAnalyze = async () => {
    if (!selectedFile) {
      setError('Please select an image first')
      return
    }

    const { name, age, gender } = patientInfo
    if (!name || !age || !gender) {
      setError('Please fill in all required fields (Name, Age, Gender)')
      return
    }

    setLoading(true)
    setError(null)

    try {
      const formData = new FormData()
      formData.append('image', selectedFile)
      formData.append('name', name)
      formData.append('age', age)
      formData.append('gender', gender)
      formData.append('location', patientInfo.location || '')

      const response = await fetch('http://localhost:5001/analyze', {
        method: 'POST',
        body: formData,
        credentials: 'include',
      })

      const result = await response.json()

      if (!response.ok || result.error) {
        setError(result.error || 'Analysis failed')
        return
      }

      setSuccess(true)
      setTimeout(() => {
        navigate('/dashboard')
      }, 2000)
    } catch (err) {
      setError('Analysis failed: ' + err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex h-screen bg-gray-50">
      <Sidebar collapsed={collapsed} setCollapsed={setCollapsed} />

      <div className={`flex-1 transition-all duration-300 ${collapsed ? 'ml-20' : 'ml-64'}`}>
        {/* Header */}
        <header className="bg-white shadow-sm border-b border-gray-200">
          <div className="px-8 py-4">
            <h1 className="text-2xl font-bold text-gray-900">New Analysis</h1>
            <p className="text-sm text-gray-600 mt-1">Upload or capture skin lesion image for AI analysis</p>
          </div>
        </header>

        {/* Content */}
        <div className="p-8 overflow-y-auto h-[calc(100vh-88px)]">
          <div className="max-w-5xl mx-auto">
            {/* Alert Messages */}
            {error && (
              <div className="mb-6 bg-red-50 border border-red-200 rounded-lg p-4 flex items-start gap-3">
                <AlertCircle className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
                <div className="flex-1">
                  <h4 className="font-semibold text-red-900">Error</h4>
                  <p className="text-sm text-red-700">{error}</p>
                </div>
                <button onClick={() => setError(null)} className="text-red-600 hover:text-red-700">
                  <X className="w-5 h-5" />
                </button>
              </div>
            )}

            {success && (
              <div className="mb-6 bg-green-50 border border-green-200 rounded-lg p-4 flex items-start gap-3">
                <CheckCircle className="w-5 h-5 text-green-600 flex-shrink-0 mt-0.5" />
                <div className="flex-1">
                  <h4 className="font-semibold text-green-900">Success!</h4>
                  <p className="text-sm text-green-700">Analysis completed. Redirecting to dashboard...</p>
                </div>
              </div>
            )}

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Left Column - Patient Info & Image Upload */}
              <div className="space-y-6">
                {/* Patient Information */}
                <div className="bg-white rounded-xl shadow-md p-6">
                  <h2 className="text-lg font-bold text-gray-900 mb-4 flex items-center gap-2">
                    <User className="w-5 h-5 text-blue-600" />
                    Patient Information
                  </h2>
                  <div className="space-y-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Full Name *
                      </label>
                      <input
                        type="text"
                        value={patientInfo.name}
                        onChange={(e) => setPatientInfo({ ...patientInfo, name: e.target.value })}
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        placeholder="Enter patient name"
                      />
                    </div>
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                          Age *
                        </label>
                        <input
                          type="number"
                          value={patientInfo.age}
                          onChange={(e) => setPatientInfo({ ...patientInfo, age: e.target.value })}
                          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                          placeholder="Age"
                          min="1"
                          max="120"
                        />
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                          Gender *
                        </label>
                        <select
                          value={patientInfo.gender}
                          onChange={(e) => setPatientInfo({ ...patientInfo, gender: e.target.value })}
                          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        >
                          <option value="">Select</option>
                          <option value="Male">Male</option>
                          <option value="Female">Female</option>
                          <option value="Other">Other</option>
                        </select>
                      </div>
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Location
                      </label>
                      <input
                        type="text"
                        value={patientInfo.location}
                        onChange={(e) => setPatientInfo({ ...patientInfo, location: e.target.value })}
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        placeholder="City, State"
                      />
                    </div>
                  </div>
                </div>

                {/* Image Upload */}
                <div className="bg-white rounded-xl shadow-md p-6">
                  <h2 className="text-lg font-bold text-gray-900 mb-4">Image Upload</h2>
                  
                  {/* Tabs */}
                  <div className="flex gap-2 mb-4">
                    <button
                      onClick={() => { setActiveTab('upload'); stopCamera(); }}
                      className={`flex-1 py-2 px-4 rounded-lg font-medium transition-colors ${
                        activeTab === 'upload'
                          ? 'bg-blue-600 text-white'
                          : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                      }`}
                    >
                      <Upload className="w-4 h-4 inline mr-2" />
                      Upload
                    </button>
                    <button
                      onClick={() => setActiveTab('camera')}
                      className={`flex-1 py-2 px-4 rounded-lg font-medium transition-colors ${
                        activeTab === 'camera'
                          ? 'bg-blue-600 text-white'
                          : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                      }`}
                    >
                      <Camera className="w-4 h-4 inline mr-2" />
                      Camera
                    </button>
                  </div>

                  {/* Upload Tab */}
                  {activeTab === 'upload' && (
                    <div
                      onDragOver={(e) => e.preventDefault()}
                      onDrop={handleDrop}
                      onClick={() => fileInputRef.current?.click()}
                      className="border-2 border-dashed border-blue-300 rounded-lg p-8 text-center cursor-pointer hover:border-blue-500 hover:bg-blue-50 transition-all"
                    >
                      <Upload className="w-12 h-12 text-blue-600 mx-auto mb-4" />
                      <p className="text-gray-700 font-medium mb-1">
                        Drop your image here or click to browse
                      </p>
                      <p className="text-sm text-gray-500">
                        Supports: JPG, JPEG, PNG (Max 16MB)
                      </p>
                      <input
                        ref={fileInputRef}
                        type="file"
                        accept="image/*"
                        onChange={(e) => e.target.files?.[0] && handleFileSelect(e.target.files[0])}
                        className="hidden"
                      />
                    </div>
                  )}

                  {/* Camera Tab */}
                  {activeTab === 'camera' && (
                    <div className="text-center">
                      {!cameraActive ? (
                        <div className="border-2 border-dashed border-gray-300 rounded-lg p-8">
                          <Camera className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                          <button
                            onClick={startCamera}
                            className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                          >
                            Start Camera
                          </button>
                        </div>
                      ) : (
                        <div>
                          <div className="relative bg-black rounded-lg overflow-hidden mb-4">
                            <video
                              ref={videoRef}
                              autoPlay
                              playsInline
                              muted
                              className="w-full h-auto rounded-lg"
                              style={{ maxHeight: '400px', objectFit: 'contain' }}
                            />
                          </div>
                          <canvas ref={canvasRef} className="hidden" />
                          <div className="flex gap-2 justify-center">
                            <button
                              onClick={captureImage}
                              className="flex items-center gap-2 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors shadow-md"
                            >
                              <Camera className="w-5 h-5" />
                              Capture
                            </button>
                            <button
                              onClick={stopCamera}
                              className="flex items-center gap-2 px-6 py-3 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition-colors"
                            >
                              <X className="w-5 h-5" />
                              Cancel
                            </button>
                          </div>
                        </div>
                      )}
                    </div>
                  )}
                </div>
              </div>

              {/* Right Column - Preview & Analysis */}
              <div className="space-y-6">
                {/* Preview */}
                <div className="bg-white rounded-xl shadow-md p-6">
                  <h2 className="text-lg font-bold text-gray-900 mb-4">Preview</h2>
                  {preview ? (
                    <div className="relative">
                      <img
                        src={preview}
                        alt="Preview"
                        className="w-full rounded-lg shadow-md"
                      />
                      <button
                        onClick={() => { setPreview(null); setSelectedFile(null); }}
                        className="absolute top-2 right-2 p-2 bg-red-500 text-white rounded-full hover:bg-red-600 transition-colors"
                      >
                        <X className="w-4 h-4" />
                      </button>
                    </div>
                  ) : (
                    <div className="aspect-video bg-gray-100 rounded-lg flex items-center justify-center">
                      <div className="text-center text-gray-400">
                        <Upload className="w-12 h-12 mx-auto mb-2" />
                        <p>No image selected</p>
                      </div>
                    </div>
                  )}
                </div>

                {/* Analysis Button */}
                <div className="bg-white rounded-xl shadow-md p-6">
                  <button
                    onClick={handleAnalyze}
                    disabled={loading || !selectedFile}
                    className="w-full py-4 bg-gradient-to-r from-blue-600 to-blue-700 text-white rounded-lg font-semibold hover:from-blue-700 hover:to-blue-800 disabled:from-gray-300 disabled:to-gray-400 disabled:cursor-not-allowed transition-all shadow-md flex items-center justify-center gap-2"
                  >
                    {loading ? (
                      <>
                        <Loader className="w-5 h-5 animate-spin" />
                        Analyzing...
                      </>
                    ) : (
                      <>
                        <CheckCircle className="w-5 h-5" />
                        Analyze Image
                      </>
                    )}
                  </button>
                  <p className="text-xs text-gray-500 text-center mt-3">
                    Analysis typically takes 3-10 seconds
                  </p>
                </div>

                {/* Info Box */}
                <div className="bg-blue-50 border border-blue-200 rounded-xl p-4">
                  <h4 className="font-semibold text-blue-900 mb-2">📋 Guidelines</h4>
                  <ul className="text-sm text-blue-800 space-y-1">
                    <li>• Ensure good lighting conditions</li>
                    <li>• Keep camera steady and focused</li>
                    <li>• Capture clear view of the lesion</li>
                    <li>• Avoid shadows and glare</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

