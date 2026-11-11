import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'

import {
  applySettings,
  DEFAULT_SETTINGS,
  loadSettings,
  resolveTheme,
  saveSettings,
} from './config'

beforeEach(() => {
  localStorage.clear()
})

afterEach(() => {
  vi.unstubAllGlobals()
  const root = document.documentElement
  delete root.dataset.theme
  delete root.dataset.accent
  delete root.dataset.bg
  delete root.dataset.density
  delete root.dataset.motion
  delete root.dataset.labels
})

describe('settings', () => {
  it('devuelve los valores por defecto sin almacenamiento', () => {
    expect(loadSettings()).toEqual(DEFAULT_SETTINGS)
  })

  it('guarda y recupera la configuración', () => {
    // Arrange
    const settings = { ...DEFAULT_SETTINGS, theme: 'dark' as const, accent: 'gray' as const }

    // Act
    saveSettings(settings)

    // Assert
    expect(loadSettings()).toEqual(settings)
  })

  it('descarta clases desconocidas al cargar', () => {
    // Arrange
    localStorage.setItem(
      'ppe.settings.v1',
      JSON.stringify({ ...DEFAULT_SETTINGS, classes: ['helmet', 'Bogus'] }),
    )

    // Act
    const settings = loadSettings()

    // Assert
    expect(settings.classes).toEqual(['helmet'])
  })

  it('resuelve el tema del sistema con matchMedia', () => {
    // Arrange
    vi.stubGlobal(
      'matchMedia',
      vi.fn(() => ({ matches: true, addEventListener: vi.fn(), removeEventListener: vi.fn() })),
    )

    // Act / Assert
    expect(resolveTheme('system')).toBe('light')
    expect(resolveTheme('dark')).toBe('dark')
  })

  it('aplica los atributos al documento', () => {
    // Act
    applySettings({
      ...DEFAULT_SETTINGS,
      theme: 'light',
      accent: 'gray',
      background: 'grid',
      thickness: 5,
    })

    // Assert
    const root = document.documentElement
    expect(root.dataset.theme).toBe('light')
    expect(root.dataset.accent).toBe('gray')
    expect(root.dataset.bg).toBe('grid')
    expect(root.style.getPropertyValue('--box-width')).toBe('5px')
  })
})
