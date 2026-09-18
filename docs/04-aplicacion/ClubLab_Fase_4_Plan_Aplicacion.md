# ClubLab — Plan de Fase 4
## Aplicación ClubLab

**Proyecto:** ClubLab v1  
**Fase:** 4  
**Nombre:** Aplicación, modelo de datos y experiencia funcional  
**Estado:** PLAN DE TRABAJO  
**Entradas principales:**  
- `D01_Diseno_Experiencia_ClubLab_01.md`
- `D02_Arquitectura_Tecnica_ClubLab.md`
- `D03_Seguridad_Aislamiento_ClubLab.md`

**Entregables principales:**  
- `APP01_Modelo_Dominio_y_Datos.md`
- `APP02_Backend_API.md`
- `APP03_Frontend_ClubLab.md`
- `APP04_Aplicacion_Integrada.md`

---

# 1. Propósito de la Fase 4

La Fase 4 construye la aplicación concreta que los alumnos investigarán durante ClubLab #01.

La pregunta principal será:

> **¿Qué aplicación debemos construir para que M0–M8 ocurran de forma natural, observable y reproducible?**

La aplicación no debe ser un “demo técnico vacío”.

Debe sentirse como un pequeño sistema real del club y contener suficiente información para que los alumnos puedan:

```text
explorar una interfaz;
seguir una request;
consultar una API;
encontrar datos en PostgreSQL;
modificar un dato;
observar servicios independientes;
diagnosticar un fallo;
reconstruir la arquitectura.
```

---

# 2. Alcance de la aplicación

La aplicación será un:

# **Dashboard interno del Club de Programación**

Contendrá como mínimo:

```text
Inicio / Dashboard
Perfil
Equipo
Ranking
Misiones
Actividad
```

Conceptualmente representará:

```text
participantes;
equipos;
misiones;
entregas;
puntos;
actividad.
```

No se construirá como producto comercial completo.

Se construirá específicamente para soportar la experiencia pedagógica diseñada en D01.

---

# 3. Principios de diseño

La aplicación debe ser:

```text
fácil de entender;
visualmente creíble;
pequeña;
con datos relacionados;
observable;
determinista;
rápida;
sin ruido funcional innecesario.
```

Evitar:

```text
chat complejo;
notificaciones push;
pagos;
roles empresariales;
microservicios;
módulos sin valor pedagógico;
CRUDs enormes.
```

---

# 4. Restricciones heredadas

La aplicación deberá respetar D02 y D03:

```text
React + TypeScript + Vite;
NestJS + TypeScript + Node 22;
PostgreSQL 18;
DB independiente por team;
API separada del frontend;
RankingRepository scenario-aware;
student DB role limitado;
lab.my_team_score;
logs pedagógicos;
health endpoint;
sin secrets en frontend;
sin credenciales administrativas en toolbox.
```

---

# 5. Flujo pedagógico que la app debe soportar

La aplicación debe permitir esta secuencia exacta:

```text
M0
Alumno explora dashboard.

M1
Observa GET /api/ranking.

M2
Consulta /api/ranking directamente.

M3
Encuentra el dato del ranking en PostgreSQL.

M4
Modifica su score mediante lab.my_team_score.

M5
Relaciona frontend/API/DB como servicios.

M6
Ranking falla y otras partes siguen funcionando.

M7
Diagnostica el flujo ranking → repository → data.

M8
Reconstruye arquitectura.
```

Si una decisión de producto dificulta este recorrido:

```text
se descarta.
```

---

# 6. División de la Fase 4

Para mantenerla manejable, se divide en solo **cuatro bloques**:

```text
BLOQUE A
Dominio + base de datos + seeds

BLOQUE B
Backend + API + logging + soporte de escenario

BLOQUE C
Frontend + UX + estados pedagógicos

BLOQUE D
Integración + pruebas + APP04 final
```

---

# BLOQUE A — Dominio, datos y seeds

# 7. Objetivo

Cerrar el modelo funcional antes de programar interfaces.

Debe definirse:

```text
entidades;
relaciones;
campos;
schema;
migrations;
vistas pedagógicas;
datos iniciales;
dataset por team.
```

---

# 8. Entidades mínimas propuestas

```text
User
Team
Mission
Submission
Score
ActivityLog
```

No añadir una entidad si no participa en:

```text
UI;
API;
misión pedagógica;
relación importante.
```

---

# 9. Modelo preliminar

## User

Campos:

```text
id
name
username
avatar
team_id
role_label
created_at
```

## Team

```text
id
name
slug
description
created_at
```

## Mission

```text
id
title
description
difficulty
points
status
created_at
```

## Submission

```text
id
user_id
mission_id
status
submitted_at
```

## Score

```text
id
team_id
score
updated_at
```

## ActivityLog

```text
id
team_id
user_id nullable
type
message
created_at
```

Los nombres finales se cerrarán en el Bloque A.

---

# 10. Relaciones principales

```text
Team 1 ─── N User

User 1 ─── N Submission

Mission 1 ─── N Submission

Team 1 ─── 1 Score

Team 1 ─── N ActivityLog
```

Estas relaciones deben ser suficientemente claras para M3.

---

# 11. Dato pedagógico principal

Se congela como dato principal:

```text
Team.score
```

o la entidad equivalente `Score.score`.

Debe aparecer en:

```text
Dashboard;
Ranking;
API;
DB;
vista lab.my_team_score.
```

Así será posible seguir exactamente el mismo valor extremo a extremo.

---

# 12. Datos secundarios

Para evitar que todo parezca artificial, también existirán:

```text
misiones completadas;
usuarios del equipo;
actividad reciente;
posición en ranking;
estado de entregas.
```

Pero el score será el dato central de M1–M4.

---

# 13. Seed determinista

Cada team tendrá un dataset conocido.

Ejemplo conceptual:

```text
Equipo del alumno → 320 pts
Byte Benders      → 410 pts
Null Pointers     → 275 pts
Stack Raiders     → 190 pts
```

No usar datos aleatorios durante una sesión.

La evidencia de los alumnos debe poder compararse con una respuesta esperada.

---

# 14. Personalización por entorno

El mismo seed template podrá parametrizar:

```text
TEAM_ID;
TEAM_NAME;
usuario principal;
score inicial;
posición inicial.
```

El resto del ranking puede ser ficticio pero estable.

---

# 15. `lab.my_team_score`

El Bloque A deberá implementar la superficie SQL definida en D03.

Debe permitir:

```text
SELECT
UPDATE(score)
```

del propio team.

No:

```text
UPDATE de otras filas;
UPDATE team_id;
DDL.
```

---

# 16. Migrations

Toda estructura se construirá mediante migrations versionadas.

No:

```text
editar DB manualmente para preparar clase.
```

Reset:

```text
migrations
→ permissions
→ seed
```

---

# 17. Salida del Bloque A

Debe quedar:

```text
modelo de dominio;
ERD;
schema SQL/ORM;
migrations;
seed strategy;
vista pedagógica;
dataset base.
```

Entregable:

```text
APP01_Modelo_Dominio_y_Datos.md
```

---

# BLOQUE B — Backend, API y observabilidad

# 18. Objetivo

Construir una API pequeña pero real que soporte toda la experiencia.

Debe implementar:

```text
endpoints;
servicios;
repositories;
health;
ranking;
perfil;
misiones;
actividad;
lab logging;
scenario-aware ranking.
```

---

# 19. Módulos backend propuestos

```text
HealthModule
UsersModule
TeamsModule
MissionsModule
RankingModule
ActivityModule
LabControlModule interno
```

No crear módulos vacíos solo por arquitectura.

---

# 20. Endpoints mínimos

```text
GET /api/health
GET /api/me
GET /api/team
GET /api/ranking
GET /api/missions
GET /api/activity
```

Opcionales si son útiles:

```text
GET /api/missions/:id
GET /api/users/:id
```

---

# 21. `/api/health`

Debe responder:

```json
{
  "status": "ok",
  "service": "api"
}
```

No debe depender del RankingRepository.

Durante el incidente:

```text
/api/health = 200
```

---

# 22. `/api/ranking`

Debe:

```text
consultar datos reales;
ordenar equipos;
devolver score;
incluir posición.
```

Este endpoint será el centro de:

```text
M1
M2
M6
M7
```

---

# 23. `/api/me`

Debe devolver el usuario principal del entorno.

Ejemplo conceptual:

```json
{
  "id": "...",
  "name": "Rafael",
  "team": {
    "id": "...",
    "name": "Equipo 01"
  }
}
```

Los datos reales del usuario de ChatGPT no se utilizarán; serán identidades ficticias o configurables de laboratorio.

---

# 24. `/api/missions`

Debe seguir funcionando durante:

```text
ranking-db-failure.
```

Esto será una prueba del fallo parcial.

---

# 25. `/api/activity`

Proporcionará actividad reciente para dar vida al dashboard.

Ejemplo:

```text
“Misión API Explorer completada”
“Equipo obtuvo 20 puntos”
“Nueva entrega registrada”
```

No requiere sistema de eventos complejo.

---

# 26. Arquitectura backend

Estructura esperada:

```text
Controller
   ↓
Service
   ↓
Repository
   ↓
PostgreSQL
```

El alumno no necesita conocer estas capas al principio, pero M7 podrá apoyarse en ellas.

---

# 27. RankingRepository

Deberá tener una abstracción clara.

Conceptualmente:

```ts
interface RankingRepository {
  getRanking(): Promise<RankingEntry[]>
}
```

Implementación normal:

```text
PostgresRankingRepository
```

---

# 28. Scenario-aware behavior

El flujo de ranking incorporará una capa pequeña:

```text
RankingService
      │
      ▼
ScenarioAwareRankingRepository
      │
      ├── normal
      │    ↓
      │  PostgreSQL
      │
      └── ranking-db-failure
           ↓
         error creíble
```

No debe afectar los demás repositories.

---

# 29. LabControl interno

Debe existir un mecanismo interno para:

```text
leer scenario state;
recover ranking-db.
```

No formará parte de la API pública mostrada en Swagger/documentación de alumno si eso revela demasiado.

---

# 30. Logging pedagógico

La API debe emitir eventos simples:

```text
API
RANKING
DATABASE
SYSTEM
```

Formato conceptual:

```text
timestamp
layer
action
result
detail
```

Ejemplo:

```text
20:14:03 API       GET /api/ranking
20:14:03 RANKING   fetching scores
20:14:03 DATABASE  connection failed
20:14:03 API       /api/ranking -> 500
```

---

# 31. Sanitización

No loggear:

```text
passwords;
DATABASE_URL completa;
tokens;
Authorization;
cookies;
stack traces sensibles en lablogs.
```

---

# 32. Errores HTTP

Cliente:

```text
error genérico.
```

Logs instructor:

```text
detalle suficiente.
```

Lablogs alumno:

```text
detalle pedagógico.
```

Tres niveles distintos.

---

# 33. Validación backend

Bloque B deberá incluir tests de:

```text
health 200;
ranking 200;
missions 200;
scenario ranking failure 500;
health sigue 200;
missions sigue 200;
recover vuelve ranking a 200;
logs correctos;
sin secrets.
```

Entregable:

```text
APP02_Backend_API.md
```

---

# BLOQUE C — Frontend y experiencia del alumno

# 34. Objetivo

Construir una interfaz suficientemente buena para sentirse como una aplicación real, pero diseñada para la investigación.

La interfaz debe favorecer:

```text
exploración;
datos visibles;
requests claras;
estados de error comprensibles.
```

---

# 35. Navegación principal

Propuesta:

```text
Dashboard
Ranking
Misiones
Equipo
Actividad
Perfil
```

Puede utilizar:

```text
sidebar
o
navbar.
```

La prioridad será claridad.

---

# 36. Dashboard

Debe mostrar al menos:

```text
nombre del usuario;
equipo;
puntos;
posición;
misiones completadas;
actividad reciente.
```

El score debe ser visible desde el primer minuto.

---

# 37. Ranking

Debe mostrar:

```text
posición;
equipo;
puntos.
```

La fila del equipo actual debe ser reconocible.

El dato visible debe coincidir exactamente con:

```text
/api/ranking
PostgreSQL
lab.my_team_score
```

---

# 38. Estado normal del ranking

Ejemplo:

```text
#1 Byte Benders       410
#2 Equipo 01          320
#3 Null Pointers      275
#4 Stack Raiders      190
```

---

# 39. Estado de carga

Debe existir un loading perceptible pero breve.

No usar un comportamiento que impida observar correctamente la request en DevTools.

---

# 40. Estado de error

Cuando `/api/ranking` devuelve 500:

```text
el resto de la aplicación sigue funcionando.
```

El ranking mostrará:

> **No se pudo cargar el ranking. Intenta nuevamente.**

No mostrar:

```text
DB_HOST;
ENOTFOUND;
stack trace;
solución.
```

---

# 41. Misiones

Vista simple:

```text
título;
dificultad;
puntos;
estado.
```

Debe seguir cargando durante el incidente.

Así el alumno puede comprobar que:

```text
API != totalmente caída.
```

---

# 42. Equipo

Muestra:

```text
nombre del team;
integrantes;
score;
misiones.
```

Ayuda a relacionar IDs y datos en M3.

---

# 43. Actividad

Lista cronológica:

```text
evento;
usuario/equipo;
fecha/hora.
```

Sirve para reforzar la sensación de sistema real.

---

# 44. Perfil

Debe ser pequeño.

No crear:

```text
editor complejo;
upload real;
settings extensas.
```

Solo información suficiente para M0.

---

# 45. Manejo de requests

Frontend usará:

```text
/api/...
```

rutas relativas.

Las requests deben ser fáciles de reconocer en Network.

Evitar:

```text
GraphQL;
batching;
requests opacas;
SDK complejo.
```

REST explícito es mejor para esta clase.

---

# 46. Caché
Durante ClubLab #01 se evitará caching agresivo que confunda M4.

Después del UPDATE y refresh:

```text
el nuevo score debe observarse inmediatamente.
```

Si se usa una librería de fetching:

```text
revalidación clara.
```

---

# 47. Auth de aplicación

La app necesita una identidad por team, pero no un sistema empresarial.

Opciones a evaluar:

```text
sesión simple;
login preconfigurado;
token de laboratorio.
```

Criterio:

```text
rápido para clase;
team-scoped;
sin credenciales cross-team;
sin distraer de la arquitectura.
```

Se cerrará durante el Bloque C.

---

# 48. UX para DevTools

No ocultar requests mediante:

```text
Service Worker;
PWA cache;
offline proxy;
SSR complejo.
```

La primera versión será:

```text
SPA simple.
```

Esto facilita M1.

---

# 49. Diseño visual

Objetivo:

```text
profesional;
limpio;
tecnológico;
no sobrecargado.
```

No convertir Fase 4 en un proyecto de diseño visual de semanas.

El valor principal es:

```text
claridad pedagógica.
```

---

# 50. Responsive

Debe funcionar correctamente en:

```text
laptop.
```

Mobile:

```text
deseable
pero no prioridad.
```

La clase está diseñada alrededor de DevTools y terminal.

---

# 51. Accesibilidad mínima

Aplicar:

```text
labels;
contraste suficiente;
navegación clara;
estados no dependientes solo de color;
focus visible.
```

---

# 52. Salida del Bloque C

Debe quedar:

```text
mapa de pantallas;
componentes principales;
estados normal/loading/error;
integración con API;
flujo M0/M1/M4/M6;
auth de laboratorio.
```

Entregable:

```text
APP03_Frontend_ClubLab.md
```

---

# BLOQUE D — Integración, validación y APP04

# 53. Objetivo

Probar la aplicación completa como experiencia ClubLab, no únicamente como software.

Debe validarse:

```text
frontend;
API;
DB;
seeds;
vista SQL;
logs;
scenario;
recover;
reset;
requests;
estados de UI.
```

---

# 54. Prueba M0

Verificar que un alumno sin explicación pueda encontrar:

```text
equipo;
score;
ranking;
misiones;
actividad.
```

Objetivo:

```text
< 6 min.
```

---

# 55. Prueba M1

DevTools debe mostrar de forma clara:

```text
GET /api/ranking
200
```

y JSON comprensible.

No debe requerir descifrar:

```text
GraphQL;
minified payloads;
batches.
```

---

# 56. Prueba M2

Desde toolbox:

```bash
curl http://api:3000/api/ranking
```

debe producir el mismo dato visible.

---

# 57. Prueba M3

Como student:

```text
\dt
\d
SELECT
```

debe ser suficiente para encontrar el score.

El schema no debe ser deliberadamente laberíntico.

---

# 58. Prueba M4

Flujo:

```text
SELECT lab.my_team_score
↓
UPDATE score
↓
GET /api/ranking
↓
refresh frontend
```

El nuevo valor debe coincidir en todos los niveles.

---

# 59. Prueba M5

`clublab status` debe encontrar:

```text
frontend;
api;
database;
toolbox.
```

La aplicación no necesita conocer Docker para funcionar.

---

# 60. Prueba M6

Activar:

```text
ranking-db-failure
```

Esperado:

```text
Dashboard parcial usable;
Misiones usable;
Perfil usable;
/api/health 200;
/api/ranking 500;
ranking UI error.
```

---

# 61. Prueba M7

Debe existir evidencia suficiente para llegar a la causa mediante:

```text
Network;
curl;
health;
psql;
lablogs.
```

Sin que una sola herramienta diga directamente:

```text
“la respuesta es X”.
```

---

# 62. Prueba Recover

Ejecutar:

```bash
clublab recover ranking-db
```

y validar:

```text
ranking vuelve 200;
UI vuelve;
score modificado en M4 se conserva.
```

Esto último es importante:

```text
recover ≠ reset.
```

---

# 63. Prueba Reset

Después:

```text
clublabctl reset teamXX
```

validar:

```text
score vuelve al seed;
logs limpios;
scenario normal;
app funcional.
```

---

# 64. Pruebas automáticas

Se deberán crear:

```text
unit tests;
integration tests;
API tests;
DB permission tests;
scenario tests.
```

E2E mínimo:

```text
normal flow;
ranking failure;
recover;
reset.
```

---

# 65. Dataset integrity test

El build/seed debe comprobar:

```text
usuario existe;
team existe;
score existe;
ranking tiene varias filas;
misiones existen;
actividad existe.
```

No arrancar una clase con seed incompleto.

---

# 66. Rendimiento

No se busca benchmarking extremo.

Objetivos prácticos:

```text
pantalla carga rápidamente;
API responde en <1s normalmente;
reset no tarda demasiado;
6 teams no saturan host.
```

Los valores reales se medirán después.

---

# 67. Definition of Done de aplicación

La app está lista cuando:

```text
M0–M8 pueden ejecutarse;
normal/recover/reset funcionan;
dataset es determinista;
errores son claros;
logs son útiles;
security contract D03 se respeta;
builds son reproducibles.
```

---

# 68. Entregable APP04

`APP04_Aplicacion_Integrada.md` documentará:

```text
stack;
pantallas;
modelo;
endpoints;
schema;
seeds;
scenario hooks;
logs;
tests;
build;
known limitations.
```

Además deberá existir el código fuente funcional.

---

# 69. Estructura de trabajo

```text
BLOQUE A
Dominio + DB + seeds
      ↓
BLOQUE B
Backend + API
      ↓
BLOQUE C
Frontend + UX
      ↓
BLOQUE D
Integración + APP04
```

Solo cuatro bloques.

---

# 70. Qué NO pertenece a Fase 4

No implementar todavía completamente:

```text
clublabctl final;
orquestador de escenarios completo;
manual del instructor;
tarjetas de roles;
cuaderno del alumno;
automatización de despliegue completa.
```

La aplicación sí debe incluir los hooks necesarios para que Fase 5 pueda controlarla.

---

# 71. Interfaces con Fase 5

Fase 4 deberá entregar a Fase 5:

```text
scenario state contract;
recover endpoint interno;
RankingRepository hook;
health contract;
lablog format;
seed/reset requirements.
```

Fase 5 construirá el orquestador alrededor de eso.

---

# 72. Interfaces con Fase 3

Antes de aceptar APP04:

```text
no secrets frontend;
DB roles correctos;
student view correcta;
runtime users definidos;
error sanitization;
scenario endpoint interno.
```

D03 es contrato obligatorio.

---

# 73. Riesgos principales

## R4-01 — App demasiado grande

Mitigación:

```text
solo features necesarias para M0–M8.
```

## R4-02 — DB demasiado simple

Mitigación:

```text
relaciones reales pero comprensibles.
```

## R4-03 — DB demasiado compleja

Mitigación:

```text
6 entidades principales;
nombres claros;
vista pedagógica.
```

## R4-04 — Frontend oculta requests

Mitigación:

```text
SPA REST simple;
sin service worker.
```

## R4-05 — Incident hook se siente falso

Mitigación:

```text
error coherente;
logs reales;
repository scoped.
```

## R4-06 — Recover pierde cambios

Mitigación:

```text
scenario state separado de DB data.
```

---

# 74. Decisiones que deben salir cerradas

Al terminar Fase 4 debe existir respuesta concreta para:

```text
¿qué entidades existen?
¿qué campos tienen?
¿cómo se relacionan?
¿qué dato rastrea el alumno?
¿qué endpoints existen?
¿qué devuelve cada uno?
¿qué pantallas existen?
¿cómo se ve un fallo?
¿cómo se genera el seed?
¿cómo funciona RankingRepository?
¿cómo emite lablogs?
¿cómo se conserva el score tras recover?
```

---

# 75. Criterios de éxito de Fase 4

```text
[ ] modelo de dominio definido
[ ] ERD definido
[ ] migrations creadas
[ ] seeds creados
[ ] lab.my_team_score implementada
[ ] API funcional
[ ] health funcional
[ ] ranking funcional
[ ] missions/me/activity funcionales
[ ] fault hook implementado
[ ] lablogs implementados
[ ] frontend funcional
[ ] ranking error state funcional
[ ] app auth team-scoped
[ ] M0–M8 validadas contra app
[ ] recover conserva datos
[ ] reset vuelve al seed
[ ] tests principales pasan
[ ] APP04 consolidado
```

---

# 76. Primer bloque a desarrollar

# BLOQUE A — Dominio + base de datos + seeds

El siguiente trabajo será cerrar:

```text
entidades;
campos;
relaciones;
ERD;
schema;
migrations;
seed determinista;
lab.my_team_score;
dataset exacto para las misiones.
```

No empezaremos por componentes React.

Primero debemos saber exactamente qué sistema estamos representando y qué dato seguirá el alumno desde la UI hasta PostgreSQL.