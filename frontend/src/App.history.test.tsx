/** AC-01, AC-02 y AC-03 (HU-088) — historial de análisis de la sesión. */

import { render, screen, waitFor, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { beforeEach, describe, expect, it, vi } from 'vitest'

import { MockDetectorClient } from './api/client'
import { App } from './App'
import {
  addHistoryEntry,
  clearHistory,
  HISTORY_KEY,
  loadHistory,
  MAX_HISTORY,
  saveHistory,
  type HistoryEntry,
} from './history'

function pngFile(name = 'foto.png'): File {
  return new File([new Uint8Array([137, 80, 78, 71])], name, { type: 'image/png' })
}

function entry(overrides: Partial<HistoryEntry> = {}): HistoryEntry {
  return {
    id: 'entry-1',
    fileName: 'foto.png',
    analyzedAt: '2026-11-28T00:00:00.000Z',
    modelVersion: 'modelo-1',
    detections: 2,
    classes: [
      { name: 'helmet', count: 1 },
      { name: 'Vest', count: 1 },
    ],
    elapsedMs: 12,
    ...overrides,
  }
}

function historyRegion(): HTMLElement {
  return screen.getByRole('region', { name: 'Historial de la sesión' })
}

async function analyze(
  user: ReturnType<typeof userEvent.setup>,
  file = pngFile(),
): Promise<void> {
  await user.upload(screen.getByLabelText('Archivo'), file)
  await user.click(screen.getByRole('button', { name: 'Analizar imagen' }))
  await waitFor(() => expect(within(historyRegion()).getByText(file.name)).toBeInTheDocument())
}

beforeEach(() => {
  localStorage.clear()
})

describe('historial de la sesión (HU-088)', () => {
  it('AC-02 carga un historial vacío sin storage', () => {
    // Arrange / Act
    const loaded = loadHistory()

    // Assert
    expect(loaded).toEqual([])
  })

  it('AC-02 agrega y recupera el más reciente primero', () => {
    // Arrange
    const first = entry({ id: 'uno', fileName: 'uno.png' })
    const second = entry({ id: 'dos', fileName: 'dos.png' })

    // Act
    addHistoryEntry(first)
    const result = addHistoryEntry(second)

    // Assert
    expect(result.map((item) => item.id)).toEqual(['dos', 'uno'])
    expect(loadHistory().map((item) => item.id)).toEqual(['dos', 'uno'])
  })

  it('AC-02 limita el historial a MAX_HISTORY', () => {
    // Arrange / Act
    for (let index = 0; index < MAX_HISTORY + 2; index += 1) {
      addHistoryEntry(entry({ id: `e-${index}` }))
    }
    const loaded = loadHistory()

    // Assert
    expect(loaded).toHaveLength(MAX_HISTORY)
    expect(loaded[0].id).toBe(`e-${MAX_HISTORY + 1}`)
  })

  it('AC-02 tolera JSON corrupto', () => {
    // Arrange
    localStorage.setItem(HISTORY_KEY, '{')

    // Act / Assert
    expect(loadHistory()).toEqual([])
  })

  it('AC-02 limpia el storage', () => {
    // Arrange
    saveHistory([entry()])

    // Act
    clearHistory()

    // Assert
    expect(localStorage.getItem(HISTORY_KEY)).toBeNull()
    expect(loadHistory()).toEqual([])
  })

  it('AC-02 no llama a fetch al analizar', async () => {
    // Arrange
    const fetchSpy = vi.fn()
    vi.stubGlobal('fetch', fetchSpy)
    const user = userEvent.setup()
    render(<App client={new MockDetectorClient()} />)

    // Act
    await analyze(user)

    // Assert
    expect(fetchSpy).not.toHaveBeenCalled()
    vi.unstubAllGlobals()
  })

  it('AC-01 muestra el estado vacío antes de analizar', () => {
    // Arrange / Act
    render(<App client={new MockDetectorClient()} />)

    // Assert
    expect(within(historyRegion()).getByText(/Aún no hay análisis/)).toBeInTheDocument()
  })

  it('AC-01 lista el análisis con miniatura, conteo y modelo', async () => {
    // Arrange
    const user = userEvent.setup()
    render(<App client={new MockDetectorClient()} />)

    // Act
    await analyze(user)

    // Assert
    const history = historyRegion()
    expect(within(history).getByText('foto.png')).toBeInTheDocument()
    expect(within(history).getByText('3 detecciones · 3 clases')).toBeInTheDocument()
    expect(within(history).getByText('Modelo mock-1.0.0')).toBeInTheDocument()
    expect(within(history).getByAltText('Miniatura de foto.png')).toBeInTheDocument()
  })

  it('AC-01 conserva varios análisis en la lista', async () => {
    // Arrange
    const user = userEvent.setup()
    render(<App client={new MockDetectorClient()} />)

    // Act
    await analyze(user, pngFile('uno.png'))
    await analyze(user, pngFile('dos.png'))

    // Assert
    const history = historyRegion()
    expect(within(history).getAllByRole('listitem')).toHaveLength(2)
    expect(within(history).getByText('dos.png')).toBeInTheDocument()
    expect(within(history).getByText('uno.png')).toBeInTheDocument()
  })

  it('AC-03 limpia el historial desde la interfaz', async () => {
    // Arrange
    const user = userEvent.setup()
    render(<App client={new MockDetectorClient()} />)
    await analyze(user)
    const history = historyRegion()

    // Act
    await user.click(within(history).getByRole('button', { name: 'Limpiar historial' }))

    // Assert
    expect(within(history).getByText(/Aún no hay análisis/)).toBeInTheDocument()
    expect(localStorage.getItem(HISTORY_KEY)).toBeNull()
  })

  it('AC-01 muestra el detalle de clases al seleccionar', async () => {
    // Arrange
    saveHistory([
      entry({
        fileName: 'detalle.png',
        detections: 3,
        classes: [
          { name: 'helmet', count: 2 },
          { name: 'Vest', count: 1 },
        ],
      }),
    ])
    const user = userEvent.setup()
    render(<App client={new MockDetectorClient()} />)
    const history = historyRegion()

    // Act
    await user.click(within(history).getByRole('button', { name: /detalle.png/ }))

    // Assert
    expect(within(history).getByText('Casco')).toBeInTheDocument()
    expect(within(history).getByText('Chaleco')).toBeInTheDocument()
    expect(within(history).getByText('2')).toBeInTheDocument()
  })

  it('AC-03 persiste al remontar', () => {
    // Arrange
    saveHistory([entry({ id: 'persistente', fileName: 'guardada.png' })])
    const first = render(<App client={new MockDetectorClient()} />)

    // Act
    first.unmount()
    render(<App client={new MockDetectorClient()} />)

    // Assert
    expect(within(historyRegion()).getByText('guardada.png')).toBeInTheDocument()
  })
})
