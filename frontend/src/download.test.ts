import { describe, expect, it } from 'vitest'

import { detectionsToCsv } from './download'
import type { Detection } from './types'

const detection: Detection = {
  class_id: 3,
  class_name: 'helmet',
  confidence: 0.923456,
  bbox: [10.123, 20.456, 30.789, 40.012],
  image_width: 100,
  image_height: 100,
}

describe('detectionsToCsv', () => {
  it('genera el encabezado y una fila por detección', () => {
    // Act
    const csv = detectionsToCsv('foto.png', [detection])

    // Assert
    const lines = csv.trim().split('\n')
    expect(lines[0]).toBe('image,class_name,confidence,x1,y1,x2,y2')
    expect(lines[1]).toBe('foto.png,helmet,0.923456,10.12,20.46,30.79,40.01')
  })

  it('escapa nombres con comas', () => {
    // Act
    const csv = detectionsToCsv('foto,1.png', [detection])

    // Assert
    expect(csv).toContain('"foto,1.png",helmet')
  })

  it('devuelve solo el encabezado sin detecciones', () => {
    // Act
    const csv = detectionsToCsv('foto.png', [])

    // Assert
    expect(csv).toBe('image,class_name,confidence,x1,y1,x2,y2\n')
  })
})
