/** Validación de archivos antes de enviarlos al detector. */

export const MAX_BYTES = 10 * 1024 * 1024
export const ALLOWED_TYPES = ['image/jpeg', 'image/png'] as const

export function validateFile(file: File): string | null {
  if (!ALLOWED_TYPES.includes(file.type as (typeof ALLOWED_TYPES)[number])) {
    return 'Formato no admitido. Usa una imagen JPEG o PNG.'
  }
  if (file.size === 0) {
    return 'El archivo está vacío.'
  }
  if (file.size > MAX_BYTES) {
    return 'La imagen supera los 10 MB. Usa una imagen más pequeña.'
  }
  return null
}
