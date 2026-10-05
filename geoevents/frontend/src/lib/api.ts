import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

export const api = axios.create({
  baseURL: `${API_BASE_URL}/api`,
  headers: {
    'Content-Type': 'application/json',
  },
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export async function login(username: string, password: string) {
  const formData = new FormData()
  formData.append('username', username)
  formData.append('password', password)
  const response = await api.post('/auth/login', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
  return response.data
}

export async function register(data: any) {
  const response = await api.post('/auth/register', data)
  return response.data
}

export async function logout() {
  // nothing to do server-side for token-based
}

export async function getCurrentUser() {
  const response = await api.get('/users/me')
  return response.data
}

export async function getEvents(params?: any) {
  const response = await api.get('/events', { params })
  return response.data
}

export async function getEvent(id: string) {
  const response = await api.get(`/events/${id}`)
  return response.data
}

export async function createEvent(data: any) {
  const response = await api.post('/events', data)
  return response.data
}

export async function getCategories() {
  const response = await api.get('/categories')
  return response.data
}

export async function getTags() {
  const response = await api.get('/categories/tags')
  return response.data
}

export async function getVenues() {
  const response = await api.get('/venues')
  return response.data
}

export async function createRsvp(data: { event_id: number; status: string }) {
  const response = await api.post('/rsvps', data)
  return response.data
}

export async function getMyRsvps() {
  const response = await api.get('/rsvps/me')
  return response.data
}

export async function getWishlist() {
  const response = await api.get('/wishlist/me')
  return response.data
}

export async function addToWishlist(eventId: number) {
  const response = await api.post(`/wishlist/events/${eventId}`)
  return response.data
}

export async function removeFromWishlist(eventId: number) {
  const response = await api.delete(`/wishlist/events/${eventId}`)
  return response.data
}

export async function createReview(data: { event_id: number; rating: number; comment?: string }) {
  const response = await api.post('/reviews', data)
  return response.data
}

export async function getEventReviews(eventId: string) {
  const response = await api.get(`/reviews/event/${eventId}`)
  return response.data
}

export async function getDashboardStats() {
  const response = await api.get('/dashboard/stats')
  return response.data
}
