import { NavLink } from 'react-router-dom'
import { APP_NAME } from '../config'

const initials = (name) =>
  name.split(' ').map((part) => part[0]).join('').slice(0, 2).toUpperCase()

export default function Sidebar({ nav, user, onLogout }) {
  return (
    <aside className="side">
      <div className="brand-sm">
        <div className="mark">{APP_NAME[0]}</div>
        <b>{APP_NAME}</b>
      </div>
      <nav className="nav" aria-label="Main">
        {nav.map((item) =>
          item.group ? (
            <div key={item.group} className="nav-group">{item.group}</div>
          ) : (
            <NavLink key={item.to} to={item.to} end>{item.label}</NavLink>
          ),
        )}
      </nav>
      <div className="side-foot">
        <div className="avatar">{initials(user.name)}</div>
        <div className="who">
          <b>{user.name}</b>
          <span>{user.role === 'admin' ? 'Treasurer' : 'Member'}</span>
        </div>
        <button type="button" className="link-btn" onClick={onLogout}>Log out</button>
      </div>
    </aside>
  )
}
