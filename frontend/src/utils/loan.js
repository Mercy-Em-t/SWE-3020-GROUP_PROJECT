import { formatKES } from './format'


// This is a UI preview only. The backend calculation is the source of truth.
export const LOAN_MULTIPLIER = 3
export const REQUIRED_GUARANTORS = 2

export function maxLoan(savings, outstanding = 0) {
  return Math.max(0, LOAN_MULTIPLIER * savings - outstanding)
}

export function validateLoan({ amount, savings, outstanding = 0, guarantors = [] }) {
  const errors = []
  const value = Number(amount)
  const limit = maxLoan(savings, outstanding)

  if (!value || value <= 0) {
    errors.push('Enter the loan amount.')
  } else if (value > limit) {
    errors.push(`The amount is above your limit of ${formatKES(limit)}.`)
  }

  const chosen = guarantors.filter(Boolean)
  if (chosen.length < REQUIRED_GUARANTORS) {
    errors.push(`Choose ${REQUIRED_GUARANTORS} guarantors.`)
  } else if (new Set(chosen).size !== chosen.length) {
    errors.push('Each guarantor must be a different member.')
  }
  return errors
}
