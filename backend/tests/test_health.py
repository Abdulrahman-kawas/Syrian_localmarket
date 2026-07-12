"""Smoke tests that need no database."""

from __future__ import annotations


def test_health(client) -> None:
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_openapi_lists_all_domains(client) -> None:
    spec = client.get("/openapi.json").json()
    paths = spec["paths"]
    for expected in [
        "/api/v1/auth/signup",
        "/api/v1/products",
        "/api/v1/qr/scan",
        "/api/v1/maps/nearby",
        "/api/v1/admin/complaints",
    ]:
        assert expected in paths, f"missing {expected}"
