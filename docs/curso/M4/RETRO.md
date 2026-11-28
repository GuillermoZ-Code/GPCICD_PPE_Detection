# Retrospectiva — M4

> **Qué es:** cierre del M4 con la dinámica *start / stop / continue* por integrante y
> acciones concretas para el siguiente módulo.
> **Alcance:** se evalúan prácticas, no personas.
> **Fecha:** 23/11/2026.

## Guillermo Zabala

### Start

- Abrir PRs de una sola HU, aunque el arreglo parezca trivial.
- Pedir revisión antes de fusionar un hotfix, incluso si el CI está rojo.

### Stop

- Fusionar cambios propios sin aprobación (pasó con el hotfix #190).
- Tocar `develop` desde ramas locales sin pasar por PR.

### Continue

- Mantener las compuertas de propiedad y CODEOWNERS.
- Revisar PRs en menos de 24 horas.

## Eliana Cardona

### Start

- Escribir el runbook antes del despliegue, no después.
- Probar el `compose` de producción en un equipo limpio.

### Stop

- Asumir que Docker corre en todos los equipos de la demo.
- Dejar la configuración de entorno para el final.

### Continue

- Validar la configuración al arrancar (HU-044).
- Documentar cada servicio con su healthcheck.

## Hernán Estrada

### Start

- Registrar SHA256, versión y `imgsz` en cada artefacto del modelo.
- Publicar el `best.pt` y el `.onnx` antes de mover `models.lock`.

### Stop

- Confiar en notebooks para reproducir entrenamientos.
- Comparar modelos con configuraciones distintas.

### Continue

- Evaluar con la misma partición y semilla.
- Documentar los límites del dataset en la Model Card.

## Jesús Riveros

### Start

- Enlazar cada spec nueva en `backlog.md` en el mismo PR.
- Revisar el espejo y la matriz antes de pedir revisión.

### Stop

- Escribir cifras de pruebas a mano en los documentos.
- Cambiar el alcance de una issue sin aprobación del dueño.

### Continue

- Usar compuertas de CI para trazabilidad, specs y propiedad.
- Repartir el trabajo por olas y respetar WIP 1.

## Acciones

| Acción | Dueño | Fecha |
|---|---|---|
| A-01 Enlazar cada spec nueva en `backlog.md` en el mismo PR | Jesús Riveros | 27/11/2026 |
| A-02 Revisar PRs en menos de 24 horas | Guillermo Zabala | 27/11/2026 |
| A-03 Ejecutar `make check` local antes de pedir revisión | Todos | 27/11/2026 |
| A-04 Publicar el artefacto de YOLO26n con SHA256 antes del rollout | Hernán Estrada | 26/11/2026 |
| A-05 Probar `compose.prod.yml` en un equipo limpio | Eliana Cardona | 27/11/2026 |

## Lecciones

1. **La compuerta automática vale más que la memoria del revisor**: propiedad, specs y
   trazabilidad detectaron errores que la revisión manual no vio.
2. **Un archivo bloqueado necesita dueño único**: el hotfix del backlog no pudo viajar en
   la PR de otro integrante.
3. **Las cifras se generan, no se escriben**: `make pruebas` y la matriz eliminaron las
   contradicciones entre documentos.

## Desviaciones del proceso (registro honesto)

1. **Se agruparon HUs por dependencia técnica, contra la regla 1 HU = 1 PR.** Las PR
   #240 (HU-066/067/068) y #241 (HU-046/071/041/070/069) fusionaron varias HU porque las
   capas no se sostienen por separado: sin `.gitlab-ci.yml` no hay job de build, sin
   `compose.prod.yml` no hay Caddy, y sin Droplet no hay despliegue que probar. La
   trazabilidad se compensó con una spec por HU, la tabla AC → prueba en cada PR y un
   comentario de cierre por issue; aun así, la regla se cumplió solo en parte y queda
   registrada aquí. Para el release `v1.0.0` no se repite: una PR por HU.
