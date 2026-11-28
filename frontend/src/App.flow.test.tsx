/** AC-01, AC-02 y AC-03 (HU-077) — flujo de carga, progreso y resultados. */

import { act, fireEvent, render, screen, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { beforeEach, describe, expect, it } from 'vitest'

import { MockDetectorClient, type DetectorClient } from './api/client'
import { App } from './App'
import type { PredictResponse } from './types'

function pngFile(name = 'foto.png'): File {
  return new File([new Uint8Array([137, 80, 78, 71])], name, { type: 'image/png' })
}

function dropzone(): HTMLElement {
  const label = screen.getByText('Arrastra tu imagen aquí')
  const container = label.closest('.dropzone')
  if (!container) {
    throw new Error('No se encontró la zona de arrastre')
  }
  return container as HTMLElement
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

beforeEach(() => {
  localStorage.clear()
})

describe('flujo de carga y resultados (HU-077)', () => {
  it('AC-01 acepta una imagen por arrastre y muestra la vista previa', async () => {
    // Arrange
    render(<App client={new MockDetectorClient()} />)

    // Act
    fireEvent.drop(dropzone(), { dataTransfer: { files: [pngFile()] } })

    // Assert
    expect(await screen.findByAltText('Vista previa: foto.png')).toBeInTheDocument()
    expect(screen.getByText('foto.png')).toBeInTheDocument()
  })

  it('AC-01 acepta una imagen por el selector y muestra la vista previa', async () => {
    // Arrange
    const user = userEvent.setup()
    render(<App client={new MockDetectorClient()} />)

    // Act
    await user.upload(screen.getByLabelText('Archivo'), pngFile('selector.png'))

    // Assert
    expect(await screen.findByAltText('Vista previa: selector.png')).toBeInTheDocument()
  })

  it('AC-01 marca la selección como paso activo', () => {
    // Arrange
    render(<App client={new MockDetectorClient()} />)

    // Act
    const flow = screen.getByRole('list', { name: 'Flujo de análisis' })
    const select = within(flow).getByText('Selección').closest('li')
    const analyze = within(flow).getByText('Análisis').closest('li')

    // Assert
    expect(select).toHaveAttribute('aria-current', 'step')
    expect(analyze).not.toHaveAttribute('aria-current')
  })

  it('AC-01 activa el análisis y muestra progreso', async () => {
    // Arrange
    const user = userEvent.setup()
    const client = new DeferredClient()
    render(<App client={client} />)

    // Act
    await user.upload(screen.getByLabelText('Archivo'), pngFile())
    await user.click(screen.getByRole('button', { name: 'Analizar imagen' }))

    // Assert
    expect(
      screen.getByRole('progressbar', { name: 'Progreso del análisis' }),
    ).toBeInTheDocument()
    const flow = screen.getByRole('list', { name: 'Flujo de análisis' })
    expect(within(flow).getByText('Análisis').closest('li')).toHaveAttribute(
      'aria-current',
      'step',
    )
    await act(async () => {
      client.resolve({ detections: [], image_width: 8, image_height: 6 })
    })
  })

  it('AC-01 mantiene la vista previa durante el análisis', async () => {
    // Arrange
    const user = userEvent.setup()
    const client = new DeferredClient()
    render(<App client={client} />)

    // Act
    await user.upload(screen.getByLabelText('Archivo'), pngFile())
    await user.click(screen.getByRole('button', { name: 'Analizar imagen' }))

    // Assert
    expect(screen.getByAltText('Vista previa: foto.png')).toBeInTheDocument()
    await act(async () => {
      client.resolve({ detections: [], image_width: 8, image_height: 6 })
    })
  })

  it('AC-02 muestra el resumen de detecciones', async () => {
    // Arrange
    const user = userEvent.setup()
    render(<App client={new MockDetectorClient()} />)

    // Act
    await user.upload(screen.getByLabelText('Archivo'), pngFile())
    await user.click(screen.getByRole('button', { name: 'Analizar imagen' }))
    const summary = await screen.findByRole('region', { name: 'Resumen de detecciones' })

    // Assert
    expect(within(summary).getByText('Detecciones')).toBeInTheDocument()
    expect(within(summary).getByText('3')).toBeInTheDocument()
    expect(within(summary).getByText('3 clases')).toBeInTheDocument()
    expect(within(summary).getByText('68 %')).toBeInTheDocument()
    expect(within(summary).getByText('mock-1.0.0')).toBeInTheDocument()
  })

  it('AC-02 muestra la leyenda por clase', async () => {
    // Arrange
    const user = userEvent.setup()
    render(<App client={new MockDetectorClient()} />)

    // Act
    await user.upload(screen.getByLabelText('Archivo'), pngFile())
    await user.click(screen.getByRole('button', { name: 'Analizar imagen' }))
    const legend = await screen.findByRole('region', { name: 'Leyenda por clase' })

    // Assert
    expect(within(legend).getByText('Casco')).toBeInTheDocument()
    expect(within(legend).getByText('Chaleco')).toBeInTheDocument()
    expect(within(legend).getByText('Guantes')).toBeInTheDocument()
    expect(within(legend).getAllByRole('listitem')).toHaveLength(3)
    expect(within(legend).getAllByText('1')).toHaveLength(3)
  })

  it('AC-03 completa el flujo y activa resultados', async () => {
    // Arrange
    const user = userEvent.setup()
    render(<App client={new MockDetectorClient()} />)

    // Act
    await user.upload(screen.getByLabelText('Archivo'), pngFile())
    await user.click(screen.getByRole('button', { name: 'Analizar imagen' }))
    const table = await screen.findByRole('table')

    // Assert
    const flow = screen.getByRole('list', { name: 'Flujo de análisis' })
    expect(within(flow).getByText('Resultados').closest('li')).toHaveAttribute(
      'aria-current',
      'step',
    )
    expect(within(table).getAllByRole('row')).toHaveLength(4)
  })
})
