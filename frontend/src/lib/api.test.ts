import { beforeEach, describe, expect, it, vi } from 'vitest'

const { http } = vi.hoisted(() => ({
  http: {
    post: vi.fn(),
    get: vi.fn(),
    delete: vi.fn(),
    interceptors: { request: { use: vi.fn() } },
  },
}))

vi.mock('axios', () => ({ default: { create: vi.fn(() => http) } }))

import { login, removeFromWishlist, getEvents } from './api'

const authHandler = http.interceptors.request.use.mock.calls[0][0] as (
  config: { headers: Record<string, string> }
) => Record<string, string>

describe('api', () => {
  beforeEach(() => {
    localStorage.clear()
    http.post.mockReset()
    http.get.mockReset()
    http.delete.mockReset()
  })

  it('attaches bearer token when present', () => {
    localStorage.setItem('token', 'token123')
    const config = { headers: {} }
    const result = authHandler(config)
    expect(result.headers.Authorization).toBe('Bearer token123')
  })

  it('does not attach a token when absent', () => {
    const config = { headers: {} }
    const result = authHandler(config)
    expect(result.headers.Authorization).toBeUndefined()
  })

  it('login posts form data to /auth/login', async () => {
    http.post.mockResolvedValue({ data: { access_token: 'token123', token_type: 'bearer' } })

    const result = await login('alice', 'secret123')

    expect(http.post).toHaveBeenCalledTimes(1)
    const [url, body, options] = http.post.mock.calls[0]
    expect(url).toBe('/auth/login')
    expect(body).toBeInstanceOf(FormData)
    expect((body as FormData).get('username')).toBe('alice')
    expect((body as FormData).get('password')).toBe('secret123')
    expect(options.headers['Content-Type']).toBe('multipart/form-data')
    expect(result.access_token).toBe('token123')
  })

  it('getEvents forwards query params', async () => {
    http.get.mockResolvedValue({ data: [{ id: 1 }] })

    const result = await getEvents({ category_id: 3 })

    expect(http.get).toHaveBeenCalledWith('/events', { params: { category_id: 3 } })
    expect(result).toEqual([{ id: 1 }])
  })

  it('removeFromWishlist deletes the event', async () => {
    http.delete.mockResolvedValue({ data: {} })

    await removeFromWishlist(7)

    expect(http.delete).toHaveBeenCalledWith('/wishlist/events/7')
  })
})