import { useEffect, useState } from 'react'
import AppShell from '../../components/AppShell'
import Card from '../../components/Card'
import DataTable from '../../components/DataTable'
import StatusTag from '../../components/StatusTag'
import { currentUser } from '../../api/auth'
import { getLedgerJournal, makeDeposit } from '../../api/deposits'
import { formatKES, isValidKenyanPhone } from '../../utils/format'

const columns = [
  {
    key: 'timestamp',
    label: 'Date',
    render: (r) => (r.timestamp ? new Date(r.timestamp).toLocaleString() : 'Recent')
  },
  { key: 'reference_code', label: 'Reference', render: (r) => <span className="mono">{r.reference_code}</span> },
  { key: 'amount', label: 'Amount', render: (r) => <span className="mono">+{formatKES(r.amount)}</span> },
  {
    key: 'balance_after',
    label: 'Balance After',
    render: (r) => <span className="mono">{formatKES(r.balance_after)}</span>
  },
  {
    key: 'status',
    label: 'Status',
    render: () => <StatusTag status="matched">Verified</StatusTag>,
  },
]

export default function Deposits() {
  const user = currentUser()
  const [deposits, setDeposits] = useState([])
  const [form, setForm] = useState({ amount: '', phone: '' })
  const [loading, setLoading] = useState(true)
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')

  const loadDeposits = async () => {
    if (!user.id) {
      setLoading(false)
      return
    }
    try {
      setLoading(true)
      const data = await getLedgerJournal(user.id)
      setDeposits(data)
      setError('')
    } catch (err) {
      setError(err.message || 'Failed to fetch deposit history.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadDeposits()
  }, [user.id])

  const handleSubmit = async (event) => {
    event.preventDefault()
    setSuccess('')
    const amount = Number(form.amount)
    if (!amount || amount < 1) return setError('Enter an amount of at least KES 1.')
    if (!isValidKenyanPhone(form.phone)) return setError('Enter a valid Safaricom phone number.')
    setError('')

    try {
      setSubmitting(true)
      const res = await makeDeposit(user.id, amount, form.phone.trim(), 'mpesa')
      setSuccess(`Deposit successful! Reference: ${res.reference_code}. New savings balance: ${formatKES(res.new_savings_balance)}`)
      setForm({ amount: '', phone: '' })
      loadDeposits()
    } catch (err) {
      setError(err.message || 'Deposit transaction failed.')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <AppShell title="Deposits" subtitle="Your contributions to the group">
      <div className="grid2">
        <Card title="Deposit history">
          {loading ? (
            <p className="sub-line">Loading transactions...</p>
          ) : (
            <DataTable columns={columns} rows={deposits} empty="No deposits found." />
          )}
        </Card>
        <Card title="Make a deposit" subtitle="Real-time M-Pesa STK push simulation with double-entry ledger settlement">
          {success && <p className="notice" role="status">{success}</p>}
          <form onSubmit={handleSubmit} noValidate>
            <div className="field">
              <label htmlFor="dep-amount">Amount (KES)</label>
              <input
                id="dep-amount"
                inputMode="numeric"
                value={form.amount}
                onChange={(e) => setForm({ ...form, amount: e.target.value })}
              />
            </div>
            <div className="field">
              <label htmlFor="dep-phone">M-Pesa phone number</label>
              <input
                id="dep-phone"
                type="tel"
                placeholder="07XX XXX XXX"
                value={form.phone}
                onChange={(e) => setForm({ ...form, phone: e.target.value })}
              />
            </div>
            {error && <p className="form-error" role="alert">{error}</p>}
            <button type="submit" className="btn-sm primary" disabled={submitting}>
              {submitting ? 'Processing deposit...' : 'Send payment prompt'}
            </button>
            <p className="fine-print">Directly updates your equity shares and double-entry ledger balance.</p>
          </form>
        </Card>
      </div>
    </AppShell>
  )
}
