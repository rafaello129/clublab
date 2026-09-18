# ClubLab — Fase 4 / Bloque C
## Frontend, UX y estados pedagógicos

**Proyecto:** ClubLab v1  
**Fase:** 4 — Aplicación ClubLab  
**Bloque:** C  
**Estado:** DISEÑO CERRADO v1 — IMPLEMENTACIÓN PENDIENTE  
**Dependencias:** D01 + D02 + D03 + APP01 + APP02  
**Entregable derivado:** `APP03_Frontend_ClubLab.md`

---

# 1. Propósito

Este bloque define la experiencia visual que utilizarán los alumnos durante ClubLab #01.

El frontend debe cumplir dos funciones al mismo tiempo:

```text
ser una aplicación creíble
+
hacer visible su arquitectura
```

No debe ocultar:

```text
requests;
estados de carga;
errores;
datos;
cambios de score.
```

Tampoco debe convertir la clase en una sesión de diseño UI.

---

# 2. Objetivos pedagógicos del frontend

Debe permitir:

```text
M0 → explorar una app realista
M1 → encontrar GET /api/ranking
M4 → observar cambio DB → API → UI
M6 → ver que solo ranking falla
M7 → comparar UI con Network/API
M8 → reconstruir las capas
```

La UI debe ayudar a observar, no resolver el diagnóstico por el alumno.

---

# 3. Stack cerrado

```text
React
TypeScript
Vite
React Router
```

Se utilizará:

```text
SPA
```

No se utilizará en v1:

```text
SSR
Next.js
PWA
Service Worker
GraphQL
Microfrontends
```

---

# 4. Librerías

Preferencia:

```text
React Router
fetch nativo o cliente HTTP mínimo
CSS Modules / CSS simple / Tailwind si se decide al implementar
```

No se necesita una librería compleja de estado global.

Estado remoto pequeño:

```text
useEffect + fetch
```

o una capa mínima propia.

La prioridad es que las requests sean transparentes en DevTools.

---

# 5. Auth de laboratorio

Se selecciona:

> **Sesión simple por cookie HttpOnly creada mediante login de laboratorio.**

Flujo:

```text
/login
→ POST /api/auth/login
→ cookie de sesión
→ aplicación
```

La sesión representa al usuario principal del team.

---

# 6. Por qué se añade login

Aunque el backend inicial no lo necesitaba para los endpoints de lectura, un login ligero aporta:

```text
sensación de aplicación real;
aislamiento de acceso entre gateway ports;
identidad de usuario;
mejor experiencia de inicio.
```

Pero debe ser breve:

```text
< 1 minuto para entrar.
```

No se construirá un sistema completo de auth empresarial.

---

# 7. Ajuste requerido en APP02

El backend deberá añadir:

```text
POST /api/auth/login
POST /api/auth/logout
GET  /api/auth/session
```

El resto de endpoints mantienen sus contratos.

Esto no cambia el flujo pedagógico principal.

---

# 8. Credenciales de login

Cada team tendrá credenciales propias de aplicación.

Ejemplo:

```text
usuario: avery
password: generado para teamXX
```

No reutilizar:

```text
terminal password
DB student password
recovery token.
```

---

# 9. Sesión

Cookie propuesta:

```text
HttpOnly
SameSite=Lax
Path=/
```

En LAN HTTP:

```text
Secure=false
```

En un futuro con HTTPS:

```text
Secure=true
```

No almacenar token de sesión en:

```text
localStorage.
```

---

# 10. Ruta inicial

```text
/login
```

Tras login:

```text
/dashboard
```

Si sesión no válida:

```text
redirect /login.
```

---

# 11. Navegación principal

Se congelan seis vistas:

```text
Dashboard
Ranking
Misiones
Equipo
Actividad
Perfil
```

Ruta:

```text
/dashboard
/ranking
/missions
/team
/activity
/profile
```

---

# 12. Shell de aplicación

Layout desktop:

```text
┌──────────────────────────────────────────────┐
│ Topbar                                       │
├─────────────┬────────────────────────────────┤
│ Sidebar     │ Content                        │
│             │                                │
│ Dashboard   │                                │
│ Ranking     │                                │
│ Misiones    │                                │
│ Equipo      │                                │
│ Actividad   │                                │
│ Perfil      │                                │
└─────────────┴────────────────────────────────┘
```

---

# 13. Topbar

Muestra:

```text
ClubLab
nombre de usuario
nombre del team
avatar
logout
```

No mostrar:

```text
Docker;
host;
scenario activo;
DB;
terminal.
```

La infraestructura debe seguir oculta al inicio.

---

# 14. Dashboard

Contenido:

```text
saludo;
score actual;
posición;
misiones completadas;
miembros del equipo;
actividad reciente;
acceso rápido al ranking.
```

---

# 15. Cards principales

Se congelan tres cards numéricas:

```text
Puntos
Posición
Misiones completadas
```

Ejemplo seed:

```text
Puntos              320
Posición             #3
Misiones completadas 3/5
```

---

# 16. Dato detonador

El dato:

```text
320 puntos
```

debe ser claramente visible en Dashboard.

Ese valor es la puerta de entrada pedagógica a:

```text
“¿de dónde salió?”
```

---

# 17. Fuente del score del Dashboard

El Dashboard no debe usar un valor hardcodeado.

Debe obtener el score desde:

```text
GET /api/team
```

La posición podrá obtenerse desde:

```text
GET /api/ranking
```

Esto permite que un fallo de ranking afecte solo la posición y ranking, no el score base del equipo.

---

# 18. Dashboard durante incidente

Durante `ranking-db-failure`:

```text
Puntos → sigue mostrando 320/valor modificado
Misiones → siguen visibles
Actividad → sigue visible
Miembros → siguen visibles
Posición → muestra “No disponible”
```

No bloquear todo el Dashboard.

---

# 19. Ranking

Tabla principal:

```text
Posición
Equipo
Puntos
```

La fila local se destaca visualmente mediante:

```text
badge “Tu equipo”
```

No depender únicamente de color.

---

# 20. Ranking normal

Ejemplo:

```text
1  Byte Benders      410
2  Runtime Rebels    355
3  Equipo 01         320   [Tu equipo]
4  Null Pointers     275
5  Stack Raiders     190
6  Syntax Syndicate  145
```

---

# 21. Ranking loading

Mientras carga:

```text
skeleton o indicador simple
```

No mantener loading artificial por varios segundos.

Objetivo:

```text
estado visible
sin perjudicar tiempos de clase.
```

---

# 22. Ranking error

Si:

```text
GET /api/ranking → 500
```

mostrar:

> **No se pudo cargar el ranking.**

Texto secundario:

> Vuelve a intentarlo en unos momentos.

Botón:

```text
Reintentar
```

No mostrar:

```text
ENOTFOUND
database-broken
500 stack
causa
solución.
```

---

# 23. Reintentar ranking

El botón:

```text
Reintentar
```

debe ejecutar una nueva:

```text
GET /api/ranking
```

Esto es útil después de:

```text
recover.
```

---

# 24. Misiones

Vista:

```text
lista/cards
```

Cada misión muestra:

```text
código
título
dificultad
puntos
estado
```

Estados visuales:

```text
Completada
En revisión
Rechazada
Disponible
```

---

# 25. Misiones durante incidente

La vista debe seguir:

```text
100% funcional
```

durante:

```text
ranking-db-failure.
```

Esto refuerza que el problema es parcial.

---

# 26. Equipo

Muestra:

```text
nombre;
descripción;
score;
integrantes.
```

Cada integrante:

```text
avatar;
display name;
role label.
```

---

# 27. Equipo y M3

Los nombres e identidad visibles deben coincidir con:

```text
app.teams
app.users
```

para que el alumno pueda relacionar fácilmente:

```text
UI ↔ SQL.
```

---

# 28. Actividad

Timeline sencillo.

Cada registro:

```text
icono
mensaje
actor
fecha/hora
```

Máximo visible inicial:

```text
8 eventos.
```

---

# 29. Perfil

Muestra:

```text
avatar
display name
username
role label
team
```

No editar perfil en v1.

No hay:

```text
upload
settings
preferences
password management.
```

---

# 30. Rutas y requests

Cada vista debe realizar requests reconocibles.

Ejemplo:

```text
/dashboard
  → /api/me
  → /api/team
  → /api/ranking
  → /api/missions
  → /api/activity
```

Esto hace visible una app compuesta por varias fuentes.

---

# 31. Evitar un único endpoint agregado

No usar:

```text
GET /api/dashboard
```

porque escondería la separación.

Queremos que en DevTools se vean varias requests independientes.

---

# 32. Request strategy

Se utilizará una capa pequeña:

```text
src/api/
```

Ejemplo:

```text
auth.api.ts
user.api.ts
team.api.ts
ranking.api.ts
missions.api.ts
activity.api.ts
```

No llamar `fetch` arbitrariamente desde cada componente visual.

---

# 33. Cliente HTTP

Wrapper mínimo:

```text
apiFetch()
```

Responsabilidades:

```text
base path;
credentials include;
JSON;
error normalizado;
request ID opcional.
```

No añadir:

```text
retries globales automáticos
```

porque pueden ocultar fallos en M6.

---

# 34. Retries

Default:

```text
0 retries automáticos.
```

El usuario decide:

```text
Reintentar.
```

Así Network muestra exactamente el comportamiento.

---

# 35. Caché

No utilizar caché persistente.

Estado en memoria únicamente.

Al recargar:

```text
nueva request.
```

Tras M4:

```text
refresh o refetch
→ valor nuevo visible.
```

---

# 36. DevTools friendly

No usar:

```text
Service Worker
IndexedDB para API data
GraphQL
batch requests
opaque proxy
```

Las llamadas deben verse como:

```text
/api/ranking
/api/team
/api/missions
```

---

# 37. Componentes principales

```text
AppShell
Sidebar
Topbar
StatCard
RankingTable
MissionCard
MissionStatusBadge
TeamMemberCard
ActivityItem
EmptyState
ErrorState
LoadingState
```

---

# 38. Componentes de página

```text
LoginPage
DashboardPage
RankingPage
MissionsPage
TeamPage
ActivityPage
ProfilePage
```

---

# 39. Hooks de datos

Se proponen hooks simples:

```text
useMe
useTeam
useRanking
useMissions
useActivity
```

Cada uno debe mantener:

```text
data
loading
error
refetch
```

No se necesita Redux.

---

# 40. Independencia de estados

Muy importante:

```text
useRanking error
```

no debe convertir:

```text
useTeam
useMissions
useActivity
```

en error.

Cada bloque mantiene su propio estado.

---

# 41. Dashboard composition

El Dashboard podrá usar:

```text
useMe
useTeam
useRanking
useMissions
useActivity
```

y renderizar cada sección independientemente.

---

# 42. Error boundary

Se añadirá:

```text
ErrorBoundary
```

para errores de render inesperados.

Pero:

```text
HTTP 500 de ranking
```

no debe activar el ErrorBoundary global.

Debe manejarse como estado normal de datos.

---

# 43. Estados vacíos

Aunque el seed normalmente tiene datos, definir:

```text
No hay actividad reciente
No hay misiones disponibles
```

Evitar pantallas rotas si alguna lista viene vacía.

---

# 44. Estado de API totalmente caída

Para escenario fallback `api-down`:

```text
frontend estático sigue cargando
```

pero las secciones de datos pueden mostrar:

```text
No pudimos conectar con el servicio.
```

Se debe distinguir visualmente de:

```text
ranking-only failure
```

sin explicar la causa.

---

# 45. Banner global API-down

Si múltiples requests críticas fallan por conexión:

```text
banner discreto:
“Hay problemas para obtener datos del servidor.”
```

No mostrar si solo ranking falla.

---

# 46. M6 — comportamiento exacto

Durante `ranking-db-failure`:

```text
Sidebar            OK
Topbar             OK
Perfil             OK
Equipo             OK
Misiones           OK
Actividad          OK
Score              OK
Ranking            ERROR
Posición Dashboard No disponible
```

Esto es contrato de UX.

---

# 47. M4 — actualización visual

Después de modificar:

```text
320 → 380
```

el alumno puede:

```text
recargar página
```

o usar:

```text
Reintentar/Actualizar
```

y observar:

```text
score 380
posición 2.
```

No añadir polling automático que haga desaparecer el momento de observación.
---

# 48. Polling

No habrá polling continuo.

Razón:

```text
reduce requests innecesarias;
facilita DevTools;
evita ruido;
hace M4 más deliberado.
```

---

# 49. Autorefresh

No usar:

```text
setInterval
```

para ranking.

La actualización ocurre por:

```text
mount
manual refetch
page reload.
```

---

# 50. Login page

Contenido:

```text
ClubLab
“Club de Programación”
usuario
contraseña
botón Entrar
```

No mencionar:

```text
Docker
API
database
arquitectura.
```

---

# 51. Error de login

Mensaje:

> Usuario o contraseña incorrectos.

No indicar:

```text
qué campo falló
si el usuario existe.
```

---

# 52. Sesión expirada

Si API devuelve:

```text
401
```

el cliente:

```text
redirige a /login
```

sin loops.

---

# 53. Logout

Botón logout:

```text
POST /api/auth/logout
```

después:

```text
/login.
```

---

# 54. Team-scoped auth

La sesión existe en:

```text
API propia del team.
```

Las credenciales de Team01:

```text
no deben funcionar en Team02.
```

Esta prueba queda heredada de D03.

---

# 55. Assets

Todos los assets:

```text
locales.
```

Avatares:

```text
SVG/PNG/WebP locales
o
initials generadas.
```

No depender de servicios externos.

---

# 56. Tipografía

Preferencia:

```text
system font stack
```

o fuente local incluida en build.

No depender de:

```text
Google Fonts.
```

---

# 57. Estilo visual

Dirección:

```text
dashboard tecnológico
limpio
sobrio
moderno
```

Evitar:

```text
estética hacker cliché;
terminales verdes decorativas;
glitch excesivo;
UI que sugiera respuestas.
```

La clase trata arquitectura, no estética de “hackeo”.

---

# 58. Jerarquía visual

Prioridad:

```text
datos
→ acciones
→ navegación
→ decoración.
```

El score y ranking deben ser fáciles de localizar.

---

# 59. Iconografía

Puede utilizarse una librería de iconos incluida en bundle.

No cargar iconos desde CDN.

Usar iconos como apoyo, no como única señal.

---

# 60. Colores

No se congelan colores exactos en este bloque.

Sí reglas:

```text
contraste suficiente;
error distinguible;
éxito distinguible;
estado no depende solo del color.
```

---

# 61. Responsive

Target principal:

```text
1366×768
1920×1080
laptops.
```

Mínimo usable:

```text
1024 px ancho.
```

Mobile:

```text
secundario.
```

---

# 62. Sidebar responsive

En pantallas pequeñas:

```text
sidebar colapsable.
```

Pero no priorizar mobile-first por encima del uso real de clase.

---

# 63. Accesibilidad

Mínimo:

```text
labels en forms;
focus visible;
aria-label donde haga falta;
tabla semántica;
botones reales;
mensajes de error textuales.
```

---

# 64. Tabla de ranking

Usar:

```text
<table>
```

semántica.

No recrear una tabla con:

```text
divs
```

sin necesidad.

---

# 65. Skeletons

Permitidos:

```text
dashboard cards
ranking
missions
activity
```

pero breves y simples.

---

# 66. Performance frontend

Objetivo:

```text
bundle pequeño;
sin librerías pesadas innecesarias;
render rápido.
```

No necesitamos:

```text
charts library
editor
drag-and-drop
animation engine pesado.
```

---

# 67. Animaciones

Solo:

```text
transiciones cortas;
hover/focus;
entrada sutil.
```

No animaciones que dificulten:

```text
capturas
DevTools
clase.
```

---

# 68. Estado local

Solo se utilizará para:

```text
UI;
formularios;
loading;
errores.
```

Los datos autoritativos siguen en:

```text
API/PostgreSQL.
```

---

# 69. No editar datos desde frontend

ClubLab v1 no expondrá una UI para cambiar el score.

M4 ocurre exclusivamente desde:

```text
PostgreSQL vía toolbox.
```

Esto es crucial.

Si la UI permitiera editar score:

```text
destruiría la intención de M4.
```

---

# 70. No botón “ver API”

No agregar atajos del tipo:

```text
Ver JSON
Abrir endpoint
Ver DB
```

porque harían el descubrimiento demasiado explícito.

---

# 71. No panel de arquitectura

No mostrar en la app:

```text
Frontend
API
Database
Container
```

antes de M8.

La arquitectura se descubre, no se presenta.

---

# 72. No console hints

No imprimir en Console:

```text
“Ranking comes from /api/ranking”
```

ni pistas deliberadas.

Console solo errores normales si aparecen.

---

# 73. Routing

Rutas públicas:

```text
/login
```

Rutas protegidas:

```text
/dashboard
/ranking
/missions
/team
/activity
/profile
```

Fallback:

```text
404 interna
→ volver al Dashboard.
```

---

# 74. Auth boot flow

Al iniciar:

```text
GET /api/auth/session
```

Estados:

```text
loading
authenticated
unauthenticated.
```

No renderizar brevemente contenido protegido antes de saber la sesión.

---

# 75. API wrapper — errores

Modelo:

```ts
type ApiError = {
  status: number;
  message: string;
  requestId?: string;
};
```

El request ID puede mostrarse discretamente en:

```text
detalle expandible de error
```

si se decide útil para instructor/alumno avanzado.

No necesario en primera vista.

---

# 76. Request ID en UI

Para el ranking error podría existir:

```text
“Código de referencia: abc123”
```

en texto secundario.

Esto permite relacionar:

```text
Network
↔ lablogs.
```

No revela la causa.

---

# 77. Recomendación para M7

Mantener el request ID visible en:

```text
respuesta Network
```

y opcionalmente en UI.

No depender de la UI para obtenerlo.

---

# 78. Dashboard normal

Wireframe conceptual:

```text
┌────────────────────────────────────────────┐
│ Hola, Avery                               │
│ Equipo 01                                 │
├────────────┬────────────┬──────────────────┤
│ 320 puntos │ #3 ranking │ 3/5 misiones    │
├────────────┴────────────┴──────────────────┤
│ Ranking rápido                            │
│ 1 Byte Benders ................. 410      │
│ 2 Runtime Rebels ............... 355      │
│ 3 Equipo 01 .................... 320      │
├─────────────────────┬──────────────────────┤
│ Misiones recientes  │ Actividad reciente  │
└─────────────────────┴──────────────────────┘
```

---

# 79. Dashboard incidente

```text
┌────────────────────────────────────────────┐
│ Hola, Avery                               │
│ Equipo 01                                 │
├────────────┬────────────┬──────────────────┤
│ 380 puntos │ -- ranking │ 3/5 misiones    │
├────────────┴────────────┴──────────────────┤
│ Ranking                                   │
│ No se pudo cargar el ranking. [Reintentar]│
├─────────────────────┬──────────────────────┤
│ Misiones OK         │ Actividad OK         │
└─────────────────────┴──────────────────────┘
```

El score modificado permanece visible.

---

# 80. Arquitectura frontend propuesta

```text
src/
├── app/
│   ├── router.tsx
│   └── App.tsx
│
├── api/
│   ├── client.ts
│   ├── auth.api.ts
│   ├── user.api.ts
│   ├── team.api.ts
│   ├── ranking.api.ts
│   ├── missions.api.ts
│   └── activity.api.ts
│
├── auth/
│   ├── AuthProvider.tsx
│   └── ProtectedRoute.tsx
│
├── components/
│   ├── layout/
│   ├── feedback/
│   ├── ranking/
│   ├── missions/
│   ├── team/
│   └── activity/
│
├── hooks/
│   ├── useMe.ts
│   ├── useTeam.ts
│   ├── useRanking.ts
│   ├── useMissions.ts
│   └── useActivity.ts
│
├── pages/
│   ├── LoginPage.tsx
│   ├── DashboardPage.tsx
│   ├── RankingPage.tsx
│   ├── MissionsPage.tsx
│   ├── TeamPage.tsx
│   ├── ActivityPage.tsx
│   └── ProfilePage.tsx
│
├── types/
└── styles/
```

---

# 81. No estado global complejo

No utilizar Redux/Zustand en v1 salvo que aparezca una necesidad concreta.

Los datos pueden vivir en:

```text
hooks
+
AuthProvider.
```

---

# 82. AuthProvider

Responsabilidades:

```text
session state;
login;
logout;
session bootstrap.
```

No guardar:

```text
DB credentials;
terminal credentials;
recovery token.
```

---

# 83. Datos del toolbox

El frontend nunca conoce:

```text
student DB password;
terminal password;
recovery token.
```

Esas credenciales viven fuera del bundle.

---

# 84. Build

Vite build:

```text
dist/
```

servido por:

```text
frontend container.
```

No runtime config con secretos.

---

# 85. Environment variables frontend

Solo valores públicos.

Ejemplo:

```text
VITE_APP_NAME=ClubLab
```

No:

```text
DB_PASSWORD
CONTROL_TOKEN
RECOVERY_TOKEN.
```

Idealmente API base:

```text
relativa /api
```

sin variable.

---

# 86. Source maps

Para la clase:

```text
opcional.
```

Preferencia inicial:

```text
deshabilitados en build de clase
```

porque no se necesitan para M0–M8 y evitan ruido.

En desarrollo:

```text
habilitados.
```

---

# 87. Tests unitarios frontend

Mínimos:

```text
RankingTable render
ranking current team badge
Mission status mapping/render
Ranking error state
Dashboard partial error
Auth redirect
```

---

# 88. Tests de integración UI

Con API mock/controlada:

```text
dashboard normal
ranking loading
ranking 500
missions stay visible
retry ranking
session expired.
```

---

# 89. E2E principal

Con backend real:

```text
login
dashboard 320/#3
ranking 320
missions
team
activity
profile.
```

---

# 90. E2E M4

Después de SQL update:

```text
reload
→ 380 puntos
→ posición #2.
```

---

# 91. E2E M6

Activar incidente:

```text
ranking error
```

mientras:

```text
team
missions
activity
profile
```

siguen utilizables.

---

# 92. E2E recover

Después:

```text
clublab recover ranking-db
```

usar:

```text
Reintentar
```

y verificar:

```text
ranking vuelve
score 380 sigue.
```

---

# 93. E2E api-down

Detener API.

Esperado:

```text
frontend shell carga;
datos fallan;
mensaje global de conexión;
sin pantalla blanca.
```

---

# 94. Definición de Done del Bloque C

```text
navegación clara;
login simple;
score visible;
ranking observable;
requests REST visibles;
error parcial correcto;
M4 visible;
no polling;
no shortcuts pedagógicos;
sin secrets;
offline-capable.
```

---

# 95. Ajustes requeridos a Backend

APP02 deberá incorporar:

```text
POST /api/auth/login
POST /api/auth/logout
GET  /api/auth/session
```

Además:

```text
CurrentUserResolver
```

usará la sesión.

No se cambia:

```text
ranking fault model;
lablogs;
scenario control;
recovery.
```

---

# 96. Contrato de Auth

## Login

```http
POST /api/auth/login
```

Body:

```json
{
  "username": "avery",
  "password": "..."
}
```

Success:

```text
204
+
Set-Cookie.
```

Invalid:

```text
401.
```

## Session

```http
GET /api/auth/session
```

```json
{
  "authenticated": true,
  "user": {
    "id": "uuid",
    "username": "avery"
  }
}
```

## Logout

```http
POST /api/auth/logout
```

```text
204.
```

---

# 97. Implementación auth preferida

Para v1:

```text
sesión firmada o session id server-side simple.
```

No construir:

```text
OAuth;
OIDC;
SSO;
refresh tokens.
```

La implementación definitiva se elegirá al codificar, respetando:
```text
HttpOnly;
team-scoped;
credenciales desechables.
```

---

# 98. Decisiones cerradas del Bloque C

### DC4-01
Frontend será SPA React + TypeScript + Vite.

### DC4-02
Habrá seis vistas principales más login.

### DC4-03
Desktop/laptop será target principal.

### DC4-04
Dashboard mostrará score, posición y progreso.

### DC4-05
Score será visible desde M0.

### DC4-06
Ranking tendrá tabla semántica y highlight del team local.

### DC4-07
Ranking tendrá loading/error/retry independientes.

### DC4-08
Un fallo de ranking no bloqueará otras vistas.

### DC4-09
No habrá `/api/dashboard`.

### DC4-10
No habrá retries automáticos globales.

### DC4-11
No habrá polling.

### DC4-12
No habrá cache persistente.

### DC4-13
M4 no tendrá UI de edición.

### DC4-14
No habrá panel de arquitectura ni pistas explícitas.

### DC4-15
No habrá Service Worker/PWA en v1.

### DC4-16
Assets serán locales.

### DC4-17
No habrá dependencias CDN obligatorias.

### DC4-18
Auth será sesión por cookie HttpOnly.

### DC4-19
Credenciales de app serán distintas por team.

### DC4-20
Frontend nunca recibirá DB/terminal/recovery secrets.

### DC4-21
Request ID podrá mostrarse como referencia de error.

### DC4-22
Source maps estarán deshabilitados en build de clase inicialmente.

---

# 99. Salida hacia Bloque D

La integración final deberá demostrar:

```text
login;
Dashboard;
Ranking;
Misiones;
Equipo;
Actividad;
Perfil;
M4;
M6;
recover;
api-down fallback.
```

Y, sobre todo:

```text
320 en UI
=
320 en API
=
320 en PostgreSQL

después:

380 en UI
=
380 en API
=
380 en PostgreSQL.
```

---

# 100. Criterios de aceptación

```text
[x] navegación definida
[x] rutas definidas
[x] Dashboard definido
[x] Ranking definido
[x] Misiones definidas
[x] Equipo definido
[x] Actividad definida
[x] Perfil definido
[x] auth definida
[x] estados loading definidos
[x] ranking error definido
[x] api-down UX definida
[x] data hooks definidos
[x] arquitectura frontend definida
[x] no polling definido
[x] no cache persistente
[x] no UI de score
[x] assets locales
[x] tests derivados
```

# BLOQUE C — DISEÑO COMPLETADO