/** AC-01, AC-02 y AC-03 de la HU-079 — vista «Acerca del modelo». */

import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { afterEach, describe, expect, it, vi } from 'vitest'

import type { ReadyResponse } from '../types'
import { ModelInfo } from './ModelInfo'

const SHA = 'E'.repeat(64)

const ready: ReadyResponse = {
  status: 'ready',
  api_version: '0.1.0',
  model_loaded: true,
  model_version: 'yolo11s_clean',
  model_reference: `sha256:${SHA}`,
  model_sha256: SHA,
  model_artifact: '/models/best.pt',
}

function stubFetch(value: ReadyResponse): ReturnType<typeof vi.fn> {
  const fetchMock = vi.fn().mockResolvedValue({
    ok: true,
    status: 200,
    json: () => Promise.resolve(value),
  })
  vi.stubGlobal('fetch', fetchMock)
  return fetchMock
}

afterEach(() => {
  vi.unstubAllGlobals()
})

describe('ModelInfo', () => {
  it('AC-01: consume /health/ready y muestra versión, referencia y SHA256', async () => {
    // Arrange
    const fetchMock = stubFetch(ready)

    // Act
    render(<ModelInfo />)

    // Assert
    expect(await screen.findByText('yolo11s_clean')).toBeInTheDocument()
    expect(screen.getByText(`sha256:${SHA}`)).toBeInTheDocument()
    expect(screen.getByText(SHA)).toBeInTheDocument()
    expect(screen.getByText('0.1.0')).toBeInTheDocument()
    expect(fetchMock.mock.calls[0][0]).toBe('/api/health/ready')
  })

  it('AC-01: usa la base de API configurada sin barras finales', async () => {
    // Arrange
    const fetchMock = stubFetch(ready)

    // Act
    render(<ModelInfo apiBaseUrl="http://api.local///" />)

    // Assert
    expect(await screen.findByText('yolo11s_clean')).toBeInTheDocument()
    expect(fetchMock.mock.calls[0][0]).toBe('http://api.local/health/ready')
  })

  it('AC-02: enlaza el código AGPL y la atribución CC-BY', async () => {
    // Arrange
    stubFetch(ready)

    // Act
    render(<ModelInfo />)

    // Assert
    const code = await screen.findByRole('link', { name: /AGPL/i })
    expect(code).toHaveAttribute(
      'href',
      'https://github.com/GuillermoZ-Code/GPCICD_PPE_Detection',
    )
    const dataset = screen.getByRole('link', { name: /CC-BY/i })
    expect(dataset).toHaveAttribute('href', 'https://huggingface.co/datasets/51ddhesh/PPE_Detection')
  })

  it('AC-03: muestra error y reintenta cuando la API no responde', async () => {
    // Arrange
    const user = userEvent.setup()
    const fetchMock = vi
      .fn()
      .mockRejectedValueOnce(new Error('sin conexión'))
      .mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: () => Promise.resolve(ready),
      })
    vi.stubGlobal('fetch', fetchMock)

    // Act
    render(<ModelInfo />)

    // Assert
    expect(await screen.findByRole('alert')).toHaveTextContent(
      'No se pudo consultar la información del modelo.',
    )
    await user.click(screen.getByRole('button', { name: 'Reintentar' }))
    expect(await screen.findByText('yolo11s_clean')).toBeInTheDocument()
    expect(fetchMock).toHaveBeenCalledTimes(2)
  })
})
