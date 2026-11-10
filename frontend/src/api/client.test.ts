import { afterEach, describe, expect, it, vi } from 'vitest'

import type { PredictResponse } from '../types'
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
})

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
})

describe('HttpDetectorClient', () => {
  it('envía la imagen a /predict y devuelve la respuesta', async () => {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: true,
      json: () => Promise.resolve(response),
    })
    vi.stubGlobal('fetch', fetchMock)

    const client = new HttpDetectorClient('http://api.local/')
    const result = await client.detect(pngFile())

    expect(result).toEqual(response)
    expect(fetchMock).toHaveBeenCalledTimes(1)
    const [url, init] = fetchMock.mock.calls[0]
    expect(url).toBe('http://api.local/predict')
    expect(init.method).toBe('POST')
    expect(init.body).toBeInstanceOf(FormData)
    expect((init.body as FormData).get('file')).toBeInstanceOf(File)
  })

  it('falla cuando la API responde con error', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn().mockResolvedValue({ ok: false, status: 500, json: () => Promise.resolve({}) }),
    )

    const client = new HttpDetectorClient('http://api.local')

    await expect(client.detect(pngFile())).rejects.toThrow('La API respondió con estado 500.')
  })
})

describe('createClient', () => {
  it('usa el cliente simulado sin URL', () => {
    expect(createClient('')).toBeInstanceOf(MockDetectorClient)
  })

  it('usa el cliente HTTP con URL', () => {
    expect(createClient('http://api.local')).toBeInstanceOf(HttpDetectorClient)
  })
})
