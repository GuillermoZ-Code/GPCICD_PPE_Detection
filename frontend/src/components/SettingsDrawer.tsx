import {
  ACCENTS,
  BACKGROUNDS,
  CLASS_NAMES,
  DENSITIES,
  THEMES,
  type Settings,
} from '../config'
import { colorFor, displayName } from '../labels'

interface SettingsDrawerProps {
  open: boolean
  settings: Settings
  canDownload: boolean
  onChange: (patch: Partial<Settings>) => void
  onClose: () => void
  onReset: () => void
  onDownload: (kind: 'json' | 'csv' | 'png') => void
}

export function SettingsDrawer({
  open,
  settings,
  canDownload,
  onChange,
  onClose,
  onReset,
  onDownload,
}: SettingsDrawerProps) {
  return (
    <>
      <div className={`backdrop${open ? ' is-open' : ''}`} onClick={onClose} aria-hidden="true" />
      <aside
        className={`drawer${open ? ' is-open' : ''}`}
        role="dialog"
        aria-modal="true"
        aria-label="Configuración"
        aria-hidden={!open}
      >
        <header className="drawer__header">
          <h2>Configuración</h2>
          <button className="icon-button" type="button" onClick={onClose} aria-label="Cerrar">
            ✕
          </button>
        </header>

        <div className="drawer__body">
          <section className="section">
            <h3>Apariencia</h3>
            <div className="row">
              <span>Tema</span>
              <div className="segmented">
                {THEMES.map((theme) => (
                  <button
                    key={theme.id}
                    type="button"
                    className={settings.theme === theme.id ? 'is-active' : ''}
                    onClick={() => onChange({ theme: theme.id })}
                  >
                    {theme.label}
                  </button>
                ))}
              </div>
            </div>

            <div className="row">
              <span>Acento</span>
              <div className="swatches">
                {ACCENTS.map((accent) => (
                  <button
                    key={accent.id}
                    type="button"
                    className={`swatch swatch--${accent.id}${
                      settings.accent === accent.id ? ' is-active' : ''
                    }`}
                    aria-label={accent.label}
                    aria-pressed={settings.accent === accent.id}
                    onClick={() => onChange({ accent: accent.id })}
                  />
                ))}
              </div>
            </div>

            <div className="row">
              <span>Animaciones</span>
              <label className="switch">
                <input
                  type="checkbox"
                  checked={settings.animations}
                  onChange={(event) => onChange({ animations: event.target.checked })}
                />
                <span />
              </label>
            </div>

            <div className="row">
              <span>Fondo</span>
              <div className="segmented segmented--wrap">
                {BACKGROUNDS.map((background) => (
                  <button
                    key={background.id}
                    type="button"
                    className={settings.background === background.id ? 'is-active' : ''}
                    onClick={() => onChange({ background: background.id })}
                  >
                    {background.label}
                  </button>
                ))}
              </div>
            </div>

            <div className="row">
              <span>Densidad</span>
              <div className="segmented">
                {DENSITIES.map((density) => (
                  <button
                    key={density.id}
                    type="button"
                    className={settings.density === density.id ? 'is-active' : ''}
                    onClick={() => onChange({ density: density.id })}
                  >
                    {density.label}
                  </button>
                ))}
              </div>
            </div>
          </section>

          <section className="section">
            <h3>Visualización</h3>
            <div className="row">
              <span>Etiquetas en las cajas</span>
              <label className="switch">
                <input
                  type="checkbox"
                  checked={settings.labels}
                  onChange={(event) => onChange({ labels: event.target.checked })}
                />
                <span />
              </label>
            </div>

            <div className="row">
              <span>
                Grosor de caja <em className="value">{settings.thickness} px</em>
              </span>
              <input
                type="range"
                min="1"
                max="6"
                value={settings.thickness}
                onChange={(event) => onChange({ thickness: Number(event.target.value) })}
              />
            </div>

            <div className="row row--stack">
              <span>Clases visibles</span>
              <div className="chips">
                {CLASS_NAMES.map((name) => {
                  const active = settings.classes.includes(name)
                  return (
                    <button
                      key={name}
                      type="button"
                      className={`chip${active ? ' is-active' : ''}`}
                      onClick={() =>
                        onChange({
                          classes: active
                            ? settings.classes.filter((item) => item !== name)
                            : [...settings.classes, name],
                        })
                      }
                    >
                      <span className="chip__dot" style={{ backgroundColor: colorFor(name) }} />
                      {displayName(name)}
                    </button>
                  )
                })}
              </div>
            </div>

            <div className="row">
              <span>
                Confianza visual <em className="value">{settings.visualConfidence} %</em>
              </span>
              <input
                type="range"
                min="0"
                max="99"
                value={settings.visualConfidence}
                onChange={(event) => onChange({ visualConfidence: Number(event.target.value) })}
              />
            </div>
            <p className="note">Filtra las detecciones ya recibidas; no vuelve a ejecutar el modelo.</p>
          </section>

          <section className="section">
            <h3>Detección</h3>
            <div className="row">
              <span>
                Umbral del modelo <em className="value">{Math.round(settings.modelConfidence * 100)} %</em>
              </span>
              <input
                type="range"
                min="1"
                max="99"
                value={Math.round(settings.modelConfidence * 100)}
                onChange={(event) =>
                  onChange({ modelConfidence: Number(event.target.value) / 100 })
                }
              />
            </div>
            <p className="note">
              Se envía a la API en cada análisis: el modelo descarta cajas por debajo de este
              valor. Cambiarlo afecta precisión y recall.
            </p>

            <div className="row">
              <span>Auto-analizar al soltar</span>
              <label className="switch">
                <input
                  type="checkbox"
                  checked={settings.autoAnalyze}
                  onChange={(event) => onChange({ autoAnalyze: event.target.checked })}
                />
                <span />
              </label>
            </div>
          </section>

          <section className="section">
            <h3>Resultados</h3>
            <div className="row row--stack">
              <span>Descargas</span>
              <div className="actions">
                <button
                  className="button button--ghost"
                  type="button"
                  disabled={!canDownload}
                  onClick={() => onDownload('json')}
                >
                  JSON
                </button>
                <button
                  className="button button--ghost"
                  type="button"
                  disabled={!canDownload}
                  onClick={() => onDownload('csv')}
                >
                  CSV
                </button>
                <button
                  className="button button--ghost"
                  type="button"
                  disabled={!canDownload}
                  onClick={() => onDownload('png')}
                >
                  PNG
                </button>
              </div>
            </div>
          </section>

          <section className="section">
            <h3>Avanzado</h3>
            <div className="row">
              <span>Endpoint</span>
              <code className="mono">{import.meta.env.VITE_API_URL || 'simulado'}</code>
            </div>
            <div className="row">
              <span>Modelo</span>
              <code className="mono">yolo11s_clean</code>
            </div>
          </section>
        </div>

        <footer className="drawer__footer">
          <button className="button button--ghost" type="button" onClick={onReset}>
            Restablecer preferencias
          </button>
        </footer>
      </aside>
    </>
  )
}
