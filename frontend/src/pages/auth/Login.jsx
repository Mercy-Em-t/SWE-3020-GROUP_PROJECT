import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import AuthLayout from '../../components/AuthLayout'
import { login } from '../../api/auth'
import { homeFor } from '../../config/nav'
import { GROUP_NAME } from '../../config'

export default function Login() {
  const navigate = useNavigate()
  const [phone, setPhone] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (event) => {
    event.preventDefault()
    setError('')
    setLoading(true)
    try {
      const user = await login({ phone, password })
      navigate(homeFor(user.role))
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <AuthLayout
      heading="Every deposit, dividend and loan in one shared ledger."
      text="One login, two experiences: members see their own savings; treasurers and admins see the whole group."
    >
      <form className="auth-card" onSubmit={handleSubmit} noValidate>
        <h1>Welcome back</h1>
        <p className="lead">Log in to {GROUP_NAME}</p>

        <div className="field">
          <label htmlFor="phone">Phone number</label>
          <input id="phone" type="tel" autoComplete="tel" placeholder="+254 7XX XXX XXX"
            value={phone} onChange={(e) => setPhone(e.target.value)} />
        </div>
        <div className="field">
          <label htmlFor="password">Password</label>
          <input id="password" type="password" autoComplete="current-password"
            value={password} onChange={(e) => setPassword(e.target.value)} />
        </div>

        {error && <p className="form-error" role="alert">{error}</p>}

        <button className="btn primary" type="submit" disabled={loading}>
          {loading ? 'Logging in…' : 'Log in'}
        </button>
        <button className="btn alt" type="button">Other login options</button>

        <p className="foot-note">New here? <Link to="/register">Create an account</Link></p>
      </form>
    </AuthLayout>
  )
}
