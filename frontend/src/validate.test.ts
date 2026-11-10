import { describe, expect, it } from 'vitest'

import { FORMAT_ERROR, MAX_BYTES, validateFile } from './validate'

function fileOf(size: number, type: string, name = 'archivo'): File {
  return new File([new Uint8Array(size)], name, { type })
}

describe('validateFile', () => {
  it('acepta una imagen PNG pequeña', () => {
    expect(validateFile(fileOf(1024, 'image/png'))).toBeNull()
  })

  it('acepta una imagen JPEG pequeña', () => {
    expect(validateFile(fileOf(1024, 'image/jpeg'))).toBeNull()
  })

  it('acepta JFIF cuando el navegador lo reporta como image/jfif', () => {
    expect(validateFile(fileOf(1024, 'image/jfif', 'foto.jfif'))).toBeNull()
  })

  it('acepta JFIF cuando el navegador deja el tipo vacío', () => {
    expect(validateFile(fileOf(1024, '', 'foto.jfif'))).toBeNull()
  })

  it('acepta PNG por extensión si el tipo viene vacío', () => {
    expect(validateFile(fileOf(1024, '', 'foto.png'))).toBeNull()
  })

  it('rechaza un tipo no admitido', () => {
    expect(validateFile(fileOf(1024, 'text/plain'))).toBe(FORMAT_ERROR)
  })

  it('rechaza AVIF aunque la extensión se parezca', () => {
    expect(validateFile(fileOf(1024, 'image/avif', 'foto.avif'))).toBe(FORMAT_ERROR)
    expect(validateFile(fileOf(1024, '', 'foto.avif'))).toBe(FORMAT_ERROR)
  })

  it('rechaza un archivo vacío', () => {
    expect(validateFile(fileOf(0, 'image/png'))).toBe('El archivo está vacío.')
  })

  it('rechaza un archivo que supera el máximo', () => {
    expect(validateFile(fileOf(MAX_BYTES + 1, 'image/png'))).toBe(
      'La imagen supera los 10 MB. Usa una imagen más pequeña.',
    )
  })
})
