# API.md — Endpoint Catalogue

## Base URL

```
https://<your-api-url>/api/v1
```

## Authentication

All protected endpoints require a JWT token in the Authorization header:

```
Authorization: Bearer <token>
```

---

## Auth Endpoints

### POST /auth/signup
Create a new user account.

**Request:**
```json
{
  "email": "user@example.com",
  "phone": "+963912345678",
  "password": "securepassword",
  "role": "consumer",
  "verification_method": "email"
}
```

**Response:** 201 Created
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "phone": "+963912345678",
  "role": "consumer",
  "verification_status": "pending"
}
```

### POST /auth/verify
Verify email/WhatsApp code.

**Request:**
```json
{
  "email": "user@example.com",
  "code": "123456"
}
```

**Response:** 200 OK
```json
{
  "access_token": "jwt_token",
  "token_type": "bearer"
}
```

### POST /auth/login
Login with email/phone and password.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "securepassword"
}
```

**Response:** 200 OK
```json
{
  "access_token": "jwt_token",
  "token_type": "bearer"
}
```

---

## Seller Endpoints

### GET /sellers/me
Get current seller profile.

**Response:** 200 OK
```json
{
  "id": "uuid",
  "type": "shop",
  "shop_name": "My Shop",
  "category_id": "uuid",
  "geo_point": {
    "type": "Point",
    "coordinates": [36.2765, 33.5138]
  },
  "plus_code": "4M7J+22 Damascus",
  "location_description": "Near Umayyad Mosque"
}
```

### PUT /sellers/me
Update seller profile.

**Request:**
```json
{
  "shop_name": "Updated Shop Name",
  "category_id": "uuid",
  "location": {
    "latitude": 33.5138,
    "longitude": 36.2765,
    "plus_code": "4M7J+22 Damascus",
    "description": "Near Umayyad Mosque"
  }
}
```

**Response:** 200 OK

---

## Product Endpoints

### GET /products
List products with filters.

**Query Parameters:**
- `type` - regular/market_discount/near_expiry
- `seller_type` - shop/factory
- `category_id` - Category UUID
- `lat`, `lng` - Coordinates for "near me"
- `radius` - Search radius in km
- `min_discount` - Minimum discount percentage
- `max_price` - Maximum price
- `sort` - price_asc/price_desc/expiry_asc/nearby

**Response:** 200 OK
```json
{
  "items": [
    {
      "id": "uuid",
      "title": "Product Name",
      "type": "near_expiry",
      "original_price": 1000,
      "discounted_price": 500,
      "expiry_date": "2024-02-01",
      "quantity": 10,
      "seller": {
        "id": "uuid",
        "shop_name": "Shop Name",
        "type": "shop"
      }
    }
  ],
  "total": 100,
  "page": 1,
  "per_page": 20
}
```

### POST /products
Create a new product (seller only).

**Request:**
```json
{
  "title": "Product Name",
  "description": "Product description",
  "type": "near_expiry",
  "original_price": 1000,
  "discounted_price": 500,
  "expiry_date": "2024-02-01",
  "expiry_class": "best_before",
  "quantity": 10
}
```

**Response:** 201 Created

### GET /products/{id}
Get product details.

**Response:** 200 OK
```json
{
  "id": "uuid",
  "title": "Product Name",
  "description": "Product description",
  "type": "near_expiry",
  "original_price": 1000,
  "discounted_price": 500,
  "expiry_date": "2024-02-01",
  "quantity": 10,
  "images": ["url1", "url2"],
  "seller": {
    "id": "uuid",
    "shop_name": "Shop Name",
    "phone": "+963912345678"
  }
}
```

### PUT /products/{id}
Update product (seller only).

### DELETE /products/{id}
Delete product (seller only).

### PUT /products/{id}/quantity
Update product quantity (seller only).

**Request:**
```json
{
  "quantity": 5
}
```

**Response:** 200 OK

---

## QR Endpoints

### GET /products/{id}/qr
Get QR code for product (seller only).

**Response:** 200 OK
```json
{
  "code": "qr_code_value",
  "image_url": "https://cdn.example.com/qr/uuid.png"
}
```

### POST /qr/scan
Scan a QR code (consumer).

**Request:**
```json
{
  "code": "qr_code_value"
}
```

**Response:** 200 OK
```json
{
  "transaction_id": "uuid",
  "status": "pending"
}
```

### POST /qr/confirm/{transaction_id}
Confirm a scanned QR (seller).

**Request:**
```json
{
  "quantity": 2
}
```

**Response:** 200 OK
```json
{
  "transaction_id": "uuid",
  "status": "confirmed",
  "proof_record": {
    "buyer": "uuid",
    "seller": "uuid",
    "product": "uuid",
    "quantity": 2,
    "timestamp": "2024-01-15T10:30:00Z"
  }
}
```

---

## Search Endpoints

### GET /search
Unified search with filters.

**Query Parameters:**
- `q` - Search query (Arabic-aware)
- `type` - Product type
- `seller_type` - Seller type
- `category_id` - Category
- `lat`, `lng` - Coordinates
- `radius` - Radius in km
- `min_discount` - Minimum discount %
- `max_price` - Maximum price
- `sort` - Sort order

**Response:** 200 OK
```json
{
  "items": [...],
  "total": 100,
  "filters_applied": {
    "type": "near_expiry",
    "lat": 33.5138,
    "lng": 36.2765,
    "radius": 5
  }
}
```

---

## Review Endpoints

### POST /reviews
Create a review.

**Request:**
```json
{
  "target_id": "uuid",
  "target_type": "seller",
  "rating": 5,
  "text": "Great shop!"
}
```

**Response:** 201 Created

### GET /reviews/{target_id}
Get reviews for a target.

**Response:** 200 OK
```json
{
  "items": [...],
  "average_rating": 4.5,
  "total_reviews": 50
}
```

---

## Complaint Endpoints

### POST /complaints
File a complaint.

**Request:**
```json
{
  "target_id": "uuid",
  "target_type": "seller",
  "listing_id": "uuid",
  "reason": "Product was not as described"
}
```

**Response:** 201 Created

---

## Chat Endpoints

### POST /conversations
Create or get conversation.

**Request:**
```json
{
  "participant_id": "uuid"
}
```

**Response:** 200 OK
```json
{
  "id": "uuid",
  "participant": {
    "id": "uuid",
    "name": "Shop Name"
  }
}
```

### GET /conversations/{id}/messages
Get messages in a conversation.

**Response:** 200 OK
```json
{
  "items": [
    {
      "id": "uuid",
      "sender_id": "uuid",
      "content": "Hello!",
      "created_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

---

## Map Endpoints

### GET /maps/nearby
Get nearby sellers.

**Query Parameters:**
- `lat` - Latitude
- `lng` - Longitude
- `radius` - Radius in km (default: 5)

**Response:** 200 OK
```json
{
  "sellers": [
    {
      "id": "uuid",
      "shop_name": "Shop Name",
      "type": "shop",
      "geo_point": {
        "type": "Point",
        "coordinates": [36.2765, 33.5138]
      },
      "category": {
        "name_ar": "بقالة",
        "name_en": "Groceries"
      }
    }
  ]
}
```

### POST /maps/directions
Get directions to a seller.

**Request:**
```json
{
  "origin": {
    "lat": 33.5138,
    "lng": 36.2765
  },
  "destination": {
    "lat": 33.5200,
    "lng": 36.2800
  }
}
```

**Response:** 200 OK
```json
{
  "distance": "1.2 km",
  "duration": "5 mins",
  "directions_url": "https://maps.google.com/..."
}
```

---

## Media Endpoints

### POST /media/upload
Upload an image.

**Request:** multipart/form-data
- `file` - Image file

**Response:** 200 OK
```json
{
  "url": "https://cdn.example.com/images/uuid.jpg",
  "thumbnail_url": "https://cdn.example.com/images/uuid_thumb.jpg"
}
```

---

## Notification Endpoints

### POST /notifications/register
Register device for push notifications.

**Request:**
```json
{
  "platform": "fcm",
  "token": "device_token"
}
```

**Response:** 200 OK

---

## Error Responses

All errors follow this format:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input",
    "details": {
      "field": "email",
      "issue": "already exists"
    }
  }
}
```

### Common Error Codes
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `409` - Conflict
- `422` - Validation Error
- `429` - Rate Limit Exceeded
- `500` - Internal Server Error

---

*This document is auto-generated from OpenAPI. Keep in sync with backend/app/api/.*
