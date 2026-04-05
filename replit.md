# Workspace

## Overview

pnpm workspace monorepo using TypeScript. Each package manages its own dependencies.

## Python Project: Módulo de Gestión de Inventario

A complete Python inventory management CLI system located in `inventory_system/`.

### Run:
```bash
cd inventory_system && python3 main.py
```

### Architecture:
- `models/` — domain classes (Producto, Inventario, Transaccion)
- `services/` — business logic (InventarioService, TransaccionService)
- `controllers/` — CLI flow (MenuController)
- `patterns/` — design patterns (factory.py, facade.py, observer.py)
- `utils/` — formatting and validation helpers
- `main.py` — entry point

### Design Patterns:
- **Factory Method** (`patterns/factory.py`): Creates SimpleProduct, PerishableProduct, DigitalProduct
- **Facade** (`patterns/facade.py`): Unified interface over all subsystems
- **Observer** (`patterns/observer.py`): Stock change notifications (alerts, logs)

## Stack

- **Monorepo tool**: pnpm workspaces
- **Node.js version**: 24
- **Package manager**: pnpm
- **TypeScript version**: 5.9
- **API framework**: Express 5
- **Database**: PostgreSQL + Drizzle ORM
- **Validation**: Zod (`zod/v4`), `drizzle-zod`
- **API codegen**: Orval (from OpenAPI spec)
- **Build**: esbuild (CJS bundle)

## Key Commands

- `pnpm run typecheck` — full typecheck across all packages
- `pnpm run build` — typecheck + build all packages
- `pnpm --filter @workspace/api-spec run codegen` — regenerate API hooks and Zod schemas from OpenAPI spec
- `pnpm --filter @workspace/db run push` — push DB schema changes (dev only)
- `pnpm --filter @workspace/api-server run dev` — run API server locally

See the `pnpm-workspace` skill for workspace structure, TypeScript setup, and package details.
