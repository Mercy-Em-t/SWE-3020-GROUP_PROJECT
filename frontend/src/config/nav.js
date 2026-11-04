export const MEMBER_NAV = [
  { to: '/dashboard', label: 'Dashboard' },
  { to: '/deposits', label: 'Deposits' },
  { to: '/savings', label: 'Savings & Dividends' },
  { to: '/loans/apply', label: 'Loans' },
  { to: '/statements', label: 'Statements' },
]

export const ADMIN_NAV = [
  { to: '/admin/dashboard', label: 'Dashboard' },
  { to: '/admin/deposits', label: 'Deposits & Reconciliation' },
  { group: 'Admin' },
  { to: '/admin/loans', label: 'Loan Approvals' },
  { to: '/admin/members', label: 'Member Register' },
  { to: '/admin/reports', label: 'Audit Trail & Statements' },
]

export const homeFor = (role) => (role === 'admin' ? '/admin/dashboard' : '/dashboard')
