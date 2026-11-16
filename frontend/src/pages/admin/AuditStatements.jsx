import { useEffect, useState } from 'react'
import AppShell from '../../components/AppShell'
import Card from '../../components/Card'
import DataTable from '../../components/DataTable'
import { getAuditLogs } from '../../api/loans'
import { getAllTransactions } from '../../api/deposits'
import { downloadCsv } from '../../utils/download'

export default function AuditStatements() {
  const [log, setLog] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const loadLogs = async () => {
    try {
      setLoading(true)
      const data = await getAuditLogs(50)
      setLog(data)
      setError('')
    } catch (err) {
      setError(err.message || 'Failed to fetch audit trail.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadLogs()
  }, [])

  const downloadGroupReport = async () => {
    try {
      const txs = await getAllTransactions(1000)
      downloadCsv(`Group_Financial_Ledger_${new Date().toISOString().slice(0, 10)}.csv`, [
        ['Transaction ID', 'Account', 'Member', 'Type', 'Amount (KES)', 'Balance After (KES)', 'Reference', 'Timestamp'],
        ...txs.map((d) => [
          d.id,
          d.account_id,
          d.member_name || 'N/A',
          d.transaction_type,
          d.amount,
          d.balance_after,
          d.reference_code,
          d.timestamp
        ]),
      ])
    } catch (err) {
      alert(`Report export failed: ${err.message}`)
    }
  }

  const statements = [
    { id: 1, title: 'Comprehensive Group Ledger (CSV)', period: 'All recorded entries' },
    { id: 2, title: 'Current Month Reconciled Statements', period: 'Current Month' }
  ]

  const columns = [
    { key: 'title', label: 'Statement' },
    { key: 'period', label: 'Period', render: (r) => <span className="mono">{r.period}</span> },
    {
      key: 'action',
      label: '',
      render: () => (
        <button type="button" className="link-btn green" onClick={downloadGroupReport}>Download CSV</button>
      ),
    },
  ]

  return (
    <AppShell title="Audit trail & statements">
      {error && <p className="form-error" role="alert">{error}</p>}
      <div className="grid2">
        <Card title="Audit log" subtitle="Immutable, tamper-evident forensic log from backend">
          {loading ? (
            <p className="sub-line">Loading audit records...</p>
          ) : (
            <ul className="audit-list">
              {log.map((entry) => (
                <li key={entry.id} className="audit-item">
                  <span className="h">
                    {entry.timestamp ? new Date(entry.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) : 'N/A'}
                  </span>
                  <p>
                    <b>{entry.actor_email}</b> — {entry.action} [{entry.entity_name} #{entry.entity_id || '-'}]
                    {entry.delta && <span className="sub-line" style={{ display: 'block', fontSize: '0.85em', color: '#666' }}>{entry.delta}</span>}
                  </p>
                </li>
              ))}
            </ul>
          )}
        </Card>
        <Card
          title="Generated statements"
          action={<button type="button" className="btn-sm primary" onClick={downloadGroupReport}>Export Full Ledger</button>}
        >
          <DataTable columns={columns} rows={statements} />
        </Card>
      </div>
    </AppShell>
  )
}
