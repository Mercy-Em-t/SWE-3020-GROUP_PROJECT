export default function Meter({ value, tone = 'green', label }) {
  const pct = Math.max(0, Math.min(100, value))
  return (
    <div className="meter" role="progressbar" aria-label={label}
      aria-valuemin={0} aria-valuemax={100} aria-valuenow={Math.round(pct)}>
      <span className={`fill ${tone}`} style={{ width: `${pct}%` }} />
    </div>
  )
}
