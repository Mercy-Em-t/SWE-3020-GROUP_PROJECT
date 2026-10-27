import { afterEach, beforeEach, describe, it, expect } from 'vitest'
import { cleanup, render, screen } from '@testing-library/react'
import { MemoryRouter, Route, Routes } from 'react-router-dom'
import ProtectedRoute from './ProtectedRoute'

function renderAt(path) {
  render(
    <MemoryRouter initialEntries={[path]}>
      <Routes>
        <Route path="/login" element={<p>Login page</p>} />
        <Route path="/dashboard" element={<ProtectedRoute role="member"><p>Member home</p></ProtectedRoute>} />
        <Route path="/admin/dashboard" element={<ProtectedRoute role="admin"><p>Admin home</p></ProtectedRoute>} />
      </Routes>
    </MemoryRouter>,
  )
}

beforeEach(() => localStorage.clear())
afterEach(cleanup)

describe('ProtectedRoute', () => {
  it('sends visitors who are not logged in to the login page', () => {
    renderAt('/dashboard')
    expect(screen.getByText('Login page')).toBeTruthy()
  })

  it('keeps a member out of admin pages', () => {
    localStorage.setItem('user', JSON.stringify({ name: 'Peter Otieno', role: 'member' }))
    renderAt('/admin/dashboard')
    expect(screen.getByText('Member home')).toBeTruthy()
    expect(screen.queryByText('Admin home')).toBeNull()
  })

  it('keeps an admin out of member pages', () => {
    localStorage.setItem('user', JSON.stringify({ name: 'Grace Achieng', role: 'admin' }))
    renderAt('/dashboard')
    expect(screen.getByText('Admin home')).toBeTruthy()
  })
})
