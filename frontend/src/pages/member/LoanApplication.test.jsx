import { afterEach, beforeEach, describe, it, expect, vi } from 'vitest'
import { cleanup, fireEvent, render, screen } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import LoanApplication from './LoanApplication'
import * as loanApi from '../../api/loans'
import * as depositApi from '../../api/deposits'
import * as memberApi from '../../api/members'

beforeEach(() => {
  vi.spyOn(depositApi, 'getSavingsSummary').mockResolvedValue({
    member_id: 1,
    total_savings: 50000,
    total_shares: 50000,
    borrowing_limit: 150000,
    updated_at: new Date().toISOString()
  })
  vi.spyOn(memberApi, 'getMemberDirectory').mockResolvedValue([
    { id: 2, full_name: 'Grace Achieng' },
    { id: 3, full_name: 'Mary Wanjiru' },
  ])
  vi.spyOn(loanApi, 'applyForLoan').mockResolvedValue({
    id: 101,
    member_id: 1,
    principal_amount: 50000,
    status: 'PENDING'
  })

  localStorage.setItem('user', JSON.stringify({ id: 1, name: 'Peter Otieno', role: 'member' }))
  render(<MemoryRouter><LoanApplication /></MemoryRouter>)
})

afterEach(() => {
  cleanup()
  localStorage.clear()
  vi.restoreAllMocks()
})

const submit = () => fireEvent.click(screen.getByRole('button', { name: /Submit application/i }))

describe('LoanApplication', () => {
  it('shows errors when the form is empty', () => {
    submit()
    expect(screen.getByRole('alert').textContent).toContain('Enter the loan amount.')
  })

  it('blocks an amount above the borrowing limit', async () => {
    fireEvent.change(screen.getByLabelText('Requested amount (KES)'), { target: { value: '300000' } })
    fireEvent.change(screen.getByLabelText('Guarantor 1'), { target: { value: '2' } })
    fireEvent.change(screen.getByLabelText('Guarantor 2'), { target: { value: '3' } })
    submit()
    expect(screen.getByRole('alert').textContent).toContain('above your limit')
  })

  it('sends a valid application', async () => {
    fireEvent.change(screen.getByLabelText('Requested amount (KES)'), { target: { value: '50000' } })
    fireEvent.change(screen.getByLabelText('Guarantor 1'), { target: { value: '2' } })
    fireEvent.change(screen.getByLabelText('Guarantor 2'), { target: { value: '3' } })
    submit()
    expect(await screen.findByText('Application sent')).toBeTruthy()
  })
})
