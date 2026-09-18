# ClubLab — Fase 4 / Bloque A
## Dominio, base de datos y seeds

**Proyecto:** ClubLab v1  
**Fase:** 4 — Aplicación ClubLab  
**Bloque:** A  
**Estado:** DISEÑO CERRADO v1 — IMPLEMENTACIÓN PENDIENTE  
**Dependencias:** D01 + D02 + D03 + Plan Fase 4  
**Entregable derivado:** `APP01_Modelo_Dominio_y_Datos.md`

---

# 1. Propósito

Este bloque define exactamente qué sistema representa ClubLab, qué información contiene y qué dato seguirá el alumno desde la interfaz hasta PostgreSQL.

La aplicación será un:

# **Dashboard interno del Club de Programación**

y no un CRUD genérico.

Debe ser suficientemente real para que el alumno encuentre:

```text
usuarios;
equipos;
misiones;
entregas;
puntos;
actividad;
relaciones entre tablas.
```

pero suficientemente pequeño para poder comprenderlo durante una clase de 120 minutos.

---

# 2. Regla de diseño

El modelo de datos se diseña alrededor de la experiencia pedagógica.

No se añade una tabla únicamente porque:

```text
“una aplicación real podría necesitarla”.
```

Una entidad entra en v1 solo si:

```text
aparece en UI;
aparece en API;
sirve para una misión;
o hace comprensible una relación importante.
```

---

# 3. Entidades definitivas de v1

Se congelan seis entidades funcionales:

```text
Team
User
Mission
Submission
Score
ActivityLog
```

Además existirá un objeto técnico dentro de `lab`:

```text
EnvironmentContext
```

Su función será identificar qué equipo representa ese entorno aislado.

---

# 4. Relación conceptual

```text
Team
 ├── Users
 ├── Score
 └── ActivityLogs

User
 └── Submissions

Mission
 └── Submissions
```

El ranking se obtiene de:

```text
Team + Score
```

No habrá una tabla `ranking`.

El ranking será una consulta derivada.

---

# 5. ERD

```mermaid
erDiagram
    TEAM ||--o{ USER : has
    TEAM ||--|| SCORE : owns
    TEAM ||--o{ ACTIVITY_LOG : generates
    USER ||--o{ SUBMISSION : creates
    USER ||--o{ ACTIVITY_LOG : may_trigger
    MISSION ||--o{ SUBMISSION : receives

    TEAM {
        uuid id PK
        varchar slug UK
        varchar name
        text description
        timestamptz created_at
    }

    USER {
        uuid id PK
        uuid team_id FK
        varchar username UK
        varchar display_name
        varchar avatar_key
        varchar role_label
        timestamptz created_at
    }

    MISSION {
        uuid id PK
        varchar code UK
        varchar title
        text description
        varchar difficulty
        integer points
        boolean is_active
        timestamptz created_at
    }

    SUBMISSION {
        uuid id PK
        uuid user_id FK
        uuid mission_id FK
        varchar status
        integer awarded_points
        timestamptz submitted_at
        timestamptz reviewed_at
    }

    SCORE {
        uuid id PK
        uuid team_id FK_UK
        integer score
        timestamptz updated_at
    }

    ACTIVITY_LOG {
        bigint id PK
        uuid team_id FK
        uuid user_id FK_NULL
        varchar event_type
        varchar message
        timestamptz created_at
    }
```

---

# 6. Schema `app`

Todos los objetos funcionales vivirán en:

```text
app
```

Tablas:

```text
app.teams
app.users
app.missions
app.submissions
app.scores
app.activity_logs
```

No se utilizará `public` para el dominio principal.

---

# 7. Schema `lab`

Objetos pedagógicos/controlados:

```text
lab.environment_context
lab.my_team_score
```

y las funciones/triggers estrictamente necesarios para hacer segura la vista actualizable.

El alumno podrá descubrir:

```text
lab.my_team_score
```

pero no administrará los objetos de `lab`.

---

# 8. `app.teams`

## Propósito

Representar los equipos que aparecen en:

```text
ranking;
perfil de equipo;
usuarios;
actividad.
```

## Campos

```text
id            UUID PRIMARY KEY
slug          VARCHAR(40) UNIQUE NOT NULL
name          VARCHAR(80) NOT NULL
description   TEXT NOT NULL
created_at    TIMESTAMPTZ NOT NULL DEFAULT now()
```

## Reglas

```text
slug estable;
name visible;
sin datos sensibles.
```

---

# 9. `app.users`

## Propósito

Representar participantes del club.

## Campos

```text
id            UUID PRIMARY KEY
team_id       UUID NOT NULL REFERENCES app.teams(id)
username      VARCHAR(40) UNIQUE NOT NULL
display_name  VARCHAR(80) NOT NULL
avatar_key    VARCHAR(80) NULL
role_label    VARCHAR(60) NOT NULL
created_at    TIMESTAMPTZ NOT NULL DEFAULT now()
```

## `role_label`

Es texto de producto, por ejemplo:

```text
Frontend
Backend
Data
Generalist
```

No es un rol de seguridad.

No confundir con:

```text
PostgreSQL roles;
auth roles;
permissions.
```

---

# 10. `app.missions`

## Propósito

Representar retos internos del club.

## Campos

```text
id            UUID PRIMARY KEY
code          VARCHAR(20) UNIQUE NOT NULL
title         VARCHAR(100) NOT NULL
description   TEXT NOT NULL
difficulty    VARCHAR(16) NOT NULL
points        INTEGER NOT NULL
is_active     BOOLEAN NOT NULL DEFAULT true
created_at    TIMESTAMPTZ NOT NULL DEFAULT now()
```

## Restricciones

```text
difficulty IN ('easy','medium','hard')
points BETWEEN 1 AND 500
```

---

# 11. `app.submissions`

## Propósito

Relacionar:

```text
User
+
Mission
```

y permitir que el dashboard muestre progreso.

## Campos

```text
id              UUID PRIMARY KEY
user_id         UUID NOT NULL REFERENCES app.users(id)
mission_id      UUID NOT NULL REFERENCES app.missions(id)
status          VARCHAR(16) NOT NULL
awarded_points  INTEGER NOT NULL DEFAULT 0
submitted_at    TIMESTAMPTZ NOT NULL DEFAULT now()
reviewed_at     TIMESTAMPTZ NULL
```

## Restricciones

```text
status IN ('submitted','approved','rejected')
awarded_points BETWEEN 0 AND 500
UNIQUE(user_id, mission_id)
```

---

# 12. `app.scores`

## Propósito

Ser la fuente autoritativa del ranking.

## Campos

```text
id          UUID PRIMARY KEY
team_id     UUID NOT NULL UNIQUE REFERENCES app.teams(id)
score       INTEGER NOT NULL
updated_at  TIMESTAMPTZ NOT NULL DEFAULT now()
```

## Restricción

```text
score BETWEEN 0 AND 9999
```

---

# 13. Por qué Score es una tabla separada

Podría haberse colocado:

```text
teams.score
```

pero mantener `Score` separado aporta valor pedagógico:

```text
muestra relación 1:1;
permite descubrir JOIN;
hace más interesante M3;
separa identidad del equipo de su estado competitivo.
```

Sin introducir complejidad excesiva.

---

# 14. Score no se calcula automáticamente desde Submission

En v1:

```text
score = valor oficial del marcador del equipo
```

Puede representar:

```text
misiones;
bonificaciones;
eventos;
ajustes del club.
```

No será una suma automática de `awarded_points`.

Esto es intencional porque M4 necesita modificar el marcador directamente y observar el cambio inmediatamente.

---

# 15. `app.activity_logs`

## Propósito

Dar contexto realista al dashboard.

## Campos

```text
id          BIGSERIAL PRIMARY KEY
team_id     UUID NOT NULL REFERENCES app.teams(id)
user_id     UUID NULL REFERENCES app.users(id)
event_type  VARCHAR(40) NOT NULL
message     VARCHAR(180) NOT NULL
created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
```

Ejemplos `event_type`:

```text
mission_completed
submission_created
score_updated
member_joined
```

Estos son eventos de producto.

No son los:

```text
lablogs técnicos
```

de M7.

---

# 16. Diferencia entre ActivityLog y lablogs

## `app.activity_logs`

Visible en la aplicación.

Ejemplo:

```text
“Lina completó Data Challenge”
```

## `lablogs`

Visible mediante:

```text
clublab logs api
```

Ejemplo:

```text
DATABASE connection failed
```

Nunca mezclar ambos conceptos.

---

# 17. Índices

Se definen:

```text
users(team_id)
submissions(user_id)
submissions(mission_id)
scores(score DESC)
activity_logs(team_id, created_at DESC)
```

Además ya existen índices implícitos para:

```text
PK;
UNIQUE.
```

No se crearán índices “por si acaso”.

---

# 18. Orden del ranking

Ranking:

```sql
ORDER BY score DESC, team_name ASC
```

La segunda columna hace determinista un empate.

La posición se puede calcular mediante:

```text
ROW_NUMBER()
```

para que el JSON siempre incluya:

```text
position.
```

---

# 19. Consulta conceptual de ranking

```sql
SELECT
    ROW_NUMBER() OVER (
        ORDER BY s.score DESC, t.name ASC
    ) AS position,
    t.id,
    t.slug,
    t.name,
    s.score
FROM app.teams t
JOIN app.scores s
    ON s.team_id = t.id
ORDER BY
    s.score DESC,
    t.name ASC;
```

Esta consulta será encapsulada por:

```text
RankingRepository.
```

---

# 20. Dato pedagógico central

Se congela como dato rastreable:

```text
score del equipo local
```

Valor seed inicial:

```text
320
```

Posición seed inicial:

```text
3
```

Recorrido:

```text
Dashboard
  ↓
Ranking
  ↓
GET /api/ranking
  ↓
RankingRepository
  ↓
app.scores
  ↓
lab.my_team_score
```

---

# 21. Ranking seed base

Cada DB tendrá seis equipos visibles.

| Posición inicial | Equipo | Slug | Score |
|---:|---|---|---:|
| 1 | Byte Benders | `byte-benders` | 410 |
| 2 | Runtime Rebels | `runtime-rebels` | 355 |
| 3 | **Equipo local** | `teamXX` | **320** |
| 4 | Null Pointers | `null-pointers` | 275 |
| 5 | Stack Raiders | `stack-raiders` | 190 |
| 6 | Syntax Syndicate | `syntax-syndicate` | 145 |

`Equipo local` se sustituye por:

```text
Equipo 01
Equipo 02
...
```

según el entorno.

---

# 22. Aislamiento del ranking

Los rankings de Team01 y Team02:

```text
no son compartidos en tiempo real.
```

Cada team posee su propia DB.

Por tanto:

```text
Team01 modifica su score
```

y:

```text
Team02 no cambia.
```

Esto es deliberado y coherente con el aislamiento definido en D02/D03.

---

# 23. Identificador del equipo local

El deployment define:

```text
TEAM_ID
TEAM_NUMBER
TEAM_NAME
```

Pero la seguridad SQL no dependerá únicamente de variables modificables por el alumno.

Se agregará:

```text
lab.environment_context
```

con una sola fila.

---

# 24. `lab.environment_context`

Campos:

```text
singleton_id SMALLINT PRIMARY KEY
team_id      UUID NOT NULL UNIQUE REFERENCES app.teams(id)
team_code    VARCHAR(20) NOT NULL
```

Restricción:

```text
singleton_id = 1
```

Ejemplo:

```text
1 | <uuid-equipo-local> | team01
```

---

# 25. Acceso a EnvironmentContext

El rol student:

```text
NO recibe SELECT;
NO recibe INSERT;
NO recibe UPDATE;
NO recibe DELETE.
```

La vista `lab.my_team_score` lo utiliza internamente.

Así:

```text
el scope del equipo no depende de una variable elegida por el alumno.
```

---

# 26. `lab.my_team_score`

Vista pedagógica:

```text
team_id
team_name
score
```

Solo devuelve:

```text
equipo local.
```

Conceptualmente:

```sql
SELECT
    t.id AS team_id,
    t.name AS team_name,
    s.score
FROM app.teams t
JOIN app.scores s
    ON s.team_id = t.id
JOIN lab.environment_context c
    ON c.team_id = t.id
WHERE c.singleton_id = 1;
```

---

# 27. La vista utilizará trigger

Se cierra la decisión que en D03 quedó como fallback:

> **`lab.my_team_score` utilizará `INSTEAD OF UPDATE`.**

Motivo:

```text
la vista incluye JOIN;
el comportamiento actualizable debe ser explícito;
la seguridad queda más fácil de probar.
```

---

# 28. Comportamiento del trigger

Solo acepta:

```text
UPDATE de score.
```

Debe rechazar:

```text
cambio de team_id;
cambio de team_name;
score fuera de rango.
```

Actualiza:

```text
app.scores
```

solo para:

```text
team_id guardado en lab.environment_context.
```

---

# 29. Función del trigger

La función será:

```text
SECURITY DEFINER
```

propiedad de:

```text
clublab_teamXX_owner.
```

Con:

```text
search_path fijo y seguro.
```

El rol student:

```text
no recibe EXECUTE directo
```

si no es necesario.

Solo llega a ella a través del trigger de la vista.

---

# 30. Defensa en profundidad del trigger

La función validará:

```text
NEW.team_id = OLD.team_id
NEW.team_name = OLD.team_name
NEW.score BETWEEN 0 AND 9999
```

y recuperará el team autorizado desde:

```text
lab.environment_context.
```

No confiará únicamente en datos enviados por el alumno.

---

# 31. `updated_at`

`app.scores.updated_at` se actualizará automáticamente.

Se creará un trigger pequeño:

```text
BEFORE UPDATE
```

que establezca:

```text
updated_at = now()
```

Así M4 deja evidencia temporal coherente.

---

# 32. Seed de equipos

Se utilizarán UUIDs deterministas dentro del seed.

Ejemplo conceptual:

```text
local team       00000000-0000-4000-8000-000000000001
Byte Benders     00000000-0000-4000-8000-000000000002
Runtime Rebels   00000000-0000-4000-8000-000000000003
Null Pointers    00000000-0000-4000-8000-000000000004
Stack Raiders    00000000-0000-4000-8000-000000000005
Syntax Syndicate 00000000-0000-4000-8000-000000000006
```

El seed del equipo local reemplaza:

```text
name
slug
team_code
```

pero mantiene el identificador lógico interno estable dentro de cada DB.

---

# 33. Motivo de IDs deterministas

Beneficios:

```text
tests reproducibles;
reset idéntico;
fixtures simples;
logs comparables;
menos aleatoriedad durante clase.
```

Para registros creados en runtime, la aplicación podrá generar UUIDs desde Node.

No necesitamos una extensión PostgreSQL solo para UUID.

---

# 34. Usuarios seed

Equipo local:

```text
Avery Morgan  — Generalist
Lina Park     — Frontend
Mateo Silva   — Backend
Noor Haddad   — Data
```

Los nombres son ficticios.

Usuario principal:

```text
Avery Morgan
username: avery
```

Será el usuario retornado inicialmente por:

```text
GET /api/me.
```

---

# 35. Usuarios de equipos ficticios

Se añadirá al menos un participante por equipo rival para hacer las relaciones creíbles.

Ejemplo:

```text
Byte Benders     → Maya Kim
Runtime Rebels   → Leo Grant
Null Pointers    → Sam Ortega
Stack Raiders    → Iris Wong
Syntax Syndicate → Theo Brooks
```

No se necesita poblar 30 usuarios.

---

# 36. Misiones seed

Se definen cinco misiones de producto.

| Código | Título | Dificultad | Puntos |
|---|---|---|---:|
| `M-101` | Primer Pull Request | easy | 40 |
| `M-102` | Bug Hunt | easy | 60 |
| `M-201` | API Sprint | medium | 90 |
| `M-202` | Data Challenge | medium | 110 |
| `M-301` | Demo Day | hard | 160 |

No son las misiones pedagógicas M0–M8.

Son contenido ficticio de la aplicación.

---

# 37. Estado de misiones del usuario principal

Para Avery:

```text
M-101 → approved
M-102 → approved
M-201 → approved
M-202 → submitted
M-301 → sin submission
```

Esto permite mostrar:

```text3 completadas;
1 en revisión;
1 disponible.
```

---

# 38. Seeds de Submission

Se añadirán submissions suficientes para:

```text
dashboard;
misiones;
actividad.
```

No se necesita completar todos los usuarios contra todas las misiones.

Objetivo:

```text
dataset legible.
```

---

# 39. Seeds de ActivityLog

Ejemplo de ocho eventos:

```text
Avery completó API Sprint
Lina completó Bug Hunt
Equipo recibió 25 puntos de bonificación
Mateo envió Data Challenge
Noor se unió al equipo
Avery completó Primer Pull Request
Lina abrió una nueva entrega
Marcador del equipo fue actualizado
```

Fechas relativas/fijas dentro del seed.

---

# 40. Timestamps deterministas

Para el seed se utilizarán timestamps fijos relativos a una fecha de escenario.

Ejemplo conceptual:

```text
2026-09-15T...
2026-09-16T...
2026-09-17T...
```

No usar:

```text
random();
now()
```

para todo el seed si hace imposible reproducir snapshots.

El deployment podrá decidir si desplaza fechas posteriormente.

---

# 41. Seed mínimo por DB

Aproximadamente:

```text
6 teams
9 users
5 missions
7–10 submissions
6 scores
8 activity logs
1 environment_context
```

Total:

```text
dataset pequeño;
suficiente para investigar.
```

---

# 42. No seed masivo

No crear:

```text
20,000 registros
```

para “hacerlo real”.

M3 debe permitir que un alumno novato encuentre el dato.

La dificultad está en descubrir la arquitectura, no en filtrar un warehouse.

---

# 43. Orden de seed

```text
1. teams
2. users
3. missions
4. submissions
5. scores
6. activity_logs
7. environment_context
```

Después:

```text
validación del dataset.
```

---

# 44. Migrations

Propuesta inicial:

```text
0001_create_schemas
0002_create_domain_tables
0003_create_indexes
0004_create_lab_context
0005_create_lab_score_view
0006_create_roles_and_grants / bootstrap security step
```

La numeración exacta dependerá del mecanismo TypeORM.

---

# 45. ORM elegido

Se selecciona:

# **TypeORM**

para el backend NestJS v1.

Motivos:

```text
integración natural con NestJS;
entidades TypeScript;
migrations explícitas;
SQL accesible;
encaja con experiencia del proyecto;
no oculta el modelo relacional.
```

---

# 46. Regla para TypeORM

No utilizar:

```text
synchronize: true
```

en la clase.

Siempre:

```text
synchronize: false
migrations versionadas
```

Motivo:

```text
schema reproducible;
reset determinista;
seguridad predecible.
```

---

# 47. Entidades TypeORM

Se crearán:

```text
TeamEntity
UserEntity
MissionEntity
SubmissionEntity
ScoreEntity
ActivityLogEntity
```

No es necesario modelar:

```text
lab.environment_context
lab.my_team_score
```

como entidades de dominio normales.

Pueden gestionarse mediante migrations SQL.

---

# 48. Naming

En TypeScript:

```text
camelCase
```

En PostgreSQL:

```text
snake_case
```

Ejemplo:

```text
displayName
→ display_name
```

Se utilizará una estrategia consistente.

---

# 49. Foreign keys

Comportamiento propuesto:

```text
Team → Users           RESTRICT
Team → Score           CASCADE si se elimina team
User → Submissions     CASCADE
Mission → Submissions  RESTRICT
Team → ActivityLog     CASCADE
User → ActivityLog     SET NULL
```

El alumno no tiene permisos DELETE, pero las reglas mantienen integridad para reset/admin.

---

# 50. CHECK constraints

Además de validación de aplicación, PostgreSQL tendrá:

```text
missions.difficulty
missions.points
submissions.status
submissions.awarded_points
scores.score
environment_context.singleton_id
```

La DB no dependerá únicamente de validación frontend.

---

# 51. Unique constraints

```text
teams.slug
users.username
missions.code
scores.team_id
submissions(user_id, mission_id)
environment_context.team_id
```

---

# 52. Dataset validation

Después del seed deben cumplirse:

```text
6 equipos;
6 scores;
1 team local;
score local = 320;
ranking local = 3;
5 missions;
usuario principal existente;
lab context apunta al local;
my_team_score devuelve 1 fila.
```

Si no:

```text
seed = FAILED.
```

---

# 53. Validación M3

Un estudiante debe poder llegar al score aproximadamente así:

```sql
\dt app.*
```

Luego:

```sql
SELECT * FROM app.teams;
SELECT * FROM app.scores;
```

y descubrir:

```text
team_id
+
score.
```

No hace falta entregar la query exacta inicialmente.

---

# 54. Validación M4

La operación preparada será similar a:

```sql
SELECT *
FROM lab.my_team_score;
```

Luego:

```sql
UPDATE lab.my_team_score
SET score = 345;
```

Resultado esperado:

```text
UPDATE 1
```

y:

```text
score local 320 → 345.
```

---

# 55. Efecto del cambio M4

Con seed inicial:

```text
Byte Benders    410
Runtime Rebels  355
Equipo local    320
```

Si el alumno cambia a:

```text
380
```

su ranking cambia:

```text
posición 3 → posición 2.
```

Esto hace que la modificación sea visualmente evidente.

---

# 56. Valor sugerido para la misión M4

El material puede sugerir:

```text
320 → 380
```

sin obligar exactamente ese valor.

Esto produce:

```text
cambio de score
+
cambio de posición
```

y refuerza la relación causa/efecto.

---

# 57. Recover no toca el score

El scenario state:

```text
no vive en app.scores.
```

Por tanto:

```text
recover ranking-db
```

debe conservar:

```text
380
```

si el alumno lo modificó.

---

# 58. Reset sí toca el score

`reset teamXX`:

```text
recrea DB/seed
```

y devuelve:

```text
score = 320
ranking = posición 3.
```

---

# 59. No guardar scenario state en tablas funcionales

El fallo:

```text
ranking-db-failure
```

no se representará modificando:

```text
teams;
scores;
missions.
```

Debe estar separado del dominio.

Esto evita que una recuperación borre datos pedagógicos.

---

# 60. API data contracts derivados

Este bloque deja preparados los datos necesarios para:

```text
GET /api/me
GET /api/team
GET /api/ranking
GET /api/missions
GET /api/activity
```

Bloque B definirá DTOs exactos.

---

# 61. Dashboard data

La UI podrá derivar:

```text
usuario
equipo
score
ranking position
misiones aprobadas
actividad reciente.
```

No hace falta añadir una tabla `dashboard`.

---

# 62. Misión completada

Para UI:

```text
submission.status = approved
```

se considera:

```text
completed.
```

`submitted`:

```text
in review.
```

Sin fila:

```text
available.
```

---

# 63. Estado del equipo

No añadiremos:

```text
team_status
```

en v1.

No aporta valor a M0–M8.

---

# 64. Avatar

`avatar_key` será:

```text
identificador de asset local
```

por ejemplo:

```text
avatar-01
```

No:

```text
URL remota obligatoria.
```

La clase debe funcionar sin Internet.

---

# 65. No archivos externos

El dataset no dependerá de:

```text
S3;
Google Drive;
CDN;
API externa.
```

Todo asset requerido por UI será local.

---

# 66. Zona horaria

DB:

```text
TIMESTAMPTZ
```

y aplicación:

```text
ISO 8601.
```

La UI podrá formatear a local.

No guardar fechas como:

```text
VARCHAR.
```

---

# 67. Integridad del ranking

`Score.team_id`:

```text
UNIQUE
```

garantiza:

```text
un marcador por team.
```

No permitir múltiples scores activos por equipo.

---

# 68. Cero scores

Todo team del seed tendrá score.

No será nullable.

Si alguna vez se crea team en runtime:

```text
la aplicación deberá crear su Score correspondiente
```

o manejar explícitamente la ausencia.

v1 no necesita alta de equipos desde UI.

---

# 69. Borrados

La UI v1 no expone:

```text
delete team;
delete user;
delete mission.
```

El modelo mantiene constraints correctos, pero no construiremos funciones que no requiere la clase.

---

# 70. Seguridad heredada de D03

El diseño debe aplicarse con roles:

```text
owner
migrator
app
student
```

El `student`:

```text
SELECT permitido
UPDATE(score) vía lab.my_team_score
```

y nada más.

No se reabre esa decisión en Fase 4.

---

# 71. Tests de DB derivados

Se deberán implementar tests para:

```text
seed count;
ranking order;
ranking tie order;
local score;
my_team_score row count;
update allowed;
update forbidden columns;
score range;
FK integrity;
submission uniqueness;
reset reproducibility.
```

---

# 72. Test de ranking

Estado seed:

```text
1 Byte Benders 410
2 Runtime Rebels 355
3 Equipo local 320
4 Null Pointers 275
5 Stack Raiders 190
6 Syntax Syndicate 145
```

Debe producir exactamente ese orden.

---

# 73. Test después de M4

Si local:

```text
320 → 380
```

ranking esperado:

```text
1 Byte Benders 410
2 Equipo local 380
3 Runtime Rebels 355
4 Null Pointers 275
5 Stack Raiders 190
6 Syntax Syndicate 145
```

---

# 74. Test de reset

Después de reset:

```text
local score = 320
local position = 3
environment_context correcto
my_team_score = 1 fila.
```

---

# 75. Decisiones cerradas del Bloque A

### DA4-01
El dominio v1 tendrá seis entidades:

```text
Team
User
Mission
Submission
Score
ActivityLog
```

### DA4-02
El ranking será derivado de `Team + Score`.

### DA4-03
`Score` permanece como entidad separada 1:1.

### DA4-04
El score no se calcula automáticamente de submissions.

### DA4-05
Schema funcional:

```text
app.
```

### DA4-06
Schema pedagógico:

```text
lab.
```

### DA4-07
El score local seed será:

```text
320
```

### DA4-08
La posición seed local será:

```text
3.
```

### DA4-09
Habrá seis equipos visibles en el ranking.

### DA4-10
El dataset será determinista.

### DA4-11
`lab.environment_context` almacenará la identidad del team local.

### DA4-12
Student no tendrá permisos directos sobre environment context.

### DA4-13
`lab.my_team_score` tendrá `INSTEAD OF UPDATE`.

### DA4-14
Solo `score` será modificable por student.

### DA4-15
Valor de score válido:

```text
0–9999.
```

### DA4-16
Se utilizarán UUIDs deterministas en seeds.

### DA4-17
Runtime UUIDs se generarán desde Node.

### DA4-18
ORM:

```text
TypeORM.
```

### DA4-19
`synchronize: false`.

### DA4-20
Schema siempre mediante migrations.

### DA4-21
Assets/datos no dependerán de Internet.

### DA4-22
Recover conservará datos; reset restaurará seed.

---

# 76. Salida hacia Bloque B

El backend deberá implementar repositories para:

```text
Users
Teams
Missions
Ranking
Activity
```

En especial:

```text
RankingRepository
```

debe consultar:

```text
app.teams
+
app.scores
```

y soportar el hook de scenario sin alterar este modelo.

---

# 77. Salida hacia Bloque C

El frontend tendrá disponibles:

```text
usuario principal;
equipo;
score;
posición;
misiones;
actividad.
```

El valor:

```text
320
```

debe aparecer de forma clara desde M0.

---

# 78. Salida hacia Bloque D

La validación integrada deberá comprobar:

```text
320 visible en UI
=
320 en /api/ranking
=
320 en app.scores
=
320 en lab.my_team_score.
```

Después de M4:

```text
380 visible en UI
=
380 en API
=
380 en DB.
```

---

# 79. Criterios de aceptación

```text
[x] dominio cerrado
[x] seis entidades definidas
[x] campos definidos
[x] relaciones definidas
[x] ERD definido
[x] constraints definidas
[x] índices definidos
[x] ranking query definida
[x] score pedagógico definido
[x] dataset de ranking definido
[x] usuarios seed definidos
[x] misiones seed definidas
[x] submissions seed definidas conceptualmente
[x] activity seed definida
[x] environment_context definido
[x] my_team_score definida
[x] trigger de UPDATE definido
[x] TypeORM decidido
[x] migrations strategy definida
[x] tests derivados
[x] reset/recover semantics preservadas
```

# BLOQUE A — DISEÑO COMPLETADO

---

# 80. Arquitectura de datos resumida

```text
                          app
                           │
         ┌─────────────────┼──────────────────┐
         │                 │                  │
       teams ──────── users              missions
         │              │                    │
         │              └──── submissions ───┘
         │
         ├──────── score
         │
         └──────── activity_logs

                          lab
                           │
                environment_context
                           │
                           ▼                   my_team_score
                           │
                   UPDATE(score)
                           │
                           ▼
                     app.scores
```

Este modelo contiene exactamente lo necesario para que el alumno siga un dato desde la pantalla hasta la base de datos y lo modifique de forma controlada.