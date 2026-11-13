/** AC-007.1, AC-007.3 y AC-007.4 — flujo completo de la interfaz. */

import { act, fireEvent, render, screen, waitFor, within } from '@testing-library/react'
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

async function analyze(user: ReturnType<typeof userEvent.setup>, file = pngFile()) {
  await user.upload(screen.getByLabelText('Archivo'), file)
  await user.click(screen.getByRole('button', { name: 'Analizar imagen' }))
}

class SpyClient implements DetectorClient {
  conf: number | undefined

  async detect(_file: File, conf?: number): Promise<PredictResponse> {
    this.conf = conf
    return {
      detections: [],
      image_width: 8,
      image_height: 6,
      model_version: 'spy-1.0',
      elapsed_ms: 1,
    }
  }
}

const helmet: PredictResponse['detections'][number] = {
  class_id: 3,
  class_name: 'helmet',
  confidence: 0.9,
  bbox: [1, 2, 30, 40],
  image_width: 100,
  image_height: 100,
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

class FailingClient implements DetectorClient {
  async detect(): Promise<PredictResponse> {
    throw new Error('la API no responde')
  }
}

class FlakyClient implements DetectorClient {
  calls = 0

  async detect(): Promise<PredictResponse> {
    this.calls += 1
    if (this.calls === 1) {
      throw new Error('fallo temporal')
    }
    return { detections: [helmet], image_width: 100, image_height: 100 }
  }
}

beforeEach(() => {
  localStorage.clear()
})

describe('App', () => {
  it('deshabilita el análisis hasta que haya una imagen', () => {
    // Arrange / Act
    render(<App client={new MockDetectorClient()} />)

    // Assert
    expect(screen.getByRole('button', { name: 'Analizar imagen' })).toBeDisabled()
  })

  it('muestra las detecciones de una imagen válida', async () => {
    // Arrange
    const user = userEvent.setup()
    render(<App client={new MockDetectorClient()} />)

    // Act
    await analyze(user)

    // Assert
    const table = await screen.findByRole('table')
    expect(within(table).getByText('Casco')).toBeInTheDocument()
    expect(within(table).getByText('Chaleco')).toBeInTheDocument()
    expect(within(table).getByText('Guantes')).toBeInTheDocument()
    expect(screen.getByText('3')).toBeInTheDocument()
    expect(screen.getByRole('img', { name: 'Imagen analizada: foto.png' })).toBeInTheDocument()
    expect(screen.getByText('mock-1.0.0')).toBeInTheDocument()
  })

  it('envía el umbral del modelo al cliente', async () => {
    // Arrange
    const user = userEvent.setup()
    const spy = new SpyClient()
    render(<App client={spy} />)

    // Act
    await analyze(user)

    // Assert
    await waitFor(() => expect(spy.conf).toBe(0.25))
  })

  it('informa cuando no hay detecciones sin tratarlo como error', async () => {
    // Arrange
    const user = userEvent.setup()
    render(<App client={new MockDetectorClient([])} />)

    // Act
    await analyze(user)

    // Assert
    expect(await screen.findByText(/No se detectaron EPP en la imagen/)).toBeInTheDocument()
    expect(screen.queryByRole('alert')).not.toBeInTheDocument()
  })

  it('rechaza un archivo inválido y sigue disponible', async () => {
    // Arrange
    render(<App client={new MockDetectorClient()} />)
    const invalid = new File(['texto'], 'nota.txt', { type: 'text/plain' })

    // Act
    fireEvent.drop(dropzone(), { dataTransfer: { files: [invalid] } })

    // Assert
    expect(await screen.findByRole('alert')).toHaveTextContent(
      'Formato no admitido. Usa JPEG (jpg, jpeg, jfif) o PNG; AVIF no está soportado.',
    )
    expect(screen.getByLabelText('Archivo')).not.toBeDisabled()
  })

  it('abre el panel de configuración', async () => {
    // Arrange
    const user = userEvent.setup()
    render(<App client={new MockDetectorClient()} />)

    // Act
    await user.click(screen.getByRole('button', { name: 'Abrir configuración' }))

    // Assert
    expect(screen.getByRole('dialog', { name: 'Configuración' })).toBeInTheDocument()
    expect(screen.getByText(/Umbral del modelo/)).toBeInTheDocument()
    expect(screen.getByText(/Confianza visual/)).toBeInTheDocument()
  })

  it('cambia entre tema claro y oscuro', async () => {
    // Arrange
    const user = userEvent.setup()
    render(<App client={new MockDetectorClient()} />)
    const initial = document.documentElement.dataset.theme

    // Act
    await user.click(screen.getByRole('button', { name: 'Cambiar tema' }))

    // Assert
    expect(document.documentElement.dataset.theme).not.toBe(initial)
  })

  it('muestra el enlace al código fuente y la atribución del dataset', () => {
    // Arrange / Act
    render(<App client={new MockDetectorClient()} />)

    // Assert
    expect(screen.getByRole('link', { name: 'Código fuente' })).toHaveAttribute(
      'href',
      'https://github.com/GuillermoZ-Code/GPCICD_PPE_Detection',
    )
    expect(screen.getByText(/CC-BY-4.0/)).toBeInTheDocument()
  })

  it('muestra el estado de carga mientras espera la inferencia', async () => {
    // Arrange
    const user = userEvent.setup()
    const client = new DeferredClient()
    render(<App client={client} />)

    // Act
    await analyze(user)

    // Assert
    expect(screen.getByRole('status')).toHaveTextContent('Analizando imagen…')
    await act(async () => {
      client.resolve({ detections: [], image_width: 100, image_height: 100 })
    })
    expect(await screen.findByText(/No se detectaron EPP/)).toBeInTheDocument()
  })

  it('muestra el error del cliente y deja la interfaz disponible', async () => {
    // Arrange
    const user = userEvent.setup()
    render(<App client={new FailingClient()} />)

    // Act
    await analyze(user)

    // Assert
    expect(await screen.findByRole('alert')).toHaveTextContent(
      'No se pudo completar el análisis. la API no responde',
    )
    expect(screen.getByLabelText('Archivo')).not.toBeDisabled()
  })

  it('permite reintentar el análisis después de un error', async () => {
    // Arrange
    const user = userEvent.setup()
    const client = new FlakyClient()
    render(<App client={client} />)

    // Act
    await analyze(user)
    expect(await screen.findByRole('alert')).toHaveTextContent('fallo temporal')
    await user.click(screen.getByRole('button', { name: 'Analizar imagen' }))

    // Assert
    expect(await screen.findByRole('table')).toBeInTheDocument()
    expect(client.calls).toBe(2)
  })

  it('avisa cuando las detecciones no pasan los filtros visuales', async () => {
    // Arrange
    const user = userEvent.setup()
    render(<App client={new MockDetectorClient()} />)
    await user.click(screen.getByRole('button', { name: 'Abrir configuración' }))
    fireEvent.change(screen.getAllByRole('slider')[1], { target: { value: '99' } })

    // Act
    await user.click(screen.getByRole('button', { name: 'Cerrar' }))
    await analyze(user)

    // Assert
    expect(
      await screen.findByText(/Hay detecciones, pero ninguna pasa los filtros/),
    ).toBeInTheDocument()
    expect(screen.queryByRole('table')).not.toBeInTheDocument()
  })

  it('analiza automáticamente al seleccionar si está configurado', async () => {
    // Arrange
    const user = userEvent.setup()
    render(<App client={new MockDetectorClient()} />)
    await user.click(screen.getByRole('button', { name: 'Abrir configuración' }))
    await user.click(screen.getAllByRole('checkbox')[2])
    await user.click(screen.getByRole('button', { name: 'Cerrar' }))

    // Act
    await user.upload(screen.getByLabelText('Archivo'), pngFile())

    // Assert
    expect(await screen.findByRole('table')).toBeInTheDocument()
  })

  it('cierra la configuración con la tecla Escape', async () => {
    // Arrange
    const user = userEvent.setup()
    render(<App client={new MockDetectorClient()} />)
    await user.click(screen.getByRole('button', { name: 'Abrir configuración' }))
    expect(screen.getByRole('dialog', { name: 'Configuración' })).toBeInTheDocument()

    // Act
    await user.keyboard('{Escape}')

    // Assert
    await waitFor(() =>
      expect(screen.queryByRole('dialog', { name: 'Configuración' })).not.toBeInTheDocument(),
    )
  })

  it('vuelve al tema inicial al alternar dos veces', async () => {
    // Arrange
    const user = userEvent.setup()
    render(<App client={new MockDetectorClient()} />)
    const initial = document.documentElement.dataset.theme

    // Act
    await user.click(screen.getByRole('button', { name: 'Cambiar tema' }))
    const changed = document.documentElement.dataset.theme
    await user.click(screen.getByRole('button', { name: 'Cambiar tema' }))

    // Assert
    expect(changed).not.toBe(initial)
    expect(document.documentElement.dataset.theme).toBe(initial)
  })

  it('habilita las descargas solo cuando hay resultados', async () => {
    // Arrange
    const user = userEvent.setup()
    render(<App client={new MockDetectorClient()} />)
    await user.click(screen.getByRole('button', { name: 'Abrir configuración' }))
    expect(screen.getByRole('button', { name: 'JSON' })).toBeDisabled()

    // Act
    await user.click(screen.getByRole('button', { name: 'Cerrar' }))
    await analyze(user)
    await user.click(screen.getByRole('button', { name: 'Abrir configuración' }))

    // Assert
    expect(screen.getByRole('button', { name: 'JSON' })).toBeEnabled()
    expect(screen.getByRole('button', { name: 'CSV' })).toBeEnabled()
    expect(screen.getByRole('button', { name: 'PNG' })).toBeEnabled()
  })
})
