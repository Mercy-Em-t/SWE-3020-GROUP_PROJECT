import { useState } from 'react'
import AppShell from '../../components/AppShell'
import Card from '../../components/Card'
import DataTable from '../../components/DataTable'
import StatCard from '../../components/StatCard'
import StatusTag from '../../components/StatusTag'
import { GROUP_DEPOSITS } from '../../data/mock'
import { formatKES } from '../../utils/format'

export default function Reconciliation() {
  const [deposits, setDeposits] = useState(GROUP_DEPOSITS)
  const reconcile = (id) =>
    setDeposits(deposits.map((d) => (d.id === id ? { ...d, status: 'matched' } : d)))

  const matched = deposits.filter((d) => d.status === 'matched').length
  const open = deposits.length - matched
  const total = deposits.reduce((sum, d) => sum + d.amount, 0)

  const columns = [
    { key: 'member', label: 'From' },
    { key: 'source', label: 'Source' },
    { key: 'ref', label: 'Reference', render: (r) => <span className="mono">{r.ref}</span> },
    { key: 'date', label: 'Date' },
    { key: 'amount', label: 'Amount', render: (r) => <span className="mono">+{formatKES(r.amount)}</span> },
    {
      key: 'status',
      label: 'Status',
      render: (r) => (
        <StatusTag status={r.status}>{r.status === 'matched' ? 'Matched' : 'Reconciling'}</StatusTag>
      ),
    },
    {
      key: 'action',
      label: '',
      render: (r) =>
        r.status === 'pending' ? (
          <button type="button" className="btn-sm ghost" aria-label={`Mark ${r.ref} as reconciled`}
            onClick={() => reconcile(r.id)}>Mark reconciled</button>
        ) : null,
    },
  ]

  return (
    <AppShell title="Deposits & reconciliation" subtitle="Mobile money and bank feeds matched to member records">
      <div className="grid3">
        <StatCard label="Matched" value={String(matched)} />
        <StatCard label="Still reconciling" value={String(open)} />
        <StatCard label="Total received" value={formatKES(total)} />
      </div>
      <Card>
        <DataTable columns={columns} rows={deposits} />
      </Card>
    </AppShell>
  )
}
