# ClubLab — Plan de Fase 3
## Seguridad y aislamiento

**Proyecto:** ClubLab v1  
**Fase:** 3  
**Nombre:** Seguridad, permisos y aislamiento efectivo  
**Estado:** PLAN DE TRABAJO  
**Entradas principales:**  
- `D00_Estado_Base_Servidor_ClubLab.md`
- `D01_Diseno_Experiencia_ClubLab_01.md`
- `D02_Arquitectura_Tecnica_ClubLab.md`

**Entregable principal:**  
`D03_Seguridad_Aislamiento_ClubLab.md`

---

# 1. Propósito de la Fase 3

La Fase 2 definió las fronteras de ClubLab.

La Fase 3 debe hacer que esas fronteras se cumplan técnicamente.

La pregunta principal será:

> **¿Cómo garantizamos que un estudiante pueda experimentar, modificar y romper su entorno sin poder afectar a otro equipo, al host o a servicios reales?**

La fase cubrirá:

```text
identidades;
credenciales;
permisos;
PostgreSQL;
terminal;
contenedores;
gateway;
secrets;
network isolation;
recovery tokens;
acciones permitidas/prohibidas;
pruebas de aislamiento.
```

No se implementará todavía toda la aplicación ni el Scenario Manager completo.

---

# 2. Principio de seguridad

ClubLab no se diseñará bajo:

```text
“el alumno no debería hacer eso”
```

sino bajo:

```text
“aunque lo intente, no debe poder hacerlo”.
```

Las restricciones deben depender principalmente de:

```text
arquitectura
+
permisos
+
aislamiento
+
validaciones
```

y no únicamente de instrucciones escritas.

---

# 3. Modelo de confianza

Se definen cuatro zonas de confianza:

```text
Z0 — Host Tulum
Z1 — Control del instructor
Z2 — Entorno del equipo
Z3 — Alumno / navegador
```

Regla:

```text
Z3 nunca recibe acceso directo a Z0.
```

El flujo permitido será:

```text
Alumno
  ↓
Gateway / Toolbox
  ↓
Recursos de su Team
```

El instructor sí podrá operar recursos ClubLab desde Z1.

---

# 4. Activos que deben protegerse

## Host

```text
Docker Engine;
filesystem;
usuarios;
SSH;
systemd;
NetworkManager;
firewalld;
Tailscale;
Caddy existente.
```

## Servicios reales

```text
WhatsApp;
postgres-main;
Pelican;
Wings;
Playit;
Cloudflare;
backups.
```

## Otros equipos

```text
DB;
terminal;
API;
logs;
scenario state;
credentials.
```

## Control de ClubLab

```text
clublabctl;
templates;
secrets;
recovery tokens;
scenario controls.
```

---

# 5. Objetivos obligatorios

Al terminar la fase debe cumplirse:

```text
un estudiante no puede tocar el host;
un estudiante no puede usar Docker;
un estudiante no puede obtener root;
un team no puede alcanzar otro team;
la DB no está publicada;
la DB solo acepta las credenciales previstas;
los permisos SQL están limitados;
el alumno no puede cambiar schema/roles;
la terminal no es anónima;
recover solo actúa sobre su team;
scenario load/reset son instructor-only;
secrets no aparecen en logs;
gateway no permite tránsito lateral;
recursos tienen límites;
acciones destructivas tienen guard rails.
```

---

# 6. Estructura de trabajo

Para mantener la fase simple, se divide en **cuatro bloques**:

```text
BLOQUE A
Identidad, credenciales y PostgreSQL

BLOQUE B
Hardening de contenedores, terminal y gateway

BLOQUE C
Control de acciones, secrets y aislamiento operacional

BLOQUE D
Pruebas de seguridad + D03 final
```

---

# BLOQUE A — Identidad, credenciales y PostgreSQL

# 7. Objetivo

Definir quién puede hacer qué dentro de cada team.

Se cerrará:

```text
usuarios;
credenciales;
roles PostgreSQL;
permisos;
separación alumno/API;
gestión de passwords;
rotación;
datos autorizados.
```

---

# 8. Identidades por equipo

Cada team tendrá identidades separadas.

Ejemplo:

```text
team01_app
team01_student
team01_recovery
```

## `team01_app`

Utilizado únicamente por API.

Permisos:

```text
SELECT;
INSERT;
UPDATE;
DELETE solo donde aplicación lo requiera.
```

Puede tener acceso completo al schema ClubLab de ese team, pero no a administración PostgreSQL.

## `team01_student`

Utilizado desde toolbox durante M3/M4.

Permisos mínimos:

```text
SELECT en tablas pedagógicas;
UPDATE únicamente en campos/filas permitidos.
```

No:

```text
CREATE;
ALTER;
DROP;
TRUNCATE;
CREATE ROLE;
GRANT;
COPY hacia archivos del servidor;
extensiones;
superuser.
```

## `team01_recovery`

No será un usuario SQL normal del estudiante.

Se reserva para acciones controladas del entorno si fuese necesario.

---

# 9. Estrategia de aislamiento PostgreSQL

Como cada team ya tiene una instancia PostgreSQL independiente:

```text
aislamiento principal = contenedor DB por team
```

No será obligatorio utilizar RLS como frontera entre equipos.

Sin embargo, dentro de la DB del equipo se deberá limitar:

```text
qué filas puede modificar el alumno.
```

---

# 10. Protección de M4

M4 necesita que el alumno pueda modificar un dato.

La opción preferida será:

```text
vista o tabla pedagógica
+
permisos limitados
+
trigger/check
```

para permitir únicamente cambios específicos.

Ejemplo:

```text
score
status
team display value
```

y evitar:

```text
IDs;
foreign keys;
credenciales;
schema;
datos sensibles.
```

---

# 11. Regla de UPDATE seguro

Se evaluará una de estas alternativas:

```text
A. vista actualizable limitada;
B. función SQL controlada;
C. trigger de validación;
D. grants de columna + restricciones.
```

La preferida debe ser la más simple que permita:

```text
UPDATE real
+
riesgo mínimo.
```

---

# 12. Credenciales PostgreSQL

Cada team tendrá credenciales diferentes.

No reutilizar:

```text
team01 password
en
team02.
```

No almacenar passwords en:

```text
Git;
README;
logs;
tarjetas impresas permanentes.
```

Las credenciales del alumno sí pueden mostrarse durante la misión si son desechables.

---

# 13. Rotación de credenciales

Antes de cada nueva generación de laboratorio se debe poder:

```text
generar nuevas;
inyectarlas;
actualizar team config;
invalidar las anteriores.
```

No se requiere rotación durante una sola clase.

---

# 14. Entregables del Bloque A

```text
modelo de identidades;
matriz de permisos;
roles PostgreSQL;
estrategia UPDATE seguro;
política de passwords;
flujo de generación de credenciales.
```

---

# BLOQUE B — Hardening de contenedores, terminal y gateway

# 15. Objetivo

Reducir la capacidad de un contenedor comprometido o mal utilizado.

Se cerrará:

```text
usuarios no-root;
capabilities;
no-new-privileges;
read-only;
tmpfs;
PIDs;
seccomp;
mounts;
terminal;
gateway.
```

---

# 16. Usuario no-root

Se exige:

```text
frontend → no-root cuando la imagen lo permita;
api → no-root;
toolbox → no-root;
gateway → no-root cuando sea viable;
```

PostgreSQL utilizará el usuario propio de la imagen oficial.

No ejecutar ClubLab con:

```text
root
```

si no existe necesidad técnica real.

---

# 17. Capabilities

Todos los contenedores deberán partir conceptualmente de:

```text
cap_drop:
  - ALL
```

y añadir únicamente lo imprescindible.

Evitar:

```text
NET_ADMIN
SYS_ADMIN
SYS_PTRACE
SYS_MODULE
DAC_READ_SEARCH
```

Toolbox tampoco debe recibir capabilities de red avanzadas.

---

# 18. `no-new-privileges`

Se aplicará:

```text
no-new-privileges:true
```

a todos los contenedores donde sea compatible.

Objetivo:

```text
evitar escalado mediante setuid/setgid.
```

---

# 19. Filesystem read-only

Evaluar:

```text
read_only: true
```

para:

```text
frontend;
api;
gateway.
```

Directorios que requieran escritura usarán:

```text
tmpfs
o
volúmenes específicos.
```

Toolbox podrá necesitar más flexibilidad, pero seguirá sin mounts del host.

---

# 20. Montajes prohibidos

No montar:

```text
/var/run/docker.sock
/home/docker-data
/etc
/proc host
/sys host
/dev host
/home/tulum
/var/www/pelican
```

Tampoco:

```text
hostPath arbitrario
```

en ninguna pieza accesible al alumno.

---

# 21. Límites de recursos

Mantener y hacer cumplir:

```text
RAM;
CPU;
PIDs.
```

Además evaluar:

```text
ulimits;
file descriptors;
process limits.
```

Objetivo:

```text
un team no degrada el host accidentalmente.
```

---

# 22. Seccomp

La primera versión utilizará:

```text
perfil seccomp por defecto de Docker
```

salvo incompatibilidad.

No se diseñará un perfil seccomp custom sin una razón concreta.

Esto evita sobrearquitectura.

---

# 23. Toolbox

El toolbox es el componente de mayor exposición al alumno.

Debe cumplir:

```text
usuario no-root;
sin sudo;
sin package manager útil para escalar privilegios;
sin Docker CLI;
sin socket;
sin host mounts;
sin host network;
sin capabilities peligrosas;
root filesystem preferiblemente controlado;
solo APP/DATA del team;
```

---

# 24. Terminal web

`ttyd` o equivalente deberá:

```text
requerir autenticación;
usar usuario no-root;
no permitir conexión anónima;
no exponer shell del host;
no compartir credenciales entre teams.
```

Fase 3 definirá el mecanismo final de autenticación.

---

# 25. Gateway

`clublab-gateway` es multired y debe endurecerse especialmente.

Debe cumplir:

```text
sin Docker socket;
sin NET_ADMIN;
sin privileged;
sin shell de alumno;
sin DATA networks;
read-only si es viable;
configuración generada y validada;
solo reverse proxy;
```

---

# 26. Prevención de proxy abierto

Caddy solo debe contener destinos definidos:

```text
team01-frontend;
team01-api;
team01-toolbox;
...
```

No debe aceptar:

```text
destino arbitrario;
URL enviada por usuario;
CONNECT proxy;
proxy genérico.
```

---

# 27. Entregables del Bloque B

```text
baseline de hardening;
política de users;
capabilities;
read-only/tmpfs;
mount policy;
terminal security;
gateway hardening;
resource enforcement.
```

---

# BLOQUE C — Control de acciones, secrets y aislamiento operacional

# 28. Objetivo

Proteger las operaciones que pueden cambiar estado.

Incluye:

```text
recover;
reset;
scenario load;
secrets;
tokens;
clublab;
clublabctl;
firewall;
auditoría.
```

---

# 29. Separación `clublab` / `clublabctl`

## Alumno

```text
clublab
```

permitirá únicamente:

```text
whoami
status
health
logs api
recover ranking-db
help
```

## Instructor

```text
clublabctl
```

permitirá:

```text
preflight
deploy
status
scenario
recover
reset
resources
spare
```

No compartir binarios/configuración administrativa con toolbox.

---

# 30. Recovery token

Cada team tendrá un token de recuperación restringido.

Propiedades:

```text
único;
desechable;
scope=teamXX;
action=recover-ranking-db;
sin permisos de scenario load/reset.
```

No debe ser válido para otro team.

---

# 31. Endpoint interno de recovery

La ruta interna:

```text
no se publica por gateway.
```

Solo será accesible desde la red/identidad prevista.

La API deberá validar:

```text
token;
team;
acción;
estado actual.
```

---

# 32. Idempotencia

`recover ranking-db` será seguro si se ejecuta más de una vez.

Estado normal:

```text
→ no-op
```

No:

```text
crear un nuevo fallo;
resetear DB;
reiniciar todo.
```

---

# 33. `clublabctl`

El instructor operará el host con su cuenta autorizada.

Los scripts deberán validar:

```text
team whitelist;
prefijo;
labels;
paths previstos;
estado previo.
```

Antes de una acción destructiva.

---

# 34. Guard rails obligatorios

Ejemplo conceptual para reset:

```text
team ∈ whitelist
AND
container name starts clublab-teamXX-
AND
label project=clublab
AND
label team=teamXX
```

Si cualquiera falla:

```text
ABORT.
```

---

# 35. Acciones globales prohibidas

Los scripts no deberán ejecutar:

```text
docker system prune
docker volume prune
docker network prune
docker stop $(docker ps -q)
docker rm -f $(docker ps -aq)
```

ni equivalentes globales.

---

# 36. Secrets

Los secrets se dividirán:

```text
DB app credential;
DB student credential;
terminal credential;
recovery token;
app secrets.
```

No se reutilizarán secretos productivos.

---

# 37. Almacenamiento de secrets

Para v1 se evaluará una solución simple:

```text
archivos .env con permisos restrictivos
```

fuera del repositorio.

Ejemplo:

```text
chmod 600
owner: tulum
```

No es necesario introducir Vault/KMS en esta etapa.

---

# 38. Secrets en contenedores

Evitar exponer más de lo necesario.

Ejemplo:

```text
frontend → no DB credentials
toolbox → student DB credential + recovery token limitado
api → app DB credential
gateway → sin DB credentials
```

---

# 39. Logs y secrets

Se deberá probar que no aparezcan:

```text
passwords;
recovery tokens;
Authorization headers;
cookies;
JWT secrets.
```

en:

```text
lablogs;
stdout;
errores HTTP;
UI.
```

---

# 40. Firewall

Fase 2 ya definió que el gateway publica:

```text
8211–8216
8219
```

Fase 3 deberá concretar reglas para:

```text
permitir desde red de clase;
evitar exposición innecesaria.
```

La frontera no dependerá solo de firewalld.

Se combinarán:

```text
bind específico;
Docker networks;
published ports mínimos;
firewall.
```

---

# 41. Network isolation

Se validará:

```text
APP/DATA internal;
team01 no puede resolver/acceder a team02;
gateway no accede DATA;
LAN no accede DB;
toolbox no accede host.
```

---

# 42. Host access

Desde toolbox se deberá comprobar que no puede:

```text
SSH al host por credenciales del lab;
acceder a Docker API;
acceder a servicios productivos;
montar filesystem;
usar host gateway para alcanzar recursos internos no autorizados.
```

La estrategia exacta se validará con pruebas.
---

# 43. Protección de `host.docker.internal`

No se añadirá automáticamente:

```text
host.docker.internal
```

ni:

```text
host-gateway
```

a los contenedores del alumno.

Si una librería lo agregara, deberá revisarse.

---

# 44. DNS

Toolbox debe resolver:

```text
api
database
frontend
```

de su team.

No debe poder resolver nombres de otros teams mediante una red compartida.

---

# 45. Auditoría

Registrar operaciones sensibles del instructor:

```text
deploy;
scenario load;
scenario clear;
recover;
reset;
spare switch.
```

Campos:

```text
timestamp;
actor;
team;
action;
result.
```

No registrar secrets.

---

# 46. Entregables del Bloque C

```text
modelo de tokens;
permisos del student CLI;
permisos de instructor CLI;
secret policy;
firewall policy;
guard rails;
audit policy;
network/host isolation rules.
```

---

# BLOQUE D — Pruebas de seguridad + D03 final

# 47. Objetivo

Demostrar que los controles funcionan.

No se cerrará Fase 3 solo porque el Compose “se ve seguro”.

Debe probarse.

---

# 48. Matriz mínima de pruebas

## T01 — alumno sin root

Desde toolbox:

```text
id
sudo
su
```

Esperado:

```text
usuario no-root;
sudo inexistente o denegado;
su no permite escalado.
```

---

# 49. T02 — Docker inaccesible

Probar:

```text
docker
/var/run/docker.sock
```

Esperado:

```text
no CLI útil;
socket inexistente.
```

---

# 50. T03 — host filesystem inaccesible

Intentar comprobar rutas sensibles.

Esperado:

```text
no mount;
no acceso.
```

---

# 51. T04 — lateral movement

Desde team01 toolbox intentar:

```text
team02 API;
team02 DB;
team02 terminal.
```

Esperado:

```text
FAIL.
```

---

# 52. T05 — PostgreSQL limitado

Como student:

```text
SELECT permitido
UPDATE permitido donde corresponda
DROP TABLE
ALTER TABLE
CREATE ROLE
TRUNCATE
```

Esperado:

```text
SELECT → OK
UPDATE autorizado → OK
acciones administrativas → DENIED
```

---

# 53. T06 — modificación fuera del scope

Intentar modificar:

```text
otro team_id;
columna prohibida;
identificador.
```

Esperado:

```text
DENIED
```

aunque sea dentro de su DB.

---

# 54. T07 — DB no publicada

Desde LAN:

```text
host:5432
```

Esperado:

```text
no disponible.
```

---

# 55. T08 — API interna no publicada

Desde LAN:

```text
host:3000
```

Esperado:

```text
no disponible.
```

La API solo existe mediante gateway.

---

# 56. T09 — terminal protegida

Sin credenciales:

```text
/terminal/
```

Esperado:

```text
401/denegado.
```

Con credenciales correctas:

```text
OK.
```

---

# 57. T10 — token cross-team

Usar token team01 en team02.

Esperado:

```text
DENIED.
```

---

# 58. T11 — recover scope

Ejecutar desde team01:

```text
clublab recover ranking-db
```

Esperado:

```text
solo team01.
```

No afecta:

```text
team02.
```

---

# 59. T12 — reset guard rail

Intentar pasar al script un identificador inválido.

Esperado:

```text
ABORT.
```

Sin acciones Docker parciales.

---

# 60. T13 — secrets en logs

Buscar patrones:

```text
password
token
Authorization
secret
```

Esperado:

```text
ningún secret real expuesto.
```

---

# 61. T14 — resource exhaustion básica

Desde toolbox provocar carga limitada controlada.

Esperado:

```text
el contenedor alcanza sus límites;
host y otros teams siguen respondiendo.
```

No se diseñará una prueba destructiva del host.

---

# 62. T15 — gateway lateral

Intentar utilizar gateway para alcanzar:

```text
DB;
team distinto;
destino arbitrario.
```

Esperado:

```text
imposible.
```

---

# 63. T16 — escenario no altera seguridad

Con:

```text
ranking-db-failure
```

los permisos deben ser idénticos a `normal`.

Un escenario pedagógico nunca debe desactivar controles de seguridad.

---

# 64. Criterio de aprobación

La Fase 3 solo se cierra si:

```text
todas las pruebas críticas pasan;
```

y cualquier excepción queda:

```text
documentada;
justificada;
mitigada;
```

antes de pasar a construir la aplicación.

---

# 65. D03 — estructura final

`D03_Seguridad_Aislamiento_ClubLab.md` incluirá:

```text
1. Objetivo
2. Modelo de confianza
3. Activos protegidos
4. Identidades
5. PostgreSQL
6. Credenciales
7. Terminal
8. Container hardening
9. Gateway
10. Networks
11. Student CLI
12. Instructor CLI
13. Recovery tokens
14. Secrets
15. Firewall
16. Logs
17. Auditoría
18. Matriz de pruebas
19. Riesgos
20. Decisiones congeladas
```

---

# 66. Qué NO se hará en Fase 3

No desarrollar todavía:

```text
frontend completo;
backend completo;
schema funcional completo;
Scenario Manager completo;
manuales;
tarjetas;
dashboard;
monitorización avanzada.
```

Sí se pueden crear pequeñas pruebas técnicas si son necesarias para validar un control.

---

# 67. Riesgos principales

## RS-01 — Toolbox demasiado permisivo

Mitigación:

```text
no-root;
cap drop;
sin mounts;
redes limitadas;
test de lateral movement.
```

## RS-02 — UPDATE pedagógico abre demasiado

Mitigación:

```text
usuario student específico;
vista/función/grants limitados;
tests negativos.
```

## RS-03 — Recovery token reutilizable fuera del team

Mitigación:

```text
scope;
validación server-side;
token distinto por team.
```

## RS-04 — Gateway como puente

Mitigación:

```text
sin forwarding;
sin NET_ADMIN;
routes estáticas;
tests de lateral movement.
```

## RS-05 — Secrets en logs

Mitigación:

```text
sanitización;
prueba automatizada.
```

## RS-06 — Configuración de seguridad demasiado compleja

Mitigación:

```text
preferir controles simples;
no introducir Vault/Kubernetes/SELinux custom sin necesidad.
```

---

# 68. Decisiones que deben salir cerradas

Al terminar Fase 3 debe existir respuesta concreta para:

```text
¿con qué usuario corre cada contenedor?
¿qué capabilities tiene?
¿qué filesystem puede escribir?
¿qué credenciales recibe cada servicio?
¿qué puede hacer student DB user?
¿cómo se protege M4?
¿cómo se autentica terminal?
¿cómo funciona recovery token?
¿qué puede hacer clublab?
¿qué puede hacer clublabctl?
¿qué puertos permite firewall?
¿cómo se prueba el aislamiento?
```

---

# 69. Flujo de trabajo

```text
BLOQUE A
Identidad + PostgreSQL
      ↓
BLOQUE B
Hardening + terminal + gateway
      ↓
BLOQUE C
Control + secrets + aislamiento operacional
      ↓
BLOQUE D
Pruebas + D03
```

Solo cuatro bloques.

---

# 70. Criterios de éxito de Fase 3

```text
[ ] modelo de confianza definido
[ ] identidades definidas
[ ] permisos DB definidos
[ ] UPDATE seguro definido
[ ] passwords/secrets definidos
[ ] users no-root definidos
[ ] capabilities definidas
[ ] no-new-privileges definido
[ ] read-only/tmpfs definidos
[ ] terminal auth definida
[ ] gateway hardening definido
[ ] recovery token definido
[ ] student CLI limitado
[ ] instructor CLI protegido
[ ] firewall definido
[ ] auditoría definida
[ ] matriz de pruebas ejecutable
[ ] lateral movement cubierto
[ ] secrets leakage cubierto
[ ] D03 consolidado
```

---

# 71. Primer bloque a desarrollar

# BLOQUE A — Identidad, credenciales y PostgreSQL

Se cerrará primero:

```text
usuarios por team;
usuario API;
usuario estudiante;
grants;
UPDATE seguro;
passwords;
credenciales;
migrations/init de permisos.
```

Esta base debe estar definida antes de endurecer terminal y contenedores, porque determina exactamente qué secretos y permisos necesita cada servicio.