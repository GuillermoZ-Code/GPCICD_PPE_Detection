import { describe, expect, it } from 'vitest'

import { DEFAULT_SETTINGS } from './config'
import { filterDetections } from './filter'
import type { Detection } from './types'

function detection(class_name: string, confidence: number): Detection {
  return {
    class_id: 0,
    class_name,
    confidence,
    bbox: [1, 2, 3, 4],
    image_width: 100,
    image_height: 100,
  }
}

describe('filterDetections', () => {
  it('aplica la confianza visual', () => {
    // Arrange
    const detections = [detection('helmet', 0.9), detection('Vest', 0.4)]
    const settings = { ...DEFAULT_SETTINGS, visualConfidence: 50 }

    // Act
    const result = filterDetections(detections, settings)

    // Assert
    expect(result.map((item) => item.class_name)).toEqual(['helmet'])
  })

  it('aplica las clases visibles', () => {
    // Arrange
    const detections = [detection('helmet', 0.9), detection('Gloves', 0.8)]
    const settings = { ...DEFAULT_SETTINGS, classes: ['helmet'] }

    // Act
    const result = filterDetections(detections, settings)

    // Assert
    expect(result.map((item) => item.class_name)).toEqual(['helmet'])
  })

  it('devuelve todo con los valores por defecto', () => {
    // Arrange
    const detections = [detection('helmet', 0.9), detection('Gloves', 0.3)]

    // Act
    const result = filterDetections(detections, DEFAULT_SETTINGS)

    // Assert
    expect(result).toHaveLength(2)
  })
})
