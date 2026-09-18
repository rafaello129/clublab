# D02 — Arquitectura Técnica de ClubLab
## Infraestructura para ClubLab #01

**Proyecto:** ClubLab v1  
**Fase:** 2 — Arquitectura técnica  
**Estado:** FINAL — FASE 2 COMPLETADA  
**Entradas:** D00 + D01  
**Objetivo operativo inicial:** 4 equipos  
**Escala inicial máxima a validar:** 6 equipos + 1 spare  

---

# 1. Objetivo

Definir una infraestructura que permita ejecutar ClubLab #01 de forma:

```text
aislada;
repetible;
segura;
observable;
reseteable;
simple para alumnos;
operable por un instructor.
```

La arquitectura debe convivir con los servicios ya existentes en el servidor Tulum sin interferir con ellos.

---

# 2. Restricciones heredadas

ClubLab no utilizará ni modificará:

```text
postgres-main
whatsapp_db
database-net
whatsapp_app-net
pelican_nw
Pelican/Wings
Playit
Caddy productivo
Cloudflare Quick Tunnel existente
Tailscale Serve existente
Docker socket para alumnos
sudo
SSH al usuario tulum
```

Tampoco publicará PostgreSQL.

Los recursos ClubLab serán identificables por:

```text
prefijo
+
labels
```

---

# 3. Arquitectura general

```text
                         ALUMNOS
                            │
                            │ LAN
                            ▼
                   ┌─────────────────┐
                   │ clublab-gateway │
                   │      Caddy      │
                   └────────┬────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
      TEAM01              TEAM02              TEAMXX
```

El gateway es la única entrada desde la LAN.

---

# 4. Arquitectura por equipo

Cada team ejecuta cuatro contenedores:

```text
frontend
api
database
toolbox
```

Modelo:

```text
                  teamXX-app
                      │
        ┌─────────────┼─────────────┐
        │             │             │
    Frontend         API         Toolbox
                      │             │
                      └──────┬──────┘
                             │
                       teamXX-data
                             │
                         PostgreSQL
```

---

# 5. Frontend

Stack:

```text
React
TypeScript
Vite
```

Runtime:

```text
Nginx Alpine o equivalente ligero
```

Responsabilidades:

```text
UI;
estado normal;
loading;
error de ranking;
requests relativas a /api.
```

No requiere Node en runtime.

---

# 6. API

Stack:

```text
NestJS
TypeScript
Node.js 22
```

Runtime:

```text
node:22-bookworm-slim
```

Endpoints pedagógicos mínimos:

```text
/api/health
/api/ranking
/api/me
/api/missions
```

Separación mínima:

```text
controllers
services
repositories
```

con `RankingRepository` controlable para fault injection.

---

# 7. PostgreSQL

Decisión:

```text
1 contenedor PostgreSQL por team
```

Imagen inicial:

```text
postgres:18-bookworm
```

Cada team posee:

```text
DB propia
usuario propio
password propio
volumen propio
seed propio
```

No existe PostgreSQL compartido entre equipos.

---

# 8. Toolbox

Imagen propia:

```text
clublab/toolbox:<version>
```

Incluye:

```text
bash
curl
psql
jq
ping
getent
dig
ss
ip
nc
ttyd o equivalente
student CLI clublab
```

El usuario del shell es:

```text
no-root
```

No contiene:

```text
sudo
Docker socket
systemctl del host
host network
```

---

# 9. Redes

Cada team tiene dos redes internas:

```text
clublab-teamXX-app
clublab-teamXX-data
```

Además existe:

```text
clublab-ingress
```

solo para el gateway.

---

# 10. IPAM

Rango reservado:

```text
10.77.0.0/16
```

Asignaciones:

| Entorno | APP | DATA |
|---|---|---|
| team01 | 10.77.1.0/24 | 10.77.101.0/24 |
| team02 | 10.77.2.0/24 | 10.77.102.0/24 |
| team03 | 10.77.3.0/24 | 10.77.103.0/24 |
| team04 | 10.77.4.0/24 | 10.77.104.0/24 |
| team05 | 10.77.5.0/24 | 10.77.105.0/24 |
| team06 | 10.77.6.0/24 | 10.77.106.0/24 |
| spare | 10.77.9.0/24 | 10.77.109.0/24 |
| ingress | 10.77.250.0/24 | — |

Antes de desplegar, `preflight` deberá confirmar que no existe colisión actual.

---

# 11. Gateway

Nombre:

```text
clublab-gateway
```

Tecnología:

```text
Caddy
```

Será independiente del Caddy ya instalado en el servidor.

Funciones:

```text
publicar frontend;
publicar /api;
publicar /terminal;
proxy WebSocket;
aislar puertos internos.
```

No se conecta a redes DATA.

---

# 12. Acceso del alumno

Acceso principal:

```text
LAN
```

Tailscale:

```text
administración / contingencia
```

Cloudflare:

```text
no requerido
```

Ejemplo de sesión:

```text
http://<CLUBLAB_BIND_IP>:8211
```

No se hardcodea la IP del host.

---

# 13. Puertos

Puertos host reservados:

```text
8211 team01
8212 team02
8213 team03
8214 team04
8215 team05
8216 team06
8219 spare
```

Puertos internos:

```text
frontend 80
api      3000
database 5432
toolbox  7681
```

Solo el gateway publica puertos.

---

# 14. Rutas del gateway

Para cada team:

```text
/terminal/* → toolbox
/api/*      → api
/*          → frontend
```

Orden:

```text
terminal
api
frontend fallback
```

El frontend usa:

```text
/api/...
```

como ruta relativa.

---

# 15. Aliases

Dentro de un team:

```text
frontend
api
database
toolbox
```

Desde el gateway:

```text
team01-frontend
team01-api
team01-toolbox
...
```

Esto evita ambigüedad DNS al estar conectado a múltiples redes APP.

---

# 16. Comunicación permitida

```text
gateway → frontend
gateway → api
gateway → toolbox

api → database

toolbox → frontend
toolbox → api
toolbox → database
```

No permitida:

```text
gateway → database
frontend → database
team01 → team02
LAN → database
LAN → api:3000
LAN → toolbox:7681
```

---

# 17. Convenciones de nombres

Contenedores:

```text
clublab-team01-frontend
clublab-team01-api
clublab-team01-db
clublab-team01-toolbox
```

Redes:

```text
clublab-team01-app
clublab-team01-data
```

Volúmenes:

```text
clublab-team01-db-data
clublab-team01-lablogs
```

Compose project:

```text
clublab-team01
```

---

# 18. Labels

Obligatorias:

```text
com.clublab.project=clublab
com.clublab.team=team01
com.clublab.role=<role>
com.clublab.managed-by=clublab
com.clublab.disposable=true
```

Scripts destructivos exigirán:

```text
prefijo correcto
+
labels correctas
```

---

# 19. Despliegue parametrizado

Se utilizará:

```text
1 template Compose
+
configuración por team
```

No seis archivos manuales independientes.

Variables:

```text
TEAM_ID
TEAM_NUMBER
TEAM_NAME
DB_NAME
DB_USER
DB_PASSWORD
NETWORK_SUBNET_APP
NETWORK_SUBNET_DATA
ACCESS_PORT
ACCESS_HOSTNAME/BIND_IP
```

---

# 20. Estructura de repositorio

```text
clublab/
├── app/
│   ├── frontend/
│   └── backend/
├── database/
│   ├── migrations/
│   ├── seeds/
│   └── init/
├── infrastructure/
│   ├── compose/
│   ├── gateway/
│   ├── toolbox/
│   ├── templates/
│   └── teams/
├── scenarios/
│   ├── normal/
│   ├── ranking-db-failure/
│   └── api-down/
├── scripts/
│   ├── deploy/
│   ├── status/
│   ├── reset/
│   └── scenario/
├── docs/
└── README.md
```

---

# 21. Versionado de imágenes

Imágenes:

```text
clublab/frontend:<version>
clublab/api:<version>
clublab/toolbox:<version>
postgres:18-bookworm
caddy:<version>
```

No utilizar `latest` para una clase.

---

# 22. Persistencia

Funcional:

```text
db-data
```

Operativa efímera:

```text
lablogs
```

Frontend/API/toolbox:

```text
sin datos persistentes
```

No existirán bind mounts a rutas productivas.

---

# 23. Seeds y reset

Cada team se crea desde:

```text
migrations
+
seed determinista
```

`reset teamXX` devuelve:

```text
DB al seed;
scenario normal;
lablogs vacíos;
servicios healthy.
```

---

# 24. Recursos

Límites iniciales por team:

| Servicio | RAM | CPU |
|---|---:|---:|
| Frontend | 128 MiB | 0.25 |
| API | 512 MiB | 0.75 |
| PostgreSQL | 640 MiB | 0.75 |
| Toolbox | 256 MiB | 0.25 |
| **Total** | **~1.5 GiB** | **2.0 CPU cap** |

Objetivo:

```text
4 teams
```

Escala a probar:

```text
6 teams
```

Spare activo:

```text
solo si ensayo confirma margen suficiente.
```

---

# 25. PIDs iniciales

```text
frontend 64
api      128
database 128
toolbox  64
```

Se validarán durante ensayo.

---

# 26. Healthchecks

Frontend:

```text
HTTP /
```

API:

```text
/api/health
```

Database:

```text
pg_isready
```

Toolbox:

```text
terminal/shell ready
```

Importante:

```text
API liveness
≠
ranking functionality
```

---

# 27. Observabilidad del alumno

CLI:

```text
clublab
```

Comandos:

```text
whoami
status
health
logs api
recover ranking-db
help
```

`status` usa checks de red/servicio.

No usa Docker.

---

# 28. Observabilidad del instructor

CLI host-side:

```text
clublabctl
```

Funciones previstas:

```text
preflight
deploy
status
resources
logs
scenario load
scenario clear
recover
reset
spare
```

No existe panel administrativo web en v1.

---

# 29. Logs pedagógicos

La API producirá eventos filtrados.

Ejemplo:

```text
API       GET /api/ranking
RANKING   loading scores
DATABASE  connecting to database-broken:5432
DATABASE  host not found
API       /api/ranking -> 500
```

El alumno accede con:

```bash
clublab logs api
```

Nunca se mostrarán secretos.

---

# 30. Escenarios

Mínimos:

```text
normal
ranking-db-failure
api-down
```

`api-down` será fallback.

---

# 31. Fault injection

El escenario principal utilizará:

```text
fault injection a nivel de aplicación
```

scoped a:

```text
RankingRepository
```

No se romperá globalmente la conexión PostgreSQL.

Resultado:

```text
/api/health    200
/api/me        200
/api/missions  200
/api/ranking   500
```

---

# 32. Recover del alumno

Permitido:

```bash
clublab recover ranking-db
```

Características:

```text
solo team actual;
solo fallo ranking-db;
idempotente;
preserva DB;
no controla Docker.
```

---

# 33. Scenario Manager del instructor

Ejemplos futuros:

```bash
clublabctl scenario load team01 ranking-db-failure
clublabctl scenario clear team01
clublabctl scenario load all ranking-db-failure
```

Toda acción valida:

```text
team whitelist;
prefijo;
labels;
estado esperado.
```

---

# 34. Reset

Niveles:

```text
R1 scenario clear
R2 recover/recreate servicio
R3 reset team
```

`reset` es destructivo para el estado del team y vuelve al seed.

Nunca opera recursos sin labels ClubLab.

---

# 35. Estados operativos

```text
ABSENT
STARTING
READY
SCENARIO
RECOVERING
RESETTING
DEGRADED
FAILED
```

Se separa:

```text
infra status
```

de:

```text
scenario status
```

Ejemplo esperado:

```text
infra=healthy
scenario=ranking-db-failure
```

---

# 36. Spare

Entorno:

```text
clublab-spare
```

Puerto:

```text
8219
```

Misma arquitectura que un team.

Objetivo:

```text
continuidad pedagógica
```

si un entorno queda inutilizable.

---

# 37. Preflight

Antes de cada sesión:

```text
Docker
RAM
disco
eno1/IP
puertos
IPAM
imágenes
credenciales
team configs
gateway
seeds
escenarios
spare
```

Si falla un elemento crítico:

```text
no desplegar automáticamente.
```

---

# 38. Pruebas obligatorias

Antes del piloto:

```text
team01 toolbox → team01 api       OK
team01 toolbox → team01 db        OK
team01 toolbox → team02 api       FAIL
team01 toolbox → team02 db        FAIL
LAN → gateway                     OK
LAN → db                          FAIL
LAN → api:3000                    FAIL
gateway → team DB                 FAIL
```

También:

```text
scenario load
recoverreset
spare switch
```

---

# 39. Seguridad estructural

La arquitectura prohíbe:

```text
privileged
host network
Docker socket
sudo
SSH host
mounts productivos
DB publicada
shared DB entre teams
shared mutable volumes
```

Controles detallados pasan a Fase 3.

---

# 40. Riesgos pendientes

## R1 — Consumo real de Pelican

Puede reducir margen disponible.

Acción:

```text
benchmark antes de clase.
```

## R2 — IP LAN por DHCP

Acción:

```text
CLUBLAB_BIND_IP + preflight.
```

## R3 — Rango 10.77/16 podría colisionar en el futuro

Acción:

```text
comprobar rutas antes de crear.
```

## R4 — Gateway multired

Acción:

```text
aliases únicos;
solo reverse proxy;
sin forwarding.
```

## R5 — Terminal web

Acción:

```text
auth;
no-root;
sin host mounts;
control en Fase 3.
```

## R6 — Logs demasiado reveladores

Acción:

```text
sanitización;
ensayo pedagógico.
```

---

# 41. Decisiones congeladas

```text
4 contenedores por team
2 redes por team
PostgreSQL por team
terminal web
gateway Caddy independiente
LAN como acceso principal
Tailscale administrativo
sin Cloudflare requerido
10.77.0.0/16 para IPAM de diseño
8211–8216 y 8219
fault injection scoped a ranking
student CLI clublab
instructor CLI clublabctl
reset por team
spare
```

Cambios posteriores deberán justificarse mediante prueba técnica o ensayo.

---

# 42. Requisitos para Fase 3

La siguiente fase deberá concretar:

```text
credenciales;
usuarios;
PostgreSQL grants;
RLS o DB isolation complementario;
auth de ttyd;
recovery tokens;
capabilities;
no-new-privileges;
read-only FS;
tmpfs;
secrets;
firewall;
protección del gateway;
validación de lateral movement;
```

---

# 43. Requisitos para Fase 4

La aplicación deberá implementar:

```text
UI ClubLab;
endpoints;
schema;
seeds;
RankingRepository scenario-aware;
lab logging;
health endpoint;
error state del ranking.
```

---

# 44. Requisitos para Fase 5

Construir:

```text
clublab
clublabctl
scenario state
normal
ranking-db-failure
api-down
recover
reset
preflight
audit
spare
```

---

# 45. Criterios de cierre de Fase 2

```text
[x] arquitectura base
[x] stack por team
[x] redes
[x] IPAM
[x] gateway
[x] acceso
[x] terminal
[x] puertos
[x] aislamiento
[x] persistencia
[x] recursos
[x] healthchecks
[x] logs
[x] escenarios
[x] recover
[x] reset
[x] operación del instructor
[x] spare
[x] riesgos
[x] validación D00
[x] validación D01
```

# FASE 2 — COMPLETADA

---

# 46. Arquitectura final resumida

```text
                          LAN
                           │
                           ▼
                  clublab-gateway
                       Caddy
                           │
          ┌────────────────┼────────────────┐
          │                │                │
     team01-app       team02-app       teamXX-app
          │
   ┌──────┼────────────┐
   │      │            │
Frontend API        Toolbox
          │            │
          └────┬───────┘
               │
          team01-data
               │
            PostgreSQL
```

Control:

```text
Alumno
→ clublab

Instructor
→ clublabctl
```

La infraestructura resultante está lista para pasar de diseño a controles concretos de seguridad.