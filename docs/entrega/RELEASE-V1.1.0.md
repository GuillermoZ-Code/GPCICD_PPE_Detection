# Release v1.1.0 — M4

> **Tag:** `v1.1.0` · **Commit:** `7aa74ccef6a48b178959473b74168abeae89e707`
> **Fecha:** 2026-11-28 · **HU:** HU-111 (#167) · **Spec:** `specs/112-hu-111-release/`
> **Release:** <https://github.com/GuillermoZ-Code/GPCICD_PPE_Detection/releases/tag/v1.1.0>
> **Estado:** publicada; quedan dos verificaciones de GitLab pendientes de acceso.

## 1. Checklist de release

- [x] Merge `develop → main` con **merge commit** (PR #282, `7aa74cc`).
- [x] Tag `v1.1.0` sobre el merge commit y release de GitHub con notas.
- [x] `CHANGELOG.md` con `## [1.1.0] - 2026-11-28` y las HUs de accesibilidad,
      historial, manual, capacidad y MLflow.
- [x] CI de GitHub Actions de las PRs incluidas en verde y en `main`.
- [ ] Pipeline de GitLab en `main` en verde (`build_image` + `deploy`): el espejo está
      en verde, pero el proyecto de GitLab es privado y esta estación no tiene token.
- [ ] Imágenes API, SPA y Caddy publicadas con el tag del commit: no verificable sin
      acceso al registry.
- [x] Modelo **YOLO26n clean** montado `:ro` con SHA256
      `FEFB1F1A120FB3AC7BC0F4DE90E5E594BBEF5E936D8168750AA78FC3FB0F27F9`.
- [x] `/health` y `/health/ready` responden en el Droplet: `status: ok`,
      `model_loaded: true`, `model_version: yolo26n-clean` (verificado 2026-11-28
      04:45 UTC; el campo `commit` no se expone).
- [x] Licencia **AGPL-3.0-only** y atribución **CC-BY-4.0** visibles.
- [x] Rollback por tag documentado y probado (`9b20972a` → `e36ae555`, 37,6 s / 36,7 s).
- [x] Runbook de despliegue y verificación (`docs/operacion/despliegue.md`).
- [x] Suite de pruebas **1.229** (1.108 pytest + 121 Vitest), superior a 1.200.

## 2. Qué incluye

- **HU-080** — accesibilidad WCAG 2.2 AA (PR #275).
- **HU-088** — historial de análisis de la sesión (PR #276).
- **HU-058** — manual de usuario de la SPA (PR #272).
- **HU-109** — capacidad y velocidad real (PR #273).
- **HU-110** — MLflow en el Droplet con autenticación, perfil opcional (PR #277).
- **HU-077** — flujo de carga, progreso y resultados (PR #267).
- Base v1.0.0: YOLO26n + ONNX 640, API REST/gRPC, SPA, Docker CPU, Caddy y MLflow.

## 3. Verificación reproducible

```bash
make check
make frontend-check
PPE_PUBLIC_URL=https://143.198.10.157.sslip.io make verify
curl -s https://143.198.10.157.sslip.io/health
```

Salida esperada de `/health`:

```json
{"status": "ok", "model_loaded": true, "model_version": "yolo26n-clean",
 "model_sha256": "FEFB1F1A120FB3AC7BC0F4DE90E5E594BBEF5E936D8168750AA78FC3FB0F27F9"}
```

## 4. Rollback

1. Desplegar el tag anterior con `make deploy TAG=<tag-anterior>`.
2. Si el problema es el modelo, restaurar `models.lock` a `yolo11s-clean` y montar su
   `best.pt` (ADR 0009).
3. Repetir `make verify` y una inferencia real.

## 5. Pendientes de cierre

| Pendiente | Dueño | Estado |
|---|---|---|
| Verificar el pipeline de GitLab en `main` (`build_image` + `deploy`) | Guillermo | Pendiente de acceso al proyecto privado |
| Confirmar las imágenes con el tag de `7aa74cc` en el registry | Guillermo | Pendiente de acceso al registry |
| Regenerar `ESTADO.md` y `AGENTS.md` §0 | Jesús | Hecho el 2026-11-28 04:47 UTC |
| Actualizar estados del `backlog.md` a cerrada | Jesús | Hecho (113/113 cerradas) |
| Desplegar el perfil `mlflow` en el Droplet | Guillermo | Pendiente de SSH |
