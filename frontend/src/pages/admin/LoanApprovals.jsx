import { useState } from 'react'
import AppShell from '../../components/AppShell'
import Card from '../../components/Card'
import DataTable from '../../components/DataTable'
import StatusTag from '../../components/StatusTag'
import { LOAN_REQUESTS } from '../../data/mock'
import { formatKES } from '../../utils/format'

const LABELS = { pending: 'Pending', approved: 'Approved', rejected: 'Rejected' }

export default function LoanApprovals() {
  const [loans, setLoans] = useState(LOAN_REQUESTS)
  const decide = (id, status) =>
    setLoans(loans.map((loan) => (loan.id === id ? { ...loan, status } : loan)))
  const waiting = loans.filter((l) => l.status === 'pending').length

  const columns = [
    { key: 'member', label: 'Member' },
    { key: 'amount', label: 'Amount', render: (r) => <span className="mono">{formatKES(r.amount)}</span> },
    { key: 'purpose', label: 'Purpose' },
    {
      key: 'guarantors',
      label: 'Guarantors',
      render: (r) => (
        <StatusTag status={r.guarantors === 2 ? 'active' : 'review'}>{r.guarantors} / 2 confirmed</StatusTag>
      ),
    },
    { key: 'status', label: 'Status', render: (r) => <StatusTag status={r.status}>{LABELS[r.status]}</StatusTag> },
    {
      key: 'decision',
      label: 'Decision',
      render: (r) => {
        if (r.status !== 'pending') return null
        if (r.guarantors < 2) return <span className="sub-line">Awaiting guarantor</span>
        return (
          <span className="actions">
            <button type="button" className="btn-sm primary" aria-label={`Approve loan for ${r.member}`}
              onClick={() => decide(r.id, 'approved')}>Approve</button>
            <button type="button" className="btn-sm reject" aria-label={`Reject loan for ${r.member}`}
              onClick={() => decide(r.id, 'rejected')}>Reject</button>
          </span>
        )
      },
    },
  ]

  return (
    <AppShell title="Loan approvals" subtitle={`${waiting} requests awaiting decision`}>
      <Card>
        <DataTable columns={columns} rows={loans} />
      </Card>
    </AppShell>
  )
}
