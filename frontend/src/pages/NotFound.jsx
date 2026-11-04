import { Link } from 'react-router-dom'
import AppShell from '../components/AppShell'
import { currentUser } from '../api/auth'
import { homeFor } from '../config/nav'

export default function NotFound() {
  return (
    <AppShell title="Page not found">
      <p className="sub-line">That page does not exist.</p>
      <Link className="btn-sm primary" to={homeFor(currentUser().role)}>Back to dashboard</Link>
    </AppShell>
  )
}
