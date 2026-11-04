import { useState } from 'react'
import AppShell from '../../components/AppShell'
import Card from '../../components/Card'
import Meter from '../../components/Meter'
import Stepper from '../../components/Stepper'
import { GUARANTORS, MEMBER } from '../../data/mock'
import { formatKES } from '../../utils/format'
import { maxLoan, REQUIRED_GUARANTORS, validateLoan } from '../../utils/loan'

const STEPS = ['Eligibility check', 'Application details', 'Guarantor sign-off', 'Treasurer review']
const PURPOSES = ['School fees', 'Business capital', 'Emergency']
const EMPTY = { amount: '', purpose: PURPOSES[0], months: '12', g1: '', g2: '' }

export default function LoanApplication() {
  const limit = maxLoan(MEMBER.savings, MEMBER.outstanding)
  const [form, setForm] = useState(EMPTY)
  const [errors, setErrors] = useState([])
  const [submitted, setSubmitted] = useState(false)

  const set = (field) => (e) => setForm({ ...form, [field]: e.target.value })
  const chosen = [form.g1, form.g2].filter(Boolean).length
  const usage = limit ? (Number(form.amount) / limit) * 100 : 0

  const handleSubmit = (event) => {
    event.preventDefault()
    const problems = validateLoan({
      amount: form.amount,
      savings: MEMBER.savings,
      outstanding: MEMBER.outstanding,
      guarantors: [form.g1, form.g2],
    })
    setErrors(problems)
    if (problems.length === 0) setSubmitted(true)
  }

  const reset = () => {
    setForm(EMPTY)
    setErrors([])
    setSubmitted(false)
  }

  return (
    <AppShell title="Loan application" subtitle="Instant eligibility · guarantor-backed">
      <Stepper steps={STEPS} current={submitted ? 2 : 1} />

      <div className="loan-grid">
        <div className="loan-box">
          <span>My eligible amount</span>
          <b>{formatKES(limit)}</b>
          <Meter value={usage} label="Requested amount compared with your limit" />
          <span>3 times my savings</span>
        </div>
        <div className="loan-box">
          <span>Guarantors chosen</span>
          <b>{chosen} / {REQUIRED_GUARANTORS}</b>
          <Meter value={(chosen / REQUIRED_GUARANTORS) * 100} tone="amber" label="Guarantors chosen" />
          <span>Fellow members who vouch for you</span>
        </div>
        <div className="loan-box">
          <span>Repayment period</span>
          <b>{form.months} months</b>
          <Meter value={(Number(form.months) / 24) * 100} tone="grey" label="Repayment period" />
          <span>Standard SACCO term</span>
        </div>
      </div>

      {submitted ? (
        <Card title="Application sent">
          <p className="notice" role="status">
            Your request for {formatKES(form.amount)} was sent. Your guarantors will be asked to
            sign off, then the treasurer will review it.
          </p>
          <button type="button" className="btn-sm ghost" onClick={reset}>Start another application</button>
        </Card>
      ) : (
        <Card title="Application details">
          <form onSubmit={handleSubmit} noValidate>
            <div className="field-row">
              <div className="field">
                <label htmlFor="amount">Requested amount (KES)</label>
                <input id="amount" inputMode="numeric" value={form.amount} onChange={set('amount')} />
              </div>
              <div className="field">
                <label htmlFor="purpose">Purpose</label>
                <select id="purpose" value={form.purpose} onChange={set('purpose')}>
                  {PURPOSES.map((p) => <option key={p}>{p}</option>)}
                </select>
              </div>
            </div>
            <div className="field-row three">
              <div className="field">
                <label htmlFor="months">Repayment period</label>
                <select id="months" value={form.months} onChange={set('months')}>
                  <option value="6">6 months</option>
                  <option value="12">12 months</option>
                  <option value="24">24 months</option>
                </select>
              </div>
              <div className="field">
                <label htmlFor="g1">Guarantor 1</label>
                <select id="g1" value={form.g1} onChange={set('g1')}>
                  <option value="">Select a member</option>
                  {GUARANTORS.map((g) => <option key={g}>{g}</option>)}
                </select>
              </div>
              <div className="field">
                <label htmlFor="g2">Guarantor 2</label>
                <select id="g2" value={form.g2} onChange={set('g2')}>
                  <option value="">Select a member</option>
                  {GUARANTORS.map((g) => <option key={g}>{g}</option>)}
                </select>
              </div>
            </div>

            {errors.length > 0 && (
              <ul className="form-error-list" role="alert">
                {errors.map((e) => <li key={e}>{e}</li>)}
              </ul>
            )}

            <button type="submit" className="btn-sm primary">Submit application</button>
          </form>
        </Card>
      )}
    </AppShell>
  )
}
