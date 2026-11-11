"""Regenera los módulos ``*_pb2*`` desde ``protos/ppe.proto`` (HU-010)."""

from __future__ import annotations

import os
from pathlib import Path

#: Directorio del paquete generado: este módulo `grpc/` + `protos`.
GEN_DIR = Path(__file__).resolve().parent
PROTO_DIR = GEN_DIR / "protos"
#: Raíz `src/`: raíz de importación para que el identificador generado sea
#: `ppe_detection.grpc.protos.ppe_pb2` y las importaciones absolutas funcionen.
SRC_ROOT = GEN_DIR.parent.parent
#: Ruta de la fuente del contrato, relativa a `SRC_ROOT`.
RELATIVE_PROTO = "ppe_detection/grpc/protos/ppe.proto"

GENERATED = (PROTO_DIR / "ppe_pb2.py", PROTO_DIR / "ppe_pb2_grpc.py")


def generate() -> tuple[Path, ...]:
    """Ejecuta `grpc_tools.protoc` y devuelve las rutas regeneradas.

    Raises:
        SystemExit: si `protoc` termina con un código distinto de cero.
    """
    from grpc_tools import protoc  # perezoso: solo la regeneración lo necesita

    # protoc exige que la ruta del archivo sea relativa a un `--proto_path`
    # exacto; por eso se trabaja con cwd=src/ y `-I .`. La salida es `src/`
    # porque protoc espeja la estructura relativa del proto en `--*_out`.
    previous_cwd = os.getcwd()
    os.chdir(SRC_ROOT)
    try:
        args = [
            "-I.",
            f"--python_out={SRC_ROOT.as_posix()}",
            f"--grpc_python_out={SRC_ROOT.as_posix()}",
            RELATIVE_PROTO,
        ]
        if protoc.main(args) != 0:
            raise SystemExit(f"protoc terminó con un código distinto de cero: {args}")
    finally:
        os.chdir(previous_cwd)
    return GENERATED


if __name__ == "__main__":
    for path in generate():
        print(f"regenerado {path}")
