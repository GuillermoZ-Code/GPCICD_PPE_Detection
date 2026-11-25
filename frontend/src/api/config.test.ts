/** AC-01 y AC-03 — resolución de la base de la API (HU-072). */

import { afterEach, describe, expect, it, vi } from 'vitest'

import { DEFAULT_API_BASE, resolveApiBaseUrl } from './config'

afterEach(() => {
  vi.unstubAllEnvs()
})

describe('resolveApiBaseUrl', () => {
  it('AC-01: usa /api cuando el valor está vacío', () => {
    // Arrange / Act
    const base = resolveApiBaseUrl('')

    // Assert
    expect(base).toBe('/api')
    expect(DEFAULT_API_BASE).toBe('/api')
  })

  it('AC-01: usa /api cuando el valor no se recibe', () => {
    expect(resolveApiBaseUrl(undefined)).toBe('/api')
  })

  it('AC-01: usa /api cuando el valor solo tiene espacios', () => {
    expect(resolveApiBaseUrl('   \n ')).toBe('/api')
  })

  it('AC-01: usa /api cuando VITE_API_URL está vacía', () => {
    // Arrange
    vi.stubEnv('VITE_API_URL', '')

    // Act / Assert
    expect(resolveApiBaseUrl()).toBe('/api')
  })

  it('AC-03: conserva una URL absoluta explícita', () => {
    expect(resolveApiBaseUrl('http://127.0.0.1:8000')).toBe('http://127.0.0.1:8000')
  })

  it('AC-03: quita las barras finales de la URL', () => {
    expect(resolveApiBaseUrl('http://api.local///')).toBe('http://api.local')
  })
})
