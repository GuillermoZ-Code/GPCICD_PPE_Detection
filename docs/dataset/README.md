# Dataset Card — PPE Detection (`51ddhesh/PPE_Detection`)

**Estado:** Documentado.

**Fecha:** 2026-11-26.

**Responsable:** Hernán Estrada (`HestradaUAO`).

**Issue:** #84 (HU-028).

**Relacionado:** [EDA](EDA.md), [ADR 0002](../adr/0002-dataset.md),
[Model Card](../model-card.md).

---

## 1. Identidad y licencia

| Campo | Valor |
|---|---|
| Nombre | PPE Detection |
| Fuente | [`51ddhesh/PPE_Detection`](https://huggingface.co/datasets/51ddhesh/PPE_Detection) |
| Licencia declarada | **CC-BY-4.0** |
| Archivo original | `PPE.zip`, 668 MB |
| SHA-256 del ZIP | `4b10c6da2abc0f9b5ddf0b37513879ae16922b9f3f21e8b75de12f45cd3de9ac` |
| Formato | JPEG 640×640 + etiquetas YOLO TXT |
| Clases | 6 |

La licencia **CC-BY-4.0 exige atribución**. El texto reutilizable está en la sección 5.

## 2. Clases y orden canónico

El orden del `data.yaml` es el contrato del proyecto:

```text
0 Gloves
1 Vest
2 goggles
3 helmet
4 mask
5 safety_shoe
```

La interfaz puede capitalizar o traducir los nombres, pero el contrato de detección
usa estos identificadores.

## 3. Particiones

| Conjunto | Imágenes |
|---|---:|
| Original | 12.078 |
| Limpio v1 (`dataset_limpio`) | 10.941 |
| Train limpio | 7.658 |
| Valid limpio | 2.188 |
| Test limpio | 1.095 |

El split corregido sin fuga (`data/ds_base`) conserva 10.941 imágenes y ajusta la
frontera a 7.659 / 2.188 / 1.094. La diferencia de una imagen entre variantes está
documentada en el [EDA](EDA.md).

## 4. Limpieza aplicada

| Acción | Resultado |
|---|---:|
| Duplicados exactos eliminados | 1.137 |
| Grupos exactos entre splits corregidos | 969 |
| Conflictos de etiquetas | 47 |
| Líneas inválidas descartadas | 1 |
| Imágenes vacías en el dataset limpio | 2.647 (24,2 %) |
| Fuga del split corregido | 0 base, 0 exacta, 0 ±4 |

La limpieza eliminó duplicados exactos y corrigió la fuga por aumentaciones con el
mismo nombre base. El detalle y las decisiones están en el [EDA](EDA.md) y en el
[ADR 0002](../adr/0002-dataset.md).

## 5. Atribución reutilizable

Este bloque puede copiarse en el README, la SPA o una publicación:

> **Dataset:** *PPE Detection* de `51ddhesh`, disponible en
> <https://huggingface.co/datasets/51ddhesh/PPE_Detection>.
> **Licencia:** CC-BY-4.0 (<https://creativecommons.org/licenses/by/4.0/>).
> **Modificaciones del proyecto:** limpieza de duplicados exactos, corrección de
> conflictos de etiquetas y regeneración del split para eliminar fuga por
> aumentaciones. Las métricas y limitaciones se documentan en la
> [Model Card](../model-card.md).

La atribución debe conservarse aunque el dataset se use solo para evaluación.

## 6. Limitaciones y riesgos

- **Fuente original no declarada:** la tarjeta de Hugging Face no indica de dónde
  provienen las fotografías ni conserva un crédito verificable; mantiene el
  placeholder `<your-username>/ppe-detection`.
- **Consentimiento de rostros no documentado:** no se declara consentimiento ni
  tratamiento de datos personales. Las imágenes pueden contener personas.
- **No hay clase `person` ni `no-EPP`:** el sistema reporta qué EPP aparecen, no si
  un trabajador cumple o incumple.
- **Desbalance:** `Vest` tiene 4.418 objetos frente a 1.431 de `goggles` (3,1×).
  `Gloves`, `mask` y `safety_shoe` requieren análisis por clase.
- **Imágenes vacías:** 24,2 % del dataset limpio no contiene objetos; afectan la
  interpretación de falsos positivos.
- **Uso responsable:** no se publican imágenes ni recortes con personas; las
  evidencias del proyecto usan conteos y geometría.

## 7. Evidencia

- [EDA del dataset](EDA.md): auditoría, conteos, duplicados y fuga.
- [ADR 0002](../adr/0002-dataset.md): decisión y riesgos.
- [Model Card](../model-card.md): métricas, sesgos y limitaciones del detector.
- `docs/evaluation/errores.md`: análisis de FP/FN.
