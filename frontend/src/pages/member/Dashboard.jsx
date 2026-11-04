import AppShell from '../../components/AppShell'
import StatCard from '../../components/StatCard'
import StatusTag from '../../components/StatusTag'
import { currentUser } from '../../api/auth'

// Placeholder data. Replace with calls to the backend.
const DEPOSITS = [
  { id: 1, label: 'M-Pesa deposit', when: 'Today, 7:52 AM', amount: '+1,000', status: 'matched' },
  { id: 2, label: 'M-Pesa deposit', when: 'Aug 24', amount: '+1,500', status: 'matched' },
]

export default function MemberDashboard() {
  const firstName = currentUser().name.split(' ')[0]
  return (
    <AppShell title={`Good morning, ${firstName}`}>
      <div className="grid3">
        <StatCard label="My savings balance" value="KES 82,400" />
        <StatCard label="My accrued dividends" value="KES 6,150" />
        <StatCard label="Deposited this month" value="KES 4,000" />
      </div>
      <section className="card">
        <div className="card-head">
          <div>
            <h2>My deposits</h2>
            <div className="sub-line">Synced from your mobile money account</div>
          </div>
        </div>
        <ul className="ledger">
          {DEPOSITS.map((d) => (
            <li className="row" key={d.id}>
              <div className="row-main"><b>{d.label}</b><span>{d.when}</span></div>
              <StatusTag status={d.status}>Matched</StatusTag>
              <div className="row-amt">{d.amount}</div>
            </li>
          ))}
        </ul>
      </section>
    </AppShell>
  )
}
