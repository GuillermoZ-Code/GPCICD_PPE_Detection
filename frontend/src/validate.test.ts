import { describe, expect, it } from 'vitest'

import { MAX_BYTES, validateFile } from './validate'

function fileOf(size: number, type: string): File {
  return new File([new Uint8Array(size)], 'archivo', { type })
}

describe('validateFile', () => {
  it('acepta una imagen PNG pequeña', () => {
    expect(validateFile(fileOf(1024, 'image/png'))).toBeNull()
  })

  it('acepta una imagen JPEG pequeña', () => {
    expect(validateFile(fileOf(1024, 'image/jpeg'))).toBeNull()
  })

  it('rechaza un tipo no admitido', () => {
    expect(validateFile(fileOf(1024, 'text/plain'))).toBe(
      'Formato no admitido. Usa una imagen JPEG o PNG.',
    )
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
