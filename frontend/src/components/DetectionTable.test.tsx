/** AC-007.2 — categoría, confianza y ubicación visibles. */

import { render, screen, within } from '@testing-library/react'
import { describe, expect, it } from 'vitest'

import type { Detection } from '../types'
import { DetectionTable } from './DetectionTable'

const detection: Detection = {
  class_id: 3,
  class_name: 'helmet',
  confidence: 0.92,
  bbox: [60, 80, 220, 260],
  image_width: 640,
  image_height: 480,
}

function detectionOf(classId: number, className: string, confidence = 0.9): Detection {
  return {
    class_id: classId,
    class_name: className,
    confidence,
    bbox: [10, 10, 50, 60],
    image_width: 100,
    image_height: 100,
  }
}

describe('DetectionTable', () => {
  it('muestra la categoría legible y la confianza', () => {
    render(<DetectionTable detections={[detection]} />)

    expect(screen.getByRole('columnheader', { name: 'Categoría' })).toBeInTheDocument()
    expect(screen.getByText('Casco')).toBeInTheDocument()
    expect(screen.getByText('92 %')).toBeInTheDocument()
  })

  it('muestra las coordenadas de la caja', () => {
    render(<DetectionTable detections={[detection]} />)

    expect(screen.getByText('60, 80, 220, 260')).toBeInTheDocument()
  })

  it('traduce las seis clases canónicas al español', () => {
    // Arrange
    const detections = [
      detectionOf(0, 'Gloves'),
      detectionOf(1, 'Vest'),
      detectionOf(2, 'goggles'),
      detectionOf(3, 'helmet'),
      detectionOf(4, 'mask'),
      detectionOf(5, 'safety_shoe'),
    ]

    // Act
    render(<DetectionTable detections={detections} />)

    // Assert
    for (const name of ['Guantes', 'Chaleco', 'Gafas', 'Casco', 'Mascarilla', 'Calzado']) {
      expect(screen.getByText(name)).toBeInTheDocument()
    }
  })

  it('redondea la confianza y ajusta la barra al porcentaje', () => {
    // Arrange
    const { container } = render(
      <DetectionTable detections={[detectionOf(3, 'helmet', 0.876)]} />,
    )

    // Act
    const bar = container.querySelector('.confidence__bar span')

    // Assert
    expect(screen.getByText('88 %')).toBeInTheDocument()
    expect(bar).toHaveStyle({ width: '88%' })
  })

  it('redondea las coordenadas de la caja', () => {
    // Arrange
    const rounded: Detection = { ...detection, bbox: [60.4, 80.6, 220.2, 259.5] }

    // Act
    render(<DetectionTable detections={[rounded]} />)

    // Assert
    expect(screen.getByText('60, 81, 220, 260')).toBeInTheDocument()
  })

  it('conserva el orden de las detecciones recibidas', () => {
    // Arrange
    const { container } = render(
      <DetectionTable
        detections={[detectionOf(1, 'Vest', 0.4), detectionOf(3, 'helmet', 0.9)]}
      />,
    )

    // Act
    const rows = within(container.querySelector('tbody') as HTMLElement).getAllByRole('row')

    // Assert
    expect(rows[0]).toHaveTextContent('Chaleco')
    expect(rows[1]).toHaveTextContent('Casco')
  })

  it('dibuja solo los encabezados cuando no hay detecciones', () => {
    // Arrange
    const { container } = render(<DetectionTable detections={[]} />)

    // Act / Assert
    expect(screen.getAllByRole('columnheader')).toHaveLength(3)
    expect(container.querySelectorAll('tbody tr')).toHaveLength(0)
  })
})
