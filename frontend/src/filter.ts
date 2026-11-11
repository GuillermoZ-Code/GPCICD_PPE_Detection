import type { Settings } from './config'
import type { Detection } from './types'

/** Aplica los filtros visuales: confianza mínima y clases visibles. */
export function filterDetections(detections: Detection[], settings: Settings): Detection[] {
  const threshold = settings.visualConfidence / 100
  return detections.filter(
    (detection) =>
      detection.confidence >= threshold && settings.classes.includes(detection.class_name),
  )
}
