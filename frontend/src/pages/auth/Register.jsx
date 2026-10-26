import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import AuthLayout from '../../components/AuthLayout'
import { register } from '../../api/auth'
import { GROUP_NAME } from '../../config'

export default function Register() {
  const navigate = useNavigate()
  const [form, setForm] = useState({
    fullName: '', nationalId: '', phone: '', password: '', agreed: false,
  })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const update = (field) => (e) =>
    setForm({ ...form, [field]: e.target.type === 'checkbox' ? e.target.checked : e.target.value })

  const handleSubmit = async (event) => {
    event.preventDefault()
    setError('')
    if (!form.fullName.trim() || !form.nationalId.trim() || !form.phone.trim()) {
      setError('Fill in your name, national ID and phone number.')
      return
    }
    if (!form.agreed) {
      setError('Accept the savings constitution and terms to continue.')
      return
    }
    setLoading(true)
    try {
      await register(form)
      navigate('/login')
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <AuthLayout
      heading="Join your savings group in minutes."
      text="Anyone can register as a member. Treasurer and admin access is granted afterwards by an existing admin."
    >
      <form className="auth-card wide" onSubmit={handleSubmit} noValidate>
        <h1>Create your account</h1>
        <p className="lead">Step 1 of 2 · Personal details</p>

        <div className="field-row">
          <div className="field">
            <label htmlFor="fullName">Full name</label>
            <input id="fullName" autoComplete="name" value={form.fullName} onChange={update('fullName')} />
          </div>
          <div className="field">
            <label htmlFor="nationalId">National ID</label>
            <input id="nationalId" inputMode="numeric" value={form.nationalId} onChange={update('nationalId')} />
          </div>
        </div>
        <div className="field-row">
          <div className="field">
            <label htmlFor="phone">Phone number</label>
            <input id="phone" type="tel" autoComplete="tel" value={form.phone} onChange={update('phone')} />
          </div>
          <div className="field">
            <label htmlFor="group">Savings group</label>
            <select id="group" defaultValue={GROUP_NAME}>
              <option>{GROUP_NAME}</option>
            </select>
          </div>
        </div>
        <div className="field">
          <label htmlFor="password">Create password</label>
          <input id="password" type="password" autoComplete="new-password"
            value={form.password} onChange={update('password')} />
        </div>

        <label className="check-row" htmlFor="agreed">
          <input id="agreed" type="checkbox" checked={form.agreed} onChange={update('agreed')} />
          <span>I agree to the group&apos;s savings constitution and the platform&apos;s Terms of Service</span>
        </label>

        {error && <p className="form-error" role="alert">{error}</p>}

        <button className="btn primary" type="submit" disabled={loading}>
          {loading ? 'Creating account…' : 'Continue'}
        </button>
        <p className="foot-note">Already registered? <Link to="/login">Log in</Link></p>
      </form>
    </AuthLayout>
  )
}
