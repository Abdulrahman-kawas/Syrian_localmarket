"""Unit tests for the Notification Hubs SAS/token helpers (no network/DB)."""

from __future__ import annotations

from app.services import notification_hub


def test_parse_connection_string() -> None:
    conn = (
        "Endpoint=sb://ns.servicebus.windows.net/;"
        "SharedAccessKeyName=DefaultFullSharedAccessSignature;"
        "SharedAccessKey=abc123def456=="
    )
    endpoint, key_name, key = notification_hub._parse_connection_string(conn)
    assert endpoint == "https://ns.servicebus.windows.net"
    assert key_name == "DefaultFullSharedAccessSignature"
    # Base64 keys ending in '==' must survive parsing intact.
    assert key == "abc123def456=="


def test_sas_token_shape() -> None:
    token = notification_hub._sas_token(
        "https://ns.servicebus.windows.net/hub", "keyName", "secretkey"
    )
    assert token.startswith("SharedAccessSignature sr=")
    assert "sig=" in token
    assert "se=" in token
    assert token.endswith("skn=keyName")
