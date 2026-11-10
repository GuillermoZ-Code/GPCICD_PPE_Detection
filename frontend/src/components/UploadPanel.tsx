import { useState } from 'react'

interface UploadPanelProps {
  onSelect: (file: File) => void
  disabled?: boolean
}

export function UploadPanel({ onSelect, disabled = false }: UploadPanelProps) {
  const [dragging, setDragging] = useState(false)
  const inputId = 'image-input'

  function handleFiles(files: FileList | null) {
    const file = files?.[0]
    if (file) {
      onSelect(file)
    }
  }

  return (
    <section className="card" aria-labelledby="upload-title">
      <h2 id="upload-title">1. Selecciona una imagen</h2>
      <p className="hint">JPEG o PNG, hasta 10 MB.</p>

      <label className="field" htmlFor={inputId}>
        Archivo
      </label>
      <input
        id={inputId}
        className="file-input"
        type="file"
        accept="image/jpeg,image/png"
        disabled={disabled}
        onChange={(event) => {
          handleFiles(event.target.files)
          event.target.value = ''
        }}
      />

      <div
        className={`dropzone${dragging ? ' dropzone--active' : ''}`}
        onDragOver={(event) => {
          event.preventDefault()
          setDragging(true)
        }}
        onDragLeave={() => setDragging(false)}
        onDrop={(event) => {
          event.preventDefault()
          setDragging(false)
          if (!disabled) {
            handleFiles(event.dataTransfer.files)
          }
        }}
      >
        <span>Arrastra una imagen aquí</span>
        <span className="hint">o usa el selector de arriba</span>
      </div>
    </section>
  )
}
