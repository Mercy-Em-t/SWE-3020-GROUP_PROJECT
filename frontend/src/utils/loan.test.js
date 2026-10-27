import { describe, it, expect } from 'vitest'
import { maxLoan, validateLoan } from './loan'

describe('maxLoan', () => {
  it('is three times savings', () => {
    expect(maxLoan(82400)).toBe(247200)
  })
  it('subtracts loans still outstanding', () => {
    expect(maxLoan(10000, 5000)).toBe(25000)
  })
  it('never goes below zero', () => {
    expect(maxLoan(1000, 9000)).toBe(0)
  })
})

describe('validateLoan', () => {
  const valid = { amount: 50000, savings: 82400, guarantors: ['Grace', 'Mary'] }

  it('accepts a valid application', () => {
    expect(validateLoan(valid)).toEqual([])
  })
  it('requires an amount', () => {
    expect(validateLoan({ ...valid, amount: '' })).toHaveLength(1)
  })
  it('accepts an amount exactly at the limit', () => {
    expect(validateLoan({ ...valid, amount: 247200 })).toEqual([])
  })
  it('rejects an amount above the limit', () => {
    const errors = validateLoan({ ...valid, amount: 247201 })
    expect(errors).toHaveLength(1)
    expect(errors[0]).toContain('limit')
  })
  it('requires two guarantors', () => {
    expect(validateLoan({ ...valid, guarantors: ['Grace', ''] })).toHaveLength(1)
  })
  it('rejects the same guarantor twice', () => {
    expect(validateLoan({ ...valid, guarantors: ['Grace', 'Grace'] })).toHaveLength(1)
  })
})
