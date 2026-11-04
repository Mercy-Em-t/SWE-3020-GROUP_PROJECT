import { afterEach, beforeEach, describe, it, expect } from 'vitest'
import { cleanup, fireEvent, render, screen } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import LoanApplication from './LoanApplication'

beforeEach(() => {
  localStorage.setItem('user', JSON.stringify({ name: 'Peter Otieno', role: 'member' }))
  render(<MemoryRouter><LoanApplication /></MemoryRouter>)
})
afterEach(() => {
  cleanup()
  localStorage.clear()
})

const submit = () => fireEvent.click(screen.getByRole('button', { name: 'Submit application' }))

describe('LoanApplication', () => {
  it('shows errors when the form is empty', () => {
    submit()
    expect(screen.getByRole('alert').textContent).toContain('Enter the loan amount.')
  })

  it('blocks an amount above the borrowing limit', () => {
    fireEvent.change(screen.getByLabelText('Requested amount (KES)'), { target: { value: '300000' } })
    fireEvent.change(screen.getByLabelText('Guarantor 1'), { target: { value: 'Grace Achieng' } })
    fireEvent.change(screen.getByLabelText('Guarantor 2'), { target: { value: 'Mary Wanjiru' } })
    submit()
    expect(screen.getByRole('alert').textContent).toContain('above your limit')
  })

  it('sends a valid application', () => {
    fireEvent.change(screen.getByLabelText('Requested amount (KES)'), { target: { value: '50000' } })
    fireEvent.change(screen.getByLabelText('Guarantor 1'), { target: { value: 'Grace Achieng' } })
    fireEvent.change(screen.getByLabelText('Guarantor 2'), { target: { value: 'Mary Wanjiru' } })
    submit()
    expect(screen.getByText('Application sent')).toBeTruthy()
  })
})
