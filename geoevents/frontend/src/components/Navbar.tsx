import { Link } from 'react-router-dom'
import { Calendar, MapPin, User, LogOut } from 'lucide-react'
import { useAuthStore } from '../lib/authStore'
import { logout } from '../lib/api'

export default function Navbar() {
  const { isAuthenticated, user, clearAuth } = useAuthStore()

  const handleLogout = async () => {
    await logout()
    clearAuth()
    window.location.href = '/'
  }

  return (
    <nav className="bg-white shadow-sm border-b">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link to="/" className="flex items-center space-x-2">
              <MapPin className="h-8 w-8 text-primary-600" />
              <span className="text-xl font-bold text-gray-900">GeoEvents</span>
            </Link>
            <div className="hidden md:ml-8 md:flex md:space-x-8">
              <Link to="/events" className="text-gray-700 hover:text-primary-600 px-3 py-2 rounded-md text-sm font-medium">
                Explore Events
              </Link>
              {isAuthenticated && (
                <Link to="/events/create" className="text-gray-700 hover:text-primary-600 px-3 py-2 rounded-md text-sm font-medium">
                  Create Event
                </Link>
              )}
            </div>
          </div>
          <div className="flex items-center space-x-4">
            {isAuthenticated ? (
              <>
                <Link to="/dashboard" className="text-gray-700 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium">
                  Dashboard
                </Link>
                <Link to="/profile" className="text-gray-700 hover:text-gray-900">
                  <User className="h-5 w-5" />
                </Link>
                <button onClick={handleLogout} className="text-gray-700 hover:text-gray-900">
                  <LogOut className="h-5 w-5" />
                </button>
              </>
            ) : (
              <>
                <Link to="/login" className="text-gray-700 hover:text-primary-600 px-3 py-2 rounded-md text-sm font-medium">
                  Login
                </Link>
                <Link to="/register" className="bg-primary-600 text-white hover:bg-primary-700 px-4 py-2 rounded-md text-sm font-medium">
                  Sign Up
                </Link>
              </>
            )}
          </div>
        </div>
      </div>
    </nav>
  )
}
