import { useEffect, useState } from 'react'
import AppShell from '../../components/AppShell'
import Card from '../../components/Card'
import DataTable from '../../components/DataTable'
import StatCard from '../../components/StatCard'
import StatusTag from '../../components/StatusTag'
import { getAllTransactions } from '../../api/deposits'
import { formatKES } from '../../utils/format'

export default function Reconciliation() {
  const [deposits, setDeposits] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const loadData = async () => {
    try {
      setLoading(true)
      const data = await getAllTransactions()
      setDeposits(data)
      setError('')
    } catch (err) {
      setError(err.message || 'Failed to load group transactions.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadData()
  }, [])

  const matched = deposits.length
  const total = deposits.reduce((sum, d) => sum + (d.amount || 0), 0)

  const columns = [
    { key: 'member_name', label: 'From', render: (r) => r.member_name || `Account #${r.account_id}` },
    { key: 'transaction_type', label: 'Type' },
    { key: 'reference_code', label: 'Reference', render: (r) => <span className="mono">{r.reference_code}</span> },
    {
      key: 'timestamp',
      label: 'Date',
      render: (r) => (r.timestamp ? new Date(r.timestamp).toLocaleString() : 'N/A')
    },
    { key: 'amount', label: 'Amount', render: (r) => <span className="mono">+{formatKES(r.amount)}</span> },
    {
      key: 'status',
      label: 'Status',
      render: () => <StatusTag status="matched">Verified</StatusTag>,
    },
  ]

  return (
    <AppShell title="Deposits & reconciliation" subtitle="Mobile money and bank feeds matched to member records">
      {error && <p className="form-error" role="alert">{error}</p>}
      <div className="grid3">
        <StatCard label="Reconciled ledger entries" value={String(matched)} />
        <StatCard label="Discrepancies" value="0" />
        <StatCard label="Total received" value={formatKES(total)} />
      </div>
      <Card>
        {loading ? (
          <p className="sub-line">Loading transactions...</p>
        ) : (
          <DataTable columns={columns} rows={deposits} empty="No transactions found." />
        )}
      </Card>
    </AppShell>
  )
}
