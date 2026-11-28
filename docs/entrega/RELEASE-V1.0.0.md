# Release v1.0.0 — M4

> **Tag:** `v1.0.0` · **Commit:** `e36ae555c4dd173817ac7b8dd3054d3426c90e3d`
> **Fecha:** 2026-11-28 03:38 UTC · **Release:** [v1.0.0 — M4](https://github.com/GuillermoZ-Code/GPCICD_PPE_Detection/releases/tag/v1.0.0)
> **HU:** HU-111 (#167) · **Spec:** `specs/112-hu-111-release/`

## 1. Checklist de release

- [x] Merge `develop → main` con **merge commit** (PR #265, `e36ae555`).
- [x] Tag `v1.0.0` sobre el merge commit y release de GitHub con notas.
- [x] `CHANGELOG.md` con `## [1.0.0] - 2026-11-27`, enlaces a HU y PRs y las
      categorías Added / Changed / Fixed.
- [x] CI de GitHub Actions en verde sobre `main` (Calidad, Frontend, Docker y Trivy,
      Secretos, Matriz, Plantilla, Propiedad y Specs).
- [x] Imagen CPU publicada por el pipeline de GitLab con tag por commit
      (`$CI_REGISTRY_IMAGE/api:<sha>` y `/web:<sha>`); Docker Hub es opcional.
- [x] Modelo **YOLO26n clean** montado en solo lectura (`:ro`) con SHA256
      `FEFB1F1A120FB3AC7BC0F4DE90E5E594BBEF5E936D8168750AA78FC3FB0F27F9`.
- [x] `/health` y `/health/ready` verificados en el Droplet:
      `https://143.198.10.157.sslip.io/health` responde `model_version:
      yolo26n-clean` y `model_loaded: true`.
- [x] Licencia **AGPL-3.0-only** enlazada en la SPA y atribución **CC-BY-4.0** del
      dataset visibles (ADR 0003 y HU-060).
- [x] Rollback documentado: restaurar el tag anterior y el modelo YOLO11s
      (`docs/operacion/despliegue.md`).
- [x] Runbook de despliegue y verificación (`docs/operacion/despliegue.md`,
      `make deploy` y `make verify`).
- [ ] Suite de pruebas **≥ 1.200**: al cortar el tag había ~1.064; el frente de cierre
      (PRs #268–#273) lleva **1.168** y las HU abiertas aportan 48 más. Se completa
      antes de la sustentación y se publica como `v1.0.1` si hace falta.

## 2. Qué incluye

- Detección de las seis clases de EPP con **YOLO26n + ONNX 640** en CPU (ADR 0009).
- API REST (`/predict`, `/health`, `/health/live`, `/health/ready`) y gRPC interno
  (ADR 0010).
- SPA React servida por Caddy con HTTPS automático y basic auth (ADR 0013).
- Pipeline de GitLab espejo de GitHub (ADR 0007) y despliegue en el Droplet
  (ADR 0008).
- 1.168 pruebas unitarias al corte de este documento (1.067 pytest + 101 Vitest).

## 3. Verificación reproducible

```bash
make check          # Ruff + ty + pytest
make frontend-check # ESLint + Vitest + build
make verify         # /health y /health/ready del sitio
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

## 5. Pendientes declarados

| Pendiente | Dueño | Impacto |
|---|---|---|
| Suite ≥ 1.200 | Equipo | Se completa con las HU abiertas (#111, #114, #136, #144, #166) |
| #166 MLflow en el Droplet | Jesús | 5 SP; requiere acceso SSH |
| Tag posterior si cambia `main` | Guillermo | Publicar `v1.0.1` con el cierre de pruebas |

> **Actualización 2026-11-28:** la suite cerró con **1.229 pruebas** (1.108 pytest + 121 Vitest); #111, #114, #136, #144 y #166 están cerradas. El cierre se publica como **v1.1.0**.
