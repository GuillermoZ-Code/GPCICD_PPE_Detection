"""Servicio gRPC de inferencia de EPP (HU-010).

Los consumidores importan los submódulos directamente:

- Servidor: ``ppe_detection.grpc.server`` / ``python -m ppe_detection.grpc``.
- Adaptador: ``ppe_detection.grpc.servicer``.
- Cliente de prueba: ``ppe_detection.grpc.client``.
- Generación: ``ppe_detection.grpc.gen`` (o `make protos`).
"""
