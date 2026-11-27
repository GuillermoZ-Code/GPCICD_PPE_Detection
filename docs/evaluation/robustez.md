# Robustez ante luz, ruido y escala — HU-032

**Estado:** Completado.

**Fecha:** 2026-11-27.

**Responsable:** Hernán Estrada (`HestradaUAO`).

**Issue:** #88.

---

## 1. Método

| Elemento | Valor |
|---|---|
| Modelo | `artifacts/models/yolo26n_clean/weights/best.pt` |
| SHA256 | `FEFB1F1A120FB3AC7BC0F4DE90E5E594BBEF5E936D8168750AA78FC3FB0F27F9` |
| Muestra | 100 imágenes fijas de test, ordenadas por nombre |
| `imgsz` | 640 |
| IoU de validación | 0,7 |
| Semilla de ruido | 42 |
| Brillo | factor 0,7 |
| Ruido | gaussiano, sigma 12 |
| Escala | factor 0,75 |

Las perturbaciones se aplican antes de la inferencia. En la variante `scale` las
cajas normalizadas se conservan; al reducir la imagen, los objetos ocupan menos
píxeles. La muestra es fija para que las cuatro filas sean comparables y la
evidencia se pueda repetir.

## 2. mAP por perturbación

| Perturbación | mAP@0.5 | mAP@0.5:0.95 | Δ mAP@0.5 vs. limpio |
|---|---:|---:|---:|
| clean | 0,860 | 0,612 | 0,000 |
| brightness | 0,847 | 0,596 | -0,014 |
| noise | 0,624 | 0,387 | -0,236 |
| scale | 0,839 | 0,575 | -0,021 |

## 3. Lectura

- `brightness` mide la caída con poca luz; `noise` simula sensores ruidosos.
- `scale` reduce la imagen al 75 % y obliga al detector a trabajar con menos píxeles.
- La tabla usa una muestra de 100 imágenes para acotar el costo en CPU; no
  sustituye la evaluación completa de `docs/evaluation/YOLO26.md`.

## 4. Limitaciones

- La muestra es pequeña y las clases pueden quedar desbalanceadas.
- Una sola semilla y una sola intensidad por perturbación.
- El resultado no demuestra robustez en cámaras reales ni en todas las condiciones.
- No se publican imágenes ni recortes.

## 5. Evidencia

- `dist/robustez/summary.json` (local, fuera de Git).
- [Informe comparativo](YOLO26.md).
- [Análisis de errores](errores.md).
