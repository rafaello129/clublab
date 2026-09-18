# APP04 — Aplicación Integrada ClubLab
## Especificación funcional final de v1

**Estado:** FINAL DE DISEÑO  
**Fase:** 4 / Bloque D  
**Implementación:** pendiente  
**Entradas:** APP01 + APP02 + APP03 + D01 + D02 + D03

---

# 1. Producto

ClubLab v1 es un dashboard interno ficticio de un Club de Programación.

Su objetivo es permitir que un alumno descubra cómo se conecta:

```text
Browser
Frontend
HTTP
API
Backend
PostgreSQL
Server
Docker
Network
```

mediante una experiencia de investigación guiada.

---

# 2. Stack

Frontend:

```text
React
TypeScript
Vite
React Router
```

Backend:

```text
NestJS
TypeScript
Node.js 22
TypeORM
```

Datos:

```text
PostgreSQL 18
```

---

# 3. Pantallas

```text
/login
/dashboard
/ranking
/missions
/team
/activity
/profile
```

---

# 4. Dominio

```text
Team
User
Mission
Submission
Score
ActivityLog
```

Schemas:

```text
app
lab
```

---

# 5. Dato pedagógico central

```text
score del team local.
```

Seed:

```text
320 puntos
posición #3.
```

Ejemplo M4:

```text
380 puntos
posición #2.
```

---

# 6. API pública

```text
POST /api/auth/login
POST /api/auth/logout
GET  /api/auth/session

GET /api/health
GET /api/me
GET /api/team
GET /api/ranking
GET /api/missions
GET /api/activity
```

---

# 7. API interna

```text
GET  /internal/health/ready
GET  /internal/lab/scenario
POST /internal/lab/scenario
POST /internal/lab/recover/ranking-db
```

No publicada por gateway.

---

# 8. Auth

Modelo v1:

```text
runtime team credential
+
cookie firmada HttpOnly.
```

Config:

```text
APP_LOGIN_USERNAME
APP_LOGIN_PASSWORD_HASH
APP_LOGIN_USER_ID
APP_SESSION_SECRET
```

No hay tabla de passwords de usuario.

---

# 9. Sesión

Cookie:

```text
HttpOnly
SameSite=Lax
Path=/
TTL ~8h
```

No:

```text
localStorage token.
```

---

# 10. Lectura interna pedagógica

Para facilitar M2, los endpoints de lectura pueden responder dentro de la red interna del team sin cookie.

La API resuelve:

```text
APP_LOGIN_USER_ID
```

como identidad por defecto del entorno.

Esta decisión solo aplica al laboratorio aislado.

---

# 11. Ranking

Fuente:

```text
app.teams
JOIN
app.scores.
```

Posición:

```text
ROW_NUMBER()
ORDER BY score DESC, name ASC.
```

---

# 12. Superficie SQL pedagógica

```text
lab.my_team_score
```

Permite:

```text
SELECT
UPDATE(score)
```

solo del team local.

Implementación:

```text
INSTEAD OF UPDATE trigger.
```

---

# 13. M4

```sql
UPDATE lab.my_team_score
SET score = 380;
```

Debe reflejarse en:

```text
app.scores
/api/team
/api/ranking
Frontend.
```

---

# 14. Scenario principal

```text
ranking-db-failure
```

Solo afecta:

```text
RankingRepository.
```

Fault adapter:

```text
ENOTFOUND
database-broken:5432.
```

---

# 15. Contrato del incidente

```text
health    200
me        200
team      200
missions  200
activity  200
ranking   500.
```

---

# 16. UX del incidente

```text
Score visible
Misiones visibles
Actividad visible
Equipo visible
Ranking error
Posición no disponible.
```

No pantalla blanca.

---

# 17. Lablogs

Ruta:

```text
/var/log/clublab/lab-events.jsonl
```

Formato:

```text
JSONL.
```

API:

```text
RW.
```

Toolbox:

```text
RO.
```

---

# 18. Ejemplo de evidencia

```text
API       GET /api/ranking
RANKING   Loading ranking scores
DATABASE  Host database-broken could not be resolved
API       GET /api/ranking -> 500
```

---

# 19. Recover

```text
clublab recover ranking-db
```

produce:

```text
scenario → normal
ranking → 200.
```

Conserva:

```text
score modificado
session
lablogs.
```

---

# 20. Reset

```text
clublabctl reset teamXX
```

produce:

```text
DB seed
score 320
rank #3
scenario normal
lablogs limpios
grants restaurados.
```

---

# 21. api-down

No es scenario interno.

Fase 5:

```text
detiene contenedor API.
```

Frontend estático sigue disponible y muestra error de servicio.

---

# 22. Flujo M0–M8

```text
M0 → explorar UI
M1 → detectar /api/ranking
M2 → curl API
M3 → localizar score en DB
M4 → UPDATE score
M5 → identificar componentes
M6 → observar fallo parcial
M7 → diagnosticar con evidencia
M8 → reconstruir arquitectura.
```

Todos quedan cubiertos por el diseño.

---

# 23. Estado normal

```text
UI score             320
/api/team             320
/api/ranking local    320
app.scores            320
lab.my_team_score     320
rank                   #3
```

---

# 24. Estado M4

```text
UI score             380
/api/team             380
/api/ranking local    380
app.scores            380
lab.my_team_score     380
rank                   #2
```

---

# 25. Estado incidente

```text
score                  380
rank                   unavailable
/api/ranking           500
other API endpoints    200
DB real                healthy
```

---

# 26. Estado recover

```text
score                  380
rank                   #2
/api/ranking           200
scenario               normal
lablogs                preserved.
```

---

# 27. Estado reset

```text
score                  320
rank                   #3
scenario               normal
lablogs                empty.
```

---

# 28. Integración con seguridad

Debe respetar:

```text
roles owner/migrator/app/student
no secrets frontend
no internal endpoints published
DB no published
recovery/control tokens separados
student DB permissions limited
```

---

# 29. Integración con infraestructura

Por team:

```text
frontend
api
database
toolbox
```

Shared:

```text
clublab-gateway
clublabctl.
```

---

# 30. Test levels

```text
L1 Database
L2 API
L3 Frontend
L4 End-to-End.
```

---

# 31. E2E obligatorio

```text
normal
direct API
M4
incident
evidence
recover
reset
api-down
team isolation
auth isolation.
```

---

# 32. Ready checks

Un team solo es READY si:

```text
frontend OK
API health 200
API readiness 200
login OK
ranking 200
seed correct
lab view correct
scenario normal
lablogs writable.
```

---

# 33. Build

Backend:

```text
npm ci
npm run build
```

Frontend:

```text
npm ci
npm run build
```

Sin:

```text
latest
hardcoded secrets
runtime Internet dependency.
```

---

# 34. Limitaciones aceptadas

```text
single user identity per team
no registration
no password recovery
no pagination
no realtime
no Redis
no queues
scenario state initially in-memory.
```

---

# 35. Limitaciones no aceptadas

```text
global ranking failure
recover resets DB
public DB port
shared team DB
frontend white screen
hardcoded secrets
synchronize:true.
```

---

# 36. Definition of Done

```text
[ ] migrations
[ ] grants
[ ] deterministic seed
[ ] my_team_score
[ ] backend build
[ ] auth
[ ] public API
[ ] internal API
[ ] scenario
[ ] lablogs
[ ] frontend build
[ ] partial error UX
[ ] M0–M8 E2E
[ ] recover
[ ] reset
[ ] tests PASS
```

---

# 37. Estado de Fase 4

```text
APP01 Dominio y datos       ✅ Diseño
APP02 Backend y API         ✅ Diseño
APP03 Frontend y UX         ✅ Diseño
APP04 Integración           ✅ Diseño

Implementación              ⏳ Pendiente
```

# FASE 4 — DISEÑO COMPLETADO