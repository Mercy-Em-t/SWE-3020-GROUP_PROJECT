import { useState } from 'react'
import AppShell from '../../components/AppShell'
import Card from '../../components/Card'
import DataTable from '../../components/DataTable'
import StatusTag from '../../components/StatusTag'
import { MEMBER_DEPOSITS } from '../../data/mock'
import { formatKES, isValidKenyanPhone, nextId } from '../../utils/format'

const columns = [
  { key: 'date', label: 'Date' },
  { key: 'ref', label: 'Reference', render: (r) => <span className="mono">{r.ref}</span> },
  { key: 'amount', label: 'Amount', render: (r) => <span className="mono">+{formatKES(r.amount)}</span> },
  {
    key: 'status',
    label: 'Status',
    render: (r) => (
      <StatusTag status={r.status}>{r.status === 'matched' ? 'Matched' : 'Awaiting confirmation'}</StatusTag>
    ),
  },
]

export default function Deposits() {
  const [deposits, setDeposits] = useState(MEMBER_DEPOSITS)
  const [form, setForm] = useState({ amount: '', phone: '' })
  const [error, setError] = useState('')

  const handleSubmit = (event) => {
    event.preventDefault()
    const amount = Number(form.amount)
    if (!amount || amount < 1) return setError('Enter an amount of at least KES 1.')
    if (!isValidKenyanPhone(form.phone)) return setError('Enter a valid Safaricom phone number.')
    setError('')
    // SIMULATION: the real flow sends an M-Pesa prompt via the backend, then waits for the confirmation callback.
    setDeposits([
      { id: nextId(deposits), ref: 'PENDING', date: 'Just now', amount, status: 'pending' },
      ...deposits,
    ])
    setForm({ amount: '', phone: '' })
  }

  return (
    <AppShell title="Deposits" subtitle="Your contributions to the group">
      <div className="grid2">
        <Card title="Deposit history">
          <DataTable columns={columns} rows={deposits} />
        </Card>
        <Card title="Make a deposit" subtitle="You will get a prompt on your phone to enter your PIN">
          <form onSubmit={handleSubmit} noValidate>
            <div className="field">
              <label htmlFor="dep-amount">Amount (KES)</label>
              <input id="dep-amount" inputMode="numeric" value={form.amount}
                onChange={(e) => setForm({ ...form, amount: e.target.value })} />
            </div>
            <div className="field">
              <label htmlFor="dep-phone">M-Pesa phone number</label>
              <input id="dep-phone" type="tel" placeholder="07XX XXX XXX" value={form.phone}
                onChange={(e) => setForm({ ...form, phone: e.target.value })} />
            </div>
            {error && <p className="form-error" role="alert">{error}</p>}
            <button type="submit" className="btn-sm primary">Send payment prompt</button>
            <p className="fine-print">Demo only: no real payment is made until the backend is connected.</p>
          </form>
        </Card>
      </div>
    </AppShell>
  )
}
