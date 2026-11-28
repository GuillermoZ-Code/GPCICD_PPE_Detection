# ADR — Architecture Decision Records

Registro de decisiones técnicas del proyecto. Cada ADR es append-only: una decisión
nueva se agrega con su propio número; no se reescribe la historia.

| ADR | Decisión |
|-----|----------|
| [0001](0001-modelo-base.md) | Modelo base: detector especializado nivel 3 (YOLO nano/small) |
| [0002](0002-dataset.md) | Dataset `51ddhesh/PPE_Detection` (CC-BY-4.0) |
| [0003](0003-licencia-agpl.md) | Licencia AGPL-3.0-only |
| [0004](0004-gitflow-spec-kit-merge.md) | Gitflow + Spec Kit + estrategia de merge |
| [0005](0005-contract-first.md) | Contract-first con detector simulado |
| [0006](0006-frontend-react.md) | Frontend web React + Vite + TypeScript (sustituye Streamlit/Tkinter) |
| [0007](0007-gitlab-ci-espejo.md) | GitLab CI/CD con espejo de *push* desde GitHub (sin Premium) |
| [0008](0008-droplet-caddy.md) | Despliegue en Droplet con Docker Compose y Caddy (HTTPS automático) |
| [0009](0009-modelo-productivo.md) | Modelo productivo: YOLO26n fine-tuneado + ONNX 640; YOLO11s como rollback |
| [0010](0010-exposicion-grpc.md) | gRPC interno en el Droplet; sin publicación de 9000 ni ruta `/grpc` |
| [0011](0011-memoria-agentes.md) | Memoria local de agentes con Engram, subordinada al repositorio |
| [0012](0012-codeowners-checks-obligatorios.md) | CODEOWNERS generado y checks obligatorios (actualiza 0004) |
| [0013](0013-basic-auth-y-dominio.md) | Basic auth del sitio en Caddy y dominio gratuito `sslip.io` |
