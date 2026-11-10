/** Cliente de inferencia: HTTP cuando hay API, simulado cuando no. */

import type { Detection, PredictResponse } from '../types'

export interface DetectorClient {
  detect(file: File): Promise<PredictResponse>
}

export const MOCK_DETECTIONS: Detection[] = [
  {
    class_id: 3,
    class_name: 'helmet',
    confidence: 0.92,
    bbox: [60, 80, 220, 260],
    image_width: 640,
    image_height: 480,
  },
  {
    class_id: 1,
    class_name: 'Vest',
    confidence: 0.74,
    bbox: [240, 120, 420, 320],
    image_width: 640,
    image_height: 480,
  },
]

export class MockDetectorClient implements DetectorClient {
  constructor(private readonly detections: Detection[] = MOCK_DETECTIONS) {}

  async detect(_file: File): Promise<PredictResponse> {
    return Promise.resolve({
      detections: this.detections.map((detection) => ({ ...detection })),
      image_width: 640,
      image_height: 480,
      model_version: 'mock-1.0.0',
      elapsed_ms: 0,
    })
  }
}

export class HttpDetectorClient implements DetectorClient {
  private readonly baseUrl: string

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl.replace(/\/+$/, '')
  }

  async detect(file: File): Promise<PredictResponse> {
    const body = new FormData()
    body.append('file', file)
    const response = await fetch(`${this.baseUrl}/predict`, { method: 'POST', body })
    if (!response.ok) {
      throw new Error(`La API respondió con estado ${response.status}.`)
    }
    return (await response.json()) as PredictResponse
  }
}

export function createClient(baseUrl?: string): DetectorClient {
  const url = (baseUrl ?? import.meta.env.VITE_API_URL ?? '').trim()
  return url ? new HttpDetectorClient(url) : new MockDetectorClient()
}
