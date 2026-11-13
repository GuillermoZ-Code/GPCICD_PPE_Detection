import { useRef, useState } from 'react'

interface UploadPanelProps {
  fileName?: string
  previewUrl?: string
  busy?: boolean
  canAnalyze: boolean
  onSelect: (file: File) => void
  onAnalyze: () => void
}

export function UploadPanel({
  fileName,
  previewUrl,
  busy = false,
  canAnalyze,
  onSelect,
  onAnalyze,
}: UploadPanelProps) {
  const [dragging, setDragging] = useState(false)
  const inputRef = useRef<HTMLInputElement>(null)

  function handleFiles(files: FileList | null) {
    const file = files?.[0]
    if (file) {
      onSelect(file)
    }
  }

  return (
    <section className="panel panel--upload" aria-labelledby="upload-title">
      <header className="panel__header">
        <span className="step">01</span>
        <div>
          <h2 id="upload-title">Selecciona una imagen</h2>
          <p className="muted">JPEG (jpg, jpeg, jfif) o PNG · máximo 10 MB</p>
        </div>
      </header>

      <label
        className={`dropzone${dragging ? ' is-dragging' : ''}${previewUrl ? ' has-preview' : ''}`}
        onDragOver={(event) => {
          event.preventDefault()
          setDragging(true)
        }}
        onDragLeave={() => setDragging(false)}
        onDrop={(event) => {
          event.preventDefault()
          setDragging(false)
          if (!busy) {
            handleFiles(event.dataTransfer.files)
          }
        }}
      >
        <input
          ref={inputRef}
          id="image-input"
          className="sr-only"
          type="file"
          accept="image/jpeg,image/png"
          aria-label="Archivo"
          disabled={busy}
          onChange={(event) => {
            handleFiles(event.target.files)
            event.target.value = ''
          }}
        />

        {previewUrl ? (
          <img className="dropzone__preview" src={previewUrl} alt={`Vista previa: ${fileName}`} />
        ) : (
          <span className="dropzone__empty">
            <span className="dropzone__icon" aria-hidden="true">
              ↑
            </span>
            <strong>Arrastra tu imagen aquí</strong>
            <span className="muted">o haz clic para elegir un archivo</span>
          </span>
        )}
      </label>

      {fileName && (
        <p className="file-meta">
          <span className="dot dot--accent" aria-hidden="true" />
          {fileName}
        </p>
      )}

      <div className="actions">
        <button
          type="button"
          className="button button--ghost"
          onClick={() => inputRef.current?.click()}
          disabled={busy}
        >
          {previewUrl ? 'Cambiar imagen' : 'Elegir imagen'}
        </button>
        <button
          type="button"
          className="button button--primary"
          onClick={onAnalyze}
          disabled={!canAnalyze || busy}
        >
          {busy ? (
            <>
              <span className="spinner" aria-hidden="true" />
              Analizando…
            </>
          ) : (
            'Analizar imagen'
          )}
        </button>
      </div>
    </section>
  )
}
