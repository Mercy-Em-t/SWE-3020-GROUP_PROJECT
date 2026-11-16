import { afterEach, beforeEach, describe, it, expect } from 'vitest'
import { cleanup, render, screen } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import LoanApprovals from './LoanApprovals'

beforeEach(() => {
  localStorage.setItem('user', JSON.stringify({ name: 'Grace Achieng', role: 'admin' }))
  render(<MemoryRouter><LoanApprovals /></MemoryRouter>)
})

afterEach(() => {
  cleanup()
  localStorage.clear()
})

describe('LoanApprovals', () => {
  it('renders heading and table or loading message', () => {
    const heading = screen.getByRole('heading', { level: 1 })
    expect(heading).toBeTruthy()
    expect(heading.textContent).toContain('Loan approvals')
  })
})
