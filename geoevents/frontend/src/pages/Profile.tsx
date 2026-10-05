import { useQuery } from '@tanstack/react-query'
import { useAuthStore } from '../lib/authStore'
import { getCurrentUser } from '../lib/api'

export default function Profile() {
  const { user } = useAuthStore()
  const { data } = useQuery({
    queryKey: ['me'],
    queryFn: getCurrentUser,
  })

  const userData = data || user

  return (
    <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div className="bg-white rounded-lg shadow-sm border p-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">My Profile</h1>
        <div className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-500 mb-1">Username</label>
            <p className="text-lg text-gray-900">{userData?.username}</p>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-500 mb-1">Email</label>
            <p className="text-lg text-gray-900">{userData?.email}</p>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-500 mb-1">Full Name</label>
            <p className="text-lg text-gray-900">{userData?.full_name || 'Not set'}</p>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-500 mb-1">Role</label>
            <p className="text-lg text-gray-900 capitalize">{userData?.role}</p>
          </div>
        </div>
      </div>
    </div>
  )
}
