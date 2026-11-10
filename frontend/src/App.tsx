import { useEffect, useMemo, useRef, useState } from 'react'

import { createClient, type DetectorClient } from './api/client'
import { AnnotatedCanvas } from './components/AnnotatedCanvas'
import { DetectionTable } from './components/DetectionTable'
import { StatusBanner } from './components/StatusBanner'
import { UploadPanel } from './components/UploadPanel'
import type { PredictResponse } from './types'
import { validateFile } from './validate'

type Analysis =
  | { status: 'idle' }
  | { status: 'loading'; fileName: string }
  | { status: 'ready'; fileName: string; imageUrl: string; response: PredictResponse }
  | { status: 'error'; message: string }

interface AppProps {
  client?: DetectorClient
}

export function App({ client }: AppProps) {
  const detector = useMemo(() => client ?? createClient(), [client])
  const [analysis, setAnalysis] = useState<Analysis>({ status: 'idle' })
  const imageUrlRef = useRef<string | null>(null)

  useEffect(() => {
    return () => {
      if (imageUrlRef.current) {
        URL.revokeObjectURL(imageUrlRef.current)
      }
    }
  }, [])

  async function handleFile(file: File) {
    const problem = validateFile(file)
    if (problem) {
      setAnalysis({ status: 'error', message: problem })
      return
    }

    if (imageUrlRef.current) {
      URL.revokeObjectURL(imageUrlRef.current)
    }
    const imageUrl = URL.createObjectURL(file)
    imageUrlRef.current = imageUrl
    setAnalysis({ status: 'loading', fileName: file.name })

    try {
      const response = await detector.detect(file)
      setAnalysis({ status: 'ready', fileName: file.name, imageUrl, response })
    } catch (error) {
      const detail = error instanceof Error ? error.message : ''
      setAnalysis({
        status: 'error',
        message: `No se pudo completar el análisis. ${detail}`.trim(),
      })
    }
  }

  return (
    <div className="page">
      <header className="header">
        <p className="eyebrow">GPCICD · Grupo 4</p>
        <h1>Detección de EPP</h1>
        <p className="lede">
          Sube una imagen y consulta qué Equipos de Protección Personal aparecen. El sistema
          reporta EPP detectado; no evalúa cumplimiento normativo.
        </p>
      </header>

      <main className="layout">
        <UploadPanel onSelect={handleFile} disabled={analysis.status === 'loading'} />

        <section className="card" aria-labelledby="result-title">
          <h2 id="result-title">2. Resultado</h2>

          {analysis.status === 'idle' && (
            <StatusBanner tone="info">
              Aún no hay análisis. Selecciona una imagen para empezar.
            </StatusBanner>
          )}

          {analysis.status === 'loading' && (
            <StatusBanner tone="info">Analizando {analysis.fileName}…</StatusBanner>
          )}

          {analysis.status === 'error' && (
            <StatusBanner tone="error">{analysis.message}</StatusBanner>
          )}

          {analysis.status === 'ready' && (
            <div className="result">
              <AnnotatedCanvas
                src={analysis.imageUrl}
                width={analysis.response.image_width}
                height={analysis.response.image_height}
                detections={analysis.response.detections}
                alt={`Imagen analizada: ${analysis.fileName}`}
              />

              {analysis.response.detections.length === 0 ? (
                <StatusBanner tone="warning">
                  No se detectaron EPP en la imagen. La inferencia terminó sin errores; la ausencia
                  de detecciones no implica que no haya EPP.
                </StatusBanner>
              ) : (
                <>
                  <p className="hint">
                    {analysis.response.detections.length} detección(es) en {analysis.fileName}
                  </p>
                  <DetectionTable detections={analysis.response.detections} />
                </>
              )}
            </div>
          )}
        </section>
      </main>

      <footer className="footer">
        <p>
          <a href="https://github.com/GuillermoZ-Code/GPCICD_PPE_Detection" rel="noreferrer">
            Código fuente
          </a>{' '}
          · Licencia AGPL-3.0-only
        </p>
        <p>
          Dataset{' '}
          <a href="https://huggingface.co/datasets/51ddhesh/PPE_Detection" rel="noreferrer">
            PPE_Detection
          </a>{' '}
          con licencia CC-BY-4.0.
        </p>
      </footer>
    </div>
  )
}
