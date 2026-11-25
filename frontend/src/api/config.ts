/** Configuración de la API de inferencia (HU-072). */

/**
 * Ruta relativa por omisión: la SPA llama al mismo origen y el proxy (Vite en
 * desarrollo, nginx en el contenedor) reenvía a la API real.
 */
export const DEFAULT_API_BASE = '/api'

/**
 * Resuelve la base de la API a partir de `VITE_API_URL`.
 *
 * Sin configuración (vacía, `undefined` o solo espacios) devuelve `DEFAULT_API_BASE`;
 * una URL absoluta se conserva sin barras finales.
 *
 * @param raw valor crudo de la variable de entorno; por omisión, `VITE_API_URL`.
 * @returns base sin barras finales y nunca vacía.
 */
export function resolveApiBaseUrl(raw: string | undefined = import.meta.env.VITE_API_URL): string {
  const value = (raw ?? '').trim()
  if (value === '') {
    return DEFAULT_API_BASE
  }
  return value.replace(/\/+$/, '')
}
