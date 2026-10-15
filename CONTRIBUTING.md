# Contributing Guide for SrotGraph

## Repository Layout

```
srotgraph/
├── apps/                  # Deployable applications
│   ├── api/               # FastAPI backend
│   └── web/               # Next.js frontend
├── packages/              # Shared libraries
│   ├── contracts/         # TypeScript data contracts
│   └── python/            # Python utilities
├── tests/                 # Cross-cutting tests
│   ├── unit/
│   ├── integration/
│   └── contract/
├── docs/                  # Documentation
├── migrations/            # Database migrations
└── .github/               # CI/CD workflows
```

## Key Rules

1. **Do not commit `.env` files** — only `.env.example` with placeholders
2. **Shared types live in packages/** — `packages/contracts` for TypeScript, `packages/python` for Python
3. **Tests mirror the structure** — unit tests next to code, integration/contract tests in `tests/`
4. **CI must pass** — linting, formatting, type checking, and tests

## Commands Reference

### Python (apps/api, packages/python)

```bash
# Install dependencies (uv)
cd apps/api && uv sync --extra dev

# Run tests
uv run pytest tests/ -v

# Format code
uv run ruff format .

# Lint code
uv run ruff check .

# Type check
uv run mypy src/
```

### TypeScript (apps/web, packages/contracts)

```bash
# Install dependencies (pnpm)
pnpm install

# Type check
pnpm typecheck

# Lint
pnpm lint

# Build
pnpm build
```

### Docker

```bash
# Start PostgreSQL
docker-compose up -d

# Stop PostgreSQL
docker-compose down
```

## PR Checklist

- [ ] Code follows project conventions (ruff/ESLint clean)
- [ ] Tests added/updated and passing
- [ ] `.env.example` updated if new env vars added
- [ ] Documentation updated if behavior changed
- [ ] CI passes on the PR

## Getting Help

- Open an issue for bugs or feature requests
- Check existing documentation in `docs/`
- Review the architecture in `docs/ARCHITECTURE.md`
