import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useMutation } from '@tanstack/react-query'
import { login, getCurrentUser } from '../lib/api'
import { useAuthStore } from '../lib/authStore'

export default function Login() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const navigate = useNavigate()
  const { setAuth } = useAuthStore()

  const mutation = useMutation({
    mutationFn: () => login(username, password),
    onSuccess: async (data) => {
      const user = await getCurrentUser()
      setAuth(data.access_token, user)
      navigate('/dashboard')
    },
    onError: () => {
      alert('Invalid credentials')
    },
  })

  return (
    <div className="min-h-[calc(100vh-4rem)] flex items-center justify-center bg-gray-50">
      <div className="max-w-md w-full bg-white rounded-lg shadow-sm border p-8">
        <h2 className="text-2xl font-bold text-center text-gray-900 mb-8">Sign In</h2>
        <form onSubmit={(e) => { e.preventDefault(); mutation.mutate() }} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Username</label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md"
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md"
              required
            />
          </div>
          <button type="submit" disabled={mutation.isPending} className="w-full bg-primary-600 text-white py-2 rounded-md hover:bg-primary-700 disabled:opacity-50">
            {mutation.isPending ? 'Signing in...' : 'Sign In'}
          </button>
        </form>
        <p className="mt-4 text-center text-sm text-gray-600">
          Don't have an account? <Link to="/register" className="text-primary-600 hover:underline">Sign up</Link>
        </p>
      </div>
    </div>
  )
}
