import { describe, it, expect } from 'vitest'
import { formatKES, isValidKenyanPhone, nextId } from './format'

describe('formatKES', () => {
  it('adds the currency and thousands separators', () => {
    expect(formatKES(82400)).toBe('KES 82,400')
  })
})

describe('isValidKenyanPhone', () => {
  it('accepts local and international formats', () => {
    expect(isValidKenyanPhone('0712 345 678')).toBe(true)
    expect(isValidKenyanPhone('+254712345678')).toBe(true)
    expect(isValidKenyanPhone('0112345678')).toBe(true)
  })
  it('rejects wrong lengths and prefixes', () => {
    expect(isValidKenyanPhone('071234567')).toBe(false)
    expect(isValidKenyanPhone('0212345678')).toBe(false)
    expect(isValidKenyanPhone('')).toBe(false)
  })
})

describe('nextId', () => {
  it('returns one more than the highest id', () => {
    expect(nextId([{ id: 1 }, { id: 4 }])).toBe(5)
    expect(nextId([])).toBe(1)
  })
})
