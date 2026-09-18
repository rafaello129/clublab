# ClubLab — Fase 3 / Bloque A
## Identidad, credenciales y PostgreSQL

**Proyecto:** ClubLab v1  
**Fase:** 3 — Seguridad y aislamiento  
**Bloque:** A  
**Estado:** CERRADO PARA DISEÑO v1  
**Dependencias:** D00 + D01 + D02 + Plan Fase 3  

---

# 1. Propósito

Este bloque define quién existe dentro de cada entorno ClubLab, qué credenciales recibe y qué operaciones puede realizar sobre PostgreSQL.

La prioridad es permitir las misiones M3 y M4 sin convertir al alumno en administrador de la base.

Debe cumplirse:

```text
el alumno puede explorar datos;
el alumno puede modificar únicamente el dato pedagógico autorizado;
la API puede operar normalmente;
migrations pueden administrar schema;
ningún rol de alumno puede administrar PostgreSQL;
ningún team comparte credenciales con otro.
```

---

# 2. Principio de mínimos privilegios

No se utilizará una sola cuenta PostgreSQL para todo.

Cada responsabilidad tendrá una identidad distinta:

```text
administrar schema
≠
ejecutar aplicación
≠
investigar como alumno
```

La regla será:

> **Cada proceso recibe únicamente los permisos que necesita para cumplir su función.**

---

# 3. Identidades PostgreSQL por team

Cada team tendrá cuatro identidades lógicas.

Ejemplo para `team01`:

```text
clublab_team01_owner
clublab_team01_migrator
clublab_team01_app
clublab_team01_student
```

Además existirá el superusuario interno de la imagen PostgreSQL para bootstrap y contingencia administrativa.

Ese superusuario:

```text
no se entrega al alumno;
no se utiliza por la API;
no se utiliza en M3/M4;
no se publica fuera del contenedor.
```

---

# 4. `clublab_team01_owner`

Tipo:

```text
NOLOGIN
```

Responsabilidad:

```text
propietario lógico del schema y objetos de aplicación.
```

No se utiliza para iniciar sesión.

Ventaja:

```text
ni API ni student son propietarios de tablas;
por tanto no pueden DROP/ALTER simplemente por ser dueños.
```

Será propietario de:

```text
schema app;
schema lab;
tablas;
vistas;
secuencias;
funciones controladas.
```

---

# 5. `clublab_team01_migrator`

Tipo:

```text
LOGIN
```

Responsabilidad:

```text
migrations;
creación/modificación de schema;
seeds estructurales.
```

Uso:

```text
solo durante deploy/reset/migration.
```

No estará presente en:

```text
frontend;
toolbox;
credenciales entregadas al estudiante.
```

Permisos previstos:

```text
SET ROLE clublab_team01_owner
```

o mecanismo equivalente controlado.

No será superuser.

---

# 6. `clublab_team01_app`

Tipo:

```text
LOGIN
```

Responsabilidad:

```text
runtime de la API.
```

Permisos:

```text
USAGE de schemas requeridos;
SELECT;
INSERT;
UPDATE;
DELETE;
USAGE de sequences;
EXECUTE de funciones necesarias.
```

No permisos de:

```text
CREATE ROLE;
ALTER ROLE;
CREATE DATABASE;
DROP schema;
ALTER schema;
CREATE EXTENSION;
superuser;
replication;
bypassrls;
```

La API tampoco será propietaria de las tablas.

---

# 7. `clublab_team01_student`

Tipo:

```text
LOGIN
```

Responsabilidad:

```text
M3;
M4;
consultas desde toolbox.
```

Permisos previstos:

```text
USAGE en schemas pedagógicos;
SELECT en tablas autorizadas;
SELECT en vistas pedagógicas;
UPDATE únicamente sobre la superficie preparada para M4.
```

No podrá:

```text
INSERT arbitrario;
DELETE;
TRUNCATE;
CREATE;
ALTER;
DROP;
GRANT;
REVOKE;
CREATE ROLE;
CREATE DATABASE;
CREATE EXTENSION;
cambiar propietarios;
administrar otros usuarios.
```

---

# 8. No habrá rol SQL `recovery` para el alumno

Se ajusta el plan preliminar.

La recuperación del incidente:

```text
clublab recover ranking-db
```

no necesita una cuenta PostgreSQL especial.

El recovery será controlado mediante:

```text
token scoped;
control interno de la aplicación;
scenario state.
```

Por tanto, no se añadirá una credencial SQL adicional sin necesidad.

---

# 9. Base y schemas

Por team:

```text
database:
clublab_team01
```

Schemas propuestos:

```text
app
lab
```

## `app`

Contiene:

```text
tablas reales;
relaciones;
secuencias;
objetos funcionales.
```

## `lab`

Contiene:

```text
vistas pedagógicas;
funciones estrictamente controladas;
objetos diseñados para interacción del alumno.
```

Esto separa:

```text
modelo funcional
```

de:

```text
superficie educativa.
```

---

# 10. Schema `public`

Se endurecerá explícitamente.

Conceptualmente:

```sql
REVOKE CREATE ON SCHEMA public FROM PUBLIC;
```

y se evitará crear objetos funcionales de ClubLab en `public`.

Los schemas relevantes serán:

```text
app
lab
```

---

# 11. Permisos de lectura para M3

M3 requiere que el alumno pueda investigar tablas reales.

Se permitirá `SELECT` únicamente sobre las tablas pedagógicamente útiles.

Ejemplo:

```text
app.users
app.teams
app.missions
app.scores
app.activity_log
```

No se concederá automáticamente:

```text
SELECT ON ALL TABLES
```

si aparecen tablas futuras que contengan:

```text
tokens;
sesiones;
credenciales;
datos internos.
```

La lista será explícita.

---

# 12. Exploración del schema

El usuario student podrá utilizar:

```text
\dt app.*
\d app.teams
\d app.scores
SELECT ...
```

Esto mantiene la misión de exploración real.

No necesita privilegios de administración para consultar metadatos básicos de objetos a los que tiene acceso.

---

# 13. Problema de M4

M4 necesita un `UPDATE` real.

Pero conceder:

```sql
UPDATE ON app.scores
```

de forma general permitiría modificar:

```text
otros equipos;
campos no previstos;
varias filas.
```

Por tanto, no se concederá `UPDATE` directo sobre la tabla base.

---

# 14. Estrategia elegida para M4

Se utilizará:

> **una vista pedagógica actualizable limitada al team del alumno.**

Ejemplo conceptual:

```text
lab.my_team_score
```

La vista expondrá únicamente:

```text
team_id
team_name
score
```

y únicamente la fila correspondiente al entorno del equipo.

---

# 15. Vista conceptual de M4

Ejemplo para Team 01:

```sql
CREATE VIEW lab.my_team_score AS
SELECT
    t.id   AS team_id,
    t.name AS team_name,
    s.score
FROM app.teams t
JOIN app.scores s ON s.team_id = t.id
WHERE t.id = '<TEAM01_ID>'
WITH LOCAL CHECK OPTION;
```

La implementación final puede adaptar nombres/tablas al schema real.

Lo importante es:

```text
solo una fila;
solo campos pedagógicos;
scope fijo del team.
```

---

# 16. Permisos sobre la vista

El alumno recibirá:

```text
SELECT
```

sobre la vista completa y:

```text
UPDATE(score)
```

únicamente sobre la columna autorizada.

Conceptualmente:

```sql
GRANT SELECT
ON lab.my_team_score
TO clublab_team01_student;

GRANT UPDATE (score)
ON lab.my_team_score
TO clublab_team01_student;
```

No se concede `UPDATE` de:

```text
team_id;
team_name.
```

---

# 17. Validación adicional del score

La tabla base deberá tener restricciones reales.

Ejemplo:

```text
score >= 0
score <= límite pedagógico razonable
```

El objetivo no es impedir que el alumno experimente, sino evitar valores extremos que rompan UI, queries o rankings.

El rango exacto se definirá junto al schema funcional.

---

# 18. Por qué se elige una vista

Ventajas:

```text
sigue siendo SQL real;
el alumno ejecuta UPDATE;
modifica PostgreSQL realmente;
no puede elegir otra fila;
no recibe UPDATE sobre tabla base;
la API ve el cambio;
la UI ve el cambio;
reset sigue siendo simple.
```

Pedagógicamente conserva:

```text
DB → API → Frontend
```

sin abrir privilegios innecesarios.

---

# 19. Si la vista no resulta automáticamente actualizable

Durante implementación se verificará esta condición con el schema real.

Si el JOIN impide una vista automáticamente actualizable, la alternativa aprobada será:

```text
INSTEAD OF UPDATE trigger
```

sobre:

```text
lab.my_team_score
```

El trigger:

```text
solo permitirá modificar score;
forzará team_id del entorno;
rechazará cualquier otro cambio.
```

No se cambiará a `UPDATE` directo sobre la tabla base solo por comodidad.

---

# 20. Alternativa descartada: RLS como primera opción

Row Level Security puede resolver el scope por fila.

Sin embargo, dado que:

```text
cada team ya tiene PostgreSQL propio;
solo M4 necesita una escritura pequeña;
```

RLS añade complejidad que no es necesaria para v1.

Por tanto:

```text
RLS = opcional/futuro
vista limitada = estrategia inicial
```

Si el modelo final vuelve más complejos los permisos, se podrá reconsiderar.

---

# 21. Permisos explícitamente prohibidos para student

El rol student no tendrá:

```text
SUPERUSER
CREATEDB
CREATEROLE
REPLICATION
BYPASSRLS
```

Tampoco ownership sobre:

```text
database;
schemas;
tables;
views.
```

Y no podrá ejecutar:

```text
DROP TABLE;
ALTER TABLE;
TRUNCATE;
CREATE TABLE;
CREATE SCHEMA;
CREATE ROLE;
GRANT;
REVOKE;
```

sobre objetos ClubLab.

---

# 22. `COPY` y acceso al servidor

El rol student no tendrá membresía en:

```text
pg_read_server_files
pg_write_server_files
pg_execute_server_program
```

Por tanto no podrá utilizar PostgreSQL como vía para:

```text
leer archivos del servidor;
escribir archivos;
ejecutar programas.
```

---

# 23. Extensiones

El alumno no tendrá privilegios para:

```text
CREATE EXTENSION
```

ni administración equivalente.

Las extensiones necesarias, si existieran, se instalarán durante build/init por el plano administrativo.

---

# 24. Search path

Se configurará explícitamente.

Para la API:

```text
app, lab, pg_catalog
```

Para student:

```text
lab, app, pg_catalog
```

Objetivo:

```text
evitar depender del schema public;
hacer nombres predecibles;
reducir objetos ambiguos.
```

---

# 25. Timeouts del usuario student

Para impedir consultas accidentalmente largas:

```text
statement_timeout
lock_timeout
idle_in_transaction_session_timeout
```

tendrán límites modestos.

Valores iniciales propuestos:

```text
statement_timeout = 10s
lock_timeout = 3s
idle_in_transaction_session_timeout = 30s
```

Se validarán durante las misiones reales.

---

# 26. Límite de conexiones del alumno

El rol student tendrá un límite pequeño.

Propuesta:

```text
CONNECTION LIMIT 4
```

Es suficiente para:

```text
psql;
reconexiones;
pruebas.
```

y evita cientos de conexiones accidentales.

---

# 27. Límite de conexiones de API

El rol app tendrá un límite mayor.

Propuesta inicial:

```text
CONNECTION LIMIT 20
```

El pool de la aplicación deberá configurarse por debajo.

Para ClubLab no se necesita un pool grande.

---

# 28. `temp_file_limit`

Se evaluará un límite por rol student.

Propuesta:

```text
64 MB
```

para reducir queries accidentales que generen grandes temporales.

El valor final se validará en implementación.

---

# 29. Passwords

Cada team tendrá passwords independientes para:

```text
postgres bootstrap;
migrator;
app;
student;
terminal;
recovery token.
```

No se reutilizarán.

---

# 30. Calidad de passwords

Generación:

```text
aleatoria;
mínimo 24 caracteres para credenciales internas;
sin patrones basados en Team ID.
```

Ejemplo NO permitido:

```text
team01_password
clublab123
```

Las credenciales mostradas al alumno pueden seguir siendo largas pero deberán copiarse fácilmente mediante la tarjeta/terminal.

---

# 31. Password del student

Es una credencial:

```text
desechable;
limitada;
solo válida dentro del DATA network del team.
```

Por ello puede entregarse al alumno durante M3.

Conocerla no permite:

```text
entrar al host;
entrar a otra DB;
administrar PostgreSQL;
alcanzar producción.
```

---

# 32. Password de API

Solo se inyecta en:

```text
API
```

No aparece en:

```text
frontend;
toolbox;
materiales;
lablogs.
```

---

# 33. Password de migrator

Solo estará disponible durante:

```text
deploy;
migration;
reset.
```

No debe permanecer innecesariamente en toolbox o frontend.

La implementación decidirá si se monta temporalmente o se consume desde configuración host-side.

---

# 34. Superusuario PostgreSQL

La imagen oficial requiere una identidad administrativa de bootstrap.

Esta credencial:

```text
es diferente por team;
no se publica;
no se entrega al alumno;
no la usa la API;
```

y se utiliza únicamente para administración excepcional/init cuando sea necesario.

---

# 35. Autenticación PostgreSQL

Se requerirá:

```text
SCRAM-SHA-256
```

para conexiones TCP.

No usar:

```text
trust
```

para conexiones de toolbox/API.

Configuración objetivo:

```text
password_encryption = scram-sha-256
```

---

# 36. `pg_hba.conf`

El acceso debe aceptar conexiones únicamente bajo autenticación fuerte.

Conceptualmente:

```text
host all all <team-data-subnet> scram-sha-256
```

La red Docker ya limita quién puede alcanzar el servicio.

`pg_hba.conf` agrega una segunda frontera.

No se agregarán rangos de LAN ni redes de otros teams.

---

# 37. DATABASE_URL

La API podrá utilizar:

```text
DATABASE_URL
```

o variables separadas.

Pero los errores/logs nunca deberán imprimir la URL completa si incluye password.

Salida permitida:

```text
database:5432
```

No:

```text
postgres://user:password@database:5432/...
```

---

# 38. Credencial student dentro de toolbox

El toolbox tendrá disponible únicamente la credencial:

```text
clublab_teamXX_student
```

Opciones aceptables:

```text
PGUSER/PGDATABASE;
.pgpass mode 0600;
helper clublab db.
```

La elección exacta puede cerrarse al construir toolbox.

Es aceptable que el alumno pueda conocer esa contraseña: es su identidad limitada y desechable.

---

# 39. El alumno no recibe credencial app

Desde toolbox no deberá existir:

```text
APP_DB_PASSWORD
```

ni archivo que contenga el password de:

```text
clublab_teamXX_app.
```

Prueba obligatoria posterior:

```text
env
filesystem search
logs
```

no deben revelarlo.
---

# 40. Default privileges

Las migrations deberán mantener los privilegios correctamente cuando se creen nuevas tablas.

Se utilizarán:

```text
ALTER DEFAULT PRIVILEGES
```

para evitar que:

```text
una nueva tabla quede accidentalmente accesible al student
```

o que:

```text
la API pierda permisos.
```

Los grants del student seguirán siendo explícitos para objetos pedagógicos.

---

# 41. Flujo de creación de un team

Conceptualmente:

```text
1. generar secrets
2. iniciar PostgreSQL
3. crear owner
4. crear migrator
5. crear app
6. crear student
7. crear schemas
8. aplicar migrations
9. aplicar grants app
10. crear vistas lab
11. aplicar grants student
12. aplicar seed
13. ejecutar tests de permisos
```

Solo después:

```text
team = READY
```

---

# 42. Flujo de reset

Durante reset:

```text
credenciales pueden conservarse durante la misma sesión;
DB se recrea;
roles/grants se recrean;
migrations se aplican;
views lab se recrean;
seed se aplica.
```

Para una nueva clase o nueva generación:

```text
rotar credenciales.
```

---

# 43. Pruebas automáticas de permisos

Cada build/reset deberá poder ejecutar checks.

Como `student`:

```text
SELECT autorizado → PASS
UPDATE score propio → PASS
UPDATE team_id → FAIL
UPDATE fila fuera de scope → FAIL
DELETE → FAIL
DROP TABLE → FAIL
CREATE TABLE → FAIL
ALTER TABLE → FAIL
CREATE ROLE → FAIL
```

Como `app`:

```text
operaciones funcionales → PASS
DROP TABLE → FAIL
CREATE ROLE → FAIL
```

---

# 44. Test de ownership

Verificar que:

```text
app
student
```

no sean propietarios de las tablas.

Esperado:

```text
owner = clublab_teamXX_owner
```

Esto evita que un grant omitido convierta indirectamente al runtime en administrador del schema.

---

# 45. Test cross-team de credenciales

Aunque las redes ya aíslan, se probará:

```text
team01_student password
```

contra:

```text
team02 database
```

Resultado esperado:

```text
authentication failed
```

Incluso si hipotéticamente existiera conectividad.

Esto crea defensa en profundidad.

---

# 46. Test de passwords repetidos

El proceso de generación deberá verificar que:

```text
student_team01 != student_team02
app_team01 != app_team02
```

y que no se reutilice una credencial administrativa entre teams.

---

# 47. Seed y permisos

El seed debe ejecutarse con:

```text
migrator/owner
```

o identidad administrativa de despliegue.

No con:

```text
student.
```

Así M4 nunca necesita permisos de inicialización.

---

# 48. Datos del ranking

Cada DB podrá contener varios equipos ficticios para que exista un ranking real.

Ejemplo:

```text
Equipo Alfa
Equipo Beta
Equipo Gamma
Equipo del alumno
```

El rol student podrá:

```text
SELECT ranking data
```

pero su superficie de escritura:

```text
lab.my_team_score
```

solo expone la fila propia.

---

# 49. Team identity en la vista

La identidad de la fila propia no dependerá de un valor escrito por el alumno.

No usar:

```text
SET team_id = ...
```

como frontera de seguridad.

La vista/configuración se genera con el Team ID del entorno.

Así el alumno no puede cambiar contexto a:

```text
team02.
```

---

# 50. Nombres previsibles pero no secretos

Nombres como:

```text
clublab_team01_student
clublab_team01
database
```

no se consideran secretos.

La seguridad depende de:

```text
network isolation;
password;
grants;
scope.
```

No de ocultar nombres.

---

# 51. Matriz de privilegios

| Acción | Owner | Migrator | App | Student |
|---|---:|---:|---:|---:|
| Login | No | Sí | Sí | Sí |
| Crear/alterar schema | Dueño | Sí, controlado | No | No |
| SELECT funcional | Sí | Sí | Sí | Sí, solo objetos permitidos |
| INSERT | Sí | Sí | Sí según app | No |
| UPDATE general | Sí | Sí | Sí según app | No |
| UPDATE score propio | Sí | Sí | Sí | Sí, vía `lab.my_team_score` |
| DELETE | Sí | Sí | Sí según app | No |
| DROP/ALTER tablas | Sí | Sí | No | No |
| Crear roles | No | No | No | No |
| Superuser | No | No | No | No |
| Crear DB | No | No | No | No |

El superusuario bootstrap no aparece en la tabla porque no es identidad normal de operación.

---

# 52. Entrega progresiva de credenciales

Inicio de clase:

```text
URL;
app login;
terminal login.
```

M3:

```text
student DB user;
student DB password;
database name.
```

No entregar antes:

```text
migrator;
app DB password;
postgres admin.
```

Esto respeta la narrativa progresiva de D01.

---

# 53. Archivos de ejemplo

El repositorio podrá contener:

```text
.env.example
```

con:

```text
DB_APP_USER=<generated>
DB_APP_PASSWORD=<generated>
DB_STUDENT_USER=<generated>
DB_STUDENT_PASSWORD=<generated>
```

Nunca valores reales.

---

# 54. Directorio de secrets

Diseño propuesto:

```text
/home/tulum/infra/clublab/runtime/secrets/
```

con archivos por team.

Ejemplo:

```text
team01.env
team02.env
...
```

Permisos mínimos:

```text
directory 700
files 600
```

Propietario:

```text
cuenta operadora autorizada
```

No accesible desde toolbox.

---

# 55. No versionar runtime secrets

`.gitignore` deberá excluir:

```text
runtime/
*.secret
*.credentials
teams/*.env
```

según estructura definitiva.

El repositorio conserva únicamente:

```text
templates;
generadores;
examples.
```

---

# 56. Regla de errores de autenticación

Los errores mostrados al alumno pueden indicar:

```text
authentication failed
permission denied
```

pero no deben revelar:

```text
password esperado;
roles internos adicionales;
configuración administrativa.
```

---

# 57. Auditoría SQL

No se habilitará inicialmente un sistema pesado de auditoría PostgreSQL.

Para v1 serán suficientes:

```text
logs normales;
lab events;
tests de permisos;
reset reproducible.
```

Se evita introducir `pgaudit` sin necesidad pedagógica u operativa demostrada.

---

# 58. Cambios de contraseña por el alumno

El rol student no necesita:

```text
ALTER ROLE
```

ni cambio de credenciales durante clase.

Se impedirá la administración de roles.

Las credenciales se gestionan desde despliegue.

---

# 59. Conexiones desde LAN

Aunque el alumno conozca:

```text
DB user;
DB password;
```

no podrá conectarse directamente desde su laptop porque:

```text
5432 no está publicado;
database vive solo en teamXX-data.
```

Debe utilizar:

```text
toolbox
```

Esto refuerza el perímetro de la misión.

---

# 60. Decisiones cerradas del Bloque A

### DA3-01
Cada team tendrá roles separados:

```text
owner
migrator
app
student
```

### DA3-02
`owner` será NOLOGIN.

### DA3-03
La API no será propietaria del schema.

### DA3-04
Student tendrá SELECT explícito en objetos pedagógicos.

### DA3-05
Student no tendrá UPDATE directo sobre tablas base.

### DA3-06
M4 utilizará:

```text
lab.my_team_score
```

o vista equivalente scoped al team.

### DA3-07
Student podrá actualizar únicamente el campo pedagógico autorizado.

### DA3-08
RLS no será requisito inicial.

### DA3-09
No se creará un usuario SQL de recovery sin necesidad.

### DA3-10
PostgreSQL utilizará SCRAM-SHA-256.

### DA3-11
`public` no será schema de aplicación y perderá CREATE para PUBLIC.

### DA3-12
Cada team tendrá passwords únicos.

### DA3-13
Student credentials serán desechables y entregables al alumno.

### DA3-14
App/migrator/admin credentials nunca se entregarán al alumno.

### DA3-15
Student tendrá timeouts y connection limit.

### DA3-16
Los grants serán explícitos y probados automáticamente.

### DA3-17
Los secrets runtime estarán fuera de Git.

### DA3-18
El reset recreará roles, grants, vistas y seed de forma reproducible.

---

# 61. Requisitos para el Bloque B

El siguiente bloque debe endurecer los contenedores sabiendo ahora exactamente qué identidades necesitan.

Debe definir:

```text
UID/GID;
root vs no-root;
cap_drop;
no-new-privileges;
read_only;
tmpfs;
mounts;
toolbox hardening;
ttyd;
gateway hardening.
```

Especial atención:

```text
toolbox contiene student DB credential,
pero nunca app/migrator credentials.
```

---

# 62. Requisitos para el Bloque C

Más adelante deberán protegerse:

```text
recovery token;
terminal credential;
app secrets;
clublabctl;
audit logs;
firewall.
```

La separación de identidades PostgreSQL ya queda congelada.

---

# 63. Criterios de aceptación

```text
[x] identidades por team definidas
[x] owner NOLOGIN definido
[x] migrator definido
[x] app runtime definido
[x] student definido
[x] schemas app/lab definidos
[x] public endurecido
[x] SELECT pedagógico definido
[x] UPDATE seguro definido
[x] vista M4 definida
[x] fallback trigger definido
[x] RLS evaluado
[x] permisos prohibidos definidos
[x] SCRAM definido
[x] pg_hba conceptual definido
[x] password policy definida
[x] secrets fuera de Git
[x] timeouts student definidos
[x] connection limits definidos
[x] default privileges contemplados
[x] tests de grants definidos
[x] cross-team credential test definido
[x] flujo de creación/reset definido
```

# BLOQUE A — COMPLETADO

---

# 64. Modelo final del Bloque A

```text
                 POSTGRESQL — TEAM XX
                         │
              ┌──────────┴──────────┐
              │                     │
         app schema             lab schema
              │                     │
       tablas reales        vistas pedagógicas
              │                     │
              │              my_team_score
              │                     │
       ┌──────┴──────┐              │
       │             │              │
      API         STUDENT───────────┘
       │             │
 app credential   SELECT
                  UPDATE(score only)

Owner:
  NOLOGIN / owns objects

Migrator:
  deploy/reset only
```

La siguiente capa de seguridad será hacer que los propios contenedores y la terminal respeten estos límites incluso si el alumno intenta salir de la ruta prevista.