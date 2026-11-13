"""Pruebas del contrato de resultado de inferencia sin detecciones (HU-004)."""

from __future__ import annotations

import numpy as np

from ppe_detection.contracts import (
    CLASSES,
    ContractError,
    Detection,
    FakeDetector,
    ImageData,
)
from ppe_detection.results import (
    NO_DETECTIONS_MESSAGE,
    RESPONSIBLE_USE_NOTE,
    build_error_result,
    build_inference_result,
)


def _image(width: int = 8, height: int = 6) -> ImageData:
    """Imagen RGB sintética válida para el contrato."""
    array = np.zeros((height, width, 3), dtype=np.uint8)
    return ImageData(array=array, width=width, height=height, format="png", source="test")


def _detection(class_id: int) -> Detection:
    """Detección sintética válida para la clase dada."""
    return Detection(
        class_id=class_id,
        class_name=CLASSES[class_id],
        confidence=0.9,
        bbox=(1.0, 1.0, 4.0, 4.0),
        image_width=8,
        image_height=6,
    )


def test_empty_inference_returns_empty_collection_and_message() -> None:
    """AC-004.1: inferencia exitosa sin detecciones devuelve la colección vacía
    y comunica que no se detectaron objetos EPP."""
    # Arrange
    detector = FakeDetector()
    image = _image()

    # Act
    detections = detector.detect(image)
    result = build_inference_result(detections)

    # Assert
    assert result.detections == ()
    assert result.is_empty is True
    assert "no se detectaron" in result.message.lower()
    assert "EPP" in result.message


def test_empty_result_is_not_classified_as_error() -> None:
    """AC-004.2: el resultado vacío no se clasifica como error de procesamiento."""
    # Arrange / Act
    result = build_inference_result([])

    # Assert
    assert result.is_error is False
    assert result.is_empty is True


def test_real_failure_is_classified_as_error_and_not_empty_success() -> None:
    """AC-004.2: los fallos reales siguen siendo errores, a diferencia del
    resultado vacío."""
    # Arrange / Act
    empty_result = build_inference_result([])
    error_result = build_error_result(ContractError("archivo corrupto"))

    # Assert
    assert empty_result.is_error is False
    assert error_result.is_error is True
    assert error_result.is_empty is False
    assert error_result.message != empty_result.message
    assert error_result.detections == ()


def test_null_response_is_rejected_as_contract_error() -> None:
    """AC-004.2 (frontera): None no se normaliza a colección vacía; es error
    de contrato, no una inferencia exitosa sin objetos."""
    # Arrange / Act
    result = build_inference_result(None)

    # Assert
    assert result.is_error is True
    assert result.is_empty is False
    assert result.detections == ()


def test_empty_message_does_not_assert_noncompliance_or_absence() -> None:
    """AC-004.3: el mensaje vacío no afirma incumplimiento ni prueba de
    ausencia real de EPP; solo comunica el resultado de la detección."""
    # Arrange
    forbidden = ("no hay", "ausencia", "incumple", "incumpli", "falta", "sin epp")

    # Act
    message = NO_DETECTIONS_MESSAGE.lower()

    # Assert
    assert "no se detectaron" in message
    assert not any(term in message for term in forbidden)


def test_nonempty_result_summarizes_detected_classes() -> None:
    """FR-005: con objetos detectados, el mensaje resume clases con recuento
    y el resultado clásica como éxito."""
    # Arrange
    detections = [_detection(3), _detection(1), _detection(3)]  # helmet, Vest, helmet

    # Act
    result = build_inference_result(detections)

    # Assert
    assert result.is_empty is False
    assert result.is_error is False
    assert result.detections == tuple(detections)
    assert "helmet (x2)" in result.message
    assert "Vest (x1)" in result.message
    assert "3 objetos EPP" in result.message


def test_listing_order_follows_canonical_catalog() -> None:
    """FR-005: el listado sigue el orden canónico del data.yaml, no el orden
    de entrada."""
    # Arrange
    detections = [_detection(3), _detection(1)]  # helmet recibido antes que Vest

    # Act
    result = build_inference_result(detections)

    # Assert
    assert result.message.index("Vest") < result.message.index("helmet")


def test_single_detection_uses_singular_wording() -> None:
    """FR-005 (edge): un solo objeto detectado usa redacción singular."""
    # Arrange / Act
    result = build_inference_result([_detection(3)])

    # Assert
    assert "Se detectó 1 objeto EPP" in result.message
    assert result.is_empty is False


def test_fake_detector_empty_result_flows_through_contract() -> None:
    """FR-006: reutiliza ImageData y FakeDetector: imagen → detect() → resultado
    vacío sin excepciones."""
    # Arrange
    detector = FakeDetector()

    # Act
    result = build_inference_result(detector.detect(_image()))

    # Assert
    assert result.message == NO_DETECTIONS_MESSAGE
    assert result.is_empty is True
    assert result.is_error is False


def test_responsible_use_note_states_detection_only() -> None:
    """FR-007: la nota de uso responsable declara que la ausencia de detección
    no indica ausencia real de EPP ni constituye incumplimiento."""
    # Arrange / Act / Assert
    assert "no indica" in RESPONSIBLE_USE_NOTE
    assert "ausencia real de EPP" in RESPONSIBLE_USE_NOTE
    assert "incumplimiento" in RESPONSIBLE_USE_NOTE
