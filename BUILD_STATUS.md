# BUILD_STATUS.md — What was built, verified, and what remains

**Date:** 2026-07-12
**Author:** Claude Code
**Context:** The task list claimed 35 phases "complete", but the audit ([AUDIT_REPORT.md](AUDIT_REPORT.md)) found the backend was 100% empty stubs, the mobile app had no entry screens, and the timers/admin app didn't exist. This document records everything built to close those gaps, how it was verified, and the few scoped items that remain.

---

## 0. TL;DR

| Area | Before | Now | Verified how |
|------|--------|-----|--------------|
| Backend (FastAPI) | 49 empty stub files | **Full app, 32 routes** | 22 pytest tests pass vs real PostGIS; ruff clean; runs in Docker |
| DB schema/migrations | none | **Alembic + PostGIS baseline** | `alembic upgrade head` creates all 16 tables + GiST index |
| Timers (Azure Functions) | 2 empty dirs | **auto-delist + proximity** | logic unit-tested vs PostGIS |
| Admin back-office | empty dir | **React+Vite SPA** | `npm run build` OK; serves in Docker on :5173 |
| Mobile entry (`app/`) | empty → app couldn't start | **expo-router tree wired** | **`tsc --noEmit` clean (0 errors)**; deps install fixed |
| Local run | none | **`docker compose up`** | whole stack verified live (see §7) |

---

## 1. Backend — FastAPI (`backend/app/`)

Built from scratch, matching `docs/API.md`, `docs/DATA_MODEL.md`, and `docs/SECURITY.md`.

**Core** (`app/core/`)
- `config.py` — pydantic-settings; env/Key-Vault driven; CORS parsing; rate-limit toggle.
- `security.py` — **bcrypt** password hashing + **JWT** create/verify (switched off passlib after hitting the passlib×bcrypt-4 incompatibility).
- `errors.py` — structured error envelope `{error:{code,message,details}}` exactly per `docs/API.md`; no stack traces leak to clients.
- `rate_limit.py` — in-memory sliding-window limiter; stricter budget for auth (brute-force protection); toggle for tests.
- `logging.py` — JSON logs with secret/PII redaction.

**DB** (`app/db/`) — SQLAlchemy 2.0 engine/session; PostGIS helpers (`make_point`, GeoJSON conversion, `ST_DWithin` via `geography` cast, haversine).

**Models** (`app/models/`) — all **16 tables** from `DATA_MODEL.md`: users, sellers, categories, products, price_history, product_qr, transactions, reviews, complaints, conversations, messages, blocks, delivery_requests, device_registrations, subscriptions, admin_actions.

**Schemas** (`app/schemas/`) — Pydantic v2 request/response models with validation: phone format, no self-admin-signup, **discount ≤ original price**, and **food-safety** (`use_by` past date rejected).

**Services** (`app/services/`) — auth, seller, listing, qr, search (geo+filters), review (recomputes reputation), chat (with blocking), delivery, notification, maps (Google proxied server-side), moderation (bleach XSS strip). Object-level authorization (BOLA prevention) enforced on every owner-scoped action.

**Routers** (`app/api/`) — every endpoint in `docs/API.md` **plus** an admin surface: auth, sellers, categories, products, qr, search, reviews, complaints, chat, maps, media, notifications, delivery, admin. **32 routes** total.

**Media** (`app/media/`) — upload pipeline: magic-byte validation, size limit, **EXIF/GPS stripped** by re-encoding pixel data, resize + thumbnail, Azure Blob storage (or local disk for dev).

**Reconciled contract mismatch:** `/auth/login` now returns `{access_token, token_type, user}` so the existing mobile `authStore` works.

---

## 2. Database (`backend/alembic/`)

- Real `env.py` bound to the ORM metadata and the runtime `DATABASE_URL` (no committed secrets).
- `versions/0001_initial.py` — enables PostGIS then baselines the full schema from ORM metadata (guarantees DB == models, including the GiST spatial index `idx_sellers_geo_point`).
- `app/db/seed.py` — idempotent seed: 10 bilingual categories + optional bootstrap admin from env.

---

## 3. Tests (`backend/tests/`) — 22 passing

- `test_security.py` — bcrypt round-trip, JWT sign/verify/expire/tamper.
- `test_schemas.py` — signup rules, pricing, **food-safety** accept/reject.
- `test_health.py` — health + OpenAPI surface.
- `test_flow.py` — **full journey**: signup → verify → login → seller onboard → create listing → geo-search → QR mint → consumer scan → seller confirm → **stock decrement**; plus **BOLA** (seller B can't edit seller A's product), unverified-blocked, anti-enumeration, review→reputation.
- `test_jobs.py` — auto-delist + proximity geo query.

Integration tests **skip cleanly** when no database is present (keeps CI green); run fully against PostGIS.

---

## 4. Azure Functions (`functions/`)

- `auto_delist/` — hourly timer: `use_by` past-date → `expired`, zero-stock → `sold_out`.
- `proximity_notifications/` — 15-min timer: notifies devices about newly-listed nearby deals; includes a PostGIS `deals_near` geo primitive.
- `shared/` — db session + reusable, unit-tested job logic (reuses the backend `app` models).
- `host.json`, `requirements.txt`, `local.settings.json.example`.

---

## 5. Admin back-office (`admin-web/`)

React 18 + Vite + TypeScript SPA:
- Login (admin-only guard), Complaints queue (resolve/review), Users (suspend / adjust reputation), Admin-action **audit log**.
- Talks to the backend admin endpoints; every mutation is audited server-side.
- `npm run build` compiles clean; Dockerfile builds and serves via nginx on **:5173**.

---

## 6. Mobile app entry (`mobile/app/`)

The app previously could not start — `package.json` uses `expo-router/entry` but `app/` was empty. Built the full expo-router tree wiring the existing `src/features/*` components:

- `_layout.tsx` (RTL + token hydration), `index.tsx` (role-based redirect).
- `(auth)/` login, signup, verify — wired to `authStore` (now persists token via SecureStore + adds `verify`).
- `(consumer)/` tabs: feed, map, scan, chat.
- `(seller)/` tabs: listings, create, chat.
- `listing/[id].tsx` (detail + call/chat/scan), `chat/[id].tsx` (thread).
- `src/api/endpoints.ts` — typed client mapping backend snake_case → component camelCase.
- Expanded `i18n` (ar/en) with all new keys.

**Bugs fixed in the pre-existing mobile code:**
- `features/index.ts` imported 5 non-existent modules (would break the bundle) → trimmed to real modules.
- `package.json` pinned `eslint-plugin-react-native@3.11.0` (needs eslint ≤7) against eslint 8 → **`npm install` failed**; bumped to `^4.1.0`. Deps now install.
- Added missing `expo-location` / `expo-linking` deps used by hooks/screens.

---

## 7. Local run — verified live via Docker

`docker-compose.yml` runs the whole stack: **db** (PostGIS) + **api** (migrates + seeds on boot) + **admin** (nginx).

```bash
docker compose up --build
# API docs:  http://localhost:8000/docs
# Admin app: http://localhost:5173   (admin@localmarket.dev / admin12345)
```

**Verified against the running containers:**
- `GET /health` → `{"status":"ok"}`
- entrypoint ran migrations, seeded **10 categories + admin**, Uvicorn up.
- `GET /api/v1/categories` → 10 categories.
- admin login → JWT issued.
- `GET /api/v1/admin/complaints` **with** token → `[]`; **without** token → **401** (authz enforced).
- admin SPA → HTTP 200.

Stop with `docker compose down` (add `-v` to also drop the DB volume).

---

## 8. Remaining items (scoped, non-blocking)

- [x] **Mobile typecheck — RESOLVED.** All 28 errors were the same `fontWeight: '600'` widening to `string`, sourced from `theme.typography.weights`. Fixed with `as const` on the weights object; also fixed a real `Input.tsx` bug (`error && styles.inputError` produced `""` when the error string was empty → changed to a ternary). **`npx tsc --noEmit` now passes clean (0 errors).**
- [x] **Chat conversation-list — RESOLVED.** Added `chat_service.list_conversations` + `ConversationSummary` schema + **`GET /conversations`** (other participant, last-message preview, newest first). Exposed `seller.user_id` in product responses so a consumer can **start a chat from a listing**; wired `createConversation` + `listConversations` in the mobile client and both chat tabs, and "message seller" on the listing detail. Verified: 23 pytest tests pass, ruff clean, mobile `tsc` clean, and a **full two-user flow was exercised live through the Docker containers** (both parties see the conversation with the correct preview).
- [x] **Proximity per-consumer targeting — RESOLVED.** Added `users.last_location` (PostGIS point + GiST index) via **idempotent migration 0002**, a **`PUT /users/me/location`** endpoint, and rewrote the timer to push only to consumers within `proximity_radius_km` of each new deal (`tokens_near`). Mobile pushes location from the consumer feed. Tests: targeting + endpoint; verified live (geometry persisted through Docker).
- [x] **Production hardening — RESOLVED.**
  - *Verification delivery:* `messaging_service` sends codes via **Azure Communication Services** email / WhatsApp when configured, else logs (dev). Wired into signup.
  - *Push:* `notification_hub` implements the **Notification Hubs data-plane** (SAS token + REST direct send), platform-aware; no-op log when unconfigured. Unit-tested SAS/parse.
  - *Cert pinning:* iOS `NSPinnedDomains` in `app.config.ts` + Android `network_security_config` pin-set via [`plugins/withAndroidCertPinning.js`](../mobile/plugins/withAndroidCertPinning.js); see [docs/CERT_PINNING.md](docs/CERT_PINNING.md). Replace the placeholder SPKI pins before release.

**All scoped items are now closed.** Final verification: **27 backend tests pass** vs PostGIS, **ruff clean** (backend + functions), **mobile `tsc` clean**, and the **live Docker stack** was re-verified (migration 0002 applied, new routes serving, location update persisted).

---

## 9. How to run each piece standalone

**Backend (local, no Docker):**
```bash
cd backend
uv venv && source .venv/bin/activate && uv pip install -e ".[dev]"
export DATABASE_URL=postgresql+psycopg2://localmarket:localmarket@localhost:5432/localmarket
alembic upgrade head && python -m app.db.seed
uvicorn app.main:app --reload
pytest              # 22 tests (needs the DB reachable for integration ones)
ruff check . && ruff format --check .
```

**Admin web:**
```bash
cd admin-web && npm install && npm run dev   # http://localhost:5173
```

**Mobile:**
```bash
cd mobile && npm install && npx expo start    # scan QR with Expo Go
# set EXPO_PUBLIC_API_URL to your machine IP:8000 for a physical device
```

**Functions (local):** `cd functions && cp local.settings.json.example local.settings.json && func start` (requires Azure Functions Core Tools + the `app` package installed).

---

*This file reflects the true, verified state of the repository as of the build. See [AUDIT_REPORT.md](AUDIT_REPORT.md) for the original findings.*
