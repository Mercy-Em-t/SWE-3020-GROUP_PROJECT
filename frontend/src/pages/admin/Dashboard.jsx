import { useEffect, useState } from 'react'
import AppShell from '../../components/AppShell'
import StatCard from '../../components/StatCard'
import { getGroupSummary } from '../../api/deposits'
import { formatKES } from '../../utils/format'

export default function AdminDashboard() {
  const [summary, setSummary] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    async function fetchSummary() {
      try {
        setLoading(true)
        const data = await getGroupSummary()
        setSummary(data)
        setError('')
      } catch (err) {
        setError(err.message || 'Failed to fetch group summary.')
      } finally {
        setLoading(false)
      }
    }
    fetchSummary()
  }, [])

  return (
    <AppShell title="Group overview">
      {error && <p className="form-error" role="alert">{error}</p>}
      <div className="grid3">
        <StatCard
          label="Group balance"
          value={loading ? 'Loading...' : formatKES(summary?.total_group_savings || 0)}
          to="/admin/deposits"
        />
        <StatCard
          label="Pending loan approvals"
          value={loading ? '...' : String(summary?.pending_loan_approvals ?? 0)}
          to="/admin/loans"
        />
        <StatCard
          label="Total active members"
          value={loading ? '...' : String(summary?.total_members ?? 0)}
          to="/admin/members"
        />
      </div>
    </AppShell>
  )
}
