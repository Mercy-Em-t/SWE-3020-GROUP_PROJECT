export default function Stepper({ steps, current }) {
  return (
    <ol className="stepper" aria-label="Progress">
      {steps.map((label, i) => {
        const state = i < current ? 'done' : i === current ? 'now' : ''
        return (
          <li key={label} className={`step ${state}`} aria-current={state === 'now' ? 'step' : undefined}>
            <span className="n">{state === 'done' ? '✓' : i + 1}</span>
            <span>{label}</span>
          </li>
        )
      })}
    </ol>
  )
}
