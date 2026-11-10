/** Preferencias de la interfaz, persistidas en localStorage. */

import { DISPLAY_NAMES } from './labels'

export type Theme = 'light' | 'dark' | 'system'
export type Accent = 'indigo' | 'cyan' | 'emerald' | 'rose' | 'gray'
export type Background = 'waves' | 'aurora' | 'grid' | 'none'
export type Density = 'comfy' | 'compact'

export const CLASS_NAMES = Object.keys(DISPLAY_NAMES)

export interface Settings {
  theme: Theme
  accent: Accent
  background: Background
  density: Density
  animations: boolean
  labels: boolean
  thickness: number
  visualConfidence: number
  modelConfidence: number
  classes: string[]
  autoAnalyze: boolean
}

export const ACCENTS: { id: Accent; label: string }[] = [
  { id: 'indigo', label: 'Índigo' },
  { id: 'cyan', label: 'Cian' },
  { id: 'emerald', label: 'Esmeralda' },
  { id: 'rose', label: 'Rosa' },
  { id: 'gray', label: 'Gris' },
]

export const BACKGROUNDS: { id: Background; label: string }[] = [
  { id: 'waves', label: 'Ondas' },
  { id: 'aurora', label: 'Aurora' },
  { id: 'grid', label: 'Rejilla' },
  { id: 'none', label: 'Ninguno' },
]

export const THEMES: { id: Theme; label: string }[] = [
  { id: 'light', label: 'Claro' },
  { id: 'dark', label: 'Oscuro' },
  { id: 'system', label: 'Sistema' },
]

export const DENSITIES: { id: Density; label: string }[] = [
  { id: 'comfy', label: 'Cómoda' },
  { id: 'compact', label: 'Compacta' },
]

export const DEFAULT_SETTINGS: Settings = {
  theme: 'system',
  accent: 'cyan',
  background: 'waves',
  density: 'comfy',
  animations: true,
  labels: true,
  thickness: 3,
  visualConfidence: 0,
  modelConfidence: 0.25,
  classes: [...CLASS_NAMES],
  autoAnalyze: false,
}

const STORAGE_KEY = 'ppe.settings.v1'

function clamp(value: number, min: number, max: number): number {
  return Math.min(max, Math.max(min, value))
}

function isKnownClass(name: string): boolean {
  return CLASS_NAMES.includes(name)
}

export function loadSettings(): Settings {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    if (!raw) {
      return { ...DEFAULT_SETTINGS }
    }
    const parsed = JSON.parse(raw) as Partial<Settings>
    const classes = Array.isArray(parsed.classes)
      ? parsed.classes.filter((name): name is string => typeof name === 'string' && isKnownClass(name))
      : DEFAULT_SETTINGS.classes
    return {
      ...DEFAULT_SETTINGS,
      ...parsed,
      thickness: clamp(Number(parsed.thickness ?? DEFAULT_SETTINGS.thickness), 1, 6),
      visualConfidence: clamp(Number(parsed.visualConfidence ?? 0), 0, 99),
      modelConfidence: clamp(
        Number(parsed.modelConfidence ?? DEFAULT_SETTINGS.modelConfidence),
        0.01,
        0.99,
      ),
      classes: classes.length > 0 ? classes : DEFAULT_SETTINGS.classes,
    }
  } catch {
    return { ...DEFAULT_SETTINGS }
  }
}

export function saveSettings(settings: Settings): void {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(settings))
}

export function resolveTheme(theme: Theme): 'light' | 'dark' {
  if (theme !== 'system') {
    return theme
  }
  if (typeof window !== 'undefined' && typeof window.matchMedia === 'function') {
    return window.matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark'
  }
  return 'dark'
}

export function applySettings(settings: Settings): void {
  const root = document.documentElement
  root.dataset.theme = resolveTheme(settings.theme)
  root.dataset.accent = settings.accent
  root.dataset.bg = settings.background
  root.dataset.density = settings.density
  root.dataset.motion = settings.animations ? 'on' : 'off'
  root.dataset.labels = settings.labels ? 'on' : 'off'
  root.style.setProperty('--box-width', `${settings.thickness}px`)
}
