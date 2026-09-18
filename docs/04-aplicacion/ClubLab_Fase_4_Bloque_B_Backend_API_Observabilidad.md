# ClubLab — Fase 4 / Bloque B
## Backend, API, observabilidad y soporte de escenarios

**Proyecto:** ClubLab v1  
**Fase:** 4 — Aplicación ClubLab  
**Bloque:** B  
**Estado:** DISEÑO CERRADO v1 — IMPLEMENTACIÓN PENDIENTE  
**Dependencias:** D01 + D02 + D03 + APP01  
**Entregable derivado:** `APP02_Backend_API.md`

---

# 1. Propósito

Este bloque define el backend que conectará:

```text
Frontend
   ↓
HTTP / REST
   ↓
NestJS
   ↓
Services
   ↓
Repositories
   ↓
PostgreSQL
```

y que, al mismo tiempo, permitirá observar de forma controlada:

```text
requests;
respuestas;
errores;
dependencias;
fallo del ranking;
recuperación.
```

El backend debe sentirse como una API real, pero mantenerse lo bastante pequeño para que un alumno pueda reconstruir mentalmente su funcionamiento durante una clase de 120 minutos.

---

# 2. Objetivos funcionales

El backend debe soportar:

```text
perfil del participante;
datos del equipo;
ranking;
misiones;
actividad;
health;
lablogs;
scenario ranking-db-failure;
recover ranking-db.
```

Debe permitir exactamente:

```text
M1 → descubrir request
M2 → usar API directamente
M3 → relacionar API con DB
M4 → observar cambio DB → API
M6 → recibir ranking 500 con API viva
M7 → diagnosticar y recuperar
```

---

# 3. Stack cerrado

```text
NestJS
TypeScript
Node.js 22
TypeORM
PostgreSQL 18
```

Runtime:

```text
build compilado de producción
```

No se utilizará durante clase:

```text
ts-node;
nodemon;
synchronize:true;
hot reload.
```

---

# 4. Puerto interno

La API escucha en:

```text
3000
```

solo dentro de:

```text
teamXX-app.
```

No publica:

```text
3000
```

al host.

Acceso del navegador:

```text
Gateway → /api/*
```

Acceso del toolbox:

```text
http://api:3000/api/*
```

---

# 5. Principio de diseño

No se construirá un backend con capas innecesarias.

La forma base será:

```text
Controller
   ↓
Service
   ↓
Repository
   ↓
PostgreSQL
```

Solo se añadirá una abstracción extra cuando tenga una función concreta.

Ejemplo legítimo:

```text
ScenarioAwareRankingRepository
```

porque permite el incidente parcial sin afectar otros módulos.

---

# 6. Módulos NestJS

Se congelan:

```text
HealthModule
UsersModule
TeamsModule
MissionsModule
RankingModule
ActivityModule
LabModule
DatabaseModule
```

No habrá módulos vacíos creados únicamente por estilo.

---

# 7. Estructura propuesta

```text
backend/
└── src/
    ├── main.ts
    ├── app.module.ts
    │
    ├── common/
    │   ├── filters/
    │   │   └── api-exception.filter.ts
    │   ├── middleware/
    │   │   └── request-id.middleware.ts
    │   └── types/
    │
    ├── config/
    │   ├── app.config.ts
    │   └── env.validation.ts
    │
    ├── database/
    │   ├── database.module.ts
    │   ├── entities/
    │   └── migrations/
    │
    ├── health/
    ├── users/
    ├── teams/
    ├── missions/
    ├── ranking/
    ├── activity/
    │
    └── lab/
        ├── lab.module.ts
        ├── logging/
        ├── scenario/
        └── control/
```

---

# 8. Endpoints públicos

Se congelan seis endpoints REST:

```text
GET /api/health
GET /api/me
GET /api/team
GET /api/ranking
GET /api/missions
GET /api/activity
```

No se necesita un:

```text
/api/dashboard
```

porque queremos que el frontend consuma varias piezas reales.

---

# 9. Contrato general HTTP

Formato:

```text
application/json
UTF-8
```

No se utilizará un envelope obligatorio tipo:

```json
{
  "data": {},
  "meta": {}
}
```

para todos los endpoints.

Las respuestas serán directas y legibles en DevTools.

---

# 10. Request ID

Cada request recibirá:

```text
requestId
```

generado por middleware.

Se devolverá como:

```text
X-Request-Id
```

y se utilizará para correlacionar:

```text
request
technical log
lablog
error.
```

No contiene información sensible.

---

# 11. `GET /api/health`

Propósito:

```text
liveness público del proceso API.
```

Respuesta:

```json
{
  "status": "ok",
  "service": "api"
}
```

Status:

```text
200
```

Debe seguir devolviendo:

```text
200
```

durante:

```text
ranking-db-failure.
```

---

# 12. Health no comprueba ranking

`/api/health` no invoca:

```text
RankingRepository.
```

Tampoco debe fallar únicamente porque el escenario del ranking está activo.

Concepto pedagógico:

```text
API viva
≠
todas sus operaciones correctas.
```

---

# 13. Readiness interno

Se añadirá:

```text
GET /internal/health/ready
```

No publicado por gateway.

Su objetivo es:

```text
operación del instructor;
preflight;
diagnóstico real.
```

Respuesta normal:

```json
{
  "status": "ready",
  "api": "ok",
  "database": "ok"
}
```

Puede devolver:

```text
503
```

si la conexión PostgreSQL real está caída.

El escenario `ranking-db-failure` no debe volverlo 503 porque la DB verdadera sigue sana.

---

# 14. `GET /api/me`

Devuelve el participante actual.

Contrato:

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

# 15. Identidad actual

El backend utilizará una abstracción:

```text
CurrentUserResolver
```

para evitar acoplar `/api/me` al mecanismo de autenticación antes del Bloque C.

Contrato conceptual:

```ts
interface CurrentUserResolver {
  getCurrentUserId(requestContext): Promise<string>;
}
```

Bloque C decidirá:

```text
cookie;
sesión;
login de laboratorio.
```

El contrato de API no cambia.

---

# 16. `GET /api/team`

Devuelve el equipo local y sus integrantes.

Contrato:

```json
{
  "id": "uuid",
  "slug": "team01",
  "name": "Equipo 01",
  "description": "Equipo local de ClubLab",
  "score": 320,
  "members": [
    {
      "id": "uuid",
      "username": "avery",
      "displayName": "Avery Morgan",
      "avatarKey": "avatar-01",
      "roleLabel": "Generalist"
    }
  ]
}
```

No devolverá:

```text
ranking position
```

desde este endpoint.

Esto evita que `/api/team` dependa del flujo `RankingRepository`.

---

# 17. Por qué `/api/team` debe seguir funcionando

Durante:

```text
ranking-db-failure
```

debe ocurrir:

```text
/api/team → 200
/api/ranking → 500
```

Esto ayuda a descartar:

```text
DB completamente caída;
API completamente caída.
```

---

# 18. `GET /api/ranking`

Contrato normal:

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

Debe devolver siempre las seis filas del seed en estado normal.

---

# 19. Orden de ranking

Fuente:

```text
app.teams
+
app.scores
```

Orden:

```text
score DESC
name ASC
```

Posición:

```text
ROW_NUMBER().
```

No calcular el ranking en frontend.

---

# 20. `isCurrentTeam`

El backend obtiene el equipo local mediante:

```text
lab.environment_context.
```

No se confía en:

```text
teamId enviado por navegador.
```

---

# 21. `GET /api/missions`

Contrato:

```json
[
  {
    "id": "uuid",
    "code": "M-101",
    "title": "Primer Pull Request",
    "description": "...",
    "difficulty": "easy",
    "points": 40,
    "status": "completed",
    "awardedPoints": 40
  },
  {
    "id": "uuid",
    "code": "M-202",
    "title": "Data Challenge",
    "description": "...",
    "difficulty": "medium",
    "points": 110,
    "status": "in_review",
    "awardedPoints": 0
  }
]
```

---

# 22. Estado de misión para API

Mapeo:

```text
Submission approved
→ completed

Submission submitted
→ in_review

Submission rejected
→ rejected

Sin Submission
→ available
```

El frontend no necesita reconstruir esta lógica.

---

# 23. `GET /api/activity`

Respuesta:

```json
[
  {
    "id": 18,
    "eventType": "mission_completed",
    "message": "Avery completó API Sprint",
    "createdAt": "2026-09-17T15:10:00Z",
    "actor": {
      "id": "uuid",
      "displayName": "Avery Morgan",
      "avatarKey": "avatar-01"
    }
  }
]
```

Si:

```text
user_id IS NULL
```

entonces:

```json
"actor": null
```

---

# 24. Número de actividades

Por defecto:

```text
últimas 8
```

ordenadas:

```text
created_at DESC.
```

No se implementa paginación en v1.

---

# 25. DTOs públicos

Se definirán DTOs explícitos:

```text
MeResponseDto
TeamResponseDto
TeamMemberDto
RankingEntryDto
MissionDto
ActivityDto
ActivityActorDto
HealthResponseDto
```

No devolver directamente:

```text
TypeORM entities.
```

---

# 26. Motivo de DTOs

Evitan exponer accidentalmente:

```text
columnas internas;
foreign keys innecesarias;
campos futuros;
objetos de ORM.
```

Además mantienen contratos estables para frontend.

---

# 27. Repositories

Se definen:

```text
UsersRepository
TeamsRepository
MissionsRepository
ActivityRepository
RankingRepository
EnvironmentContextRepository
```

No es necesario crear:

```text
GenericRepository<T>
```

si no aporta valor real.

---

# 28. `UsersRepository`

Responsabilidades:

```text
obtener participante actual;
obtener usuarios de team.
```

No contiene:

```text
HTTP;
DTOs;
scenario logic.
```

---

# 29. `TeamsRepository`

Responsabilidades:

```text
obtener equipo local;
obtener score local;
obtener miembros.
```

No usa:

```text
RankingRepository.
```

---

# 30. `MissionsRepository`

Responsabilidad:

```text
misiones + submission del usuario actual.
```

Consulta puede resolver:

```text
mission
LEFT JOIN submission.
```

---

# 31. `ActivityRepository`

Responsabilidad:

```text
actividad del team local
```

limitada a:

```text
últimas 8.
```

---

# 32. `EnvironmentContextRepository`

Responsabilidad:

```text
obtener team local desde lab.environment_context.
```

Solo API utiliza esta abstracción.

El alumno no recibe permisos SQL directos sobre la tabla.

---

# 33. Contrato `RankingRepository`

Se define como puerto:

```ts
interface RankingRepository {
  findRanking(): Promise<RankingEntry[]>;
}
```

Implementación normal:

```text
PostgresRankingRepository.
```

---

# 34. `PostgresRankingRepository`

Realiza la query de ranking real sobre:

```text
app.teams
app.scores
lab.environment_context
```

Debe producir:

```text
position;
teamId;
slug;
name;
score;
isCurrentTeam.
```

---

# 35. Wrapper scenario-aware

El servicio consumirá:

```text
ScenarioAwareRankingRepository
```

que implementa el mismo contrato.

Conceptualmente:

```text
RankingService
      │
      ▼
ScenarioAwareRankingRepository
      │
      ├── scenario=normal
      │      ↓
      │ PostgresRankingRepository
      │
      └── scenario=ranking-db-failure
             ↓
       RankingFaultAdapter
```

---

# 36. Fault adapter elegido

Para v1 se selecciona:

> **fallo determinista a nivel de aplicación que reproduce el contrato de un error de resolución/conexión a una dependencia.**

No se realizará una conexión real a Internet ni una espera larga de DNS.

El adapter produce un error tipado:

```text
RankingDependencyError
code=ENOTFOUND
target=database-broken:5432
```

---

# 37. Por qué no realizar un fallo de red real

Ventajas del adapter determinista:

```text
misma evidencia cada vez;
sin dependencia de resolver DNS;
sin timeouts variables;
sin afectar conexión real de otros módulos;
incidente se activa instantáneamente;
ensayo reproducible.
```

Pedagógicamente sigue representando:

```text
RankingRepository no puede alcanzar su dependencia.
```

---

# 38. Honestidad técnica

Internamente, documentación del instructor debe indicar:

```text
fault injection deliberado.
```

No se presentará como una falla espontánea real del servidor.

La experiencia del alumno sigue siendo válida porque diagnostica:

```text
síntoma;
capa;
dependencia;
evidencia.
```

---

# 39. `RankingDependencyError`

Campos internos:

```text
code
target
message
causeType
```

Ejemplo:

```text
code: ENOTFOUND
target: database-broken:5432
causeType: dependency-resolution
```

No se serializa completo al cliente.

---

# 40. Respuesta pública del incidente

`GET /api/ranking`

durante escenario:

```text
500
```

Body:

```json
{  "statusCode": 500,
  "message": "Unable to load ranking",
  "error": "Internal Server Error",
  "requestId": "..."
}
```

No incluir:

```text
database-broken;
ENOTFOUND;
stack trace;
password;
DATABASE_URL.
```

---

# 41. Otros endpoints durante incidente

Deben permanecer:

```text
/api/health    → 200
/api/me        → 200
/api/team      → 200
/api/missions  → 200
/api/activity  → 200
```

Este contrato es obligatorio.

---

# 42. Scenario state

Se define una interfaz:

```ts
type LabScenario =
  | 'normal'
  | 'ranking-db-failure';

interface ScenarioStateStore {
  get(): Promise<LabScenario>;
  set(scenario: LabScenario): Promise<void>;
}
```

---

# 43. Implementación inicial de ScenarioStateStore

La aplicación v1 puede iniciar con:

```text
InMemoryScenarioStateStore
```

porque:

```text
el escenario existe durante una sesión;
recover ocurre con API viva;
no añade otro volumen;
simplifica implementación.
```

Si Fase 5 requiere persistencia ante restart:

```text
se reemplaza el adapter
```

sin modificar `RankingService`.

---

# 44. Comportamiento ante restart

Con store in-memory:

```text
restart API
→ scenario vuelve a normal.
```

Esto se considera aceptable para aplicación v1.

Fase 5 decidirá si el orquestador debe:

```text
reaplicar scenario
```

después de un restart.

---

# 45. `api-down`

No pertenece al `ScenarioStateStore`.

Razón:

```text
una API no puede representar correctamente su propia caída
mediante una variable interna.
```

`api-down` será:

```text
escenario de infraestructura
```

de Fase 5:

```text
stop/restart del contenedor API.
```

---

# 46. Endpoints internos de control

Se congelan:

```text
GET  /internal/lab/scenario
POST /internal/lab/scenario
POST /internal/lab/recover/ranking-db
```

No se publican por gateway.

---

# 47. `GET /internal/lab/scenario`

Uso:

```text
instructor / clublabctl.
```

Auth:

```text
X-ClubLab-Control-Token.
```

Respuesta:

```json
{
  "scenario": "normal"
}
```

---

# 48. `POST /internal/lab/scenario`

Auth:

```text
X-ClubLab-Control-Token.
```

Body:

```json
{
  "scenario": "ranking-db-failure"
}
```

Valores permitidos:

```text
normal
ranking-db-failure
```

No acepta:

```text
api-down
strings arbitrarios.
```

---

# 49. Respuesta de scenario load

```json
{
  "previousScenario": "normal",
  "currentScenario": "ranking-db-failure",
  "changed": true
}
```

Debe registrar evento de control técnico, no lablog dirigido al alumno antes de tiempo.

---

# 50. `POST /internal/lab/recover/ranking-db`

Uso:

```text
clublab recover ranking-db.
```

Auth:

```text
X-ClubLab-Recovery-Token.
```

No recibe:

```text
teamId.
```

El team es implícito porque cada API pertenece a un único entorno.

---

# 51. Recover response

Si activo:

```json
{
  "action": "recover-ranking-db",
  "previousScenario": "ranking-db-failure",
  "currentScenario": "normal",
  "changed": true
}
```

Si ya normal:

```json
{
  "action": "recover-ranking-db",
  "previousScenario": "normal",
  "currentScenario": "normal",
  "changed": false
}
```

Idempotente.

---

# 52. Separación de tokens

API recibirá:

```text
CLUBLAB_CONTROL_TOKEN
CLUBLAB_RECOVERY_TOKEN
```

No son iguales.

Toolbox recibe solo:

```text
RECOVERY token.
```

`clublabctl`/instructor recibe:

```text
CONTROL token.
```

---

# 53. Comparación de tokens

La implementación debe evitar comparaciones ingenuas cuando sea sencillo.

Preferencia:

```text
timing-safe comparison
```

sobre valores en memoria.

No loggear tokens.

---

# 54. Lab logging

Se implementará un servicio específico:

```text
LabEventLogger.
```

No sustituye al logger técnico de Nest.

---

# 55. Dos canales de logging

## Technical log

Destino:

```text
stdout/stderr.
```

Audiencia:

```text
instructor.
```

Contiene:

```text
startup;
exceptions;
stack trace sanitizable;
DB errors;
control actions.
```

## Lablog

Destino:

```text
lablogs volume.
```

Audiencia:

```text
alumno durante M7.
```

Contiene:

```text
eventos pedagógicos seleccionados.
```

---

# 56. Formato del lablog

Se utilizará:

```text
JSON Lines
```

en almacenamiento.

Ejemplo:

```json
{"ts":"2026-09-17T20:14:03.120Z","requestId":"abc123","layer":"API","event":"request","detail":"GET /api/ranking"}
{"ts":"2026-09-17T20:14:03.128Z","requestId":"abc123","layer":"RANKING","event":"fetch","detail":"Loading ranking scores"}
{"ts":"2026-09-17T20:14:03.131Z","requestId":"abc123","layer":"DATABASE","event":"dependency_error","detail":"Host database-broken could not be resolved"}
{"ts":"2026-09-17T20:14:03.133Z","requestId":"abc123","layer":"API","event":"response","detail":"GET /api/ranking -> 500"}
```

---

# 57. Archivo

Ruta lógica:

```text
/var/log/clublab/lab-events.jsonl
```

Montaje:

```text
API     → RW
Toolbox → RO.
```

Directorio pertenece al volumen:

```text
lablogs.
```

---

# 58. Escritura de lablogs

`LabEventLogger`:

```text
append-only;
una línea JSON por evento;
sin formatos multilinea;
sin stack traces.
```

Esto facilita:

```text
tail;
parsing;
clublab logs api.
```

---

# 59. Eventos normales de ranking

Ejemplo:

```text
API       GET /api/ranking
RANKING   Loading ranking scores
DATABASE  Ranking query completed
API       GET /api/ranking -> 200
```

No hace falta loggear cada request de toda la aplicación.

---

# 60. Eventos durante incidente

Secuencia mínima:

```text
API       GET /api/ranking
RANKING   Loading ranking scores
DATABASE  Host database-broken could not be resolved
API       GET /api/ranking -> 500
```

Esto es suficiente para M7.

---

# 61. Qué no incluir en lablogs

Prohibido:

```text
password;
DATABASE_URL completa;
control token;
recovery token;
Authorization header;
cookies;
filesystem host;
container ID;
otros teams;
stack trace completo.
```

---

# 62. Log pedagógico no da la respuesta completa

No escribir:

```text
“CAUSE: ranking-db-failure scenario is enabled”
```

ni:

```text
“Run clublab recover ranking-db”.
```

El alumno debe inferir:

```text
qué capa falla;
qué evidencia lo demuestra.
```

---

# 63. Rotación

V1:

```text
máximo 5–10 MiB por team
```

La implementación puede utilizar:

```text
simple truncation/reset;
rotación pequeña;
límite gestionado por LabEventLogger.
```

No introducir:

```text
Loki;
ELK;
logging daemon.
```

---

# 64. Reset de lablogs

`reset teamXX`:

```text
limpia lab-events.jsonl.
```

Recover:

```text
NO limpia lablogs.
```

Los alumnos necesitan conservar evidencia del incidente hasta M8.

---

# 65. Exception filter

Se implementará:

```text
ApiExceptionFilter
```

para garantizar respuestas sanitizadas.

Responsabilidades:

```text
requestId;
status;
message pública;
evitar stack traces;
normalizar 500.
```

---

# 66. Errores esperados

## 404

Ejemplo:

```json
{
  "statusCode": 404,
  "message": "Resource not found",
  "error": "Not Found",
  "requestId": "..."
}
```

## 500 ranking

```json
{
  "statusCode": 500,
  "message": "Unable to load ranking",
  "error": "Internal Server Error",
  "requestId": "..."
}
```

---

# 67. ValidationPipe

NestJS utilizará:

```text
ValidationPipe
```

con:

```text
whitelist=true
forbidNonWhitelisted=true
transform=true
```

especialmente para:

```text
internal control DTOs.
```

---

# 68. Swagger

No se expondrá Swagger públicamente durante ClubLab #01.

Motivo:

```text
revelaría todos los endpoints antes de la exploración.
```

Puede existir:

```text
solo dev;
deshabilitado en build de clase.
```

---

# 69. CORS

Frontend y API estarán bajo:

```text
mismo origen
```

mediante gateway.

Por tanto:

```text
CORS no es necesario para flujo normal.
```

No se habilitará:

```text
Access-Control-Allow-Origin: *
```

por defecto.

---

# 70. Database connection

TypeORM utilizará:

```text
DB app credential
```

del team.

Configuración:

```text
synchronize=false
migrationsRun=false en runtime normal
logging controlado.
```

Migrations se ejecutan durante:

```text
deploy/reset.
```

---

# 71. Pool de DB

ClubLab no necesita un pool grande.

Propuesta inicial:

```text
max connections app pool = 8
```

por debajo del:

```text
CONNECTION LIMIT 20
```

definido para rol app.

Validar en pruebas.

---

# 72. Configuración requerida

Variables backend previstas:

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

No exponer:

```text
DB_PASSWORD
tokens
```

en logs.

---

# 73. Validación de configuración

Al arrancar:

```text
env.validation.ts
```

deberá fallar si falta una variable crítica.

No usar defaults inseguros para:

```text
DB password;
control token;
recovery token.
```

---

# 74. Startup

Orden lógico:

```text
validate config
↓
initialize TypeORM
↓
initialize repositories
↓
ScenarioState = normal
↓
start HTTP
```

---

# 75. Estado inicial

Cada API arranca con:

```text
scenario=normal.
```

No iniciar una clase accidentalmente en modo fallo.

---

# 76. Services

Se definen:

```text
UsersService
TeamsService
MissionsService
RankingService
ActivityService
HealthService
ScenarioService
LabRecoveryService
```

---

# 77. `RankingService`

Responsabilidad:

```text
solicitar ranking;
convertir error de dependencia;
emitir lab events;
devolver DTO.
```

No debe:

```text
conocer HTTP headers;
leer tokens;
controlar scenario directamente.
```

---

# 78. `ScenarioService`

Responsabilidad:

```text
get scenario;
set scenario mediante control autorizado.
```

No conoce:

```text
Docker;
container state;
api-down.
```

---

# 79. `LabRecoveryService`

Responsabilidad:

```text
si ranking-db-failure → normal;
si normal → no-op.
```

No:

```text
reset DB;
reiniciar API;
borrar logs.
```

---

# 80. Guards internos

Se utilizarán guards separados:

```text
ControlTokenGuard
RecoveryTokenGuard
```

No reutilizar auth del usuario web.

---

# 81. Rutas públicas vs internas

Gateway solo debe publicar:

```text
/api/*
```

No:

```text
/internal/*
```

---

# 82. Tests unitarios mínimos

```text
RankingService normal
RankingService dependency error
ScenarioService set/get
LabRecoveryService active
LabRecoveryService idempotent
Mission status mapping
DTO mapping
```

---

# 83. Tests de integración DB

Con PostgreSQL real de test:

```text
ranking order
current team flag
team response
mission state
activity order
score update visible
```

---

# 84. Tests E2E API

Estado normal:

```text
GET /api/health    200
GET /api/me        200
GET /api/team      200
GET /api/ranking   200
GET /api/missions  200
GET /api/activity  200
```

---

# 85. E2E del incidente

Activar internamente:

```text
ranking-db-failure
```

Validar:

```text
health   200
me       200
team     200
missions 200
activity 200
ranking  500
```

---

# 86. E2E de recover

Con incidente activo:

```text
POST recover
```

Después:

```text
ranking 200
```

y:

```text
score modificado previamente sigue igual.
```

---

# 87. E2E de tokens

Probar:

```text
sin token             → 401/403
token incorrecto      → 401/403
recovery en control   → denied
control en recovery   → denied
```

---

# 88. Test de sanitización

Provocar:
```text
RankingDependencyError
DB auth failure controlado en entorno test
validation error
```

Buscar en HTTP y lablogs:

```text
passwords
tokens
DATABASE_URL
```

Esperado:

```text
ninguno.
```

---

# 89. Test de correlación

Para request de ranking:

```text
X-Request-Id
```

debe coincidir con:

```text
requestId de lablogs.
```

---

# 90. Performance objetivo

Objetivo normal local:

```text
health < 200 ms
me/team/missions/activity < 500 ms
ranking < 500 ms
```

Se medirá durante implementación.

---

# 91. No caching agresivo

Para M4:

```text
UPDATE score
↓
GET /api/ranking
```

debe mostrar inmediatamente el valor nuevo.

No añadir:

```text
Redis;
ranking cache;
HTTP cache persistente.
```

---

# 92. Sin dependencias externas

Backend no llamará:

```text
APIs externas;
Internet;
CDNs;
SaaS.
```

durante flujo normal.

---

# 93. Decisiones cerradas del Bloque B

```text
API REST NestJS
puerto interno 3000
6 endpoints públicos
readiness interno
DTOs explícitos
request ID
repositorios concretos
ScenarioAwareRankingRepository
fault adapter determinista
scenario normal/ranking-db-failure
api-down fuera de la app
internal control API
control/recovery tokens separados
lablogs JSONL
technical logs separados
recover conserva datos y logs
Swagger no público
sin CORS wildcard
pool inicial 8
sin cache de ranking
```

---

# 94. Salida hacia Bloque C

El frontend deberá consumir exactamente:

```text
/api/me
/api/team
/api/ranking
/api/missions
/api/activity
```

y manejar el ranking de manera independiente para que un `500` no bloquee toda la aplicación.

---

# 95. Salida hacia Fase 5

Fase 5 utilizará:

```text
GET  /internal/lab/scenario
POST /internal/lab/scenario
POST /internal/lab/recover/ranking-db
```

`api-down` se implementará desde infraestructura.

---

# 96. Criterios de aceptación

```text
[x] módulos definidos
[x] endpoints definidos
[x] contratos JSON definidos
[x] DTO strategy definida
[x] repositories definidos
[x] ranking scenario-aware definido
[x] fault adapter definido
[x] internal control definido
[x] recover definido
[x] lablogs definidos
[x] sanitización definida
[x] request correlation definida
[x] config contract definido
[x] tests derivados
```

# BLOQUE B — DISEÑO COMPLETADO