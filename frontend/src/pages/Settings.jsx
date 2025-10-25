import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import Sidebar from '../components/Sidebar'
import { Settings as SettingsIcon, User, Bell, Lock, Database, Palette, Info } from 'lucide-react'

export default function Settings() {
  const navigate = useNavigate()
  const [collapsed, setCollapsed] = useState(false)
  const [activeTab, setActiveTab] = useState('profile')

  const tabs = [
    { id: 'profile', label: 'Profile', icon: User },
    { id: 'notifications', label: 'Notifications', icon: Bell },
    { id: 'security', label: 'Security', icon: Lock },
    { id: 'data', label: 'Data & Privacy', icon: Database },
    { id: 'appearance', label: 'Appearance', icon: Palette },
    { id: 'about', label: 'About', icon: Info },
  ]

  return (
    <div className="flex h-screen bg-gray-50">
      {/* Sidebar */}
      <Sidebar collapsed={collapsed} setCollapsed={setCollapsed} />

      {/* Main Content */}
      <div className={`flex-1 transition-all duration-300 ${collapsed ? 'ml-20' : 'ml-64'}`}>
        {/* Header */}
        <header className="bg-white shadow-sm border-b border-gray-200">
          <div className="px-8 py-4">
            <div className="flex items-center justify-between">
              <div>
                <h1 className="text-2xl font-bold text-gray-900 flex items-center gap-2">
                  <SettingsIcon className="w-7 h-7 text-blue-600" />
                  Settings
                </h1>
                <p className="text-sm text-gray-600 mt-1">
                  Manage your account and application preferences
                </p>
              </div>
            </div>
          </div>
        </header>

        {/* Content Area */}
        <div className="p-8 overflow-y-auto h-[calc(100vh-88px)]">
          <div className="max-w-6xl mx-auto">
            <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
              {/* Sidebar Tabs */}
              <div className="lg:col-span-1">
                <div className="bg-white rounded-xl shadow-md p-4">
                  <nav className="space-y-1">
                    {tabs.map((tab) => (
                      <button
                        key={tab.id}
                        onClick={() => setActiveTab(tab.id)}
                        className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${
                          activeTab === tab.id
                            ? 'bg-blue-50 text-blue-700 font-medium'
                            : 'text-gray-700 hover:bg-gray-50'
                        }`}
                      >
                        <tab.icon className="w-5 h-5" />
                        <span>{tab.label}</span>
                      </button>
                    ))}
                  </nav>
                </div>
              </div>

              {/* Content Area */}
              <div className="lg:col-span-3">
                <div className="bg-white rounded-xl shadow-md p-6">
                  {activeTab === 'profile' && (
                    <div>
                      <h2 className="text-xl font-bold text-gray-900 mb-6">Profile Settings</h2>
                      <div className="space-y-6">
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-2">
                            Full Name
                          </label>
                          <input
                            type="text"
                            placeholder="Enter your name"
                            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                          />
                        </div>
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-2">
                            Email Address
                          </label>
                          <input
                            type="email"
                            placeholder="your.email@example.com"
                            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                          />
                        </div>
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-2">
                            Role
                          </label>
                          <select className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                            <option>Doctor</option>
                            <option>Nurse</option>
                            <option>Administrator</option>
                            <option>Technician</option>
                          </select>
                        </div>
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-2">
                            Medical License Number
                          </label>
                          <input
                            type="text"
                            placeholder="License number"
                            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                          />
                        </div>
                        <div className="pt-4">
                          <button className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
                            Save Changes
                          </button>
                        </div>
                      </div>
                    </div>
                  )}

                  {activeTab === 'notifications' && (
                    <div>
                      <h2 className="text-xl font-bold text-gray-900 mb-6">Notification Settings</h2>
                      <div className="space-y-4">
                        <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                          <div>
                            <h3 className="font-medium text-gray-900">High Risk Alerts</h3>
                            <p className="text-sm text-gray-600">Get notified about melanoma cases</p>
                          </div>
                          <input type="checkbox" defaultChecked className="w-5 h-5 text-blue-600" />
                        </div>
                        <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                          <div>
                            <h3 className="font-medium text-gray-900">Analysis Complete</h3>
                            <p className="text-sm text-gray-600">Notify when analysis is done</p>
                          </div>
                          <input type="checkbox" defaultChecked className="w-5 h-5 text-blue-600" />
                        </div>
                        <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                          <div>
                            <h3 className="font-medium text-gray-900">Daily Summary</h3>
                            <p className="text-sm text-gray-600">Receive daily analysis summary</p>
                          </div>
                          <input type="checkbox" className="w-5 h-5 text-blue-600" />
                        </div>
                        <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                          <div>
                            <h3 className="font-medium text-gray-900">System Updates</h3>
                            <p className="text-sm text-gray-600">Updates about new features</p>
                          </div>
                          <input type="checkbox" className="w-5 h-5 text-blue-600" />
                        </div>
                      </div>
                    </div>
                  )}

                  {activeTab === 'security' && (
                    <div>
                      <h2 className="text-xl font-bold text-gray-900 mb-6">Security Settings</h2>
                      <div className="space-y-6">
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-2">
                            Current Password
                          </label>
                          <input
                            type="password"
                            placeholder="Enter current password"
                            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                          />
                        </div>
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-2">
                            New Password
                          </label>
                          <input
                            type="password"
                            placeholder="Enter new password"
                            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                          />
                        </div>
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-2">
                            Confirm New Password
                          </label>
                          <input
                            type="password"
                            placeholder="Confirm new password"
                            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                          />
                        </div>
                        <div className="pt-4 border-t">
                          <h3 className="font-medium text-gray-900 mb-4">Two-Factor Authentication</h3>
                          <button className="px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors">
                            Enable 2FA
                          </button>
                        </div>
                      </div>
                    </div>
                  )}

                  {activeTab === 'data' && (
                    <div>
                      <h2 className="text-xl font-bold text-gray-900 mb-6">Data & Privacy</h2>
                      <div className="space-y-6">
                        <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg">
                          <h3 className="font-medium text-blue-900 mb-2">Data Storage</h3>
                          <p className="text-sm text-blue-800">
                            All patient data is encrypted and stored securely on HIPAA-compliant servers.
                          </p>
                        </div>
                        <div className="space-y-4">
                          <h3 className="font-medium text-gray-900">Export Options</h3>
                          <button className="w-full px-4 py-3 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors text-left">
                            <div className="font-medium text-gray-900">Export All Data</div>
                            <div className="text-sm text-gray-600">Download all your analysis records</div>
                          </button>
                          <button className="w-full px-4 py-3 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors text-left">
                            <div className="font-medium text-gray-900">Export Patient Records</div>
                            <div className="text-sm text-gray-600">Download patient information</div>
                          </button>
                        </div>
                        <div className="pt-4 border-t">
                          <h3 className="font-medium text-red-900 mb-2">Danger Zone</h3>
                          <button className="px-6 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors">
                            Delete All Data
                          </button>
                        </div>
                      </div>
                    </div>
                  )}

                  {activeTab === 'appearance' && (
                    <div>
                      <h2 className="text-xl font-bold text-gray-900 mb-6">Appearance</h2>
                      <div className="space-y-6">
                        <div>
                          <h3 className="font-medium text-gray-900 mb-4">Theme</h3>
                          <div className="grid grid-cols-3 gap-4">
                            <button className="p-4 border-2 border-blue-600 rounded-lg bg-white">
                              <div className="w-full h-20 bg-gradient-to-br from-blue-500 to-blue-700 rounded mb-2"></div>
                              <div className="text-sm font-medium">Light (Current)</div>
                            </button>
                            <button className="p-4 border-2 border-gray-300 rounded-lg bg-gray-50 opacity-50 cursor-not-allowed">
                              <div className="w-full h-20 bg-gradient-to-br from-gray-800 to-gray-900 rounded mb-2"></div>
                              <div className="text-sm font-medium">Dark (Soon)</div>
                            </button>
                            <button className="p-4 border-2 border-gray-300 rounded-lg bg-gray-50 opacity-50 cursor-not-allowed">
                              <div className="w-full h-20 bg-gradient-to-br from-blue-500 via-purple-500 to-pink-500 rounded mb-2"></div>
                              <div className="text-sm font-medium">Auto (Soon)</div>
                            </button>
                          </div>
                        </div>
                        <div>
                          <h3 className="font-medium text-gray-900 mb-4">Display Density</h3>
                          <select className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500">
                            <option>Comfortable</option>
                            <option>Compact</option>
                            <option>Spacious</option>
                          </select>
                        </div>
                      </div>
                    </div>
                  )}

                  {activeTab === 'about' && (
                    <div>
                      <h2 className="text-xl font-bold text-gray-900 mb-6">About</h2>
                      <div className="space-y-6">
                        <div className="text-center py-6">
                          <div className="w-20 h-20 bg-blue-600 rounded-2xl flex items-center justify-center mx-auto mb-4">
                            <SettingsIcon className="w-10 h-10 text-white" />
                          </div>
                          <h3 className="text-2xl font-bold text-gray-900 mb-2">SkinCare AI</h3>
                          <p className="text-gray-600 mb-1">Version 2.0.0</p>
                          <p className="text-sm text-gray-500">Detection System</p>
                        </div>
                        <div className="border-t pt-6 space-y-3">
                          <div className="flex justify-between py-2">
                            <span className="text-gray-600">Release Date</span>
                            <span className="font-medium">October 2025</span>
                          </div>
                          <div className="flex justify-between py-2">
                            <span className="text-gray-600">AI Model Version</span>
                            <span className="font-medium">XGBoost Ensemble v3.2</span>
                          </div>
                          <div className="flex justify-between py-2">
                            <span className="text-gray-600">Database</span>
                            <span className="font-medium">SQLite</span>
                          </div>
                          <div className="flex justify-between py-2">
                            <span className="text-gray-600">License</span>
                            <span className="font-medium">Medical Use Only</span>
                          </div>
                        </div>
                        <div className="pt-4 border-t">
                          <button className="w-full px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors">
                            Check for Updates
                          </button>
                        </div>
                        <div className="text-center text-sm text-gray-500">
                          <p>© 2025 SkinCare AI. All rights reserved.</p>
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

