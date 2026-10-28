import AppShell from '../../components/AppShell'
import Card from '../../components/Card'
import DataTable from '../../components/DataTable'
import StatCard from '../../components/StatCard'
import { DIVIDENDS, MEMBER, MONTHLY_SAVINGS } from '../../data/mock'
import { formatKES } from '../../utils/format'
import { maxLoan } from '../../utils/loan'

const columns = [
  { key: 'period', label: 'Period' },
  { key: 'amount', label: 'Dividend', render: (r) => <span className="mono">{formatKES(r.amount)}</span> },
  { key: 'status', label: 'Status', render: () => 'Paid' },
]

export default function Savings() {
  const peak = Math.max(...MONTHLY_SAVINGS.map((m) => m.amount))
  return (
    <AppShell title="Savings & dividends">
      <div className="grid3">
        <StatCard label="Savings balance" value={formatKES(MEMBER.savings)} />
        <StatCard label="Accrued dividends" value={formatKES(MEMBER.dividends)} />
        <StatCard label="Borrowing limit" value={formatKES(maxLoan(MEMBER.savings, MEMBER.outstanding))} />
      </div>
      <div className="grid2">
        <Card title="Monthly savings">
          <div className="bars" role="img" aria-label="Savings per month, April to September">
            {MONTHLY_SAVINGS.map((m, i) => (
              <div
                key={m.month}
                className={`b ${i === MONTHLY_SAVINGS.length - 1 ? 'hi' : ''}`}
                style={{ height: `${(m.amount / peak) * 100}%` }}
              >
                <span>{m.month}</span>
              </div>
            ))}
          </div>
        </Card>
        <Card title="Dividend history">
          <DataTable columns={columns} rows={DIVIDENDS} />
        </Card>
      </div>
    </AppShell>
  )
}
