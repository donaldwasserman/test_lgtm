import { beforeEach, describe, expect, it } from 'vitest'
import { useAuthStore } from './authStore'

describe('authStore', () => {
  beforeEach(() => {
    localStorage.clear()
    useAuthStore.setState({
      isAuthenticated: false,
      user: null,
      token: null,
    })
  })

  it('starts logged out', () => {
    expect(useAuthStore.getState().isAuthenticated).toBe(false)
    expect(useAuthStore.getState().user).toBeNull()
    expect(useAuthStore.getState().token).toBeNull()
  })

  it('setAuth persists token and user', () => {
    const user = { id: 1, username: 'alice', email: 'alice@example.com', role: 'attendee' }
    useAuthStore.getState().setAuth('token123', user)

    const state = useAuthStore.getState()
    expect(state.isAuthenticated).toBe(true)
    expect(state.token).toBe('token123')
    expect(state.user).toEqual(user)
    expect(localStorage.getItem('token')).toBe('token123')
    expect(localStorage.getItem('user')).toBe(JSON.stringify(user))
  })

  it('clearAuth removes token and user', () => {
    const user = { id: 1, username: 'alice', email: 'alice@example.com', role: 'attendee' }
    useAuthStore.getState().setAuth('token123', user)
    useAuthStore.getState().clearAuth()

    const state = useAuthStore.getState()
    expect(state.isAuthenticated).toBe(false)
    expect(state.token).toBeNull()
    expect(state.user).toBeNull()
    expect(localStorage.getItem('token')).toBeNull()
    expect(localStorage.getItem('user')).toBeNull()
  })
})