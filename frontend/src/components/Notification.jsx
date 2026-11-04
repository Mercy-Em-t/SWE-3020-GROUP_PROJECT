export default function Notifications({ items }) {
  return (
    <ul className="notif-list">
      {items.map((n) => (
        <li key={n.id} className="notif">
          <span className={`nd ${n.tone}`} aria-hidden="true" />
          <div>
            <b>{n.title}</b>
            <span>{n.text}</span>
          </div>
        </li>
      ))}
    </ul>
  )
}
