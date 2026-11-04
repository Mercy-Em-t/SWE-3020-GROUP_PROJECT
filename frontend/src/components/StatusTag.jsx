const TONES = { matched: 'green', active: 'green', pending: 'amber', review: 'amber', rejected: 'red' }

export default function StatusTag({ status, children }) {
  const tone = TONES[status] ?? 'amber'
  return <span className={`tag tag-${tone}`}>{children}</span>
}
