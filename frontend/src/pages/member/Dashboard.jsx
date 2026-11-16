import { useEffect, useState } from 'react'
import AppShell from '../../components/AppShell'
import StatCard from '../../components/StatCard'
import StatusTag from '../../components/StatusTag'
import { currentUser } from '../../api/auth'
import { getSavingsSummary, getLedgerJournal } from '../../api/deposits'
import { formatKES } from '../../utils/format'

export default function MemberDashboard() {
  const user = currentUser()
  const firstName = (user.name || 'Member').split(' ')[0]

  const [summary, setSummary] = useState(null)
  const [deposits, setDeposits] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    async function loadData() {
      if (!user.id) {
        setLoading(false)
        return
      }
      try {
        setLoading(true)
        const [sumRes, ledRes] = await Promise.all([
          getSavingsSummary(user.id),
          getLedgerJournal(user.id)
        ])
        setSummary(sumRes)
        setDeposits(ledRes.slice(0, 5))
        setError('')
      } catch (err) {
        setError(err.message || 'Failed to retrieve account data.')
      } finally {
        setLoading(false)
      }
    }
    loadData()
  }, [user.id])

  return (
    <AppShell title={`Good morning, ${firstName}`}>
      {error && <p className="form-error" role="alert">{error}</p>}
      <div className="grid3">
        <StatCard
          label="My savings balance"
          value={loading ? '...' : formatKES(summary?.total_savings || 0)}
          to="/deposits"
        />
        <StatCard
          label="My total shares"
          value={loading ? '...' : formatKES(summary?.total_shares || 0)}
          to="/savings"
        />
        <StatCard
          label="Borrowing limit (3x)"
          value={loading ? '...' : formatKES(summary?.borrowing_limit || 0)}
          to="/loans/apply"
        />
      </div>
      <section className="card">
        <div className="card-head">
          <div>
            <h2>My deposits</h2>
            <div className="sub-line">Verified append-only ledger entries</div>
          </div>
        </div>
        {loading ? (
          <p className="sub-line" style={{ padding: '1rem' }}>Loading recent deposits...</p>
        ) : deposits.length === 0 ? (
          <p className="sub-line" style={{ padding: '1rem' }}>No deposits recorded yet.</p>
        ) : (
          <ul className="ledger">
            {deposits.map((d) => (
              <li className="row" key={d.id}>
                <div className="row-main">
                  <b>{d.description || d.transaction_type}</b>
                  <span>{d.timestamp ? new Date(d.timestamp).toLocaleString() : 'Recent'}</span>
                </div>
                <StatusTag status="matched">Verified</StatusTag>
                <div className="row-amt">+{formatKES(d.amount)}</div>
              </li>
            ))}
          </ul>
        )}
      </section>
    </AppShell>
  )
}
