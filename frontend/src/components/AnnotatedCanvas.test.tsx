import { render, screen } from '@testing-library/react'
import { describe, expect, it } from 'vitest'

import type { Detection } from '../types'
import { AnnotatedCanvas } from './AnnotatedCanvas'

const detection: Detection = {
  class_id: 3,
  class_name: 'helmet',
  confidence: 0.92,
  bbox: [60, 80, 220, 260],
  image_width: 640,
  image_height: 480,
}

describe('AnnotatedCanvas', () => {
  it('reserva el tamaño de la imagen y es accesible', () => {
    render(
      <AnnotatedCanvas
        src="blob:mock"
        width={640}
        height={480}
        detections={[detection]}
        alt="Imagen analizada: foto.png"
      />,
    )

    const canvas = screen.getByRole('img', { name: 'Imagen analizada: foto.png' })
    expect(canvas).toHaveAttribute('width', '640')
    expect(canvas).toHaveAttribute('height', '480')
  })

  it('no falla si el navegador no expone el contexto 2D', () => {
    render(
      <AnnotatedCanvas
        src="blob:mock"
        width={640}
        height={480}
        detections={[]}
        alt="Imagen sin detecciones"
      />,
    )

    expect(screen.getByRole('img')).toBeInTheDocument()
  })
})
