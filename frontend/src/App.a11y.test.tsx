/** AC-01, AC-02 y AC-03 (HU-080) — accesibilidad de la SPA. */

import { readFileSync } from 'node:fs'
import { resolve } from 'node:path'

import { act, render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { beforeEach, describe, expect, it } from 'vitest'

import { MockDetectorClient, type DetectorClient } from './api/client'
import { App } from './App'
import type { PredictResponse } from './types'

const CSS = readFileSync(resolve(process.cwd(), 'src/design.css'), 'utf-8')

function cssBlock(selector: string): string {
  const start = CSS.indexOf(selector)
  if (start < 0) {
    throw new Error(`no se encontró ${selector}`)
  }
  const open = CSS.indexOf('{', start)
  const close = CSS.indexOf('}', open)
  return CSS.slice(open + 1, close)
}

function tokens(block: string): Record<string, string> {
  const result: Record<string, string> = {}
  for (const match of block.matchAll(/--([a-z0-9-]+)\s*:\s*(#[0-9a-fA-F]{6})/g)) {
    result[match[1]] = match[2]
  }
  return result
}

function luminance(hex: string): number {
  const value = hex.replace('#', '')
  const channels = [0, 2, 4].map((index) => {
    const channel = Number.parseInt(value.slice(index, index + 2), 16) / 255
    return channel <= 0.03928 ? channel / 12.92 : ((channel + 0.055) / 1.055) ** 2.4
  })
  return 0.2126 * channels[0] + 0.7152 * channels[1] + 0.0722 * channels[2]
}

function contrast(foreground: string, background: string): number {
  const first = luminance(foreground)
  const second = luminance(background)
  const lighter = Math.max(first, second)
  const darker = Math.min(first, second)
  return (lighter + 0.05) / (darker + 0.05)
}

const DARK = tokens(cssBlock(':root {'))
const LIGHT = { ...DARK, ...tokens(cssBlock(":root[data-theme='light']")) }

function expectAA(theme: Record<string, string>): void {
  expect(contrast(theme.text, theme.bg)).toBeGreaterThanOrEqual(4.5)
  expect(contrast(theme.text, theme['panel-solid'])).toBeGreaterThanOrEqual(4.5)
  expect(contrast(theme.muted, theme['panel-solid'])).toBeGreaterThanOrEqual(4.5)
  expect(contrast(theme['on-accent'], theme.accent)).toBeGreaterThanOrEqual(4.5)
  for (const name of ['success', 'warning', 'error']) {
    expect(contrast(theme[name], theme['panel-solid'])).toBeGreaterThanOrEqual(3)
  }
}

function pngFile(): File {
  return new File([new Uint8Array([137, 80, 78, 71])], 'foto.png', { type: 'image/png' })
}

class DeferredClient implements DetectorClient {
  private pending: Array<(response: PredictResponse) => void> = []

  detect(): Promise<PredictResponse> {
    return new Promise<PredictResponse>((resolve) => {
      this.pending.push(resolve)
    })
  }

  resolve(response: PredictResponse): void {
    this.pending.shift()?.(response)
  }
}

async function analyze(user: ReturnType<typeof userEvent.setup>): Promise<void> {
  await user.upload(screen.getByLabelText('Archivo'), pngFile())
  await user.click(screen.getByRole('button', { name: 'Analizar imagen' }))
}

beforeEach(() => {
  localStorage.clear()
})

describe('accesibilidad de la SPA (HU-080)', () => {
  it('AC-01 ofrece un enlace para saltar al contenido', () => {
    // Arrange
    render(<App client={new MockDetectorClient()} />)

    // Act
    const skip = screen.getByRole('link', { name: 'Saltar al contenido' })

    // Assert
    expect(skip).toHaveAttribute('href', '#main')
  })

  it('AC-01 mantiene un landmark principal enfocable', () => {
    // Arrange
    render(<App client={new MockDetectorClient()} />)

    // Act
    const main = screen.getByRole('main')

    // Assert
    expect(main).toHaveAttribute('id', 'main')
    expect(main).toHaveAttribute('tabindex', '-1')
  })

  it('AC-01 mueve el foco al título de resultados', async () => {
    // Arrange
    const user = userEvent.setup()
    render(<App client={new MockDetectorClient()} />)

    // Act
    await analyze(user)

    // Assert
    await waitFor(() =>
      expect(screen.getByRole('heading', { name: 'Resultado' })).toHaveFocus(),
    )
  })

  it('AC-01 anuncia los resultados con aria-live', async () => {
    // Arrange
    const user = userEvent.setup()
    render(<App client={new MockDetectorClient()} />)

    // Act
    await analyze(user)
    const summary = await screen.findByRole('region', { name: 'Resumen de detecciones' })

    // Assert
    expect(summary).toHaveAttribute('aria-live', 'polite')
  })

  it('AC-01 marca el panel como ocupado durante la carga', async () => {
    // Arrange
    const user = userEvent.setup()
    const client = new DeferredClient()
    render(<App client={client} />)

    // Act
    await user.upload(screen.getByLabelText('Archivo'), pngFile())
    await user.click(screen.getByRole('button', { name: 'Analizar imagen' }))
    const panel = screen.getByRole('region', { name: 'Resultado' })

    // Assert
    expect(panel).toHaveAttribute('aria-busy', 'true')
    expect(
      screen.getByRole('progressbar', { name: 'Progreso del análisis' }),
    ).toBeInTheDocument()
    await act(async () => {
      client.resolve({ detections: [], image_width: 8, image_height: 6 })
    })
  })

  it('AC-02 cumple contraste AA en el tema oscuro', () => {
    // Arrange / Act / Assert
    expectAA(DARK)
  })

  it('AC-02 cumple contraste AA en el tema claro', () => {
    // Arrange / Act / Assert
    expectAA(LIGHT)
  })

  it('AC-03 expone roles y etiquetas accesibles', async () => {
    // Arrange
    const user = userEvent.setup()
    render(<App client={new MockDetectorClient()} />)

    // Act
    await user.click(screen.getByRole('button', { name: 'Abrir configuración' }))
    const dialog = screen.getByRole('dialog', { name: 'Configuración' })
    await waitFor(() =>
      expect(screen.getByRole('button', { name: 'Cerrar' })).toHaveFocus(),
    )
    await user.keyboard('{Escape}')
    await analyze(user)
    const table = await screen.findByRole('table', { name: 'Detecciones encontradas' })

    // Assert
    expect(dialog).toBeInTheDocument()
    expect(table).toBeInTheDocument()
    expect(screen.getByLabelText('Archivo')).toBeInTheDocument()
    expect(screen.getByRole('region', { name: 'Resumen de detecciones' })).toBeInTheDocument()
    expect(screen.getByRole('region', { name: 'Leyenda por clase' })).toBeInTheDocument()
  })
})
