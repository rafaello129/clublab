# ClubLab — Fase 4 / Bloque D
## Integración, validación y cierre de APP04

**Proyecto:** ClubLab v1  
**Fase:** 4 — Aplicación ClubLab  
**Bloque:** D  
**Estado:** DISEÑO INTEGRADO CERRADO — IMPLEMENTACIÓN PENDIENTE  
**Dependencias:** APP01 + APP02 + APP03 + D01 + D02 + D03  
**Entregable principal:** `APP04_Aplicacion_Integrada.md`

---

# 1. Propósito

Este bloque integra el dominio, backend y frontend en una sola especificación coherente.

La pregunta final de Fase 4 es:

> **¿Puede la aplicación completa ejecutar M0–M8 exactamente como se diseñaron, sin contradicciones entre UI, API, DB, auth, scenario y recovery?**

La validación de este bloque es de diseño.

La ejecución real quedará pendiente hasta que exista el código funcional.

---

# 2. Resultado esperado

La aplicación completa debe soportar:

```text
login
dashboard
ranking
missions
team
activity
profile
toolbox interaction
DB inspection
DB controlled update
partial incident
diagnosis
recover
reset
```

Sin depender de:

```text
Internet;
servicios externos;
datos reales;
credenciales productivas.
```

---

# 3. Arquitectura integrada

```text
Alumno
  │
  ▼
Browser
  │
  ▼
clublab-gateway
  │
  ├── /              → Frontend React
  ├── /api/*         → NestJS API
  └── /terminal/*    → Toolbox
                         │
                         ├── curl → API
                         └── psql → PostgreSQL

NestJS API
  │
  ├── UsersRepository
  ├── TeamsRepository
  ├── MissionsRepository
  ├── ActivityRepository
  └── ScenarioAwareRankingRepository
         │
         ├── normal → PostgreSQL
         └── ranking-db-failure → Fault Adapter
```

---

# 4. Flujo de autenticación integrado

Se incorpora formalmente al backend:

```text
POST /api/auth/login
GET  /api/auth/session
POST /api/auth/logout
```

Flujo:

```text
/login
  ↓
POST /api/auth/login
  ↓
Set-Cookie HttpOnly
  ↓
GET /api/auth/session
  ↓
/dashboard
```

La sesión pertenece únicamente a la API del team.

---

# 5. Endpoints públicos definitivos

Se congelan:

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

No habrá en v1:

```text
/api/dashboard
/api/admin
/api/scenario
```

públicos.

---

# 6. Endpoints internos definitivos

No publicados por gateway:

```text
GET  /internal/health/ready
GET  /internal/lab/scenario
POST /internal/lab/scenario
POST /internal/lab/recover/ranking-db
```

---

# 7. Contrato visual normal

Después de login:

```text
Dashboard
  Puntos: 320
  Posición: #3
  Misiones: 3/5

Ranking
  #1 Byte Benders      410
  #2 Runtime Rebels    355
  #3 Equipo local      320
  #4 Null Pointers     275
  #5 Stack Raiders     190
  #6 Syntax Syndicate  145
```

---

# 8. Contrato DB normal

Debe cumplirse:

```text
app.scores local = 320
lab.my_team_score = 320
/api/team score = 320
/api/ranking local score = 320
Frontend score = 320
```

---

# 9. Contrato M4

El alumno ejecuta:

```sql
UPDATE lab.my_team_score
SET score = 380;
```

Resultado esperado:

```text
UPDATE 1
```

Después:

```text
app.scores local = 380
/api/team score = 380
/api/ranking local score = 380
Frontend score = 380
posición = #2
```

---

# 10. Contrato recover

Si después de M4 se activa:

```text
ranking-db-failure
```

y luego el alumno ejecuta:

```bash
clublab recover ranking-db
```

debe ocurrir:

```text
scenario → normal
ranking vuelve
score sigue 380
posición sigue #2
lablogs siguen disponibles
```

Recover nunca equivale a reset.

---

# 11. Contrato reset

`clublabctl reset teamXX`:

```text
recrea DB
reaplica migrations
reaplica grants
reaplica seed
limpia lablogs
scenario → normal
```

Resultado:

```text
score → 320
posición → #3
```

---

# 12. Validación M0

## Objetivo

Explorar la aplicación sin conocer arquitectura.

## Debe encontrar

```text
usuario
team
score
ranking
missions
activity
```

## Criterio

Un alumno debe poder ubicar estos elementos en:

```text
5–6 minutos.
```

## Estado de diseño

```text
CUBIERTO.
```

---

# 13. Validación M1

## Acción

Abrir:

```text
DevTools → Network
```

y recargar Ranking.

## Debe observar

```text
GET /api/ranking
status 200
JSON legible
```

## No debe observar

```text
GraphQL
batch opaque
service worker interception
```

## Estado de diseño

```text
CUBIERTO.
```

---

# 14. Validación M2

Desde Toolbox:

```bash
curl http://api:3000/api/ranking
```

Debe devolver el mismo score.

Resultado esperado:

```text
320 antes de M4
380 después de M4
```

## Estado de diseño

```text
CUBIERTO.
```

---

# 15. Validación M3

Desde psql:

```text
\dt app.*
SELECT * FROM app.teams;
SELECT * FROM app.scores;
```

El alumno debe poder encontrar:

```text
team local
score local
```

sin acceso administrativo.

## Estado de diseño

```text
CUBIERTO.
```

---

# 16. Validación M4

Flujo:

```text
SELECT lab.my_team_score
↓
UPDATE score
↓
GET /api/team
↓
GET /api/ranking
↓
Frontend
```

Debe existir consistencia completa.

## Estado de diseño

```text
CUBIERTO.
```

---

# 17. Validación M5

`clublab status` debe reportar:

```text
frontend reachable
api reachable
database reachable
toolbox ready
```

La aplicación sigue funcionando sin conocer Docker.

## Estado de diseño

```text
CUBIERTO POR APP + REQUISITO FASE 5.
```

---

# 18. Validación M6

Activar:

```text
ranking-db-failure
```

Resultado:

```text
/api/health    200
/api/me        200
/api/team      200
/api/missions  200
/api/activity  200
/api/ranking   500
```

Frontend:

```text
score visible
missions visibles
activity visible
ranking error
posición no disponible
```

## Estado de diseño

```text
CUBIERTO.
```

---

# 19. Validación M7

Herramientas disponibles:

```text
DevTools
curl
clublab health
clublab status
psql
clublab logs api
```

Evidencia esperada:

```text
API viva
DB real viva
otros endpoints sanos
ranking 500
lablog muestra dependency resolution failure
```

La causa puede inferirse sin mostrar:

```text
scenario=ranking-db-failure
```

directamente.

## Estado de diseño

```text
CUBIERTO.
```

---

# 20. Validación M8

El sistema observado permite reconstruir:

```text
Browser
→ Frontend
→ API
→ PostgreSQL
```

y añadir:

```text
Server
Docker
containers
network
```

durante la explicación final.

## Estado de diseño

```text
CUBIERTO.
```

---

# 21. Matriz M0–M8

| Misión | UI | API | DB | Toolbox | Scenario | Estado |
|---|---:|---:|---:|---:|---:|---|
| M0 | Sí | Indirecta | No | No | No | Cubierta |
| M1 | Sí | Sí | No | No | No | Cubierta |
| M2 | No | Sí | No | Sí | No | Cubierta |
| M3 | No | Indirecta | Sí | Sí | No | Cubierta |
| M4 | Sí | Sí | Sí | Sí | No | Cubierta |
| M5 | Indirecta | Sí | Sí | Sí | No | Cubierta con F5 |
| M6 | Sí | Sí | Sí | Opcional | Sí | Cubierta |
| M7 | Sí | Sí | Sí | Sí | Sí | Cubierta |
| M8 | Sí | Sí | Sí | Sí | Sí | Cubierta |

---

# 22. Integridad de datos

Antes de declarar un entorno READY:

```text
6 teams
6 scores
5 missions
1 local team
local score = 320
local rank = 3
main user exists
environment_context points local
my_team_score returns 1 row
```

Cualquier incumplimiento:

```text
READY = false.
```

---

# 23. Integridad de API

Smoke test normal:

```text
auth login        204
auth session      200
health            200
me                200
team              200
ranking           200
missions          200
activity          200
```

---

# 24. Integridad del escenario

Con `ranking-db-failure`:

```text
ranking           500
health            200
me                200
team              200
missions          200
activity          200
readiness         200
```

Porque PostgreSQL real sigue sana.

---

# 25. Integridad de recovery

Después de recover:

```text
scenario          normal
ranking           200
score             preservado
lablogs           preservados
session           preservada
```

---

# 26. Integridad de reset

Después de reset:

```text
session/app creds siguen según generación
DB vuelve al seed
score 320
rank #3
lablogs vacíos
scenario normal
permissions recreados
```

---

# 27. Auth y aislamiento por team

Las credenciales de app:

```text
Team01
```

no deben autenticar en:

```text
Team02.
```

Se probará:

```text
login Team01 en Team02 → 401
```

---

# 28. Sesión y scenario

Activar un scenario:

```text
NO invalida la sesión.
```

Recover:

```text
NO invalida la sesión.
```

Reset:

```text
puede invalidar sesiones si session state depende de DB.
```

Para v1 se recomienda que el reset preserve o regenere una sesión simple de forma predecible.

---

# 29. Decisión de sesión para v1

Para simplificar reset, se elige:

> **sesión firmada stateless con cookie HttpOnly y secreto por team.**

La cookie contiene únicamente:

```text
userId
issuedAt
```

firmados.

No contiene:

```text
password
DB secrets
team secrets
```

---

# 30. Ventajas de sesión stateless

```text
no necesita tabla sessions;
reset de DB no añade otra tabla;
menos complejidad;
identity remains simple.
```

Después de reset:

```text
el userId seed vuelve a existir
```

porque los UUIDs del seed son deterministas.

Por tanto la sesión puede seguir siendo válida.

---

# 31. Password de app

El login no utilizará una tabla de passwords del dominio.

Para v1:

```text
APP_LOGIN_USERNAME
APP_LOGIN_PASSWORD_HASH
APP_LOGIN_USER_ID
```

se inyectan como configuración runtime por team.

Esto evita añadir:

```text
password_hash
```

a `app.users`.

---

# 32. Ajuste a configuración backend

Variables adicionales:

```text
APP_LOGIN_USERNAME
APP_LOGIN_PASSWORD_HASH
APP_LOGIN_USER_ID
APP_SESSION_SECRET
```

No se exponen al frontend.

---

# 33. Motivo

La autenticación de ClubLab es infraestructura pedagógica, no parte del dominio que queremos enseñar.

No necesitamos construir:

```text
registro
forgot password
user credential table
password reset.
```

---

# 34. Contrato de login final

```text
username
+
password
↓
validación contra runtime config
↓
cookie firmada HttpOnly
↓
userId seed
```

`CurrentUserResolver` extrae:

```text
userId
```

de la sesión.

---

# 35. Expiración

Sesión:

```text
duración suficiente para una clase
```

Propuesta:

```text
8 horas.
```

No hace falta refresh token.

---

# 36. Logout

Logout:

```text
borra cookie.
```

No necesita blacklist en v1.

---

# 37. Frontend y error auth

Si un request público protegido devuelve:

```text
401
```

el frontend:

```text
limpia estado auth
redirige /login.
```

No aplicar esto a:

```text
500 ranking.
```

---

# 38. Estado del ranking independiente

`RankingPage` y bloque ranking de Dashboard comparten:

```text
useRanking
```

pero deben poder:

```text
refetch
```

sin refrescar toda la app.

---

# 39. No single-point UI failure

No usar:

```text
Promise.all
```

de forma que un único rechazo impida renderizar todo el Dashboard.

Usar cargas independientes o:

```text
Promise.allSettled
```

si se agrupan.

---

# 40. Dashboard y datos independientes

Debe poder renderizar:

```text
team success
missions success
activity success
ranking fail
```

simultáneamente.

---

# 41. App shell offline-like

Aunque la API caiga:

```text
HTML/CSS/JS frontend
```

siguen disponibles porque el frontend es contenedor independiente.

Esto permite el fallback:

```text
api-down.
```

---

# 42. Contrato `api-down`

Con API detenida:

```text
Frontend asset shell → carga
/api/*                → 502/503/conexión fallida vía gateway
```

UX:

```text
banner de servicio
secciones de datos con error
sin pantalla blanca.
```

---

# 43. Lablogs y UI

Los lablogs:

```text
NO aparecen en frontend.
```

Solo:

```text
clublab logs api
```

desde toolbox.

Esto obliga a cambiar de herramienta durante M7.

---

# 44. Security contract

APP04 debe respetar D03:

```text
sin secrets en bundle
sin endpoints /internal publicados
sin DB ports públicos
sin app DB password en toolbox
session secret solo API
recovery token solo toolbox/API
control token instructor/API
```

---
# 45. Pruebas de integración obligatorias

Se definen cuatro niveles:

```text
L1 — Database
L2 — API
L3 — Frontend
L4 — End-to-End ClubLab
```

---

# 46. L1 — Database

Debe probar:

```text
migrations
seed
ranking query
my_team_score
UPDATE permitido
UPDATE prohibido
reset reproducible
```

---

# 47. L2 — API

Debe probar:

```text
auth
health
me
team
ranking
missions
activity
scenario
recover
sanitización
requestId
```

---

# 48. L3 — Frontend

Debe probar:

```text
login
routing
Dashboard normal
Ranking normal
Ranking error
partial failure
retry
logout
```

---

# 49. L4 — End-to-End

Debe ejecutar:

```text
normal
M4
scenario
diagnosis evidence
recover
reset
api-down fallback
```

con servicios reales.

---

# 50. E2E-01 — Normal

Pasos:

```text
1. login
2. dashboard
3. ranking
4. missions
5. team
6. activity
```

Esperado:

```text
score 320
rank #3
sin errores.
```

---

# 51. E2E-02 — Direct API

Desde toolbox:

```bash
curl http://api:3000/api/ranking
```

Esperado:

```text
200
320 local.
```

Auth de API deberá contemplar el uso pedagógico de curl.

---

# 52. Decisión: endpoints de lectura y curl

Para que M2 sea simple, se elige:

> **Los endpoints de lectura pedagógicos no exigirán sesión dentro de la red interna del team.**

Pero desde gateway/navegador la app sigue usando sesión.

La seguridad principal viene de:

```text
team network isolation
+
gateway
+
app login.
```

---

# 53. Aclaración de auth

Rutas:

```text
/api/me
/api/team
/api/ranking
/api/missions
/api/activity
```

podrán responder dentro del team sin cookie.

El CurrentUserResolver en ausencia de sesión usará:

```text
APP_LOGIN_USER_ID
```

solo porque cada API representa un único entorno.

---

# 54. Riesgo y justificación

Esto sería inapropiado para una app multiusuario productiva.

En ClubLab v1 es aceptable porque:

```text
1 API = 1 team
datos ficticios
red aislada
objetivo pedagógico M2
sin acceso directo desde LAN excepto gateway
```

Desde el gateway, la UI seguirá protegida por login a nivel de frontend/session flow.

---

# 55. Alternativa futura

Si posteriormente se quiere auth real en API pública:

```text
clublab curl
```

podría inyectar una credencial pedagógica.

No es necesario en v1.

---

# 56. E2E-03 — M4

Pasos:

```text
1. SELECT lab.my_team_score
2. UPDATE score 380
3. curl /api/ranking
4. reload UI
```

Esperado:

```text
380
#2.
```

---

# 57. E2E-04 — Incident

Activar:

```text
ranking-db-failure
```

Esperado:

```text
ranking 500
others 200
UI partial error.
```

---

# 58. E2E-05 — Evidence

Verificar:

```text
X-Request-Id
lablog same requestId
dependency error visible
no secret visible.
```

---

# 59. E2E-06 — Recover

Ejecutar:

```bash
clublab recover ranking-db
```

Luego:

```text
ranking 200
score 380
rank #2
session intact
lablogs intact.
```

---

# 60. E2E-07 — Reset

Ejecutar:

```text
clublabctl reset teamXX
```

Esperado:

```text
320
#3
scenario normal
lablogs empty
DB grants intact.
```

---

# 61. E2E-08 — api-down

Instructor detiene API.

Esperado:

```text
frontend shell available
data unavailable
global service warning
no white screen.
```

---

# 62. E2E-09 — Team isolation

Con dos stacks:

```text
M4 Team01
```

no cambia:

```text
Team02.
```

Scenario Team01:

```text
no cambia Team02.
```

---

# 63. E2E-10 — Auth isolation

```text
Team01 app credential
→ Team01 login success
→ Team02 login fail.
```

---

# 64. Datos que nunca deben divergir

En estado normal:

```text
/api/team.score
/api/ranking[current].score
app.scores.score
lab.my_team_score.score
Frontend score
```

deben coincidir.

---

# 65. Posición no almacenada

La posición:

```text
NO se guarda en DB.
```

Se deriva siempre del ranking.

Evita inconsistencias.

---

# 66. Mission progress

El frontend no guarda:

```text
completed count
```

como dato independiente.

Lo deriva de:

```text
/api/missions.
```

---

# 67. Build reproducible

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

Imágenes:

```text
versionadas
sin latest.
```

---

# 68. Configuración de clase

La imagen no debe contener:

```text
team password
DB password
session secret
control token
recovery token.
```

Todo se inyecta en runtime.

---

# 69. Preflight de aplicación

Antes de sesión:

```text
frontend responds
api health 200
api readiness 200
login works
ranking 200
seed correct
lab view correct
scenario normal
lablogs writable
```

---

# 70. Smoke test rápido

Objetivo:

```text
< 60 segundos por team automatizado.
```

Resultado:

```text
READY
o
FAILED.
```

---

# 71. Observabilidad mínima

Instructor debe poder distinguir:

```text
frontend failure
API failure
DB failure
scenario expected failure
auth failure.
```

Alumno solo ve lo necesario para la misión.

---

# 72. Performance funcional

Objetivos de diseño:

```text
UI usable sin esperas perceptibles
API normal < 500 ms
scenario activation inmediata
recover < pocos segundos
```

La carga real se valida después.

---

# 73. Compatibilidad

Browser objetivo:

```text
Chrome / Edge / Firefox modernos.
```

No soportar navegadores legacy.

---

# 74. Dependencia de Internet

La aplicación integrada debe funcionar con:

```text
Internet desconectado
```

si la LAN y servidor siguen disponibles.

---

# 75. Contrato de privacidad

Solo datos ficticios.

No guardar:

```text
nombre real del alumno
correo real
teléfono
tokens reales
actividad personal.
```

---

# 76. Deuda técnica aceptable

En v1 se acepta:

```text
single-user-per-team app identity
session simple
scenario store in-memory
no pagination
no Redis
no queue
no realtime
```

porque no afectan objetivos pedagógicos.

---

# 77. Deuda técnica no aceptable

No se acepta:

```text
hardcoded secrets
synchronize:true
public DB port
shared DB between teams
ranking failure global
recover that resets data
frontend white screen on 500
```

---

# 78. Criterio de implementación lista

APP04 podrá marcarse IMPLEMENTADA cuando:

```text
DB migrations funcionan
seeds funcionan
backend compila
frontend compila
auth funciona
M0–M8 funcionan
scenario funciona
recover funciona
reset funciona
tests principales pasan.
```

---

# 79. Criterio de Fase 4

Con este bloque:

```text
[A] Dominio + DB + seeds          ✅ Diseño
[B] Backend + API                 ✅ Diseño
[C] Frontend + UX                 ✅ Diseño
[D] Integración + validación      ✅ Diseño
```

# **FASE 4 — DISEÑO COMPLETADO**

La implementación real todavía está pendiente.

---

# 80. Próximo paso

La Fase 5 deberá construir la capa operativa que permita al instructor:

```text
deploy
status
scenario load
scenario clear
recover
reset
spare
preflight
audit
```

sobre la aplicación aquí definida.