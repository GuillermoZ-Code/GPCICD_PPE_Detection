# Análisis de falsos positivos y negativos — HU-030

**Estado:** Completado.

**Fecha:** 2026-11-24.

**Responsable:** Hernán Estrada (`HestradaUAO`).

**Issue:** #86.

---

## 1. Configuración

| Parámetro | Valor |
|---|---|
| Modelo | `yolo26n-clean` |
| SHA256 | `FEFB1F1A120FB3AC7BC0F4DE90E5E594BBEF5E936D8168750AA78FC3FB0F27F9` |
| Partición | `test` |
| Imágenes | 1095 |
| Objetos GT | 1920 |
| Predicciones | 1890 |
| Confianza | 0,25 |
| IoU de emparejamiento | 0,50 |
| Objeto pequeño | área < 1 % de la imagen |

No se publican imágenes ni recortes. El informe solo usa conteos, clases,
confianza y geometría de las cajas.

## 2. Resumen

| TP | FP | FN | Precision | Recall | F1 |
|---:|---:|---:|---:|---:|---:|
| 1636 | 254 | 284 | 0,866 | 0,852 | 0,859 |

## 3. Categorías

| Categoría | Casos |
|---|---:|
| background | 94 |
| class_confusion | 6 |
| duplicate | 18 |
| localization | 98 |
| occlusion_or_missed | 92 |
| small_object | 230 |

## 4. Errores por clase

| Clase | TP | FP | FN |
|---|---:|---:|---:|
| Gloves | 199 | 67 | 68 |
| Vest | 421 | 43 | 19 |
| goggles | 133 | 14 | 10 |
| helmet | 474 | 64 | 119 |
| mask | 249 | 30 | 27 |
| safety_shoe | 160 | 36 | 41 |

## 5. Ejemplos

Los ejemplos se identifican por imagen y clase; no se adjuntan recortes.

### Falsos positivos

| Imagen | Clase | Categoría | Confianza | IoU con GT | Área relativa |
|---|---|---|---:|---:|---:|
| 00126_jpg.rf.0cfc9e44de939093f2fc5c7bb5fa8e3d.jpg | Vest | background | 0,542 | 0,000 | 0,132 |
| 00173_jpg.rf.a7a7d29dcbea92d98284d6f096a560ff.jpg | Vest | background | 0,671 | 0,000 | 0,015 |
| 00173_jpg.rf.a7a7d29dcbea92d98284d6f096a560ff.jpg | Vest | background | 0,632 | 0,000 | 0,017 |
| 00269_jpg.rf.f8970aaa0e97f72edb2e86cf4e2de285.jpg | goggles | background | 0,373 | 0,000 | 0,042 |
| 005308_jpg.rf.7faf545c7704680ac6a605a478c8c6a6.jpg | helmet | small_object | 0,811 | 0,000 | 0,009 |
| 005330_jpg.rf.f18434f65a6336f59e69de7f4a922243.jpg | helmet | background | 0,611 | 0,000 | 0,010 |
| 005330_jpg.rf.f18434f65a6336f59e69de7f4a922243.jpg | helmet | background | 0,352 | 0,013 | 0,027 |
| 005342_jpg.rf.947556cc3388d84cbdec7c92df1baa3d.jpg | helmet | localization | 0,579 | 0,431 | 0,003 |
| 005360_jpg.rf.8be2d3a7a5eb1383cec8da015aa0dd1e.jpg | helmet | small_object | 0,313 | 0,000 | 0,001 |
| 005366_jpg.rf.cd84d93b691c718986566f3341b9c0d2.jpg | mask | background | 0,307 | 0,089 | 0,179 |

### Falsos negativos

| Imagen | Clase | Categoría | IoU con predicción | Área relativa |
|---|---|---|---:|---:|
| 00052_jpg.rf.6b74b9df804347c0118cea0fcdf5c542.jpg | Vest | occlusion_or_missed | 0,000 | 0,314 |
| 00052_jpg.rf.6b74b9df804347c0118cea0fcdf5c542.jpg | Vest | occlusion_or_missed | 0,000 | 0,377 |
| 00231_jpg.rf.8b47136f1db0c8ff2642600a756ac3a4.jpg | Vest | occlusion_or_missed | 0,000 | 0,077 |
| 00231_jpg.rf.9a2e8eca297c963735691a8da3a42a32.jpg | Vest | occlusion_or_missed | 0,000 | 0,077 |
| 00231_jpg.rf.fba54c7826028a40eb82388a7565aa8d.jpg | Vest | occlusion_or_missed | 0,000 | 0,077 |
| 005342_jpg.rf.947556cc3388d84cbdec7c92df1baa3d.jpg | helmet | small_object | 0,006 | 0,008 |
| 005342_jpg.rf.947556cc3388d84cbdec7c92df1baa3d.jpg | helmet | localization | 0,431 | 0,008 |
| 005358_jpg.rf.ef6113dd8698a0789d24ba443822293d.jpg | helmet | small_object | 0,075 | 0,003 |
| 005360_jpg.rf.8be2d3a7a5eb1383cec8da015aa0dd1e.jpg | helmet | small_object | 0,000 | 0,005 |
| 005360_jpg.rf.8be2d3a7a5eb1383cec8da015aa0dd1e.jpg | helmet | small_object | 0,000 | 0,002 |

## 6. Lectura

- `small_object` es la causa más frecuente: **230 de 538 errores (42,8 %)**. El
  detector pierde o inventa cajas en objetos con área menor al 1 % de la imagen.
- `localization` aporta **98** errores: la clase es correcta, pero la caja no alcanza
  IoU 0,50.
- `background` aporta **94** falsos positivos sin solapamiento relevante.
- `occlusion_or_missed` aporta **92** falsos negativos sin predicción cercana; requiere
  revisión visual para distinguir oclusión de objeto no anotado.
- `duplicate` (**18**) y `class_confusion` (**6**) son causas menores.
- `helmet` concentra **119 FN**; `Gloves` tiene **67 FP** y **68 FN**. Son las clases
  que más conviene revisar en la sustentación.
- `Vest` es la clase más sólida: **421 TP**, 43 FP y 19 FN.

## 7. Limitaciones

- La categoría es geométrica; la oclusión real necesita revisión de imágenes.
- El análisis usa IoU 0,50 y confianza 0,25; otros umbrales cambian los conteos.
- Las imágenes con personas no se publican ni se recortan.

