import AppShell from '../../components/AppShell'
import Card from '../../components/Card'
import DataTable from '../../components/DataTable'
import { MEMBER_DEPOSITS, MEMBER_STATEMENTS } from '../../data/mock'
import { downloadCsv } from '../../utils/download'

const download = (statement) =>
  downloadCsv(`${statement.title}.csv`, [
    ['Date', 'Reference', 'Amount (KES)'],
    ...MEMBER_DEPOSITS.map((d) => [d.date, d.ref, d.amount]),
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

export default function Statements() {
  return (
    <AppShell title="My statements" subtitle="Your personal transaction statements">
      <Card>
        <DataTable columns={columns} rows={MEMBER_STATEMENTS} />
      </Card>
    </AppShell>
  )
}
