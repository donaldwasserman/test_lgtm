import { create } from 'zustand'

interface User {
  id: number
  username: string
  email: string
  full_name?: string
  role: string
}

interface AuthState {
  isAuthenticated: boolean
  user: User | null
  token: string | null
  setAuth: (token: string, user: User) => void
  clearAuth: () => void
}

export const useAuthStore = create<AuthState>((set) => ({
  isAuthenticated: !!localStorage.getItem('token'),
  user: localStorage.getItem('user') ? JSON.parse(localStorage.getItem('user')!) : null,
  token: localStorage.getItem('token'),
  setAuth: (token, user) => {
    localStorage.setItem('token', token)
    localStorage.setItem('user', JSON.stringify(user))
    set({ isAuthenticated: true, token, user })
  },
  clearAuth: () => {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    set({ isAuthenticated: false, token: null, user: null })
  },
}))
