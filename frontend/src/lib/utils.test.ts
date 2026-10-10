import { describe, expect, it } from 'vitest'
import { cn } from './utils'

describe('cn', () => {
  it('joins class names', () => {
    expect(cn('px-2', 'text-red-500')).toBe('px-2 text-red-500')
  })

  it('merges conflicting tailwind classes (last wins)', () => {
    expect(cn('px-2', 'px-4')).toBe('px-4')
  })

  it('drops falsy values', () => {
    expect(cn('a', false, null, undefined, 0, 'b')).toBe('a b')
  })

  it('handles conditional class strings', () => {
    expect(cn('a', true && 'b', false && 'c')).toBe('a b')
  })
})