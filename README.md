# SrotGraph

**Evidence-Preserving Intelligence System**

SrotGraph processes continuous or recorded audio, video and text streams, extracts timestamped claims, tracks claim evolution, connects evidence and sources, and measures accuracy, latency, memory consumption and information loss.

## Repository Structure

This is a monorepo using pnpm workspaces for the frontend and uv for Python packages.

```
srotgraph/
├── apps/
│   ├── api/              # FastAPI backend
│   │   ├── src/
│   │   │   ├── main.py   # Application entry point
│   │   │   └── config.py # Configuration
│   │   ├── tests/
│   │   │   └── test_main.py
│   │   ├── pyproject.toml
│   │   └── Dockerfile
│   └── web/              # Next.js frontend
│       ├── src/
│       │   └── app/
│       │       ├── page.tsx      # Status page
│       │       ├── layout.tsx    # Root layout
│       │       ├── globals.css   # Global styles
│       │       └── api/
│       │           └── health/
│       │               └── route.ts  # Health API proxy
│       ├── package.json
│       ├── tsconfig.json
│       └── Dockerfile
├── packages/
│   ├── contracts/        # Shared TypeScript data contracts
│   │   ├── src/
│   │   │   └── index.ts
│   │   ├── package.json
│   │   └── tsconfig.json
│   └── python/           # Shared Python utilities
│       ├── src/
│       │   ├── __init__.py
│       │   └── config.py
│       └── pyproject.toml
├── tests/
│   ├── unit/             # Unit tests
│   ├── integration/      # Integration tests
│   └── contract/         # Contract tests
├── docs/                 # Documentation
├── migrations/           # Database migrations (future)
├── .github/
│   └── workflows/
│       └── ci.yml        # CI pipeline
├── docker-compose.yml    # Local PostgreSQL
├── pnpm-workspace.yaml   # pnpm workspace config
├── pyproject.toml        # Root Python config (uv)
├── .env.example          # Environment template
├── .gitignore
├── LICENSE
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── SECURITY.md
└── README.md
```

## Quick Start

### Prerequisites

- Python 3.12+
- Node.js 20+
- pnpm 9+
- uv (Python package manager)
- Docker and Docker Compose (for local PostgreSQL)

### Install uv

```bash
# Install uv (Python package manager)
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Install Dependencies

```bash
# Install all pnpm dependencies
pnpm install

# Install Python dependencies for API
cd apps/api
uv sync --extra dev

# Install Python dependencies for shared package
cd ../packages/python
uv sync --extra dev
```

### Start PostgreSQL (optional, for development)

```bash
docker-compose up -d
```

### Run the API

```bash
cd apps/api
uv run uvicorn srotgraph_api.main:app --reload
```

The API will be available at http://localhost:8000

- Health: http://localhost:8000/health
- Docs: http://localhost:8000/docs

### Run the Web App

```bash
cd apps/web
pnpm dev
```

The web app will be available at http://localhost:3000

## Development

### Code Quality

```bash
# Python formatting and linting (using Ruff)
cd apps/api
uv run ruff format .
uv run ruff check .

# TypeScript type checking
cd apps/web
pnpm typecheck

# ESLint
cd apps/web
pnpm lint
```

### Tests

```bash
# Run API unit tests
cd apps/api
uv run pytest tests/ -v

# Run Python package tests
cd packages/python
uv run pytest tests/ -v

# Run contract tests
cd tests/contract
uv run pytest tests/contract/ -v

# Run TypeScript/Next.js tests (when added)
cd apps/web
pnpm test
```

## Project Conventions

- **Python**: Use `uv` for dependency management, `ruff` for linting/formatting
- **TypeScript**: Strict mode, ESLint with Next.js config
- **Shared types**: Defined in `packages/contracts` and used by both apps
- **API design**: REST with JSON, versioned via URL prefix (`/api/v1/`)

## Documentation

- [Architecture](docs/ARCHITECTURE.md) - System design and component responsibilities
- [Data Model](docs/DATA_MODEL.md) - Database schema and entity relationships
- [Roadmap](docs/ROADMAP.md) - Implementation phases and priorities

## License

MIT License - see [LICENSE](LICENSE) for details.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.

## Security

See [SECURITY.md](SECURITY.md) for security reporting instructions.
