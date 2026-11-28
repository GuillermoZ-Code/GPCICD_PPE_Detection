# Sesgo de tamaño por clase — HU-037

**Estado:** Completado.

**Fecha:** 2026-11-26.

**Responsable:** Hernán Estrada (`HestradaUAO`).

**Issue:** #93.

---

## 1. Método

| Elemento | Valor |
|---|---|
| Modelo | `artifacts/models/yolo26n_clean/weights/best.pt` |
| SHA256 | `FEFB1F1A120FB3AC7BC0F4DE90E5E594BBEF5E936D8168750AA78FC3FB0F27F9` |
| Imágenes | 1095 |
| `imgsz` | 640 |
| `conf` de recolección | 0,001 |
| `iou` de evaluación | 0,7 |
| IoU de emparejamiento | 0,50 |
| Pequeño | área relativa < 1 % |
| Mediano | 1 % ≤ área < 4 % |
| Grande | área ≥ 4 % |

La clasificación usa el área de la caja respecto al área de la imagen. Las
predicciones se asignan por su propio tamaño; las etiquetas por el tamaño del
objeto anotado.

## 2. AP por clase y tamaño

| Clase | AP pequeño | AP mediano | AP grande | GT pequeño | GT mediano | GT grande |
|---|---:|---:|---:|---:|---:|---:|
| Gloves | 0,625 | 0,710 | 0,912 | 120 | 54 | 93 |
| Vest | 0,856 | 0,782 | 0,944 | 8 | 76 | 356 |
| goggles | 0,650 | 0,780 | 0,723 | 19 | 69 | 55 |
| helmet | 0,817 | 0,836 | 0,835 | 322 | 176 | 95 |
| mask | 0,854 | 0,912 | 0,952 | 140 | 74 | 62 |
| safety_shoe | 0,796 | 0,644 | 0,844 | 55 | 55 | 91 |

## 3. Lectura

- AP bajo en `small` indica que el detector pierde objetos pequeños.
- Comparar los tres buckets permite separar el sesgo de tamaño del rendimiento global.
- Los conteos GT muestran si el bucket tiene soporte suficiente.

## 4. Limitaciones

- La partición de test tiene clases desbalanceadas.
- El umbral de tamaño es relativo a la imagen, no absoluto en píxeles.
- El informe no publica imágenes ni recortes.

## 5. Evidencia

- `dist/analisis/tamano/summary.json` (local, fuera de Git).
- [Informe comparativo](YOLO26.md).
- [Análisis de errores](errores.md).
