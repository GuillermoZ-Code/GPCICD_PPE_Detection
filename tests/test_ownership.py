"""Pruebas de la compuerta de propiedad (HU-082).

Cubre los tres AC del manifiesto:
    AC-01: el manifiesto declara dueño por ruta y archivos bloqueados.
    AC-02: un archivo bloqueado de otro dueño hace fallar la compuerta.
    AC-03: CODEOWNERS se genera desde el manifiesto, sin edición manual.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from ppe_detection.tools import ownership

MANIFEST_TOML = """
[[locked]]
path = "uv.lock"
owner = "GuillermoZ-Code"

[[owner]]
github = "GuillermoZ-Code"
nombre = "Guillermo Zabala"
paths = ["frontend/", "uv.lock"]

[[owner]]
github = "HestradaUAO"
nombre = "Hernan Estrada"
paths = ["src/ppe_detection/detection/", "models.lock"]
"""


@pytest.fixture
def manifest(tmp_path: Path) -> ownership.Manifest:
    """Manifiesto de prueba escrito en un archivo temporal."""
    path = tmp_path / "propiedad.toml"
    path.write_text(MANIFEST_TOML, encoding="utf-8")
    return ownership.load_manifest(path)


def test_load_manifest_lee_duenos_y_bloqueos(manifest: ownership.Manifest) -> None:
    """AC-01: dueños por ruta y bloqueos quedan disponibles."""
    # Arrange / Act ya ocurrieron en el fixture.

    # Assert
    assert manifest.owners["HestradaUAO"] == ("src/ppe_detection/detection/", "models.lock")
    assert manifest.locked["uv.lock"] == "GuillermoZ-Code"
    assert manifest.names["HestradaUAO"] == "Hernan Estrada"


def test_load_manifest_sin_duenos_falla(tmp_path: Path) -> None:
    """AC-01: un manifiesto vacío es un error, no un pase libre."""
    # Arrange
    path = tmp_path / "vacio.toml"
    path.write_text("# sin dueños\n", encoding="utf-8")

    # Act / Assert
    with pytest.raises(ValueError, match="no declara"):
        ownership.load_manifest(path)


def test_matches_carpeta_por_prefijo() -> None:
    """AC-01: un patrón con barra final cubre todo lo que cuelga de ella."""
    assert ownership.matches("frontend/src/App.tsx", "frontend/")
    assert not ownership.matches("docs/frontend.md", "frontend/")


def test_matches_archivo_exacto_y_globo() -> None:
    """AC-01: se aceptan rutas exactas y comodines."""
    assert ownership.matches("uv.lock", "uv.lock")
    assert ownership.matches("compose.prod.yml", "compose.*.yml")
    assert not ownership.matches("compose.prod.yml", "compose.yml")


def test_owner_of_prefiere_el_patron_mas_especifico(manifest: ownership.Manifest) -> None:
    """AC-01: ante dos coincidencias gana la ruta más concreta."""
    # Arrange
    manifest.owners["otro"] = ("src/ppe_detection/",)

    # Act
    owner = ownership.owner_of("src/ppe_detection/detection/yolo.py", manifest)

    # Assert
    assert owner == "HestradaUAO"


def test_owner_of_devuelve_none_si_no_hay_regla(manifest: ownership.Manifest) -> None:
    """AC-01: una ruta sin declarar no tiene dueño."""
    assert ownership.owner_of("docs/random.md", manifest) is None


def test_lock_of_detecta_archivo_bloqueado(manifest: ownership.Manifest) -> None:
    """AC-02: `uv.lock` está bloqueado a su dueño."""
    assert ownership.lock_of("uv.lock", manifest) == "GuillermoZ-Code"
    assert ownership.lock_of("frontend/src/App.tsx", manifest) is None


def test_evaluate_sin_choques(manifest: ownership.Manifest) -> None:
    """AC-02: el dueño puede tocar sus archivos sin avisos."""
    # Act
    report = ownership.evaluate(["frontend/src/App.tsx", "uv.lock"], "GuillermoZ-Code", manifest)

    # Assert
    assert report.ok
    assert report.blocked == []
    assert report.foreign == []


def test_evaluate_bloquea_archivo_de_un_solo_escritor(manifest: ownership.Manifest) -> None:
    """AC-02: tocar `uv.lock` ajeno es un fallo, no una advertencia."""
    # Act
    report = ownership.evaluate(["uv.lock"], "ElianaCardona", manifest)

    # Assert
    assert not report.ok
    assert report.blocked == [("uv.lock", "GuillermoZ-Code")]


def test_evaluate_avisa_sin_bloquear_archivo_ajeno(manifest: ownership.Manifest) -> None:
    """AC-02: un archivo ajeno no bloqueado solo genera aviso."""
    # Act
    report = ownership.evaluate(["models.lock"], "ElianaCardona", manifest)

    # Assert
    assert report.ok
    assert report.foreign == [("models.lock", "HestradaUAO")]


def test_evaluate_registra_rutas_libres(manifest: ownership.Manifest) -> None:
    """AC-01: lo que no está en el manifiesto se reporta como libre."""
    # Act
    report = ownership.evaluate(["docs/notas.md"], "jesusriverosUAO", manifest)

    # Assert
    assert report.ok
    assert report.unowned == ["docs/notas.md"]


def test_evaluate_sin_autor_no_bloquea(manifest: ownership.Manifest) -> None:
    """AC-02: sin autor (ejecución local) no se puede acusar a nadie."""
    # Act
    report = ownership.evaluate(["uv.lock"], None, manifest)

    # Assert
    assert report.ok
    assert report.blocked == []
    assert report.foreign == []


def test_render_codeowners_ordena_de_menos_a_mas_especifico(manifest: ownership.Manifest) -> None:
    """AC-03: CODEOWNERS deja al final la regla más concreta, que es la que gana."""
    # Act
    text = ownership.render_codeowners(manifest)

    # Assert
    lines = [line for line in text.splitlines() if line and not line.startswith("#")]
    patterns = [line.split(" @")[0] for line in lines]
    assert patterns == sorted(patterns, key=ownership.specificity)
    assert "uv.lock @GuillermoZ-Code" in lines
    assert patterns[-1] == "src/ppe_detection/detection/"


def test_write_codeowners_escribe_el_archivo(manifest: ownership.Manifest, tmp_path: Path) -> None:
    """AC-03: el archivo se genera en la ruta indicada."""
    # Arrange
    target = tmp_path / ".github" / "CODEOWNERS"

    # Act
    written = ownership.write_codeowners(manifest, target)

    # Assert
    assert written == target
    assert "@HestradaUAO" in target.read_text(encoding="utf-8")


def test_main_falla_con_archivo_bloqueado(
    manifest: ownership.Manifest,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """AC-02: el CLI devuelve 1 cuando hay un bloqueo."""
    # Arrange
    monkeypatch.setattr(ownership, "load_manifest", lambda _path=None: manifest)
    monkeypatch.setattr(ownership, "changed_files", lambda _base: ["uv.lock"])

    # Act
    code = ownership.main(["--author", "ElianaCardona"])

    # Assert
    assert code == 1
    assert "BLOQUEADO" in capsys.readouterr().out


def test_main_termina_en_cero_sin_bloqueos(
    manifest: ownership.Manifest,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """AC-02: sin bloqueos el CLI termina en 0."""
    # Arrange
    monkeypatch.setattr(ownership, "load_manifest", lambda _path=None: manifest)
    monkeypatch.setattr(ownership, "changed_files", lambda _base: ["models.lock"])

    # Act
    code = ownership.main(["--author", "HestradaUAO"])

    # Assert
    assert code == 0
    assert "ownership: ok" in capsys.readouterr().out


def test_changed_files_reporta_base_invalida(monkeypatch: pytest.MonkeyPatch) -> None:
    """AC-02: una referencia inexistente falla con mensaje claro."""

    # Arrange
    class Result:
        returncode = 128
        stdout = ""
        stderr = "fatal: bad revision"

    monkeypatch.setattr(ownership.subprocess, "run", lambda *a, **k: Result())

    # Act / Assert
    with pytest.raises(SystemExit, match="bad revision"):
        ownership.changed_files("origin/inexistente")
