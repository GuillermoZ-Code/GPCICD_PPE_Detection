import { useEffect, useRef } from 'react'
import type { RefObject } from 'react'

import { colorFor, displayName } from '../labels'
import type { Detection } from '../types'

interface AnnotatedCanvasProps {
  src: string
  width: number
  height: number
  detections: Detection[]
  alt: string
  thickness?: number
  showLabels?: boolean
  canvasRef?: RefObject<HTMLCanvasElement | null>
}

export function AnnotatedCanvas({
  src,
  width,
  height,
  detections,
  alt,
  thickness = 3,
  showLabels = true,
  canvasRef,
}: AnnotatedCanvasProps) {
  const localRef = useRef<HTMLCanvasElement>(null)
  const ref = canvasRef ?? localRef

  useEffect(() => {
    const canvas = ref.current
    if (!canvas) {
      return
    }
    canvas.width = width
    canvas.height = height
    const context = canvas.getContext('2d')
    if (!context) {
      return
    }

    const image = new Image()
    image.onload = () => {
      canvas.width = image.naturalWidth || width
      canvas.height = image.naturalHeight || height
      context.drawImage(image, 0, 0, canvas.width, canvas.height)

      const base = Math.max(canvas.width, canvas.height)
      const lineWidth = Math.max(1, Math.round((thickness * base) / 640))
      const fontSize = Math.max(12, Math.round(base / 40))

      for (const detection of detections) {
        const scaleX = canvas.width / detection.image_width
        const scaleY = canvas.height / detection.image_height
        const [x1, y1, x2, y2] = detection.bbox
        const color = colorFor(detection.class_name)

        context.strokeStyle = color
        context.lineWidth = lineWidth
        context.strokeRect(x1 * scaleX, y1 * scaleY, (x2 - x1) * scaleX, (y2 - y1) * scaleY)

        if (!showLabels) {
          continue
        }
        const label = `${displayName(detection.class_name)} ${detection.confidence.toFixed(2)}`
        context.font = `600 ${fontSize}px system-ui, sans-serif`
        context.textBaseline = 'top'
        const textWidth = context.measureText(label).width
        const labelX = x1 * scaleX
        const labelY = Math.max(0, y1 * scaleY - fontSize - 8)

        context.fillStyle = color
        context.fillRect(labelX, labelY, textWidth + 10, fontSize + 8)
        context.fillStyle = '#ffffff'
        context.fillText(label, labelX + 5, labelY + 4)
      }
    }
    image.src = src
  }, [src, width, height, detections, thickness, showLabels, ref])

  return (
    <canvas
      ref={ref}
      className="canvas"
      width={width}
      height={height}
      role="img"
      aria-label={alt}
    />
  )
}
