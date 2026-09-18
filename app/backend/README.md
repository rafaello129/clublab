# Backend

API de ClubLab.

## Stack previsto

```text
NestJS
TypeScript
Node.js 22
TypeORM
PostgreSQL 18
```

## Endpoints públicos previstos

```text
POST /api/auth/login
POST /api/auth/logout
GET  /api/auth/session
GET  /api/health
GET  /api/me
GET  /api/team
GET  /api/ranking
GET  /api/missions
GET  /api/activity
```

## Escenario principal

`ranking-db-failure` afecta únicamente al flujo del ranking. La API, la DB real y el resto de endpoints deben continuar sanos.

Los endpoints internos de control no deben publicarse por el gateway.
