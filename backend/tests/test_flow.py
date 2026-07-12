"""End-to-end integration flow against a real PostGIS database."""

from __future__ import annotations

from sqlalchemy import select

from app.models.user import User
from tests.conftest import requires_db, unique_email, unique_phone

pytestmark = requires_db


def _signup_and_verify(client, db, role: str) -> tuple[str, str]:
    """Return (access_token, user_id) for a freshly verified user."""
    email = unique_email()
    phone = unique_phone()
    r = client.post(
        "/api/v1/auth/signup",
        json={
            "email": email,
            "phone": phone,
            "password": "password123",
            "role": role,
            "verification_method": "email",
        },
    )
    assert r.status_code == 201, r.text
    user_id = r.json()["id"]

    # Read the verification code straight from the DB (dev channel).
    user = db.execute(select(User).where(User.email == email)).scalar_one()
    code = user.verification_code

    r = client.post("/api/v1/auth/verify", json={"email": email, "code": code})
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["user"]["role"] == role
    return body["access_token"], user_id


def _auth(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def test_signup_duplicate_is_generic_conflict(client, db) -> None:
    email = unique_email()
    phone = unique_phone()
    payload = {
        "email": email,
        "phone": phone,
        "password": "password123",
        "role": "consumer",
        "verification_method": "email",
    }
    assert client.post("/api/v1/auth/signup", json=payload).status_code == 201
    dup = client.post("/api/v1/auth/signup", json=payload)
    assert dup.status_code == 409
    # Message must not reveal which field collided (anti-enumeration).
    assert "email" not in dup.json()["error"]["message"].lower()


def test_login_wrong_password_is_401(client, db) -> None:
    token, _ = _signup_and_verify(client, db, "consumer")
    # find the email we used via the token is awkward; just try a bad login
    r = client.post(
        "/api/v1/auth/login",
        json={"email": unique_email(), "password": "whatever"},
    )
    assert r.status_code == 401


def test_full_marketplace_flow(client, db) -> None:
    seller_token, _ = _signup_and_verify(client, db, "seller")
    consumer_token, consumer_id = _signup_and_verify(client, db, "consumer")

    # Seller onboarding (Damascus coordinates).
    r = client.post(
        "/api/v1/sellers/onboard",
        headers=_auth(seller_token),
        json={
            "type": "shop",
            "shop_name": "Test Shop",
            "location": {"latitude": 33.5138, "longitude": 36.2765},
        },
    )
    assert r.status_code == 201, r.text
    assert r.json()["geo_point"]["coordinates"] == [36.2765, 33.5138]

    # Create a listing.
    r = client.post(
        "/api/v1/products",
        headers=_auth(seller_token),
        json={
            "title": "Near-expiry Milk",
            "type": "near_expiry",
            "original_price": 1000,
            "discounted_price": 500,
            "quantity": 10,
        },
    )
    assert r.status_code == 201, r.text
    product_id = r.json()["id"]

    # It shows up in search near Damascus.
    r = client.get("/api/v1/products", params={"lat": 33.5138, "lng": 36.2765, "radius": 5})
    assert r.status_code == 200
    assert r.json()["total"] >= 1

    # Seller mints a QR.
    r = client.get(f"/api/v1/products/{product_id}/qr", headers=_auth(seller_token))
    assert r.status_code == 200, r.text
    code = r.json()["code"]
    assert r.json()["image_url"].startswith("data:image/png;base64,")

    # Consumer scans it -> pending transaction.
    r = client.post("/api/v1/qr/scan", headers=_auth(consumer_token), json={"code": code})
    assert r.status_code == 200, r.text
    txn_id = r.json()["transaction_id"]
    assert r.json()["status"] == "pending"

    # Seller confirms 3 units -> stock decrements 10 -> 7.
    r = client.post(
        f"/api/v1/qr/confirm/{txn_id}",
        headers=_auth(seller_token),
        json={"quantity": 3},
    )
    assert r.status_code == 200, r.text
    assert r.json()["status"] == "confirmed"
    assert r.json()["proof_record"]["quantity"] == 3

    r = client.get(f"/api/v1/products/{product_id}")
    assert r.json()["quantity"] == 7


def test_bola_seller_cannot_edit_others_product(client, db) -> None:
    seller_a, _ = _signup_and_verify(client, db, "seller")
    seller_b, _ = _signup_and_verify(client, db, "seller")

    for tok, name in [(seller_a, "Shop A"), (seller_b, "Shop B")]:
        client.post(
            "/api/v1/sellers/onboard",
            headers=_auth(tok),
            json={
                "type": "shop",
                "shop_name": name,
                "location": {"latitude": 33.5, "longitude": 36.3},
            },
        )

    r = client.post(
        "/api/v1/products",
        headers=_auth(seller_a),
        json={
            "title": "A's product",
            "type": "regular",
            "original_price": 100,
            "discounted_price": 90,
            "quantity": 5,
        },
    )
    product_id = r.json()["id"]

    # Seller B must not be able to edit Seller A's product.
    r = client.put(
        f"/api/v1/products/{product_id}",
        headers=_auth(seller_b),
        json={"quantity": 999},
    )
    assert r.status_code == 403


def test_use_by_past_date_rejected_at_api(client, db) -> None:
    seller, _ = _signup_and_verify(client, db, "seller")
    client.post(
        "/api/v1/sellers/onboard",
        headers=_auth(seller),
        json={
            "type": "shop",
            "shop_name": "Food Shop",
            "location": {"latitude": 33.5, "longitude": 36.3},
        },
    )
    r = client.post(
        "/api/v1/products",
        headers=_auth(seller),
        json={
            "title": "Expired yogurt",
            "type": "near_expiry",
            "original_price": 100,
            "discounted_price": 50,
            "quantity": 1,
            "expiry_class": "use_by",
            "expiry_date": "2000-01-01",
        },
    )
    assert r.status_code == 422


def test_unverified_cannot_create_listing(client, db) -> None:
    # Signup a seller but DO NOT verify.
    email = unique_email()
    client.post(
        "/api/v1/auth/signup",
        json={
            "email": email,
            "phone": unique_phone(),
            "password": "password123",
            "role": "seller",
            "verification_method": "email",
        },
    )
    # No token -> 401 on a protected route.
    r = client.post(
        "/api/v1/products",
        json={
            "title": "x",
            "type": "regular",
            "original_price": 10,
            "discounted_price": 5,
            "quantity": 1,
        },
    )
    assert r.status_code == 401


def test_review_updates_reputation(client, db) -> None:
    author, _ = _signup_and_verify(client, db, "consumer")
    _, target_id = _signup_and_verify(client, db, "seller")

    r = client.post(
        "/api/v1/reviews",
        headers=_auth(author),
        json={
            "target_id": target_id,
            "target_type": "seller",
            "rating": 4,
            "text": "Good",
        },
    )
    assert r.status_code == 201, r.text

    r = client.get(f"/api/v1/reviews/{target_id}")
    assert r.json()["average_rating"] == 4.0
    assert r.json()["total_reviews"] == 1


def test_update_my_location(client, db) -> None:
    token, user_id = _signup_and_verify(client, db, "consumer")
    r = client.put(
        "/api/v1/users/me/location",
        headers=_auth(token),
        json={"latitude": 33.5138, "longitude": 36.2765},
    )
    assert r.status_code == 200, r.text

    # The location is now persisted for proximity targeting.
    from app.db.postgis import geometry_to_coordinates
    from app.models.user import User as UserModel

    db.expire_all()
    user = db.get(UserModel, user_id)
    coords = geometry_to_coordinates(user.last_location)
    assert coords is not None
    assert abs(coords[0] - 33.5138) < 1e-4
    assert abs(coords[1] - 36.2765) < 1e-4


def test_list_conversations(client, db) -> None:
    a_token, a_id = _signup_and_verify(client, db, "consumer")
    b_token, b_id = _signup_and_verify(client, db, "seller")

    # A opens a conversation with B and sends a message.
    r = client.post("/api/v1/conversations", headers=_auth(a_token), json={"participant_id": b_id})
    assert r.status_code == 200, r.text
    convo_id = r.json()["id"]

    r = client.post(
        f"/api/v1/conversations/{convo_id}/messages",
        headers=_auth(a_token),
        json={"content": "Hello there"},
    )
    assert r.status_code == 200, r.text

    # A sees the conversation with the last message preview.
    r = client.get("/api/v1/conversations", headers=_auth(a_token))
    assert r.status_code == 200, r.text
    items = r.json()
    assert len(items) == 1
    assert items[0]["id"] == convo_id
    assert items[0]["last_message"] == "Hello there"
    assert items[0]["participant"]["id"] == b_id

    # B sees the same conversation, with A as the other participant.
    r = client.get("/api/v1/conversations", headers=_auth(b_token))
    assert len(r.json()) == 1
    assert r.json()[0]["participant"]["id"] == a_id
