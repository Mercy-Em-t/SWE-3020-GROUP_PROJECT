import { afterEach, describe, it, expect } from 'vitest'
import { cleanup, render, screen } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import MemberDashboard from './member/Dashboard'
import Deposits from './member/Deposits'
import Savings from './member/Savings'
import Statements from './member/Statements'
import AdminDashboard from './admin/Dashboard'
import MemberRegister from './admin/MemberRegister'
import AuditStatements from './admin/AuditStatements'
import Reconciliation from './admin/Reconciliation'
import NotFound from './NotFound'

const MEMBER_PAGES = [MemberDashboard, Deposits, Savings, Statements, NotFound]
const ADMIN_PAGES = [AdminDashboard, MemberRegister, AuditStatements, Reconciliation]

afterEach(() => {
  cleanup()
  localStorage.clear()
})

function renderPage(Page, user) {
  localStorage.setItem('user', JSON.stringify(user))
  render(<MemoryRouter><Page /></MemoryRouter>)
}

describe('every page renders with a heading', () => {
  MEMBER_PAGES.forEach((Page) => {
    it(`member: ${Page.name}`, () => {
      renderPage(Page, { name: 'Peter Otieno', role: 'member' })
      expect(screen.getByRole('heading', { level: 1 })).toBeTruthy()
    })
  })
  ADMIN_PAGES.forEach((Page) => {
    it(`admin: ${Page.name}`, () => {
      renderPage(Page, { name: 'Grace Achieng', role: 'admin' })
      expect(screen.getByRole('heading', { level: 1 })).toBeTruthy()
    })
  })
})
