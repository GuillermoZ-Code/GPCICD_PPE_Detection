"""Descarga y verificación del artefacto del modelo (HU-026).

Lee `models.lock`, descarga la URL declarada en un archivo temporal, verifica su
SHA256 y solo entonces reemplaza el destino. No versiona pesos ni usa red en las
pruebas.
"""

from __future__ import annotations

import argparse
import shutil
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import url2pathname, urlopen

from ppe_detection.detector_config import (
    DEFAULT_MANIFEST_PATH,
    ModelManifest,
    ModelManifestError,
    load_model_manifest,
    sha256_file,
)

DEFAULT_DESTINATION = Path("artifacts/models/best.pt")
DEFAULT_TIMEOUT = 30.0


class ArtifactError(RuntimeError):
    """El artefacto no se pudo descargar o no coincide con el manifiesto."""


@dataclass(frozen=True, slots=True)
class ArtifactFetchResult:
    """Resultado de una descarga verificada."""

    path: Path
    sha256: str
    bytes_written: int


def _part_path(destination: Path) -> Path:
    """Archivo temporal junto al destino, para un reemplazo atómico."""
    return destination.with_name(destination.name + ".part")


def _download(url: str, target: Path, timeout: float) -> None:
    """Descarga una URL file/http/https en `target`."""
    parsed = urlparse(url)
    if parsed.scheme == "file":
        source = Path(url2pathname(parsed.path))
        if not source.is_file():
            raise ArtifactError(f"No existe el archivo de origen: {source}")
        try:
            with source.open("rb") as source_file, target.open("wb") as target_file:
                shutil.copyfileobj(source_file, target_file)
        except OSError as exc:
            raise ArtifactError(f"No se pudo copiar {source}: {exc}") from exc
        return

    if parsed.scheme in {"http", "https"}:
        try:
            with urlopen(url, timeout=timeout) as response, target.open("wb") as target_file:
                shutil.copyfileobj(response, target_file)
        except OSError as exc:
            raise ArtifactError(f"No se pudo descargar {url}: {exc}") from exc
        return

    raise ArtifactError(f"Esquema no soportado en {url!r}: usa file://, http:// o https://.")


def fetch_artifact(
    manifest: ModelManifest,
    destination: Path = DEFAULT_DESTINATION,
    *,
    timeout: float = DEFAULT_TIMEOUT,
) -> ArtifactFetchResult:
    """Descarga, verifica y reemplaza el destino de forma segura."""
    target = Path(destination)
    target.parent.mkdir(parents=True, exist_ok=True)
    partial = _part_path(target)
    try:
        _download(manifest.url, partial, timeout)
        digest = sha256_file(partial)
        expected = manifest.sha256.upper()
        if digest != expected:
            raise ArtifactError(
                f"El SHA256 de {manifest.url} no coincide: esperado {expected}, obtenido {digest}."
            )
        partial.replace(target)
    except Exception:
        partial.unlink(missing_ok=True)
        raise

    return ArtifactFetchResult(
        path=target,
        sha256=manifest.sha256.upper(),
        bytes_written=target.stat().st_size,
    )


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ppe-artifact",
        description="Descarga y verifica el artefacto declarado en models.lock.",
    )
    commands = parser.add_subparsers(dest="command", required=True)
    fetch = commands.add_parser("fetch", help="descarga el modelo y verifica su SHA256")
    fetch.add_argument(
        "--manifest",
        type=Path,
        default=None,
        help=f"manifiesto a leer (por omisión: {DEFAULT_MANIFEST_PATH})",
    )
    fetch.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_DESTINATION,
        help=f"archivo destino (por omisión: {DEFAULT_DESTINATION})",
    )
    fetch.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """CLI de descarga; devuelve 0 si el artefacto queda verificado."""
    args = _build_parser().parse_args(argv)
    try:
        if args.command != "fetch":
            raise ArtifactError(f"Comando no soportado: {args.command}")
        manifest = (
            load_model_manifest(args.manifest)
            if args.manifest is not None
            else load_model_manifest()
        )
        result = fetch_artifact(manifest, args.output, timeout=args.timeout)
    except (ArtifactError, ModelManifestError, OSError) as exc:
        print(f"artifact: {exc}", file=sys.stderr)
        return 1

    print(f"artifact: {result.path} ({result.sha256})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
