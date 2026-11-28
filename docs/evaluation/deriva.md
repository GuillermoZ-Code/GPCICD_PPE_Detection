# Estadísticas de entrada para deriva — HU-038

**Estado:** Completado.

**Fecha:** 2026-11-27.

**Responsable:** Hernán Estrada (`HestradaUAO`).

**Issue:** #94.

---

## 1. Método

| Elemento | Valor |
|---|---|
| Fuente | `dataset_limpio/test/images` |
| Muestra | 100 imágenes fijas, ordenadas por nombre |
| Brillo | luminancia ITU-R BT.601: 0,299 R + 0,587 G + 0,114 B |
| Relación de aspecto | ancho / alto |
| Almacenamiento | solo agregados numéricos; no se guardan imágenes |

## 2. Resumen

| Métrica | Valor |
|---|---:|
| Imágenes | 100 |
| Ancho medio | 640,000 px |
| Alto medio | 640,000 px |
| Aspecto medio | 1,000 |
| Brillo medio | 127,476 |
| Brillo mínimo | 37,356 |
| Brillo máximo | 195,304 |

## 3. Uso previsto

Estos valores forman la línea base para comparar lotes de producción. Un cambio
sostenido de brillo medio o de relación de aspecto puede indicar una cámara,
resolución o iluminación distintas; no demuestra por sí solo una caída del modelo.

## 4. Privacidad y límites

- No se almacena la imagen, el nombre del archivo ni datos personales.
- La muestra es pequeña y no cubre todas las condiciones de captura.
- El brillo es una media global; no detecta cambios locales ni regiones oscuras.
- No se usa para decidir cumplimiento de EPP.

## 5. Evidencia

- `dist/deriva/summary.json` (local, fuera de Git).
- [Informe de evaluación](YOLO26.md).
