import type { Detection } from './types'

function quote(value: string): string {
  return /[",\n]/.test(value) ? `"${value.replaceAll('"', '""')}"` : value
}

export function detectionsToCsv(imageName: string, detections: Detection[]): string {
  const header = 'image,class_name,confidence,x1,y1,x2,y2'
  const rows = detections.map((detection) =>
    [
      quote(imageName),
      detection.class_name,
      detection.confidence.toFixed(6),
      ...detection.bbox.map((value) => value.toFixed(2)),
    ].join(','),
  )
  return [header, ...rows].join('\n') + '\n'
}

export function downloadBlob(blob: Blob, filename: string): void {
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = filename
  link.rel = 'noopener'
  link.click()
  URL.revokeObjectURL(url)
}

export function downloadText(filename: string, text: string, mime: string): void {
  downloadBlob(new Blob([text], { type: mime }), filename)
}
