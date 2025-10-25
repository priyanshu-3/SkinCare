import { useState } from 'react'
import { useNavigate, useLocation } from 'react-router-dom'
import { 
  LayoutDashboard, 
  History, 
  Settings,
  LogOut,
  ChevronLeft,
  ChevronRight,
  Activity
} from 'lucide-react'

export default function Sidebar({ collapsed, setCollapsed }) {
  const navigate = useNavigate()
  const location = useLocation()

  const menuItems = [
    { icon: LayoutDashboard, label: 'Dashboard', path: '/dashboard' },
    { icon: Activity, label: 'New Analysis', path: '/analysis' },
    { icon: History, label: 'History', path: '/history' },
  ]

  const isActive = (path) => location.pathname === path

  const handleLogout = () => {
    // Add logout logic here
    navigate('/login')
  }

  return (
    <div 
      className={`bg-gradient-to-b from-blue-900 to-blue-800 text-white h-screen fixed left-0 top-0 transition-all duration-300 ${
        collapsed ? 'w-20' : 'w-64'
      } shadow-xl z-50`}
    >
      {/* Header */}
      <div className="p-6 flex items-center justify-between border-b border-blue-700">
        {!collapsed && (
          <div className="flex items-center gap-2">
            <div className="w-10 h-10 bg-white rounded-lg flex items-center justify-center">
              <Activity className="w-6 h-6 text-blue-600" />
            </div>
            <div>
              <h1 className="font-bold text-lg">SkinCare AI</h1>
              <p className="text-xs text-blue-200">Detection System</p>
            </div>
          </div>
        )}
        <button
          onClick={() => setCollapsed(!collapsed)}
          className="p-2 hover:bg-blue-700 rounded-lg transition-colors"
        >
          {collapsed ? <ChevronRight className="w-5 h-5" /> : <ChevronLeft className="w-5 h-5" />}
        </button>
      </div>

      {/* Navigation Menu */}
      <nav className="p-4 space-y-2">
        {menuItems.map((item) => (
          <button
            key={item.path}
            onClick={() => navigate(item.path)}
            className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-all ${
              isActive(item.path)
                ? 'bg-white text-blue-900 shadow-md'
                : 'hover:bg-blue-700 text-white'
            }`}
            title={collapsed ? item.label : ''}
          >
            <item.icon className="w-5 h-5 flex-shrink-0" />
            {!collapsed && <span className="font-medium">{item.label}</span>}
            {isActive(item.path) && !collapsed && (
              <div className="ml-auto w-2 h-2 bg-blue-600 rounded-full"></div>
            )}
          </button>
        ))}
      </nav>

      {/* Bottom Section */}
      <div className="absolute bottom-0 left-0 right-0 p-4 border-t border-blue-700">
        <button
          onClick={() => navigate('/settings')}
          className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg hover:bg-blue-700 transition-colors mb-2 ${
            isActive('/settings') ? 'bg-white text-blue-900' : ''
          }`}
          title={collapsed ? 'Settings' : ''}
        >
          <Settings className="w-5 h-5 flex-shrink-0" />
          {!collapsed && <span className="font-medium">Settings</span>}
        </button>
        <button
          onClick={handleLogout}
          className="w-full flex items-center gap-3 px-4 py-3 rounded-lg hover:bg-red-600 transition-colors text-red-200"
          title={collapsed ? 'Logout' : ''}
        >
          <LogOut className="w-5 h-5 flex-shrink-0" />
          {!collapsed && <span className="font-medium">Logout</span>}
        </button>
      </div>
    </div>
  )
}

