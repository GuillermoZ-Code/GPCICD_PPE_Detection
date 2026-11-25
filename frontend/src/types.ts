/** Tipos espejo del contrato `ImageData → list[Detection]` (TA-11). */

export type BoundingBox = [number, number, number, number]

export interface Detection {
  class_id: number
  class_name: string
  confidence: number
  bbox: BoundingBox
  image_width: number
  image_height: number
}

export interface PredictResponse {
  detections: Detection[]
  image_width: number
  image_height: number
  model_version?: string
  model_sha256?: string | null
  model_artifact?: string | null
  model_reference?: string
  elapsed_ms?: number
}

/** Espejo del contrato `GET /health/ready` (HU-045), usado por HU-079. */
export interface ReadyResponse {
  status: 'ready' | 'not_ready'
  api_version: string
  model_loaded: boolean
  model_version: string
  model_reference: string
  model_sha256?: string | null
  model_artifact?: string | null
}
