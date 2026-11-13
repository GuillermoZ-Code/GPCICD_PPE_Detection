import type { ReactNode } from 'react'

export type Tone = 'info' | 'success' | 'warning' | 'error'

interface StatusBannerProps {
  tone: Tone
  children: ReactNode
}

export function StatusBanner({ tone, children }: StatusBannerProps) {
  const role = tone === 'error' ? 'alert' : 'status'
  return (
    <p className={`status status--${tone}`} role={role}>
      {children}
    </p>
  )
}
