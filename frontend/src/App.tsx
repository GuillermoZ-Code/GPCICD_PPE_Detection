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
  | { status: 'selected'; file: File; imageUrl: string }
  | { status: 'loading'; file: File; imageUrl: string }
  | { status: 'ready'; file: File; imageUrl: string; response: PredictResponse }
  | { status: 'error'; message: string; file?: File; imageUrl?: string }

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

  const file = 'file' in analysis ? analysis.file : undefined
  const imageUrl = 'imageUrl' in analysis ? analysis.imageUrl : undefined
  const busy = analysis.status === 'loading'

  function handleSelect(nextFile: File) {
    const problem = validateFile(nextFile)
    if (problem) {
      setAnalysis({ status: 'error', message: problem })
      return
    }
    if (imageUrlRef.current) {
      URL.revokeObjectURL(imageUrlRef.current)
    }
    const nextUrl = URL.createObjectURL(nextFile)
    imageUrlRef.current = nextUrl
    setAnalysis({ status: 'selected', file: nextFile, imageUrl: nextUrl })
  }

  async function handleAnalyze() {
    if (!file || !imageUrl) {
      return
    }
    setAnalysis({ status: 'loading', file, imageUrl })
    try {
      const response = await detector.detect(file)
      setAnalysis({ status: 'ready', file, imageUrl, response })
    } catch (error) {
      const detail = error instanceof Error ? error.message : ''
      setAnalysis({
        status: 'error',
        message: `No se pudo completar el análisis. ${detail}`.trim(),
        file,
        imageUrl,
      })
    }
  }

  return (
    <div className="app">
      <header className="topbar">
        <div className="brand">
          <span className="brand__mark">EPP</span>
          <span className="brand__name">Vision</span>
        </div>
        <span className="badge">GPCICD · M3</span>
      </header>

      <main className="main">
        <section className="hero">
          <p className="eyebrow">Visión por computador · 6 categorías</p>
          <h1>Detecta Equipos de Protección Personal en una imagen</h1>
          <p className="lede">
            Sube una foto, ejecuta el detector y revisa qué EPP aparecen y dónde. El sistema
            reporta detecciones; no evalúa cumplimiento normativo.
          </p>
        </section>

        <div className="workspace">
          <UploadPanel
            fileName={file?.name}
            previewUrl={imageUrl}
            busy={busy}
            canAnalyze={Boolean(file)}
            onSelect={handleSelect}
            onAnalyze={handleAnalyze}
          />

          <section className="panel panel--result" aria-labelledby="result-title">
            <header className="panel__header">
              <span className="step">02</span>
              <div>
                <h2 id="result-title">Resultado</h2>
                <p className="muted">Detecciones y ubicación</p>
              </div>
            </header>

            {analysis.status === 'idle' && (
              <div className="empty-state">
                <span className="empty-state__icon" aria-hidden="true">
                  ◉
                </span>
                <strong>Los resultados aparecerán aquí</strong>
                <p className="muted">Selecciona una imagen y pulsa «Analizar imagen».</p>
              </div>
            )}

            {analysis.status === 'selected' && (
              <div className="empty-state">
                <span className="empty-state__icon empty-state__icon--ready" aria-hidden="true">
                  ✓
                </span>
                <strong>Imagen lista para analizar</strong>
                <p className="muted">Pulsa «Analizar imagen» para ejecutar el detector.</p>
              </div>
            )}

            {analysis.status === 'loading' && (
              <div className="loading" role="status" aria-live="polite">
                <span className="spinner spinner--lg" aria-hidden="true" />
                <div>
                  <strong>Analizando imagen…</strong>
                  <p className="muted">El modelo está procesando los píxeles.</p>
                </div>
                <div className="skeleton" aria-hidden="true">
                  <span />
                  <span />
                  <span />
                </div>
              </div>
            )}

            {analysis.status === 'error' && (
              <StatusBanner tone="error">{analysis.message}</StatusBanner>
            )}

            {analysis.status === 'ready' && (
              <div className="result">
                <div className="stats">
                  <div className="stat">
                    <span>Detecciones</span>
                    <strong>{analysis.response.detections.length}</strong>
                  </div>
                  <div className="stat">
                    <span>Tiempo</span>
                    <strong>{Math.round(analysis.response.elapsed_ms ?? 0)} ms</strong>
                  </div>
                  <div className="stat">
                    <span>Modelo</span>
                    <strong>{analysis.response.model_version ?? '—'}</strong>
                  </div>
                </div>

                <AnnotatedCanvas
                  src={analysis.imageUrl}
                  width={analysis.response.image_width}
                  height={analysis.response.image_height}
                  detections={analysis.response.detections}
                  alt={`Imagen analizada: ${analysis.file.name}`}
                />

                {analysis.response.detections.length === 0 ? (
                  <StatusBanner tone="warning">
                    No se detectaron EPP en la imagen. La inferencia terminó sin errores; la
                    ausencia de detecciones no implica que no haya EPP.
                  </StatusBanner>
                ) : (
                  <DetectionTable detections={analysis.response.detections} />
                )}
              </div>
            )}
          </section>
        </div>
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
