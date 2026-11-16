import { useEffect, useState } from 'react'
import AppShell from '../../components/AppShell'
import Card from '../../components/Card'
import DataTable from '../../components/DataTable'
import { currentUser } from '../../api/auth'
import { getLedgerJournal } from '../../api/deposits'
import { downloadCsv } from '../../utils/download'
import { formatKES } from '../../utils/format'

export default function Statements() {
  const user = currentUser()
  const [transactions, setTransactions] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function loadData() {
      if (!user.id) {
        setLoading(false)
        return
      }
      try {
        setLoading(true)
        const data = await getLedgerJournal(user.id)
        setTransactions(data)
      } catch (err) {
        console.error(err)
      } finally {
        setLoading(false)
      }
    }
    loadData()
  }, [user.id])

  const downloadPersonalStatement = () => {
    downloadCsv(`Personal_Statement_${user.name || 'Member'}_${new Date().toISOString().slice(0, 10)}.csv`, [
      ['Date', 'Reference', 'Type', 'Amount (KES)', 'Running Balance (KES)', 'Description'],
      ...transactions.map((d) => [
        d.timestamp ? new Date(d.timestamp).toLocaleString() : 'N/A',
        d.reference_code,
        d.transaction_type,
        d.amount,
        d.balance_after,
        d.description || ''
      ]),
    ])
  }

  const columns = [
    {
      key: 'timestamp',
      label: 'Date',
      render: (r) => (r.timestamp ? new Date(r.timestamp).toLocaleDateString() : 'Recent')
    },
    { key: 'reference_code', label: 'Reference', render: (r) => <span className="mono">{r.reference_code}</span> },
    { key: 'transaction_type', label: 'Type' },
    { key: 'amount', label: 'Amount', render: (r) => <span className="mono">+{formatKES(r.amount)}</span> },
    { key: 'balance_after', label: 'Balance After', render: (r) => <span className="mono">{formatKES(r.balance_after)}</span> },
  ]

  return (
    <AppShell
      title="My statements"
      subtitle="Your personal immutable transaction records directly from the ledger"
    >
      <Card
        title="Ledger records"
        action={
          <button
            type="button"
            className="btn-sm primary"
            onClick={downloadPersonalStatement}
            disabled={transactions.length === 0}
          >
            Download CSV Statement
          </button>
        }
      >
        {loading ? (
          <p className="sub-line">Loading transactions...</p>
        ) : (
          <DataTable columns={columns} rows={transactions} empty="No ledger records found." />
        )}
      </Card>
    </AppShell>
  )
}
