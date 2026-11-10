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
  elapsed_ms?: number
}
