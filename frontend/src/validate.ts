/** Validación de archivos antes de enviarlos al detector. */

export const MAX_BYTES = 10 * 1024 * 1024
export const ALLOWED_TYPES = ['image/jpeg', 'image/jfif', 'image/png'] as const
export const ALLOWED_EXTENSIONS = ['.jpg', '.jpeg', '.jfif', '.png'] as const

export const FORMAT_ERROR =
  'Formato no admitido. Usa JPEG (jpg, jpeg, jfif) o PNG; AVIF no está soportado.'

function hasAllowedExtension(name: string): boolean {
  const lower = name.toLowerCase()
  return ALLOWED_EXTENSIONS.some((extension) => lower.endsWith(extension))
}

export function validateFile(file: File): string | null {
  const type = file.type.toLowerCase()
  const typeAllowed = (ALLOWED_TYPES as readonly string[]).includes(type)
  // Algunos navegadores no conocen .jfif y dejan `type` vacío: se acepta por extensión
  // y el servidor valida los bytes reales.
  const extensionAllowed = type === '' && hasAllowedExtension(file.name)
  if (!typeAllowed && !extensionAllowed) {
    return FORMAT_ERROR
  }
  if (file.size === 0) {
    return 'El archivo está vacío.'
  }
  if (file.size > MAX_BYTES) {
    return 'La imagen supera los 10 MB. Usa una imagen más pequeña.'
  }
  return null
}
