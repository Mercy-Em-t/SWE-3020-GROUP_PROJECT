import { useEffect, useState } from 'react'
import AppShell from '../../components/AppShell'
import Card from '../../components/Card'
import DataTable from '../../components/DataTable'
import StatCard from '../../components/StatCard'
import { currentUser } from '../../api/auth'
import { getSavingsSummary, getLedgerJournal } from '../../api/deposits'
import { formatKES } from '../../utils/format'

const columns = [
  { key: 'period', label: 'Period' },
  { key: 'amount', label: 'Dividend / Yield', render: (r) => <span className="mono">{formatKES(r.amount)}</span> },
  { key: 'status', label: 'Status', render: () => 'Accrued' },
]

export default function Savings() {
  const user = currentUser()
  const [summary, setSummary] = useState(null)
  const [recentTransactions, setRecentTransactions] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function fetchAccount() {
      if (!user.id) {
        setLoading(false)
        return
      }
      try {
        setLoading(true)
        const [sRes, lRes] = await Promise.all([
          getSavingsSummary(user.id),
          getLedgerJournal(user.id)
        ])
        setSummary(sRes)
        setRecentTransactions(lRes)
      } catch (err) {
        console.error(err)
      } finally {
        setLoading(false)
      }
    }
    fetchAccount()
  }, [user.id])

  const totalShares = summary?.total_shares || 0
  const totalSavings = summary?.total_savings || 0
  const estimatedDividend = totalShares * 0.08

  const dividends = [
    { id: 1, period: '2026 Annual Projected Yield (8%)', amount: estimatedDividend },
    { id: 2, period: 'Prior Retained Earnings', amount: 0 },
  ]

  return (
    <AppShell title="Savings & dividends">
      <div className="grid3">
        <StatCard label="Savings balance" value={loading ? '...' : formatKES(totalSavings)} to="/deposits" />
        <StatCard label="Total equity shares" value={loading ? '...' : formatKES(totalShares)} />
        <StatCard label="Max borrowing limit (3x)" value={loading ? '...' : formatKES(summary?.borrowing_limit || 0)} to="/loans/apply" />
      </div>
      <div className="grid2">
        <Card title="Recent ledger deposits">
          {loading ? (
            <p className="sub-line">Loading...</p>
          ) : recentTransactions.length === 0 ? (
            <p className="sub-line">No contributions made yet.</p>
          ) : (
            <ul className="audit-list">
              {recentTransactions.slice(0, 6).map((tx) => (
                <li key={tx.id} className="audit-item">
                  <span className="h">{new Date(tx.timestamp).toLocaleDateString()}</span>
                  <p><b>+{formatKES(tx.amount)}</b> via {tx.reference_code}</p>
                </li>
              ))}
            </ul>
          )}
        </Card>
        <Card title="Dividend & return projection">
          <DataTable columns={columns} rows={dividends} />
        </Card>
      </div>
    </AppShell>
  )
}
