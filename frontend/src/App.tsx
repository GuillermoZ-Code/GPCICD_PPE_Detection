import { useEffect, useMemo, useRef, useState } from 'react'

import { createClient, type DetectorClient } from './api/client'
import { AnnotatedCanvas } from './components/AnnotatedCanvas'
import { Background } from './components/Background'
import { DetectionTable } from './components/DetectionTable'
import { SettingsDrawer } from './components/SettingsDrawer'
import { StatusBanner } from './components/StatusBanner'
import { UploadPanel } from './components/UploadPanel'
import {
  applySettings,
  DEFAULT_SETTINGS,
  loadSettings,
  resolveTheme,
  saveSettings,
  type Settings,
} from './config'
import { detectionsToCsv, downloadBlob, downloadText } from './download'
import { filterDetections } from './filter'
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
  const [settings, setSettings] = useState<Settings>(loadSettings)
  const [analysis, setAnalysis] = useState<Analysis>({ status: 'idle' })
  const [drawerOpen, setDrawerOpen] = useState(false)
  const imageUrlRef = useRef<string | null>(null)
  const canvasRef = useRef<HTMLCanvasElement>(null)

  useEffect(() => {
    applySettings(settings)
    saveSettings(settings)
  }, [settings])

  useEffect(() => {
    if (settings.theme !== 'system' || typeof window.matchMedia !== 'function') {
      return
    }
    const media = window.matchMedia('(prefers-color-scheme: light)')
    const handler = () => applySettings(settings)
    media.addEventListener?.('change', handler)
    return () => media.removeEventListener?.('change', handler)
  }, [settings])

  useEffect(() => {
    return () => {
      if (imageUrlRef.current) {
        URL.revokeObjectURL(imageUrlRef.current)
      }
    }
  }, [])

  useEffect(() => {
    if (!drawerOpen) {
      return
    }
    const handler = (event: KeyboardEvent) => {
      if (event.key === 'Escape') {
        setDrawerOpen(false)
      }
    }
    document.addEventListener('keydown', handler)
    return () => document.removeEventListener('keydown', handler)
  }, [drawerOpen])

  const file = 'file' in analysis ? analysis.file : undefined
  const imageUrl = 'imageUrl' in analysis ? analysis.imageUrl : undefined
  const busy = analysis.status === 'loading'
  const visible =
    analysis.status === 'ready'
      ? filterDetections(analysis.response.detections, settings)
      : []

  function updateSettings(patch: Partial<Settings>) {
    setSettings((current) => ({ ...current, ...patch }))
  }

  async function analyze(target: File, url: string) {
    setAnalysis({ status: 'loading', file: target, imageUrl: url })
    try {
      const response = await detector.detect(target, settings.modelConfidence)
      setAnalysis({ status: 'ready', file: target, imageUrl: url, response })
    } catch (error) {
      const detail = error instanceof Error ? error.message : ''
      setAnalysis({
        status: 'error',
        message: `No se pudo completar el análisis. ${detail}`.trim(),
        file: target,
        imageUrl: url,
      })
    }
  }

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
    if (settings.autoAnalyze) {
      void analyze(nextFile, nextUrl)
    }
  }

  function handleAnalyze() {
    if (file && imageUrl) {
      void analyze(file, imageUrl)
    }
  }

  function handleDownload(kind: 'json' | 'csv' | 'png') {
    if (analysis.status !== 'ready') {
      return
    }
    const base = analysis.file.name.replace(/\.[^.]+$/, '')
    const visible = filterDetections(analysis.response.detections, settings)
    if (kind === 'json') {
      const payload = {
        file: analysis.file.name,
        model_version: analysis.response.model_version,
        elapsed_ms: analysis.response.elapsed_ms,
        image_width: analysis.response.image_width,
        image_height: analysis.response.image_height,
        filters: {
          visual_confidence: settings.visualConfidence / 100,
          classes: settings.classes,
        },
        detections: visible,
      }
      downloadText(
        `${base}-detecciones.json`,
        JSON.stringify(payload, null, 2),
        'application/json',
      )
      return
    }
    if (kind === 'csv') {
      downloadText(
        `${base}-detecciones.csv`,
        detectionsToCsv(analysis.file.name, visible),
        'text/csv',
      )
      return
    }
    canvasRef.current?.toBlob((blob) => {
      if (blob) {
        downloadBlob(blob, `${base}-anotada.png`)
      }
    }, 'image/png')
  }

  const resolvedTheme = resolveTheme(settings.theme)
  const canDownload = analysis.status === 'ready'

  return (
    <div className="app">
      <Background />

      <header className="topbar">
        <div className="brand">
          <span className="brand__mark">EPP</span>
          <span className="brand__name">Vision</span>
        </div>
        <div className="topbar__actions">
          <span className="badge">GPCICD · M3</span>
          <button
            className="icon-button"
            type="button"
            aria-label="Cambiar tema"
            title="Cambiar tema"
            onClick={() => updateSettings({ theme: resolvedTheme === 'dark' ? 'light' : 'dark' })}
          >
            {resolvedTheme === 'dark' ? '☀' : '☾'}
          </button>
          <button
            className="icon-button"
            type="button"
            aria-label="Abrir configuración"
            title="Configuración"
            onClick={() => setDrawerOpen(true)}
          >
            ⚙
          </button>
        </div>
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
                  <p className="muted">
                    Validando, enviando y detectando con umbral{' '}
                    {Math.round(settings.modelConfidence * 100)} %.
                  </p>
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
                    <strong>{visible.length}</strong>
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
                  detections={visible}
                  thickness={settings.thickness}
                  showLabels={settings.labels}
                  canvasRef={canvasRef}
                  alt={`Imagen analizada: ${analysis.file.name}`}
                />

                {analysis.response.detections.length === 0 && (
                  <StatusBanner tone="warning">
                    No se detectaron EPP en la imagen. La inferencia terminó sin errores; la
                    ausencia de detecciones no implica que no haya EPP.
                  </StatusBanner>
                )}

                {analysis.response.detections.length > 0 &&
                  visible.length === 0 && (
                    <StatusBanner tone="warning">
                      Hay detecciones, pero ninguna pasa los filtros actuales de confianza o
                      clase.
                    </StatusBanner>
                  )}

                {visible.length > 0 && (
                  <DetectionTable detections={visible} />
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

      <SettingsDrawer
        open={drawerOpen}
        settings={settings}
        canDownload={canDownload}
        onChange={updateSettings}
        onClose={() => setDrawerOpen(false)}
        onReset={() => setSettings({ ...DEFAULT_SETTINGS })}
        onDownload={handleDownload}
      />
    </div>
  )
}
