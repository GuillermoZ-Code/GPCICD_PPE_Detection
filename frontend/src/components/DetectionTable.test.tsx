import { render, screen } from '@testing-library/react'
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
})
