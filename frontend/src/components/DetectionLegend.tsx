/** HU-077 — leyenda por clase con color, conteo y confianza media. */

import { colorFor, displayName } from '../labels'
import type { Detection } from '../types'

interface DetectionLegendProps {
  detections: Detection[]
}

interface Group {
  count: number
  total: number
}

export function DetectionLegend({ detections }: DetectionLegendProps) {
  const groups = new Map<string, Group>()
  for (const detection of detections) {
    const group = groups.get(detection.class_name) ?? { count: 0, total: 0 }
    group.count += 1
    group.total += detection.confidence
    groups.set(detection.class_name, group)
  }

  const items = [...groups.entries()].sort(
    ([nameA, groupA], [nameB, groupB]) =>
      groupB.count - groupA.count ||
      displayName(nameA).localeCompare(displayName(nameB)),
  )

  if (items.length === 0) {
    return null
  }

  return (
    <section className="legend" aria-label="Leyenda por clase">
      <h3>Clases detectadas</h3>
      <ul>
        {items.map(([name, group]) => {
          const average = Math.round((group.total / group.count) * 100)
          return (
            <li key={name} className="legend__item">
              <span
                className="dot"
                style={{ backgroundColor: colorFor(name) }}
                aria-hidden="true"
              />
              <span className="legend__name">{displayName(name)}</span>
              <span className="legend__count" aria-label={`${group.count} detecciones`}>
                {group.count}
              </span>
              <span className="legend__bar" aria-hidden="true">
                <span style={{ width: `${average}%` }} />
              </span>
              <span className="legend__confidence">{average} %</span>
            </li>
          )
        })}
      </ul>
    </section>
  )
}
