export default function Card({ title, subtitle, action, children }) {
  return (
    <section className="card">
      {(title || action) && (
        <div className="card-head">
          <div>
            {title && <h2>{title}</h2>}
            {subtitle && <div className="sub-line">{subtitle}</div>}
          </div>
          {action}
        </div>
      )}
      {children}
    </section>
  )
}
