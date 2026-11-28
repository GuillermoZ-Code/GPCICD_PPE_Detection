/** HU-088 — historial de análisis de la sesión, solo en el navegador. */

import type { PredictResponse } from './types'

export const HISTORY_KEY = 'ppe.history.v1'
export const MAX_HISTORY = 8

export interface HistoryClassCount {
  name: string
  count: number
}

export interface HistoryEntry {
  id: string
  fileName: string
  analyzedAt: string
  modelVersion?: string
  detections: number
  classes: HistoryClassCount[]
  elapsedMs?: number
  thumbnail?: string
}

function isClassCount(value: unknown): value is HistoryClassCount {
  if (typeof value !== 'object' || value === null) {
    return false
  }
  const item = value as Record<string, unknown>
  return typeof item.name === 'string' && typeof item.count === 'number'
}

function isHistoryEntry(value: unknown): value is HistoryEntry {
  if (typeof value !== 'object' || value === null) {
    return false
  }
  const entry = value as Record<string, unknown>
  return (
    typeof entry.id === 'string' &&
    typeof entry.fileName === 'string' &&
    typeof entry.analyzedAt === 'string' &&
    typeof entry.detections === 'number' &&
    Array.isArray(entry.classes) &&
    entry.classes.every(isClassCount) &&
    (entry.modelVersion === undefined || typeof entry.modelVersion === 'string') &&
    (entry.elapsedMs === undefined || typeof entry.elapsedMs === 'number') &&
    (entry.thumbnail === undefined || typeof entry.thumbnail === 'string')
  )
}

function store(storage?: Storage): Storage {
  return storage ?? window.localStorage
}

/** Carga el historial validando el JSON; un dato corrupto devuelve lista vacía. */
export function loadHistory(storage?: Storage): HistoryEntry[] {
  try {
    const raw = store(storage).getItem(HISTORY_KEY)
    if (!raw) {
      return []
    }
    const parsed: unknown = JSON.parse(raw)
    if (!Array.isArray(parsed)) {
      return []
    }
    return parsed.filter(isHistoryEntry).slice(0, MAX_HISTORY)
  } catch {
    return []
  }
}

/** Guarda como máximo MAX_HISTORY entradas; las blob: no se persisten. */
export function saveHistory(entries: HistoryEntry[], storage?: Storage): void {
  try {
    const persisted = entries.slice(0, MAX_HISTORY).map((entry) => {
      if (!entry.thumbnail?.startsWith('blob:')) {
        return entry
      }
      const copy = { ...entry }
      delete copy.thumbnail
      return copy
    })
    store(storage).setItem(HISTORY_KEY, JSON.stringify(persisted))
  } catch {
    // El historial es auxiliar: si el storage falla, la inferencia sigue.
  }
}

/** Agrega una entrada y devuelve la lista resultante, más reciente primero. */
export function addHistoryEntry(entry: HistoryEntry, storage?: Storage): HistoryEntry[] {
  const next = [
    entry,
    ...loadHistory(storage).filter((item) => item.id !== entry.id),
  ].slice(0, MAX_HISTORY)
  saveHistory(next, storage)
  return next
}

/** Borra el historial del almacenamiento. */
export function clearHistory(storage?: Storage): void {
  try {
    store(storage).removeItem(HISTORY_KEY)
  } catch {
    // Sin storage no hay nada que borrar.
  }
}

/** Construye una entrada a partir de la respuesta del detector. */
export function makeHistoryEntry(
  response: PredictResponse,
  file: File,
  thumbnail?: string,
): HistoryEntry {
  const counts = new Map<string, number>()
  for (const detection of response.detections) {
    counts.set(detection.class_name, (counts.get(detection.class_name) ?? 0) + 1)
  }
  const classes = [...counts.entries()]
    .map(([name, count]) => ({ name, count }))
    .sort((first, second) => second.count - first.count || first.name.localeCompare(second.name))
  const id =
    (globalThis.crypto as { randomUUID?: () => string } | undefined)?.randomUUID?.() ??
    `${Date.now()}-${Math.random().toString(36).slice(2, 8)}`

  return {
    id,
    fileName: file.name,
    analyzedAt: new Date().toISOString(),
    modelVersion: response.model_version,
    detections: response.detections.length,
    classes,
    elapsedMs: response.elapsed_ms,
    thumbnail,
  }
}
