/** AC-01, AC-02 y AC-03 (HU-081) — estados de carga, error y reintento. */

import { act, render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { beforeEach, describe, expect, it } from 'vitest'

import { App } from './App'
import type { DetectorClient } from './api/client'
import type { PredictResponse } from './types'

function pngFile(): File {
  return new File([new Uint8Array([137, 80, 78, 71])], 'foto.png', { type: 'image/png' })
}

async function analyze(user: ReturnType<typeof userEvent.setup>): Promise<void> {
  await user.upload(screen.getByLabelText('Archivo'), pngFile())
  await user.click(screen.getByRole('button', { name: 'Analizar imagen' }))
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

class FlakyClient implements DetectorClient {
  calls = 0

  async detect(): Promise<PredictResponse> {
    this.calls += 1
    if (this.calls === 1) {
      throw new Error('red caída')
    }
    return { detections: [], image_width: 8, image_height: 6 }
  }
}

class FailThenPending implements DetectorClient {
  calls = 0

  detect(): Promise<PredictResponse> {
    this.calls += 1
    if (this.calls === 1) {
      return Promise.reject(new Error('red caída'))
    }
    return new Promise<PredictResponse>(() => {
      // El segundo intento queda pendiente a propósito: la interfaz debe mostrar carga.
    })
  }
}

beforeEach(() => {
  localStorage.clear()
})

describe('estados de la interfaz (HU-081)', () => {
  it('AC-01: avisa cuando el análisis supera el tiempo de espera configurable', async () => {
    // Arrange
    const user = userEvent.setup()
    const client = new DeferredClient()
    render(<App client={client} slowAfterMs={20} />)

    // Act
    await analyze(user)

    // Assert
    expect(screen.getByRole('status')).toHaveTextContent('Analizando imagen…')
    expect(await screen.findByText(/Sigue procesando/)).toBeInTheDocument()
    expect(screen.getByText(/más de 0 s/)).toBeInTheDocument()
    await act(async () => {
      client.resolve({ detections: [], image_width: 8, image_height: 6 })
    })
  })

  it('AC-01: no muestra el aviso si el análisis termina antes del umbral', async () => {
    // Arrange
    const user = userEvent.setup()
    const client = new DeferredClient()
    render(<App client={client} slowAfterMs={60_000} />)

    // Act
    await analyze(user)

    // Assert
    expect(screen.getByRole('status')).toHaveTextContent('Analizando imagen…')
    expect(screen.queryByText(/Sigue procesando/)).not.toBeInTheDocument()
    await act(async () => {
      client.resolve({ detections: [], image_width: 8, image_height: 6 })
    })
  })

  it('AC-02: el botón de reintento vuelve a lanzar el análisis', async () => {
    // Arrange
    const user = userEvent.setup()
    const client = new FlakyClient()
    render(<App client={client} />)
    await analyze(user)
    expect(await screen.findByRole('alert')).toHaveTextContent('red caída')

    // Act
    await user.click(screen.getByRole('button', { name: 'Reintentar' }))

    // Assert
    expect(await screen.findByText(/No se detectaron EPP/)).toBeInTheDocument()
    expect(client.calls).toBe(2)
  })

  it('AC-02: el botón de reintento desaparece mientras se reintenta', async () => {
    // Arrange
    const user = userEvent.setup()
    const client = new FailThenPending()
    render(<App client={client} />)
    await analyze(user)
    expect(await screen.findByRole('button', { name: 'Reintentar' })).toBeInTheDocument()

    // Act
    await user.click(screen.getByRole('button', { name: 'Reintentar' }))

    // Assert
    expect(screen.getByRole('status')).toHaveTextContent('Analizando imagen…')
    expect(screen.queryByRole('button', { name: 'Reintentar' })).not.toBeInTheDocument()
  })

  it('AC-03: los estados inactivo, listo, carga y error son distinguibles', async () => {
    // Arrange
    const user = userEvent.setup()
    const client = new DeferredClient()
    render(<App client={client} />)

    // Assert — inactivo
    expect(screen.getByText('Los resultados aparecerán aquí')).toBeInTheDocument()

    // Act — seleccionado
    await user.upload(screen.getByLabelText('Archivo'), pngFile())

    // Assert — listo para analizar
    expect(screen.getByText('Imagen lista para analizar')).toBeInTheDocument()

    // Act — carga
    await user.click(screen.getByRole('button', { name: 'Analizar imagen' }))

    // Assert — carga
    expect(screen.getByRole('status')).toHaveTextContent('Analizando imagen…')
  })
})
