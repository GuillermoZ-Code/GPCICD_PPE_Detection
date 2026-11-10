/** Nombres legibles y colores por clase canónica del `data.yaml`. */

export const DISPLAY_NAMES: Record<string, string> = {
  Gloves: 'Guantes',
  Vest: 'Chaleco',
  goggles: 'Gafas',
  helmet: 'Casco',
  mask: 'Mascarilla',
  safety_shoe: 'Calzado',
}

export const COLORS: Record<string, string> = {
  Gloves: '#d62728',
  Vest: '#1f77b4',
  goggles: '#2ca02c',
  helmet: '#ff7f0e',
  mask: '#9467bd',
  safety_shoe: '#17becf',
}

export const FALLBACK_COLOR = '#94a3b8'

export function displayName(className: string): string {
  return DISPLAY_NAMES[className] ?? className
}

export function colorFor(className: string): string {
  return COLORS[className] ?? FALLBACK_COLOR
}
