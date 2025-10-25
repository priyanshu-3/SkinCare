import { SignedIn, SignedOut } from '@clerk/clerk-react'
import { Link } from 'react-router-dom'
import { Brain, Shield, Zap, Users } from 'lucide-react'

export default function Home() {
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      {/* Hero Section */}
      <div className="text-center mb-16">
        <h1 className="text-5xl font-bold text-gray-900 mb-6">
          AI-Powered Skin Cancer Detection
        </h1>
        <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
          Advanced machine learning system with XGBoost ensemble, uncertainty
          quantification, and explainable AI for accurate skin lesion analysis
        </p>

        <SignedOut>
          <div className="flex justify-center gap-4">
            <a href="#features" className="btn-primary">
              Learn More
            </a>
            <a href="#" className="btn-secondary">
              View Demo
            </a>
          </div>
        </SignedOut>

        <SignedIn>
          <Link to="/analysis" className="btn-primary inline-block">
            Start Analysis →
          </Link>
        </SignedIn>
      </div>

      {/* Features Grid */}
      <div id="features" className="grid md:grid-cols-2 lg:grid-cols-4 gap-8 mb-16">
        <FeatureCard
          icon={<Brain className="w-8 h-8" />}
          title="XGBoost Ensemble"
          description="Multiple CNN models combined with XGBoost for superior accuracy"
        />
        <FeatureCard
          icon={<Shield className="w-8 h-8" />}
          title="Uncertainty Quantification"
          description="Know when the model is confident or needs expert review"
        />
        <FeatureCard
          icon={<Zap className="w-8 h-8" />}
          title="Explainable AI"
          description="LIME & SHAP visualizations show what influenced predictions"
        />
        <FeatureCard
          icon={<Users className="w-8 h-8" />}
          title="Skin Tone Fair"
          description="Tested and balanced across all skin tones for equity"
        />
      </div>

      {/* Statistics */}
      <SignedIn>
        <div className="card bg-gradient-to-r from-primary-50 to-purple-50 border border-primary-200">
          <div className="grid md:grid-cols-3 gap-8 text-center">
            <div>
              <div className="text-4xl font-bold text-primary-600 mb-2">
                95-97%
              </div>
              <div className="text-gray-600">Target Accuracy</div>
            </div>
            <div>
              <div className="text-4xl font-bold text-primary-600 mb-2">7</div>
              <div className="text-gray-600">Lesion Types Classified</div>
            </div>
            <div>
              <div className="text-4xl font-bold text-primary-600 mb-2">5</div>
              <div className="text-gray-600">AI Innovations Combined</div>
            </div>
          </div>
        </div>
      </SignedIn>

      {/* How It Works */}
      <div className="mt-16">
        <h2 className="text-3xl font-bold text-center mb-12">How It Works</h2>
        <div className="grid md:grid-cols-3 gap-8">
          <StepCard
            number="1"
            title="Upload Image"
            description="Take a photo or upload an existing image of the skin lesion"
          />
          <StepCard
            number="2"
            title="AI Analysis"
            description="Our ensemble model analyzes with uncertainty quantification"
          />
          <StepCard
            number="3"
            title="Get Results"
            description="Receive predictions, confidence scores, and recommendations"
          />
        </div>
      </div>
    </div>
  )
}

function FeatureCard({ icon, title, description }) {
  return (
    <div className="card text-center hover:shadow-xl transition-shadow">
      <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-primary-100 text-primary-600 mb-4">
        {icon}
      </div>
      <h3 className="text-xl font-semibold mb-2">{title}</h3>
      <p className="text-gray-600">{description}</p>
    </div>
  )
}

function StepCard({ number, title, description }) {
  return (
    <div className="relative">
      <div className="flex items-start">
        <div className="flex-shrink-0">
          <div className="flex items-center justify-center w-12 h-12 rounded-full bg-primary-600 text-white text-xl font-bold">
            {number}
          </div>
        </div>
        <div className="ml-4">
          <h3 className="text-lg font-semibold mb-2">{title}</h3>
          <p className="text-gray-600">{description}</p>
        </div>
      </div>
    </div>
  )
}

