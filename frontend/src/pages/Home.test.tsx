import { render, screen } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import { describe, expect, it } from 'vitest'
import Home from './Home'

describe('Home', () => {
  it('renders the hero heading', () => {
    render(
      <MemoryRouter>
        <Home />
      </MemoryRouter>
    )

    expect(
      screen.getByRole('heading', { name: /Discover Events Around the World/i })
    ).toBeInTheDocument()
  })

  it('links to events and register', () => {
    render(
      <MemoryRouter>
        <Home />
      </MemoryRouter>
    )

    expect(screen.getByRole('link', { name: /Explore Events/i })).toHaveAttribute('href', '/events')
    expect(screen.getByRole('link', { name: /Get Started/i })).toHaveAttribute('href', '/register')
  })
})