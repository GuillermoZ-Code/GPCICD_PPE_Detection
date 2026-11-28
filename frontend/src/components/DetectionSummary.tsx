/** HU-077 — resumen de los resultados visibles del detector. */

import type { Detection } from '../types'

interface DetectionSummaryProps {
  detections: Detection[]
  elapsedMs?: number
  modelVersion?: string
}

export function DetectionSummary({
  detections,
  elapsedMs,
  modelVersion,
}: DetectionSummaryProps) {
  const classes = new Set(detections.map((detection) => detection.class_name)).size
  const average = detections.length
    ? detections.reduce((sum, detection) => sum + detection.confidence, 0) / detections.length
    : 0

  return (
    <section className="summary" aria-label="Resumen de detecciones" aria-live="polite">
      <div className="stat">
        <span>Detecciones</span>
        <strong>{detections.length}</strong>
      </div>
      <div className="stat">
        <span>Clases</span>
        <strong>{classes} clases</strong>
      </div>
      <div className="stat">
        <span>Confianza media</span>
        <strong>{Math.round(average * 100)} %</strong>
      </div>
      <div className="stat">
        <span>Tiempo</span>
        <strong>{Math.round(elapsedMs ?? 0)} ms</strong>
      </div>
      <div className="stat">
        <span>Modelo</span>
        <strong>{modelVersion ?? '—'}</strong>
      </div>
    </section>
  )
}
