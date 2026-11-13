/** AC-007.1 y AC-007.4 — cliente HTTP y simulado de inferencia. */

import { afterEach, describe, expect, it, vi } from 'vitest'

import type { Detection, PredictResponse } from '../types'
import {
  createClient,
  HttpDetectorClient,
  MockDetectorClient,
  MOCK_DETECTIONS,
} from './client'

const response: PredictResponse = {
  detections: [
    {
      class_id: 3,
      class_name: 'helmet',
      confidence: 0.9,
      bbox: [1, 2, 3, 4],
      image_width: 100,
      image_height: 100,
    },
  ],
  image_width: 100,
  image_height: 100,
}

function pngFile(): File {
  return new File([new Uint8Array([1, 2, 3])], 'foto.png', { type: 'image/png' })
}

afterEach(() => {
  vi.unstubAllGlobals()
  vi.unstubAllEnvs()
})

function stubFetch(payload: PredictResponse, status = 200): ReturnType<typeof vi.fn> {
  const fetchMock = vi.fn().mockResolvedValue({
    ok: status < 400,
    status,
    json: () => Promise.resolve(payload),
  })
  vi.stubGlobal('fetch', fetchMock)
  return fetchMock
}

describe('MockDetectorClient', () => {
  it('devuelve las detecciones por defecto', async () => {
    const client = new MockDetectorClient()

    const result = await client.detect(pngFile())

    expect(result.detections).toHaveLength(MOCK_DETECTIONS.length)
    expect(result.detections[0].class_name).toBe('helmet')
  })

  it('no comparte el arreglo entre llamadas', async () => {
    const client = new MockDetectorClient()

    const first = await client.detect(pngFile())
    first.detections.pop()
    const second = await client.detect(pngFile())

    expect(second.detections).toHaveLength(MOCK_DETECTIONS.length)
  })

  it('filtra por el umbral del modelo', async () => {
    const client = new MockDetectorClient()

    const result = await client.detect(pngFile(), 0.8)

    expect(result.detections.map((detection) => detection.class_name)).toEqual(['helmet'])
  })

  it('usa las detecciones personalizadas que recibe', async () => {
    // Arrange
    const custom: Detection[] = [
      {
        class_id: 4,
        class_name: 'mask',
        confidence: 0.66,
        bbox: [10, 10, 40, 40],
        image_width: 320,
        image_height: 240,
      },
    ]

    // Act
    const result = await new MockDetectorClient(custom).detect(pngFile())

    // Assert
    expect(result.detections).toEqual(custom)
  })

  it('copia cada detección para no compartir las cajas', async () => {
    // Arrange
    const original = structuredClone(MOCK_DETECTIONS)
    const client = new MockDetectorClient()
    const first = await client.detect(pngFile())

    // Act
    first.detections[0].bbox[0] = -1

    // Assert
    const second = await client.detect(pngFile())
    expect(second.detections).toEqual(original)
  })

  it('conserva la detección cuando la confianza iguala el umbral', async () => {
    // Arrange
    const client = new MockDetectorClient()

    // Act
    const result = await client.detect(pngFile(), 0.92)

    // Assert
    expect(result.detections.map((detection) => detection.class_name)).toEqual(['helmet'])
  })

  it('devuelve una respuesta vacía con el umbral máximo', async () => {
    // Arrange
    const client = new MockDetectorClient()

    // Act
    const result = await client.detect(pngFile(), 1)

    // Assert
    expect(result.detections).toEqual([])
  })
})

describe('HttpDetectorClient', () => {
  it('envía la imagen a /predict y devuelve la respuesta', async () => {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: true,
      json: () => Promise.resolve(response),
    })
    vi.stubGlobal('fetch', fetchMock)

    const client = new HttpDetectorClient('http://api.local/')
    const result = await client.detect(pngFile(), 0.4)

    expect(result).toEqual(response)
    expect(fetchMock).toHaveBeenCalledTimes(1)
    const [url, init] = fetchMock.mock.calls[0]
    expect(url).toBe('http://api.local/predict')
    expect(init.method).toBe('POST')
    expect(init.body).toBeInstanceOf(FormData)
    expect((init.body as FormData).get('file')).toBeInstanceOf(File)
    expect((init.body as FormData).get('conf')).toBe('0.4')
  })

  it('falla cuando la API responde con error', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn().mockResolvedValue({ ok: false, status: 500, json: () => Promise.resolve({}) }),
    )

    const client = new HttpDetectorClient('http://api.local')

    await expect(client.detect(pngFile())).rejects.toThrow('La API respondió con estado 500.')
  })

  it('omite el campo conf cuando no se indica umbral', async () => {
    // Arrange
    const fetchMock = stubFetch(response)
    const client = new HttpDetectorClient('http://api.local')

    // Act
    await client.detect(pngFile())

    // Assert
    const body = fetchMock.mock.calls[0][1].body as FormData
    expect(body.has('conf')).toBe(false)
    expect(body.get('file')).toBeInstanceOf(File)
  })

  it('normaliza las barras finales de la URL base', async () => {
    // Arrange
    const fetchMock = stubFetch(response)
    const client = new HttpDetectorClient('http://api.local///')

    // Act
    await client.detect(pngFile())

    // Assert
    expect(fetchMock.mock.calls[0][0]).toBe('http://api.local/predict')
  })

  it('propaga el estado HTTP de un error de cliente', async () => {
    // Arrange
    stubFetch(response, 422)
    const client = new HttpDetectorClient('http://api.local')

    // Act / Assert
    await expect(client.detect(pngFile())).rejects.toThrow(
      'La API respondió con estado 422.',
    )
  })

  it('conserva la identidad del modelo en la respuesta', async () => {
    // Arrange
    const payload: PredictResponse = {
      ...response,
      model_version: 'yolo11s_clean',
      model_sha256: 'A'.repeat(64),
      model_reference: `sha256:${'A'.repeat(64)}`,
      elapsed_ms: 87,
    }
    stubFetch(payload)
    const client = new HttpDetectorClient('http://api.local')

    // Act
    const result = await client.detect(pngFile())

    // Assert
    expect(result.model_version).toBe('yolo11s_clean')
    expect(result.model_reference).toBe(`sha256:${'A'.repeat(64)}`)
    expect(result.elapsed_ms).toBe(87)
  })
})

describe('createClient', () => {
  it('usa el cliente simulado sin URL', () => {
    expect(createClient('')).toBeInstanceOf(MockDetectorClient)
  })

  it('usa el cliente HTTP con URL', () => {
    expect(createClient('http://api.local')).toBeInstanceOf(HttpDetectorClient)
  })

  it('ignora una URL con solo espacios', () => {
    expect(createClient('   ')).toBeInstanceOf(MockDetectorClient)
  })

  it('usa VITE_API_URL cuando no recibe argumento', () => {
    // Arrange
    vi.stubEnv('VITE_API_URL', 'http://env.local')

    // Act / Assert
    expect(createClient()).toBeInstanceOf(HttpDetectorClient)
  })
})
