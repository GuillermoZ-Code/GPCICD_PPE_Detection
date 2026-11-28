/** HU-088 — historial de la sesión con miniatura, conteo y detalle por clase. */

import { useState } from 'react'

import type { HistoryEntry } from '../history'
import { displayName } from '../labels'

interface HistoryProps {
  entries: HistoryEntry[]
  onClear: () => void
}

export function History({ entries, onClear }: HistoryProps) {
  const [selectedId, setSelectedId] = useState<string | null>(null)
  const selected = entries.find((entry) => entry.id === selectedId) ?? null

  return (
    <section className="history" aria-label="Historial de la sesión">
      <header className="history__header">
        <div>
          <h2>Historial de la sesión</h2>
          <p className="muted">Solo en este navegador; no se envía al servidor.</p>
        </div>
        {entries.length > 0 && (
          <button type="button" className="button button--ghost" onClick={onClear}>
            Limpiar historial
          </button>
        )}
      </header>

      {entries.length === 0 ? (
        <p className="history__empty muted">Aún no hay análisis en esta sesión.</p>
      ) : (
        <ul className="history__list">
          {entries.map((entry) => {
            const isSelected = entry.id === selectedId
            return (
              <li key={entry.id} className="history__item">
                <button
                  type="button"
                  className={`history__button${isSelected ? ' is-selected' : ''}`}
                  aria-pressed={isSelected}
                  onClick={() => setSelectedId(isSelected ? null : entry.id)}
                >
                  {entry.thumbnail ? (
                    <img
                      className="history__thumb"
                      src={entry.thumbnail}
                      alt={`Miniatura de ${entry.fileName}`}
                    />
                  ) : (
                    <span
                      className="history__thumb history__thumb--fallback"
                      aria-hidden="true"
                    >
                      {entry.fileName.slice(0, 1).toUpperCase()}
                    </span>
                  )}
                  <span className="history__body">
                    <span className="history__name">{entry.fileName}</span>
                    <span className="history__meta">
                      {entry.detections} detecciones · {entry.classes.length} clases
                    </span>
                    <span className="history__model">Modelo {entry.modelVersion ?? '—'}</span>
                  </span>
                </button>

                {isSelected && selected && (
                  <div className="history__detail">
                    {selected.classes.length === 0 ? (
                      <p className="muted">Sin clases detectadas.</p>
                    ) : (
                      <ul>
                        {selected.classes.map((item) => (
                          <li key={item.name}>
                            <span>{displayName(item.name)}</span>
                            <strong>{item.count}</strong>
                          </li>
                        ))}
                      </ul>
                    )}
                  </div>
                )}
              </li>
            )
          })}
        </ul>
      )}
    </section>
  )
}
