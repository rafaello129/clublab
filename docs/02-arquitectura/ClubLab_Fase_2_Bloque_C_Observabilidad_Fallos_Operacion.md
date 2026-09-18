# ClubLab — Fase 2 / Bloque C
## Observabilidad, fallos y operación

**Proyecto:** ClubLab v1  
**Fase:** 2 — Arquitectura técnica  
**Bloque:** C  
**Estado:** CERRADO PARA DISEÑO v1  
**Dependencias:** Fase 0 + D01 + Fase 2/Bloques A–B

---

# 1. Propósito

Este bloque define cómo se observará, romperá, diagnosticará, recuperará y reseteará cada entorno ClubLab.

Debe responder:

```text
¿Cómo sabe el alumno qué componentes siguen vivos?
¿Cómo obtiene logs sin acceso a Docker?
¿Cómo se inyecta el fallo del ranking?
¿Cómo recupera el alumno el escenario?
¿Qué puede hacer únicamente el instructor?
¿Cómo se resetea un equipo?
¿Cómo se observa toda la clase?
¿Qué ocurre si un entorno queda inutilizable?
```

La arquitectura debe permitir una experiencia real sin convertir al alumno en administrador del host.

---

# 2. Principio central

Se separarán dos planos:

```text
PLANO DEL ALUMNO
→ observa y opera únicamente su equipo

PLANO DEL INSTRUCTOR
→ despliega, inyecta escenarios, resetea y supervisa
```

Nunca se mezclan credenciales ni permisos.

---

# 3. Plano del alumno

El alumno interactuará mediante:

```text
navegador
terminal web del toolbox
```

Desde el toolbox tendrá un pequeño CLI:

```text
clublab
```

Comandos previstos:

```text
clublab whoami
clublab status
clublab health
clublab logs api
clublab recover ranking-db
```

No tendrá:

```text
docker
docker compose
systemctl
sudo
clublab scenario load
clublab reset
```

---

# 4. Plano del instructor

El instructor utilizará una CLI separada en el host:

```text
clublabctl
```

Comandos conceptuales:

```text
clublabctl preflight
clublabctl status all
clublabctl status team01

clublabctl deploy team01
clublabctl deploy all

clublabctl scenario load team01 ranking-db-failure
clublabctl scenario clear team01

clublabctl logs team01 api
clublabctl recover team01
clublabctl reset team01

clublabctl spare status
clublabctl spare start
```

Las acciones definitivas se implementarán en Fase 5.

---

# 5. Ubicación del control del instructor

Para ClubLab v1 se selecciona:

> **CLI host-side, no panel web administrativo y no contenedor con Docker socket.**

Motivo:

```text
menor superficie de ataque;
menos componentes;
más fácil auditar;
no exponer Docker API;
no montar /var/run/docker.sock en servicios web.
```

Los alumnos nunca ejecutarán `clublabctl`.

---

# 6. Ubicación prevista del runtime de ClubLab

Rutas conceptuales futuras:

```text
/home/tulum/apps/clublab
/home/tulum/infra/clublab
/home/tulum/backups/clublab
```

Estas rutas fueron clasificadas como disponibles para ClubLab en Fase 0.

Estructura operativa sugerida:

```text
/home/tulum/infra/clublab/
├── config/
├── teams/
├── runtime/
├── audit/
└── scripts/
```

No se implementa todavía.

---

# 7. Capas de observabilidad

Se utilizarán tres niveles diferentes:

```text
NIVEL 1 — experiencia del usuario
NIVEL 2 — observabilidad del equipo
NIVEL 3 — observabilidad del instructor
```

Cada nivel expone únicamente lo necesario.

---

# 8. Nivel 1 — Experiencia del usuario

Herramientas:

```text
interfaz web
DevTools
Network
HTTP status
Response
```

Permite descubrir:

```text
qué funciona;
qué request falla;
qué status devuelve;
qué parte de la UI se degrada.
```

No expone información administrativa.

---

# 9. Nivel 2 — Observabilidad del equipo

Disponible desde toolbox.

Incluye:

```text
clublab status
clublab health
clublab logs api
curl
psql
```

Debe permitir diagnosticar M5–M7 sin acceso al host.

---

# 10. Nivel 3 — Observabilidad del instructor

`clublabctl` podrá consultar:

```text
estado de contenedores;
Docker health;
CPU;
RAM;
escenario cargado;
gateway;
redes;
volúmenes;
últimas acciones;
logs completos permitidos.
```

El alumno no ve este nivel.

---

# 11. `clublab whoami`

Salida conceptual:

```text
ClubLab Team: team03
Role environment: student
API: api:3000
Database: database:5432
```

No mostrar:

```text
host IP sensible;
Docker container IDs;
credenciales;
otros teams.
```

Objetivo:

```text
reducir confusión cuando se usan varios entornos.
```

---

# 12. `clublab status`

Debe responder una pregunta:

> **¿Qué componentes de mi equipo parecen activos?**

Ejemplo normal:

```text
ClubLab — team01

frontend   reachable
api        reachable
database   reachable
toolbox    ready
```

Durante el incidente principal:

```text
frontend   reachable
api        reachable
database   reachable
toolbox    ready
```

Esto es intencional.

El fallo del ranking no debe convertir un servicio entero en `down`.

---

# 13. Cómo calcula `status`

El CLI del toolbox no consulta Docker.

Realiza pruebas desde dentro del team:

```text
frontend
→ HTTP a frontend interno

api
→ /api/health

database
→ pg_isready

toolbox
→ proceso local
```

Por tanto:

```text
status
≠
docker ps
```

Esto mantiene el aislamiento.

---

# 14. `clublab health`

Será un poco más detallado, pero no resolverá automáticamente el incidente.

Ejemplo normal:

```text
API liveness        OK
Database readiness  OK
Frontend reach      OK
```

Ejemplo incidente:

```text
API liveness        OK
Database readiness  OK
Frontend reach      OK
```

No incluir:

```text
“RankingRepository DB_HOST incorrecto”
```

---

# 15. Liveness vs funcionalidad

Se congela una distinción importante:

```text
SERVICIO VIVO
≠
TODAS SUS FUNCIONES CORRECTAS
```

Por eso:

```text
/api/health
```

será principalmente un liveness check de API.

Puede devolver:

```http
200 OK
```

aunque:

```text
/api/ranking
```

falle.

Esto es necesario para M6/M7.

---

# 16. Healthchecks Docker del instructor

A nivel Docker se requerirán:

```text
frontend healthcheck
api healthcheck
database healthcheck
toolbox healthcheck básico
```

Objetivo:

```text
operación;
arranque ordenado;
reset;
preflight.
```

No son necesariamente los mismos checks que se enseñan a alumnos.

---

# 17. Healthcheck de frontend

Conceptualmente:

```text
HTTP GET /
```

desde el contenedor o red.

Debe validar:

```text
Nginx responde;
build existe.
```

No necesita comprobar API.

---

# 18. Healthcheck de API

Conceptualmente:

```text
GET /api/health
```

Debe comprobar:

```text
proceso Node vivo;
router funcionando;
event loop respondiendo.
```

No debe convertir un fallo scoped de ranking en `unhealthy`.

---

# 19. Healthcheck de PostgreSQL

Utilizar:

```text
pg_isready
```

con credenciales/configuración del propio team.

Debe indicar:

```text
PostgreSQL acepta conexiones.
```

---

# 20. Healthcheck de toolbox

Puede ser mínimo:

```text
terminal web activa
+
shell disponible
```

No debe depender de API o DB para marcar toolbox como sano.

---

# 21. Logs del alumno

M7 necesita logs, pero los alumnos no usarán:

```text
docker logs
```

Se diseñará un:

> **log pedagógico del API**

accesible con:

```bash
clublab logs api
```

---

# 22. Fuente del log pedagógico

La API generará un stream estructurado específico de laboratorio.

Ejemplos:

```text
20:14:03 API       GET /api/ranking
20:14:03 RANKING   loading scores
20:14:03 DATABASE  connecting to database-broken:5432
20:14:03 DATABASE  host not found
20:14:03 API       GET /api/ranking -> 500
```

Este stream debe ser real respecto al escenario que se está ejecutando.

---

# 23. Log completo vs log pedagógico

La API puede tener:

```text
stdout/stderr técnico completo
```

para instructor.

Y en paralelo:

```text
eventos pedagógicos filtrados
```

para alumnos.

No se entregará un stack trace de 200 líneas como única pista.

---

# 24. Almacenamiento del log pedagógico

Se utilizará un recurso efímero y desechable por equipo.

Nombre conceptual:

```text
clublab-team01-lablogs
```

Podrá implementarse como:

```text
named volume efímero
```

montado:

```text
API     → escritura
Toolbox → solo lectura
```

No será almacenamiento de negocio.

Se limpia en reset.

---

# 25. Ajuste a la política de persistencia del Bloque A

La decisión del Bloque A sigue vigente:

```text
PostgreSQL = única persistencia de negocio
```

El volumen de logs:

```text
no contiene datos funcionales;
es desechable;
se puede eliminar sin perder estado de la aplicación.
```

Por tanto se clasifica como:

```text
persistencia operativa efímera
```

y no como almacenamiento de aplicación.

---

# 26. Sanitización obligatoria de logs

Nunca escribir en logs del alumno:

```text
DB_PASSWORD;
JWT secret;
tokens;
cookies;
headers Authorization completos;
connection strings con password;
variables de entorno completas;
rutas del host;
datos productivos.
```

Sí se puede mostrar:

```text
nombre lógico de servicio;
endpoint;
status;
hostname ficticio del escenario;
tipo de error;
timestamp.
```

---

# 27. Rotación de logs

Los logs pedagógicos deben ser pequeños.

Objetivo:

```text
máximo aproximado 5–10 MiB por team
```

o política equivalente.

El reset los elimina.

No se pretende conservar historial de semanas.

---

# 28. `clublab logs api`

Salida por defecto:

```text
últimas 30–50 líneas
```

Opciones futuras:

```text
clublab logs api --tail 20
clublab logs api --follow
```

No permitir rutas arbitrarias.

---

# 29. Escenarios

Fase 2 congela tres escenarios mínimos:

```text
normal
ranking-db-failure
api-down
```

`api-down` es fallback.

La implementación detallada se realiza en Fase 5.

---

# 30. Escenario `normal`

Estado:

```text
frontend = healthy
api = healthy
database = healthy

/api/health = 200
/api/ranking = 200
/api/me = 200
/api/missions = 200
```

Es el estado inicial y final.

---

# 31. Escenario `ranking-db-failure`

Requisito funcional:

```text
frontend = healthy
api = healthy
database = healthy

/api/health = 200
/api/me = 200
/api/missions = 200
/api/ranking = 500
```

Debe producir logs suficientes para descubrir:

```text
fallo de dependencia del ranking
```

sin revelar directamente la solución.

---

# 32. Mecanismo de fault injection seleccionado

La Fase 2 define el enfoque:

> **Fault injection a nivel de aplicación, scoped al flujo de ranking.**

No se romperá globalmente:

```text
DB_HOST de toda la API
```

porque dañaría otras funciones.

---

# 33. Adapter de fallo

El backend deberá incluir un punto controlable alrededor de:

```text
RankingRepository
```

Conceptualmente:

```text
RankingService
      │
      ▼
ScenarioAwareRankingRepository
      │
      ├── normal → conexión real
      │
      └── ranking-db-failure
             → dependencia falsa/inválida
             → error controlado
```

Esto mantiene:

```text
UserRepository normal
MissionRepository normal
```

---

# 34. Realismo del fallo

Aunque se inyecte a nivel de aplicación, la experiencia debe producir un error técnicamente creíble.

Ejemplo:

```text
attempt host:
database-broken

error:
ENOTFOUND
```

La API devolverá:

```text
500 genérico
```

y el log pedagógico mostrará la capa de dependencia.

---

# 35. Estado del escenario

La arquitectura requiere un estado de escenario por team:

```text
team01 → normal
team02 → normal
team03 → ranking-db-failure
```

No habrá estado global único.

---

# 36. Control del estado de escenario

Solo el plano del instructor puede:

```text
cargar escenario;
cambiar escenario arbitrariamente;
forzar api-down.
```

Los alumnos no pueden ejecutar:

```text
scenario load
```

---

# 37. Recuperación del alumno

Para cumplir D01, el alumno sí podrá ejecutar una acción estrecha:

```bash
clublab recover ranking-db
```

Esta acción:

```text
solo aplica al team actual;
solo limpia ranking-db-failure;
no puede cargar otro escenario;
no controla Docker;
no modifica otros teams.
```

---

# 38. Mecanismo conceptual de `recover`

El toolbox llamará una operación interna y autenticada del propio entorno.

Conceptualmente:

```text
Toolbox
  │
  │ recovery token scoped
  ▼
API internal lab-control
  │
  ▼
scenario state → normal
```

La ruta de control:

```text
NO se publica por gateway
```

y no forma parte de la API pública.

---

# 39. Token de recuperación

Cada equipo tendrá un token:

```text
desechable;
limitado a recover;
diferente por team.
```

No permitirá:

```text
reset;
load scenario;
leer secretos;
operar Docker.
```

Fase 3 definirá almacenamiento y permisos concretos.

---

# 40. Ventaja del recover interno

El estudiante puede realmente recuperar:

```text
su propio fallo
```

sin recibir:

```text
Docker socket;
sudo;
control del host.
```

Además, la recuperación puede explicar:

```text
“Restaurando dependencia de ranking…”
```

sin ser un botón completamente opaco.

---

# 41. `api-down` como fallback

Si se utiliza:

```text
API container = stopped
```

el endpoint de recovery del propio API no puede funcionar.

Por ello:

```text
api-down
```

será un escenario instructor-assisted.

El equipo diagnostica.

Después:

```text
instructor
→ clublabctl recover teamXX
```

o una capa de control futura.

Esto es aceptable porque `api-down` no es el escenario principal.

---

# 42. `clublabctl scenario load`

Ejemplo:

```bash
clublabctl scenario load team01 ranking-db-failure
```

Debe:

```text
validar team;
validar escenario;
confirmar recursos;
activar únicamente team01;
registrar acción;
verificar síntoma esperado.
```

No debe:

```text
operar todos los contenedores Docker;
hacer prune;
tocar recursos sin label ClubLab.
```

---
# 43. Verificación automática al cargar escenario

Después de cargar:

```text
ranking-db-failure
```

el instructor CLI debe comprobar:

```text
/api/health = 200
/api/ranking = 500
DB = ready
```

Si no se cumple:

```text
escenario = FAILED
```

y no debería iniciarse M6 hasta corregirlo.

---

# 44. `clublabctl scenario clear`

Debe devolver el team a:

```text
normal
```

y validar:

```text
/api/health = 200
/api/ranking = 200
```

sin resetear necesariamente los datos modificados durante M4.

---

# 45. Diferencia entre recover y reset

## Recover

Objetivo:

```text
reparar el incidente actual
```

Preserva:

```text
datos del alumno;
score modificado;
evidencias;
DB.
```

Ejemplo:

```text
ranking-db-failure → normal
```

---

## Reset

Objetivo:

```text
volver todo el team al estado inicial
```

Puede destruir:

```text
cambios en DB;
logs;
estado de escenario;
sesión.
```

Vuelve a:

```text
seed inicial.
```

---

# 46. Niveles de recuperación del instructor

Se definen tres niveles:

```text
R1 — scenario clear
R2 — recover/recreate service
R3 — reset team
```

Orden preferido:

```text
R1
↓
R2
↓
R3
```

No empezar con R3.

---

# 47. `clublabctl reset team01`

Debe:

```text
validar Team ID;
detener recursos ClubLab de team01;
eliminar únicamente volúmenes desechables del team;
recrear DB data;
aplicar migrations;
aplicar seed;
limpiar lablogs;
dejar scenario=normal;
arrancar servicios;
esperar healthchecks;
validar endpoints.
```

No toca:

```text
team02;
producción;
otras redes;
otros volúmenes.
```

---

# 48. Reset destructivo y confirmación

Para un solo team:

```text
clublabctl reset team01
```

puede pedir confirmación clara:

```text
RESET team01 and restore seed? [y/N]
```

Para:

```text
reset all
```

se exigirá una confirmación más fuerte.

Ejemplo:

```text
--confirm-all
```

y listado previo de teams afectados.

---

# 49. Guard rails del `clublabctl`

Toda acción destructiva deberá validar:

```text
TEAM_ID permitido;
prefijo clublab-;
labels ClubLab;
scope esperado.
```

Si un recurso no cumple:

```text
ABORTAR.
```

No “adivinar”.

---

# 50. Teams válidos iniciales

Whitelist:

```text
team01
team02
team03
team04
team05
team06
spare
```

No aceptar strings arbitrarios como:

```text
../../
prod
postgres-main
whatsapp-backend
```

---

# 51. Auditoría de acciones

El control del instructor deberá registrar:

```text
timestamp;
usuario;
acción;
team;
escenario;
resultado.
```

Ejemplo:

```text
2026-09-17 18:10
scenario.load
team03
ranking-db-failure
success
```

No registrar secretos.

---

# 52. Observabilidad del instructor

`clublabctl status all` deberá producir una vista compacta:

```text
TEAM    FRONT   API   DB   TOOLBOX   SCENARIO
01      OK      OK    OK   OK        normal
02      OK      OK    OK   OK        normal
03      OK      OK    OK   OK        ranking-db-failure
04      OK      OK    OK   OK        normal
```

Opcionalmente:

```text
RAM
CPU
```

en modo detallado.

---

# 53. Recursos del host

El instructor debe poder ejecutar:

```text
clublabctl resources
```

o equivalente para ver:

```text
RAM total ClubLab;
CPU actual;
contenedores por team;
volúmenes;
```

El objetivo es detectar si Pelican u otros servicios están consumiendo más de lo esperado antes de iniciar.

---

# 54. Fuente de métricas

El plano instructor puede usar:

```text
docker inspect;
docker stats --no-stream;
health status;
labels.
```

Siempre filtrado por:

```text
com.clublab.project=clublab
```

y nunca mostrando todos los servicios al alumno.

---

# 55. Dashboard del instructor

No se construirá en v1.

La primera versión utilizará:

```text
CLI
```

porque:

```text
menos trabajo;
menos superficie;
más fácil auditar;
suficiente para 2–6 equipos.
```

Un dashboard puede añadirse si la operación real lo justifica.

---

# 56. Preflight completo

Antes de desplegar la clase:

```bash
clublabctl preflight
```

deberá revisar conceptualmente:

```text
Docker activo;
RAM disponible;
disco disponible;
eno1/IP;
puertos 8211–8216/8219;
rango 10.77.0.0/16;
imágenes disponibles;
configuración;
credenciales;
gateway;
seeds;
escenarios;
spare;
```

---

# 57. Resultado de preflight

Ejemplo:

```text
Docker              OK
Host memory          OK
Disk                 OK
LAN bind             OK
Gateway ports        OK
IPAM                 OK
Images               OK
Team configs         OK
Spare                READY

PRECHECK PASSED
```

Si algo crítico falla:

```text
PRECHECK FAILED
```

y no se despliega automáticamente.

---

# 58. Prueba previa al incidente

Antes del minuto 70, el instructor deberá ejecutar:

```text
clublabctl status all
```

y verificar:

```text
todos los teams normal;
ranking 200;
DB ready.
```

Después:

```text
scenario load
```

por team.

---

# 59. Activación sincronizada del incidente

Se deberá soportar:

```bash
clublabctl scenario load all ranking-db-failure
```

pero internamente deberá iterar explícitamente sobre:

```text
team01…team06
```

y validar cada resultado.

No usar:

```text
docker restart $(docker ps -q)
```

ni ninguna operación global equivalente.

---

# 60. Fallo de activación en un solo team

Si cinco teams cargan el escenario y uno falla:

```text
no romper los cinco correctos.
```

El instructor podrá:

```text
reintentar solo ese team;
usar spare;
usar fallback.
```

El CLI deberá reportar:

```text
5 success
1 failed
```

---

# 61. Entorno `spare`

El spare utilizará exactamente:

```text
frontend
api
database
toolbox
```

y las mismas imágenes.

Acceso:

```text
gateway port 8219
```

Puede permanecer:

```text
desplegado y detenido
```

o:

```text
desplegable rápidamente.
```

La decisión operativa preferida será tenerlo:

```text
precreado y healthy antes de clase
```

si el consumo medido lo permite.

---

# 62. Uso del spare

Si un team queda inutilizable:

```text
1. instructor entrega URL 8219;
2. equipo usa credenciales spare;
3. continúa la misión;
4. team original puede repararse sin bloquear clase.
```

No es necesario que el spare imite exactamente todos los cambios realizados por el equipo.

Su objetivo es continuidad pedagógica.

---

# 63. Evidencia de reset

Después de cualquier reset:

```text
frontend = healthy
api = healthy
db = healthy
toolbox = healthy
scenario = normal
ranking = 200
```

Si alguno falla:

```text
reset = FAILED
```

y el entorno no se considera listo.

---

# 64. Start order

Orden recomendado:

```text
database
↓ healthy
api
↓ healthy
frontend
toolbox
gateway routes available
```

El toolbox puede arrancar antes, pero la experiencia no se marca `READY` hasta que el stack esté sano.

---

# 65. Stop order

No existe una dependencia pedagógica estricta.

Para reset controlado:

```text
gateway route remains
services recycle
```

El alumno puede ver temporalmente error, pero el reset se realiza antes de iniciar o como contingencia.

---

# 66. Estado formal de un team

Se utilizarán estados conceptuales:

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

Ejemplo:

```text
READY
→ scenario load
→ SCENARIO
→ student recover
→ READY
```

---

# 67. Estado `DEGRADED`

Significa:

```text
stack parcialmente operativo;
no cumple experiencia normal;
puede diagnosticarse.
```

No debe confundirse automáticamente con el escenario pedagógico.

El CLI instructor mostrará por separado:

```text
infra status
scenario status
```

---

# 68. Diferencia entre fallo pedagógico y fallo accidental

Ejemplo:

```text
scenario=ranking-db-failure
infra=healthy
```

→ esperado.

Pero:

```text
scenario=normal
api container=unhealthy
```

→ fallo accidental.

Esta separación es esencial para no confundir al instructor.

---

# 69. Alertas

No se implementará un sistema complejo de alerting.

Para v1 bastará:

```text
preflight;
status all;
healthchecks;
cronómetro del instructor.
```

ClubLab no necesita Prometheus/Grafana para seis equipos.

---

# 70. Herramientas que explícitamente NO añadimos

Para evitar sobrearquitectura:

```text
Kubernetes
Prometheus
Grafana
Loki
ELK
Portainer para alumnos
Docker socket proxy
SSH multiusuario al host
```

Pueden evaluarse en el futuro si existe necesidad real.

---

# 71. Compatibilidad con el incidente

La arquitectura operativa resultante cumple:

```text
alumno ve 500;
API sigue viva;
DB sigue viva;
otros endpoints siguen vivos;
logs muestran dependencia;
alumno puede recover;
instructor puede reset;
otro team no se afecta.
```

Esto satisface D01.

---

# 72. Seguridad del recovery del alumno

La acción de estudiante debe ser:

```text
idempotente.
```

Ejecutar:

```bash
clublab recover ranking-db
```

cuando ya está normal debe devolver algo como:

```text
No active ranking-db failure.
Environment already healthy.
```

No debe causar un fallo nuevo.

---

# 73. Seguridad de los comandos del alumno

El binario/script `clublab` no aceptará:

```text
paths arbitrarios;
container names;
shell commands;
team IDs externos;
URLs arbitrarias para control.
```

Solo subcomandos definidos.

---

# 74. Interfaz de ayuda

Desde toolbox:

```bash
clublab help
```

mostrará únicamente herramientas pedagógicas disponibles.

Ejemplo:

```text
whoami
status
health
logs api
recover ranking-db
```

No documentará comandos del instructor.

---

# 75. Decisiones cerradas del Bloque C

### DC2-01
Habrá dos planos separados: alumno e instructor.

### DC2-02
El alumno utilizará `clublab` desde toolbox.

### DC2-03
El instructor utilizará `clublabctl` host-side.

### DC2-04
No habrá panel administrativo web en v1.

### DC2-05
No se montará Docker socket en servicios web.

### DC2-06
`clublab status` realizará checks de red/servicio, no `docker ps`.

### DC2-07
`/api/health` será liveness y podrá seguir 200 durante el incidente.

### DC2-08
Existirá un log pedagógico filtrado del API.

### DC2-09
El log pedagógico usará almacenamiento efímero por team.

### DC2-10
Escenarios mínimos:

```text
normal
ranking-db-failure
api-down
```

### DC2-11
El incidente principal usará fault injection scoped a ranking.

### DC2-12
El alumno podrá ejecutar únicamente `recover ranking-db`.

### DC2-13
El escenario se carga solo desde plano instructor.

### DC2-14
Recover preservará datos de la sesión.

### DC2-15
Reset devolverá el team al seed inicial.

### DC2-16
Todo reset se valida con healthchecks y endpoints.

### DC2-17
`clublabctl` operará solo recursos con prefijo + labels ClubLab.

### DC2-18
Existirá auditoría de acciones del instructor.

### DC2-19
`status all` será la vista principal de operación durante clase.

### DC2-20
El spare se mantendrá listo antes de clase si los recursos lo permiten.

### DC2-21
No se introducirán Kubernetes ni stacks de observabilidad pesados.

---

# 76. Arquitectura operativa congelada

```text
                       INSTRUCTOR
                           │
                           ▼
                      clublabctl
                     (host-side)
                           │
              ┌────────────┼────────────┐
              │            │            │
           Team01        Team02       TeamXX
              │
              │ scenario / reset / inspect
              ▼

ALUMNO
   │
   ▼
Gateway
   │
   ├──── Frontend
   │
   └──── Terminal Web
              │
              ▼
           Toolbox
              │
              ├── clublab status
              ├── clublab health
              ├── clublab logs api
              └── clublab recover ranking-db
                    │
                    ▼
              Team-local control only
```

---

# 77. Lo que pasa al Bloque D

El Bloque D cerrará la Fase 2 mediante:

```text
validación contra D00;
validación contra D01;
mapa final de servicios;
mapa final de redes;
mapa de puertos;
presupuesto consolidado;
riesgos;
preflight arquitectónico;
D02 final.
```

No se diseñarán más componentes grandes salvo que la validación encuentre una incompatibilidad real.

---

# 78. Criterios de aceptación

```text
[x] plano alumno definido
[x] plano instructor definido
[x] student CLI definido
[x] instructor CLI definido
[x] healthchecks definidos
[x] liveness separado de funcionalidad
[x] logs pedagógicos definidos
[x] sanitización definida
[x] escenarios mínimos definidos
[x] fault injection definido
[x] recover del alumno definido
[x] recover del instructor definido
[x] reset definido
[x] guard rails definidos
[x] auditoría definida
[x] status all definido
[x] preflight definido
[x] activación sincronizada definida
[x] spare definido
[x] estados de team definidos
[x] sobrearquitectura descartada
```

# BLOQUE C — COMPLETADO