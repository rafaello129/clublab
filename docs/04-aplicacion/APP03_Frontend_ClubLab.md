# APP03 — Frontend ClubLab
## UX y experiencia funcional

**Estado:** FINAL DE DISEÑO  
**Fase:** 4 / Bloque C  
**Implementación:** pendiente  
**Dependencias:** APP01 + APP02 + D01 + D03

---

# 1. Stack

```text
React
TypeScript
Vite
React Router
SPA
```

Sin:

```text
SSR
PWA
Service Worker
GraphQL
polling
cache persistente.
```

---

# 2. Pantallas

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

# 3. Dashboard

Muestra:

```text
usuario;
team;
score;
posición;
misiones completadas;
ranking rápido;
actividad reciente.
```

Seed:

```text
320 puntos
posición #3
3/5 misiones.
```

El score debe ser visible inmediatamente.

---

# 4. Ranking

Columnas:

```text
Posición
Equipo
Puntos
```

El equipo actual muestra:

```text
Tu equipo.
```

---

# 5. Ranking error

Durante:

```text
ranking-db-failure
```

mostrar:

> No se pudo cargar el ranking.

Acción:

```text
Reintentar.
```

No revelar causa técnica.

---

# 6. Comportamiento parcial

Durante el incidente:

```text
Perfil     OK
Equipo     OK
Misiones   OK
Actividad  OK
Score      OK
Ranking    ERROR
Posición   No disponible
```

---

# 7. Misiones

Cada card:

```text
código
título
dificultad
puntos
estado.
```

Estados:

```text
Completada
En revisión
Rechazada
Disponible
```

---

# 8. Equipo

Muestra:

```text
nombre;
descripción;
score;
miembros.
```

Los datos coinciden con PostgreSQL.

---

# 9. Actividad

Timeline con:

```text
mensaje
actor
timestamp.
```

Hasta 8 eventos iniciales.

---

# 10. Perfil

Muestra:

```text
avatar
display name
username
role label
team.
```

Sin edición en v1.

---

# 11. Requests visibles

Dashboard realiza requests independientes:

```text
/api/me
/api/team
/api/ranking
/api/missions
/api/activity
```

No existe:

```text
/api/dashboard.
```

---

# 12. Fetching

Capa:

```text
src/api/
```

Wrapper:

```text
apiFetch()
```

Default:

```text
0 retries automáticos.
```

Sin polling.

---

# 13. Hooks

```text
useMe
useTeam
useRanking
useMissions
useActivity
```

Cada uno:

```text
data
loading
error
refetch.
```

Errores independientes.

---

# 14. M4

La UI no permite editar score.

El alumno actualiza desde PostgreSQL:

```sql
UPDATE lab.my_team_score
SET score = 380;
```

Después de reload/refetch:

```text
320 → 380
#3 → #2.
```

---

# 15. M6

Ranking 500:

```text
solo Ranking y posición fallan.
```

La aplicación no queda en pantalla blanca.

---

# 16. api-down

Frontend estático sigue cargando.

Datos muestran:

> Hay problemas para obtener datos del servidor.

No confundir con error exclusivo de ranking.

---

# 17. Login

Auth v1:

```text
usuario/password del team
+
cookie HttpOnly.
```

Endpoints requeridos:

```text
POST /api/auth/login
GET  /api/auth/session
POST /api/auth/logout
```

---

# 18. Sesión

Cookie:

```text
HttpOnly
SameSite=Lax
Path=/
```

En LAN HTTP:

```text
Secure=false.
```

Con HTTPS futuro:

```text
Secure=true.
```

No localStorage para auth.

---

# 19. Credenciales

App login:

```text
diferente por team.
```

No reutiliza:

```text
terminal password;
DB student password;
recovery token.
```

---

# 20. Estructura frontend

```text
src/
├── app/
├── api/
├── auth/
├── components/
├── hooks/
├── pages/
├── types/
└── styles/
```

---

# 21. Componentes

```text
AppShell
Sidebar
Topbar
StatCard
RankingTable
MissionCard
TeamMemberCard
ActivityItem
LoadingState
ErrorState
EmptyState
```

---

# 22. UX pedagógica

No incluir:

```text
botón Ver API;
botón Ver DB;
panel de arquitectura;
hints en Console;
editor de score.
```

El descubrimiento debe venir de:

```text
observación
+
DevTools
+
toolbox.
```

---

# 23. Assets

Todos locales.

No depender de:

```text
Google Fonts;
CDNs;
servicios de avatar;
Internet.
```

---

# 24. Responsive

Prioridad:

```text
laptop / desktop.
```

Objetivo:

```text
1024px+ usable.
```

Mobile secundario.

---

# 25. Accesibilidad

```text
forms con label;
focus visible;
tabla semántica;
error textual;
estado no dependiente solo de color.
```

---

# 26. Performance

No librerías pesadas innecesarias.

No:

```text
charts
drag-and-drop
animation engine
editor.
```

---

# 27. Build

```text
vite build
→ dist/
```

Servido como archivos estáticos.

Frontend no contiene:

```text
DB credentials;
control token;
recovery token;
terminal credentials.
```

---

# 28. Tests

Unit:

```text
RankingTable
Mission states
Ranking error
Dashboard partial error
Auth redirect.
```

E2E:

```text
login
normal flow
M4
ranking failure
recover
api-down.
```

---

# 29. Contrato visual central

Normal:

```text
Score 320
Posición #3
Ranking visible.
```

Después M4:

```text
Score 380
Posición #2.
```

Incidente:

```text
Score 380
Posición no disponible
Ranking error
resto funcional.
```

Recover:

```text
Score 380
Posición #2
Ranking visible nuevamente.
```

Reset:

```text
Score 320
Posición #3.
```

---

# 30. Definition of Done

```text
[ ] login
[ ] dashboard
[ ] ranking
[ ] missions
[ ] team
[ ] activity
[ ] profile
[ ] loading states
[ ] partial error
[ ] retry
[ ] session handling
[ ] no polling
[ ] no persistent cache
[ ] offline assets
[ ] E2E principal
```

---

# 31. Estado

```text
UX CONTRACT        ✅
ROUTES             ✅
SCREENS            ✅
AUTH MODEL         ✅
ERROR STATES       ✅
DATA FLOW          ✅
PEDAGOGICAL RULES  ✅

CÓDIGO             ⏳
TESTS              ⏳
INTEGRACIÓN        ⏳
```

# APP03 — DISEÑO COMPLETADO