# APP02 — Backend y API
## ClubLab v1

**Estado:** FINAL DE DISEÑO  
**Fase:** 4 / Bloque B  
**Implementación:** pendiente  
**Dependencias:** APP01 + D02 + D03

---

# 1. Stack

```text
NestJS
TypeScript
Node.js 22
TypeORM
PostgreSQL 18
REST
```

Puerto interno:

```text
3000
```

Sin publicación directa al host.

---

# 2. Endpoints públicos

```text
GET /api/health
GET /api/me
GET /api/team
GET /api/ranking
GET /api/missions
GET /api/activity
```

---

# 3. Health

```http
GET /api/health
```

```json
{
  "status": "ok",
  "service": "api"
}
```

Representa liveness.

Durante `ranking-db-failure` sigue:

```text
200.
```

---

# 4. Readiness interno

```http
GET /internal/health/ready
```

Uso:

```text
instructor/preflight.
```

No publicado por gateway.

---

# 5. Me

```http
GET /api/me
```

```json
{
  "id": "uuid",
  "username": "avery",
  "displayName": "Avery Morgan",
  "avatarKey": "avatar-01",
  "roleLabel": "Generalist",
  "team": {
    "id": "uuid",
    "slug": "team01",
    "name": "Equipo 01"
  }
}
```

---

# 6. Team

```http
GET /api/team
```

Devuelve:

```text
identidad;
descripción;
score;
miembros.
```

No depende de RankingRepository.

---

# 7. Ranking

```http
GET /api/ranking
```

```json
[
  {
    "position": 1,
    "teamId": "uuid",
    "slug": "byte-benders",
    "name": "Byte Benders",
    "score": 410,
    "isCurrentTeam": false
  },
  {
    "position": 3,
    "teamId": "uuid",
    "slug": "team01",
    "name": "Equipo 01",
    "score": 320,
    "isCurrentTeam": true
  }
]
```

Fuente:

```text
app.teams + app.scores.
```

---

# 8. Missions

```http
GET /api/missions
```

Estados:

```text
completed
in_review
rejected
available
```

---

# 9. Activity

```http
GET /api/activity
```

Devuelve las últimas:

```text
8 actividades.
```

---

# 10. Arquitectura

```text
Controller
→ Service
→ Repository
→ PostgreSQL
```

Ranking:

```text
RankingService
→ ScenarioAwareRankingRepository
→ normal/fault.
```

---

# 11. Repositories

```text
UsersRepository
TeamsRepository
MissionsRepository
ActivityRepository
RankingRepository
EnvironmentContextRepository
```

---

# 12. Scenario-aware ranking

```text
normal
→ PostgresRankingRepository

ranking-db-failure
→ RankingFaultAdapter
```

---

# 13. Fault Adapter

Produce de manera determinista:

```text
code=ENOTFOUND
target=database-broken:5432
```

No realiza conexión externa real.

---

# 14. Error público

```json
{
  "statusCode": 500,
  "message": "Unable to load ranking",
  "error": "Internal Server Error",
  "requestId": "..."
}
```

---

# 15. Contrato del incidente

```text
/api/health    200
/api/me        200
/api/team      200
/api/missions  200
/api/activity  200
/api/ranking   500
```

---

# 16. Scenario state

Valores:

```text
normal
ranking-db-failure
```

Adapter:

```text
ScenarioStateStore
```

Inicialmente puede ser:

```text
in-memory.
```

---

# 17. api-down

No pertenece a la app.

Será scenario de infraestructura de Fase 5.

---

# 18. Internal control API

```text
GET  /internal/lab/scenario
POST /internal/lab/scenario
POST /internal/lab/recover/ranking-db
```

No publicada por gateway.

---

# 19. Tokens

Scenario control:

```text
X-ClubLab-Control-Token
```

Recover:

```text
X-ClubLab-Recovery-Token
```

No intercambiables.

---

# 20. Recover

Activo:

```text
ranking-db-failure → normal
```

Ya normal:

```text
no-op.
```

No modifica:

```text
score;
missions;
activity;
lablogs.
```

---

# 21. Lablogs

Formato:

```text
JSON Lines
```

Ruta:

```text
/var/log/clublab/lab-events.jsonl
```

Mount:

```text
API RW
Toolbox RO
```

---

# 22. Ejemplo lablog

```text
20:14:03 API       GET /api/ranking
20:14:03 RANKING   Loading ranking scores
20:14:03 DATABASE  Host database-broken could not be resolved
20:14:03 API       GET /api/ranking -> 500
```

No revela:

```text
scenario name;
recovery command;
secrets.
```

---

# 23. Request ID

Cada request devuelve:

```text
X-Request-Id.
```

El mismo valor aparece en lablogs relacionados.

---

# 24. Error handling

`ApiExceptionFilter`:

```text
sanitiza errores;
no stack trace público;
incluye requestId.
```

---

# 25. Validation

```text
ValidationPipe
whitelist=true
forbidNonWhitelisted=true
transform=true
```

---

# 26. Swagger

No público durante la clase.

Puede existir únicamente en desarrollo.

---

# 27. TypeORM

```text
synchronize=false
migrationsRun=false
```

Migrations se ejecutan en deploy/reset.

---

# 28. Pool

Propuesta inicial:

```text
max=8 conexiones.
```

---

# 29. Configuración backend

```text
NODE_ENV
PORT
TEAM_ID
DB_HOST
DB_PORT
DB_NAME
DB_USER
DB_PASSWORD
CLUBLAB_CONTROL_TOKEN
CLUBLAB_RECOVERY_TOKEN
LABLOG_PATH
```

Variables críticas faltantes:

```text
startup FAIL.
```

---

# 30. Tests

Unit:

```text
ranking
scenario
recover
mission mapping
```

Integration:

```text
ranking order
current team
team data
missions
activity
```

E2E:

```text
normal
ranking failure
recover
tokens
sanitization
```

---

# 31. Definition of Done

```text
[ ] 6 endpoints públicos
[ ] DTOs
[ ] repositories
[ ] health/readiness
[ ] ranking
[ ] fault adapter
[ ] scenario API
[ ] recover
[ ] token guards
[ ] lablogs
[ ] request ID
[ ] error filter
[ ] tests PASS
```

---

# 32. Estado

```text
API CONTRACT       ✅
MODULES            ✅
REPOSITORIES       ✅
SCENARIO CONTRACT  ✅
FAULT MODEL        ✅
LABLOG FORMAT      ✅
RECOVER CONTRACT   ✅

CÓDIGO             ⏳
TESTS              ⏳
INTEGRACIÓN        ⏳
```

# APP02 — DISEÑO COMPLETADO