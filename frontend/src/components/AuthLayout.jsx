import { APP_NAME } from '../config'

export default function AuthLayout({ heading, text, children }) {
  return (
    <div className="auth">
      <div className="auth-side">
        <div className="brand">
          <div className="mark">{APP_NAME[0]}</div>
          <b>{APP_NAME}</b>
        </div>
        <div>
          <h2>{heading}</h2>
          <p>{text}</p>
        </div>
        <p className="fine">Bank-grade encryption · mobile money integrated</p>
      </div>
      <div className="auth-form">{children}</div>
    </div>
  )
}
