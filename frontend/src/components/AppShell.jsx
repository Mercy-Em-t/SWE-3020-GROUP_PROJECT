import { useNavigate } from 'react-router-dom'
import Sidebar from './Sidebar'
import { currentUser, logout } from '../api/auth'
import { ADMIN_NAV, MEMBER_NAV } from '../config/nav'
import { GROUP_NAME } from '../config'

export default function AppShell({ title, subtitle, children }) {
  const navigate = useNavigate()
  const user = currentUser()
  const nav = user.role === 'admin' ? ADMIN_NAV : MEMBER_NAV

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <div className="shell">
      <Sidebar nav={nav} user={user} onLogout={handleLogout} />
      <main className="main">
        <header className="pagebar">
          <h1>{title}</h1>
          {subtitle && <div className="sub">{subtitle}</div>}
          <div className="pill-btn">{GROUP_NAME}</div>
        </header>
        {children}
      </main>
    </div>
  )
}
