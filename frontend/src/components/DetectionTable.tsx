import { colorFor, displayName } from '../labels'
import type { Detection } from '../types'

interface DetectionTableProps {
  detections: Detection[]
}

export function DetectionTable({ detections }: DetectionTableProps) {
  return (
    <table className="table">
      <caption>Detecciones encontradas</caption>
      <thead>
        <tr>
          <th scope="col">Categoría</th>
          <th scope="col">Confianza</th>
          <th scope="col">Caja (x1, y1, x2, y2)</th>
        </tr>
      </thead>
      <tbody>
        {detections.map((detection, index) => (
          <tr key={`${detection.class_name}-${index}`}>
            <td>
              <span
                className="dot"
                style={{ backgroundColor: colorFor(detection.class_name) }}
                aria-hidden="true"
              />
              {displayName(detection.class_name)}
            </td>
            <td>{Math.round(detection.confidence * 100)} %</td>
            <td className="mono">{detection.bbox.map((value) => Math.round(value)).join(', ')}</td>
          </tr>
        ))}
      </tbody>
    </table>
  )
}
