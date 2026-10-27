import { useState } from 'react'
import AppShell from '../../components/AppShell'
import Card from '../../components/Card'
import DataTable from '../../components/DataTable'
import { AUDIT_LOG, GROUP_DEPOSITS, GROUP_STATEMENTS } from '../../data/mock'
import { downloadCsv } from '../../utils/download'
import { nextId } from '../../utils/format'

const download = (statement) =>
  downloadCsv(`${statement.title}.csv`, [
    ['Member', 'Source', 'Reference', 'Amount (KES)'],
    ...GROUP_DEPOSITS.map((d) => [d.member, d.source, d.ref, d.amount]),
  ])

const columns = [
  { key: 'title', label: 'Statement' },
  { key: 'period', label: 'Period', render: (r) => <span className="mono">{r.period}</span> },
  {
    key: 'action',
    label: '',
    render: (r) => (
      <button type="button" className="link-btn green" onClick={() => download(r)}>Download</button>
    ),
  },
]

export default function AuditStatements() {
  const [log, setLog] = useState(AUDIT_LOG)
  const [statements, setStatements] = useState(GROUP_STATEMENTS)

  // The audit log is append-only: entries are only ever added at the top, never edited or removed.
  const generate = () => {
    const month = new Date().toLocaleString('en-US', { month: 'long', year: 'numeric' })
    setStatements([{ id: nextId(statements), title: month, period: 'Current month', type: 'Group summary' }, ...statements])
    setLog([{ id: nextId(log), time: 'Just now', actor: 'G. Achieng', action: `generated the ${month} statement` }, ...log])
  }

  return (
    <AppShell title="Audit trail & statements">
      <div className="grid2">
        <Card title="Audit log" subtitle="Append-only: entries cannot be edited or deleted">
          <ul className="audit-list">
            {log.map((entry) => (
              <li key={entry.id} className="audit-item">
                <span className="h">{entry.time}</span>
                <p><b>{entry.actor}</b> {entry.action}</p>
              </li>
            ))}
          </ul>
        </Card>
        <Card
          title="Generated statements"
          action={<button type="button" className="btn-sm primary" onClick={generate}>Generate statement</button>}
        >
          <DataTable columns={columns} rows={statements} />
        </Card>
      </div>
    </AppShell>
  )
}
