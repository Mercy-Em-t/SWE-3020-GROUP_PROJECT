import { afterEach, describe, it, expect } from 'vitest'
import { cleanup, render, screen } from '@testing-library/react'
import StatusTag from './StatusTag'

afterEach(cleanup)

describe('StatusTag', () => {
  it('shows its label', () => {
    render(<StatusTag status="matched">Matched</StatusTag>)
    expect(screen.getByText('Matched')).toBeTruthy()
  })

  it('uses the green style for matched and the amber style for pending', () => {
    render(
      <>
        <StatusTag status="matched">Matched</StatusTag>
        <StatusTag status="pending">Reconciling</StatusTag>
      </>,
    )
    expect(screen.getByText('Matched').className).toContain('tag-green')
    expect(screen.getByText('Reconciling').className).toContain('tag-amber')
  })
})
