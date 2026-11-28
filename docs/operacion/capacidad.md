# Capacidad del servicio — validación local del instrumento

**Fecha:** 2026-11-27 · **Etiqueta:** validación local del instrumento (servidor ficticio)

> ⚠️ Esta medición se ejecutó contra un servidor local o ficticio para validar el instrumento; **no es una medición real del Droplet**. La medición real contra el servicio desplegado queda pendiente y es responsabilidad de Guillermo Zabala (@GuillermoZ-Code).

## 1. Configuración

| Parámetro | Valor |
|---|---|
| Objetivo | `http://127.0.0.1:8765/health` |
| Peticiones | 120 |
| Concurrencia | 4 |
| Timeout | 10.0 s |
| Cuerpo | sin cuerpo (GET) |
| Muestreo de recursos | cada 0.05 s |

## 2. Resultados

| Métrica | Valor |
|---|---:|
| p50 | 7.0 ms |
| p95 | 12.2 ms |
| Throughput | 511.18 req/s |
| Éxitos | 120/120 |
| Errores | 0 |
| Duración | 0.23 s |

### Errores

Sin errores.

## 3. CPU y RAM

| Métrica | Valor |
|---|---:|
| CPU máxima del proceso | 50.0 % |
| RSS máxima | 39.5 MB |
| RAM del sistema | 83.0 % |
| Muestras | 3 |

## 4. Recomendación provisional (validación local)

| Parámetro | Valor |
|---|---|
| Droplet | `s-1vcpu-2gb` |
| Workers API | 2 |
| Motivo | hipótesis local: 2 workers; confirmar en el Droplet |

> La recomendación se deriva de una medición local: no autoriza cambiar el despliegue hasta repetir el ensayo en el Droplet.

## 5. Reproducción

```bash
uv run python -m ppe_detection.tools.load_test \
  --url http://127.0.0.1:8765 --path /health \
  --requests 120 --concurrency 4 \
  --output docs/operacion/capacidad.md
```

## 6. Pendiente real

- [ ] Guillermo: ejecutar el mismo script contra la URL pública con basic auth.
- [ ] Guillermo: adjuntar salida real, repetir con `--image` sobre `/predict`.
- [ ] Guillermo: decidir tamaño y workers definitivos con esa medición.
