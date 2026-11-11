const WAVES = [
  {
    className: 'wave-track wave-track--3',
    d: 'M0,160 C200,220 520,100 720,160 C920,220 1240,100 1440,160 L1440,320 L0,320 Z',
  },
  {
    className: 'wave-track wave-track--2',
    d: 'M0,200 C300,140 500,260 720,200 C940,140 1140,260 1440,200 L1440,320 L0,320 Z',
  },
  {
    className: 'wave-track wave-track--1',
    d: 'M0,180 C240,240 480,120 720,180 C960,240 1200,120 1440,180 L1440,320 L0,320 Z',
  },
]

export function Background() {
  return (
    <div className="bg" aria-hidden="true">
      <span className="blob blob--1" />
      <span className="blob blob--2" />
      <span className="blob blob--3" />
      <span className="grid" />
      <div className="waves">
        {WAVES.map((wave) => (
          <div className={wave.className} key={wave.className}>
            <svg viewBox="0 0 1440 320" preserveAspectRatio="none">
              <path d={wave.d} />
            </svg>
            <svg viewBox="0 0 1440 320" preserveAspectRatio="none">
              <path d={wave.d} />
            </svg>
          </div>
        ))}
      </div>
    </div>
  )
}
