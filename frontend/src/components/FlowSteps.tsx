/** HU-077 — pasos visibles del flujo de carga, análisis y resultados. */

const STEPS = [
  { id: 'select', number: '01', label: 'Selección' },
  { id: 'analyze', number: '02', label: 'Análisis' },
  { id: 'results', number: '03', label: 'Resultados' },
] as const

export type FlowStep = (typeof STEPS)[number]['id']

interface FlowStepsProps {
  current: FlowStep
}

export function FlowSteps({ current }: FlowStepsProps) {
  const active = STEPS.findIndex((step) => step.id === current)

  return (
    <ol className="flow" aria-label="Flujo de análisis">
      {STEPS.map((step, index) => {
        const state = index < active ? 'done' : index === active ? 'active' : 'pending'
        return (
          <li
            key={step.id}
            className={`flow__step flow__step--${state}`}
            aria-current={state === 'active' ? 'step' : undefined}
          >
            <span className="flow__number">{step.number}</span>
            <span className="flow__label">{step.label}</span>
          </li>
        )
      })}
    </ol>
  )
}
