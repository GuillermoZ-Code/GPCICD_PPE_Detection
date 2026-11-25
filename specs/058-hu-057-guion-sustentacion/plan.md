# Plan: HU-057 — Guion de la sustentación M4 y checklist

**Input**: `specs/058-hu-057-guion-sustentacion/spec.md` e issue #113.

## Enfoque

Crear `docs/entrega/FICHA-M4.md` con cuatro bloques:

1. **Datos rápidos**: repositorio, tablero, rama y comandos de arranque.
2. **Guion**: seis intervalos continuos de 0:00 a 15:00; cada uno con responsable,
   evidencia y frase de cierre. Reparto: Eliana (alcance y demo REST), Hernán
   (modelo y métricas), Guillermo (CI/CD y contenedor), Jesús (trazabilidad,
   riesgos y retro).
3. **Checklist §5.4**: tabla con Ítem, Comando, Criterio y Responsable. Incluye
   `develop`, tablero, `uv sync`, pesos fuera de Git, Docker, SPA y CI verde.
4. **Ensayo cronometrado**: tabla con Objetivo/Real/Estado por bloque y nota que
   separa la validación estática del ensayo real pendiente.

## Archivos

- `docs/entrega/FICHA-M4.md` — nuevo; ficha y guion de entrega.
- `tests/test_docs_ficha_m4.py` — nuevo; 8 pruebas de contenido.
- `specs/058-hu-057-guion-sustentacion/` — spec, plan y tareas.

## Decisiones

- Usar nombres de responsables del equipo, no usuarios de GitHub, para que el guion
  se lea en voz alta.
- No inventar minutos reales: la columna `Real` queda «—» hasta el ensayo.
- Evitar rutas personales: comandos con `$env:PPE_MODEL_PATH` y marcadores.

## Riesgos

- Que el guion exceda 15 minutos: se asignan 2/3/3/3/2.5/1.5 minutos.
- Que la ficha quede desactualizada tras fusionar otras PRs: se citan rutas estables
  y se registra la fecha de corte.
