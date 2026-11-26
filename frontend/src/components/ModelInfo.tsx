import { useEffect, useState } from 'react'

import { resolveApiBaseUrl } from '../api/config'
import type { ReadyResponse } from '../types'
import { StatusBanner } from './StatusBanner'

type ModelState =
  | { status: 'loading' }
  | { status: 'ready'; data: ReadyResponse }
  | { status: 'error'; message: string }

interface ModelInfoProps {
  /** Base de la API; por omisión, la resuelta desde `VITE_API_URL`. */
  apiBaseUrl?: string
}

const CODE_URL = 'https://github.com/GuillermoZ-Code/GPCICD_PPE_Detection'
const DATASET_URL = 'https://huggingface.co/datasets/51ddhesh/PPE_Detection'

/** Muestra la identidad del modelo publicada por `GET /health/ready` (HU-079). */
export function ModelInfo({ apiBaseUrl = resolveApiBaseUrl() }: ModelInfoProps) {
  const [state, setState] = useState<ModelState>({ status: 'loading' })
  const [attempt, setAttempt] = useState(0)
  const base = apiBaseUrl.replace(/\/+$/, '')

  useEffect(() => {
    const controller = new AbortController()

    async function load() {
      setState({ status: 'loading' })
      try {
        const response = await fetch(`${base}/health/ready`, {
          signal: controller.signal,
        })
        if (!response.ok) {
          throw new Error(`La API respondió con estado ${response.status}.`)
        }
        const data = (await response.json()) as ReadyResponse
        if (!controller.signal.aborted) {
          setState({ status: 'ready', data })
        }
      } catch (error) {
        if (controller.signal.aborted) {
          return
        }
        const detail = error instanceof Error ? error.message : ''
        setState({
          status: 'error',
          message: `No se pudo consultar la información del modelo. ${detail}`.trim(),
        })
      }
    }

    void load()
    return () => controller.abort()
  }, [base, attempt])

  return (
    <section className="panel model-info" aria-labelledby="model-info-title">
      <header className="panel__header">
        <span className="step">i</span>
        <div>
          <h2 id="model-info-title">Acerca del modelo</h2>
          <p className="muted">Identidad del artefacto que generó las detecciones</p>
        </div>
      </header>

      {state.status === 'loading' && (
        <p className="muted" role="status">
          Consultando la API…
        </p>
      )}

      {state.status === 'error' && (
        <div className="model-info__error">
          <StatusBanner tone="error">{state.message}</StatusBanner>
          <button type="button" onClick={() => setAttempt((value) => value + 1)}>
            Reintentar
          </button>
        </div>
      )}

      {state.status === 'ready' && (
        <>
          <dl className="model-info__grid">
            <div>
              <dt>Versión</dt>
              <dd>{state.data.model_version || '—'}</dd>
            </div>
            <div>
              <dt>Referencia (commit)</dt>
              <dd>{state.data.model_reference || '—'}</dd>
            </div>
            <div>
              <dt>SHA256</dt>
              <dd>{state.data.model_sha256 || '—'}</dd>
            </div>
            <div>
              <dt>Versión de API</dt>
              <dd>{state.data.api_version || '—'}</dd>
            </div>
          </dl>
          <p className="muted">
            Código bajo licencia{' '}
            <a href={CODE_URL} rel="noreferrer">
              AGPL-3.0-only
            </a>
            . Dataset{' '}
            <a href={DATASET_URL} rel="noreferrer">
              PPE_Detection (CC-BY-4.0)
            </a>
            .
          </p>
        </>
      )}
    </section>
  )
}
