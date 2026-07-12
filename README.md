# localmarket

A cross-platform mobile marketplace for Syria connecting local shops and factories with consumers through discovery and connection.

## Purpose

Help people access affordable goods by connecting sellers with near-expiry or discounted products to nearby buyers. No in-app payments — all transactions happen offline.

## Tech Stack

| Layer | Technology |
|-------|------------|
| Mobile | React Native + Expo |
| Backend | Python + FastAPI |
| Database | Azure PostgreSQL Flexible Server + PostGIS |
| Real-time | Azure SignalR Service |
| Push Notifications | Azure Notification Hubs |
| Storage | Azure Blob Storage + CDN |
| Maps | Google Maps Platform (proxied) |
| CI/CD | GitHub Actions |

## Project Structure

```
localmarket/
├── backend/          # FastAPI application
├── mobile/           # React Native + Expo app
├── admin-web/        # Back-office React app
├── infra/            # Azure infrastructure (Bicep)
├── functions/        # Azure Functions (timers)
├── docs/             # Documentation
└── .github/          # CI/CD workflows
```

## Development

### Prerequisites

- Node.js 20+
- Python 3.12+
- Docker (optional, for containerized development)

### Quick Start

```bash
# Install dependencies
npm install
cd backend && pip install -e ".[dev]"

# Run linting
npm run lint
cd backend && ruff check .

# Run tests
npm test
cd backend && pytest
```

## Environment Variables

Copy `.env.example` to `.env` and configure:
- Database connection
- Azure services
- Google Maps API key

## Documentation

- [Architecture](docs/ARCHITECTURE.md)
- [Data Model](docs/DATA_MODEL.md)
- [API Reference](docs/API.md)
- [Security](docs/SECURITY.md)

## License

Proprietary — All rights reserved.
