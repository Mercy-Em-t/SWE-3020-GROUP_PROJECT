import { useEffect, useState } from 'react'
import AppShell from '../../components/AppShell'
import Card from '../../components/Card'
import StatCard from '../../components/StatCard'
import DataTable from '../../components/DataTable'
import StatusTag from '../../components/StatusTag'
import { getAllLoans, vetLoan } from '../../api/loans'
import { formatKES } from '../../utils/format'

const LABELS = {
  PENDING: 'Pending',
  pending: 'Pending',
  APPROVED: 'Approved',
  approved: 'Approved',
  REJECTED: 'Rejected',
  rejected: 'Rejected',
  DISBURSED: 'Disbursed',
  disbursed: 'Disbursed',
  CLOSED: 'Closed',
  closed: 'Closed'
}

export default function LoanApprovals() {
  const [loans, setLoans] = useState([])
  const [loading, setLoading] = useState(true)
  const [filter, setFilter] = useState('all') // 'all' | 'pending' | 'approved'
  const [error, setError] = useState('')

  const loadLoans = async () => {
    try {
      setLoading(true)
      const data = await getAllLoans()
      setLoans(data)
      setError('')
    } catch (err) {
      setError(err.message || 'Failed to fetch loan portfolio.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadLoans()
  }, [])

  const decide = async (id, status) => {
    try {
      await vetLoan(id, status)
      // Reload full portfolio to reflect approval status
      loadLoans()
    } catch (err) {
      alert(`Decision error: ${err.message}`)
    }
  }

  const pendingList = loans.filter((l) => (l.status || '').toUpperCase() === 'PENDING')
  const approvedList = loans.filter((l) =>
    ['APPROVED', 'DISBURSED', 'CLOSED'].includes((l.status || '').toUpperCase())
  )
  const totalApprovedVolume = approvedList.reduce((sum, l) => sum + (l.principal_amount || 0), 0)

  const shownLoans = filter === 'pending'
    ? pendingList
    : filter === 'approved'
      ? approvedList
      : loans

  const columns = [
    { key: 'borrower_name', label: 'Member', render: (r) => r.borrower_name || `Member #${r.member_id}` },
    {
      key: 'principal_amount',
      label: 'Principal',
      render: (r) => <span className="mono">{formatKES(r.principal_amount)}</span>,
    },
    {
      key: 'duration_months',
      label: 'Term',
      render: (r) => `${r.duration_months} mo`,
    },
    {
      key: 'total_repayable',
      label: 'Total Repayable',
      render: (r) => <span className="mono">{formatKES(r.total_repayable || 0)}</span>,
    },
    {
      key: 'balance_outstanding',
      label: 'Outstanding',
      render: (r) => (
        <span className="mono" style={{ color: r.balance_outstanding > 0 ? '#f59e0b' : '#10b981' }}>
          {formatKES(r.balance_outstanding ?? r.total_repayable ?? 0)}
        </span>
      ),
    },
    {
      key: 'guarantors',
      label: 'Guarantors',
      render: (r) => {
        const count = r.guarantor_count ?? (r.guarantors ? r.guarantors.length : 0)
        return (
          <StatusTag status={count >= 1 ? 'active' : 'review'}>
            {count} confirmed
          </StatusTag>
        )
      },
    },
    {
      key: 'status',
      label: 'Status',
      render: (r) => {
        const s = (r.status || 'pending').toUpperCase()
        const tagStatus = s === 'APPROVED' || s === 'DISBURSED' || s === 'CLOSED'
          ? 'active'
          : s === 'REJECTED'
            ? 'rejected'
            : 'review'
        return <StatusTag status={tagStatus}>{LABELS[r.status] || r.status}</StatusTag>
      },
    },
    {
      key: 'decision',
      label: 'Action',
      render: (r) => {
        if ((r.status || '').toUpperCase() === 'PENDING') {
          return (
            <span className="actions">
              <button
                type="button"
                className="btn-sm primary"
                aria-label={`Approve loan for ${r.borrower_name || r.member_id}`}
                onClick={() => decide(r.id, 'APPROVED')}
              >
                Approve
              </button>
              <button
                type="button"
                className="btn-sm reject"
                aria-label={`Reject loan for ${r.borrower_name || r.member_id}`}
                onClick={() => decide(r.id, 'REJECTED')}
              >
                Reject
              </button>
            </span>
          )
        }
        return <span className="sub-line" style={{ fontSize: '0.85rem' }}>Decision Recorded</span>
      },
    },
  ]

  return (
    <AppShell title="Loan approvals" subtitle={`${pendingList.length} requests awaiting decision`}>
      {error && <p className="form-error" role="alert">{error}</p>}

      <div className="grid3" style={{ marginBottom: '1.5rem' }}>
        <StatCard
          label="Pending vetting requests"
          value={loading ? '...' : String(pendingList.length)}
        />
        <StatCard
          label="Approved / Active loans"
          value={loading ? '...' : String(approvedList.length)}
        />
        <StatCard
          label="Total capital committed"
          value={loading ? '...' : formatKES(totalApprovedVolume)}
        />
      </div>

      <div className="toolbar" style={{ marginBottom: '1rem', display: 'flex', gap: '0.5rem' }}>
        <button
          type="button"
          className={`btn-sm ${filter === 'all' ? 'primary' : 'ghost'}`}
          onClick={() => setFilter('all')}
        >
          All loans ({loans.length})
        </button>
        <button
          type="button"
          className={`btn-sm ${filter === 'pending' ? 'primary' : 'ghost'}`}
          onClick={() => setFilter('pending')}
        >
          Pending ({pendingList.length})
        </button>
        <button
          type="button"
          className={`btn-sm ${filter === 'approved' ? 'primary' : 'ghost'}`}
          onClick={() => setFilter('approved')}
        >
          Approved & Active ({approvedList.length})
        </button>
      </div>

      <Card title={filter === 'pending' ? 'Pending Applications Queue' : filter === 'approved' ? 'Approved Loans Ledger' : 'All SACCO Loans Portfolio'}>
        {loading ? (
          <p className="sub-line">Loading loan records...</p>
        ) : (
          <DataTable
            columns={columns}
            rows={shownLoans}
            empty="No loans match the current filter."
          />
        )}
      </Card>
    </AppShell>
  )
}
