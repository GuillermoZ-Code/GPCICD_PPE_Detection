/** AC-003.2 y AC-003.3 — transformación espacial de las detecciones. */

import { render, screen } from '@testing-library/react'
import { afterEach, describe, expect, it, vi } from 'vitest'

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

interface FakeContext {
  drawImage: ReturnType<typeof vi.fn>
  strokeRect: ReturnType<typeof vi.fn>
  fillRect: ReturnType<typeof vi.fn>
  fillText: ReturnType<typeof vi.fn>
  measureText: ReturnType<typeof vi.fn>
  strokeStyle: string
  fillStyle: string
  lineWidth: number
  font: string
  textBaseline: string
}

function stubContext(): FakeContext {
  const context: FakeContext = {
    drawImage: vi.fn(),
    strokeRect: vi.fn(),
    fillRect: vi.fn(),
    fillText: vi.fn(),
    measureText: vi.fn(() => ({ width: 30 })),
    strokeStyle: '',
    fillStyle: '',
    lineWidth: 0,
    font: '',
    textBaseline: '',
  }
  vi.spyOn(HTMLCanvasElement.prototype, 'getContext').mockReturnValue(
    context as unknown as CanvasRenderingContext2D,
  )
  return context
}

function stubImage(naturalWidth: number, naturalHeight: number): void {
  class FakeImage {
    onload: (() => void) | null = null
    naturalWidth: number
    naturalHeight: number

    constructor() {
      this.naturalWidth = naturalWidth
      this.naturalHeight = naturalHeight
    }

    set src(_value: string) {
      this.onload?.()
    }
  }
  vi.stubGlobal('Image', FakeImage)
}

afterEach(() => {
  vi.unstubAllGlobals()
})

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

  it('escala la caja de la detección al tamaño real del lienzo', () => {
    // Arrange
    const context = stubContext()
    stubImage(200, 200)
    const scaled: Detection = {
      ...detection,
      bbox: [10, 20, 30, 40],
      image_width: 100,
      image_height: 100,
    }

    // Act
    render(
      <AnnotatedCanvas
        src="blob:mock"
        width={200}
        height={200}
        detections={[scaled]}
        alt="Imagen escalada"
      />,
    )

    // Assert
    expect(context.strokeRect).toHaveBeenCalledWith(20, 40, 40, 40)
  })

  it('no dibuja cajas cuando no hay detecciones', () => {
    // Arrange
    const context = stubContext()
    stubImage(640, 480)

    // Act
    render(
      <AnnotatedCanvas
        src="blob:mock"
        width={640}
        height={480}
        detections={[]}
        alt="Imagen sin detecciones"
      />,
    )

    // Assert
    expect(context.drawImage).toHaveBeenCalledTimes(1)
    expect(context.strokeRect).not.toHaveBeenCalled()
  })

  it('omite las etiquetas cuando showLabels es falso', () => {
    // Arrange
    const context = stubContext()
    stubImage(640, 480)

    // Act
    render(
      <AnnotatedCanvas
        src="blob:mock"
        width={640}
        height={480}
        detections={[detection]}
        showLabels={false}
        alt="Imagen sin etiquetas"
      />,
    )

    // Assert
    expect(context.strokeRect).toHaveBeenCalledTimes(1)
    expect(context.fillText).not.toHaveBeenCalled()
  })

  it('mantiene la etiqueta dentro del lienzo si la caja toca el borde superior', () => {
    // Arrange
    const context = stubContext()
    stubImage(200, 200)
    const topEdge: Detection = {
      ...detection,
      bbox: [10, 0, 30, 10],
      image_width: 100,
      image_height: 100,
    }

    // Act
    render(
      <AnnotatedCanvas
        src="blob:mock"
        width={200}
        height={200}
        detections={[topEdge]}
        alt="Imagen con caja en el borde"
      />,
    )

    // Assert
    const [x, y] = context.fillRect.mock.calls[0] as [number, number, number, number]
    expect(x).toBe(20)
    expect(y).toBe(0)
  })
})
