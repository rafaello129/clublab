# ClubLab — Plan de Fase 5
## Scenario Manager, operación y automatización del laboratorio

**Proyecto:** ClubLab v1  
**Fase:** 5  
**Nombre:** Scenario Manager y operación del laboratorio  
**Estado:** PLAN DE TRABAJO  
**Entradas principales:**  
- `D00_Estado_Base_Servidor_ClubLab.md`
- `D01_Diseno_Experiencia_ClubLab_01.md`
- `D02_Arquitectura_Tecnica_ClubLab.md`
- `D03_Seguridad_Aislamiento_ClubLab.md`
- `APP01_Modelo_Dominio_y_Datos.md`
- `APP02_Backend_API.md`
- `APP03_Frontend_ClubLab.md`
- `APP04_Aplicacion_Integrada.md`

**Entregables principales previstos:**  
- `D04_Scenario_Manager_y_Operacion_ClubLab.md`
- `SYS01_CLI_clublab.md`
- `SYS02_CLI_clublabctl.md`
- `SYS03_Preflight_Reset_Recovery.md`

---

# 1. Propósito de la Fase 5

La Fase 5 construirá la capa operativa que permite ejecutar ClubLab como un laboratorio real y repetible.

Hasta ahora tenemos:

```text
pedagogía definida;
arquitectura definida;
seguridad definida;
aplicación definida.
```

Falta convertir todo eso en operaciones simples.

La pregunta principal será:

> **¿Cómo puede el instructor levantar, romper, diagnosticar, recuperar y resetear un entorno sin tocar manualmente Docker ni arriesgar servicios productivos?**

---

# 2. Objetivo general

La fase deberá producir dos herramientas claramente separadas:

```text
clublab
```

para alumnos, y:

```text
clublabctl
```

para instructor.

Además deberá automatizar:

```text
preflight;
deploy;
status;
scenario load;
scenario clear;
recover;
reset;
spare;
logs;
audit.
```

---

# 3. Principio de operación

El instructor no debería necesitar durante la clase:

```text
recordar nombres de contenedores;
recordar subnets;
hacer docker inspect manual;
editar env;
recrear DB a mano;
buscar qué team falló.
```

La herramienta debe traducir operaciones pedagógicas a acciones técnicas seguras.

---

# 4. Restricciones heredadas

La Fase 5 deberá respetar obligatoriamente:

```text
no tocar recursos productivos;
no usar prune global;
no usar Docker socket dentro de contenedores alumno;
no publicar DB;
no publicar API directamente;
no usar redes productivas;
no compartir state entre teams;
no usar secrets productivos;
no permitir reset/scenario desde alumno;
```

---

# 5. Decisión estructural

La fase se divide en solo **cuatro bloques**:

```text
BLOQUE A
Modelo operativo + CLI del alumno + CLI del instructor

BLOQUE B
Scenario Manager + recovery + reset

BLOQUE C
Preflight + status + logs + spare + auditoría

BLOQUE D
Integración operativa + validación + D04 final
```

---

# BLOQUE A — Modelo operativo y CLIs

# 6. Objetivo

Definir exactamente:

```text
qué comandos existen;
quién puede ejecutarlos;
qué reciben;
qué muestran;
qué nunca hacen.
```

---

# 7. CLI del alumno — `clublab`

Disponible únicamente dentro de:

```text
toolbox.
```

Comandos previstos:

```text
clublab help
clublab whoami
clublab status
clublab health
clublab logs api
clublab recover ranking-db
```

No incluir:

```text
reset
scenario
deploy
docker
resources
spare
```

---

# 8. `clublab whoami`

Debe mostrar:

```text
Team ID
Team name
logical API host
logical DB host
toolbox identity
```

Ejemplo:

```text
Team: team01
Name: Equipo 01
API: api:3000
Database: database:5432
Toolbox user: student
```

No mostrar:

```text
passwords;
tokens;
container IDs;
host IPs;
other teams.
```

---

# 9. `clublab status`

Objetivo:

```text
mostrar si los componentes del entorno son alcanzables.
```

Checks:

```text
frontend HTTP
api /api/health
database pg_isready
toolbox local
```

Salida conceptual:

```text
Frontend   OK
API        OK
Database   OK
Toolbox    OK
```

Durante `ranking-db-failure`:

```text
Frontend   OK
API        OK
Database   OK
Toolbox    OK
```

Porque el fallo es funcional, no de liveness.

---

# 10. `clublab health`

Mostrará un poco más de detalle.

Ejemplo:

```text
API /api/health              200
Database accepting           yes
Ranking endpoint             500
```

Pero no debe decir:

```text
scenario=ranking-db-failure.
```

La herramienta ayuda a observar, no resuelve el diagnóstico.

---

# 11. `clublab logs api`

Debe mostrar:

```text
últimas 30–50 líneas
```

del:

```text
lab-events.jsonl.
```

Con render human-readable:

```text
20:14:03 API       GET /api/ranking
20:14:03 RANKING   Loading ranking scores
20:14:03 DATABASE  Host database-broken could not be resolved
20:14:03 API       GET /api/ranking -> 500
```

No permitir:

```text
ruta arbitraria;
servicio arbitrario;
team arbitrario.
```

---

# 12. `clublab recover ranking-db`

Debe:

```text
usar recovery token del propio team;
llamar endpoint interno;
mostrar resultado;
ser idempotente.
```

Salida posible:

```text
Recovery completed.
Ranking dependency restored.
```

Si ya está normal:

```text
Environment already healthy.
```

---

# 13. CLI del instructor — `clublabctl`

Host-side.

Subcomandos previstos:

```text
clublabctl preflight
clublabctl deploy
clublabctl status
clublabctl resources
clublabctl logs
clublabctl scenario
clublabctl recover
clublabctl reset
clublabctl spare
clublabctl audit
```

---

# 14. Targeting

Toda operación se hará sobre:

```text
team01
team02
team03
team04
team05
team06
spare
all
```

Pero:

```text
all
```

solo en comandos donde tenga sentido y con confirmación si es destructivo.

---

# 15. Resolución de recursos

`clublabctl` localizará recursos por:

```text
Team ID
+
labels
+
prefix.
```

Nunca por:

```text
“primer container que coincida”.
```

---

# 16. Inventario de teams

Se definirá un inventario estructurado.

Ejemplo conceptual:

```yaml
teams:
  team01:
    access_port: 8211
    app_subnet: 10.77.1.0/24
    data_subnet: 10.77.101.0/24
  team02:
    access_port: 8212
    app_subnet: 10.77.2.0/24
    data_subnet: 10.77.102.0/24
```

No incluir secrets en el inventario versionado.

---

# 17. Ubicación de herramientas

Propuesta:

```text
/home/tulum/infra/clublab/bin/clublabctl
/home/tulum/infra/clublab/scripts/
```

El `clublab` del alumno vive dentro de la imagen toolbox.

---

# 18. Entregables del Bloque A

```text
command map;
CLI contracts;
output formats;
exit codes;
team targeting;
resource resolution;
inventory model.
```

Entregables derivados:

```text
SYS01_CLI_clublab.md
SYS02_CLI_clublabctl.md
```

---

# BLOQUE B — Scenario Manager, recovery y reset

# 19. Objetivo

Construir operaciones seguras para cambiar el estado del laboratorio.

Escenarios mínimos:

```text
normal
ranking-db-failure
api-down
```

---

# 20. Scenario Manager

Contrato del instructor:

```text
clublabctl scenario load <team> <scenario>
clublabctl scenario clear <team>
clublabctl scenario status <team>
```

---

# 21. Scenario `normal`

Estado esperado:

```text
frontend healthy
api healthy
database healthy
toolbox healthy
ranking 200
health 200
```

---

# 22. Scenario `ranking-db-failure`

Implementación:

```text
POST /internal/lab/scenario
```

con:

```text
ranking-db-failure
```

Validación posterior:

```text
/api/health → 200
/api/ranking → 500
database ready
```

---

# 23. Scenario `api-down`

Implementación:

```text
stop/recreate controlado del API del team
```

No por variable interna.

Esperado:

```text
frontend UP
api DOWN
database UP
toolbox UP
```

Y desde gateway:

```text
/api/* → 502/503
```

---

# 24. `scenario load`

Flujo:

```text
1. validar team
2. validar scenario
3. validar resources
4. leer estado actual
5. aplicar cambio
6. esperar estabilización
7. ejecutar smoke checks
8. registrar audit
9. devolver resultado
```

---

# 25. `scenario clear`

Para:

```text
ranking-db-failure
```

debe poner:

```text
scenario → normal.
```

Para:

```text
api-down
```

debe:

```text
levantar API;
esperar health;
validar ranking.
```

---

# 26. Scenario state observable

`clublabctl scenario status team01`

puede mostrar:

```text
Expected scenario: ranking-db-failure
Infra state: healthy
Ranking: 500
Health: 200
```

Alumno:

```text
NO ve el nombre del scenario.
```

---

# 27. Recover instructor-side

Comando:

```text
clublabctl recover team01
```

Debe intentar en orden:

```text
R1 — clear scenario
R2 — recreate/restart servicio afectado
R3 — reset team
```

No saltar directamente a reset salvo emergencia.

---

# 28. Recovery levels

## R1

```text
scenario clear.
```

Conserva:

```text
DB
score M4
session
lablogs.
```

## R2

```text
recreate API/frontend/toolbox individual
```

según fallo.

## R3

```text
reset completo del team.
```

Destructivo.

---

# 29. Reset

Comando:

```text
clublabctl reset team01
```

Debe reconstruir:

```text
DB data
migrations
roles
grants
seed
scenario
lablogs
service health.
```

---

# 30. Reset scope

Debe afectar únicamente:

```text
team indicado.
```

No recrear:

```text
gateway global;
otros teams;
imágenes;
servicios productivos.
```

---

# 31. Reset algorithm

Conceptualmente:

```text
validate target
↓
mark RESETTING
↓
stop team services
↓
remove team disposable volumes
↓
create DB data
↓
run migrations
↓
run grants
↓
run seed
↓
clear lablogs
↓
start services
↓
wait health
↓
run smoke tests
↓
mark READY
```

---

# 32. Recursos eliminables

Por team:

```text
db-data
lablogs
runtime scenario state if external
```

Solo si:

```text
labels correctas.
```

---

# 33. Recursos que reset NO elimina

```text
images
gateway
global ingress network
repo
host configs
audit logs
other teams.
```

---

# 34. Reset y credenciales

Dentro de una misma sesión:

```text
pueden conservarse.
```

Entre generaciones:

```text
rotate credentials.
```

---

# 35. `reset all`

Permitido únicamente al instructor.

Debe requerir:

```text
confirmación fuerte.
```

Ejemplo:

```text
Type RESET-ALL to continue.
```

---

# 36. Estado operativo por team

Se congelan:

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

---

# 37. Estado separado

La herramienta debe distinguir:

```text
infra_state
scenario_state
```

Ejemplo:

```text
infra=READY
scenario=ranking-db-failure
```

Esto evita marcar el fallo pedagógico como:

```text
infra failure.
```

---

# 38. Idempotencia

Comandos que deben ser idempotentes:

```text
scenario clear
recover
status
preflight
deploy cuando estado ya es correcto
```

Reset:

```text
repetible
```

aunque destructivo.

---

# 39. Entregables del Bloque B

```text
scenario contracts;
scenario state transitions;
recover levels;
reset algorithm;
team state machine;
validation checks.
```

---

# BLOQUE C — Preflight, status, logs, spare y auditoría

# 40. Objetivo

Hacer operable la clase sin improvisaciones.

Debe cubrir:

```text
antes de clase;
durante clase;
fallo de team;
spare;
observación;
auditoría.
```

---

# 41. `clublabctl preflight`

Debe comprobar al menos:

```text
Docker activo
RAM disponible
disco disponible
LAN IP actual
puertos libres
IPAM sin colisión
images presentes
team config presente
secret files presentes
permisos secrets correctos
gateway config válida
DB ports no publicados
containers no privileged
Docker socket no montado
teams esperados
scenario normal
spare disponible
```

---

# 42. Preflight fail-closed

Si falla una condición crítica:

```text
no desplegar.
```

Salida:

```text
PASS
WARN
FAIL
```

Ejemplo:

```text
Docker             PASS
LAN IP             PASS
Port 8211          PASS
Port 8212          FAIL
Secrets team03     PASS
Spare              WARN
```

---

# 43. Categorías preflight

```text
HOST
NETWORK
PORTS
IMAGES
CONFIG
SECRETS
SECURITY
TEAMS
SPARE
```

---

# 44. Memoria mínima

El preflight deberá comparar:

```text
MemAvailable
```

contra el presupuesto estimado del despliegue.

No basta con mirar:

```text
RAM total.
```
---

# 45. Recursos activos existentes

Debe observar:

```text
Pelican
WhatsApp
otros contenedores
```

solo para estimar margen.

No debe:

```text
pararlos automáticamente.
```

---

# 46. `clublabctl status all`

Salida conceptual:

```text
TEAM    FRONT   API   DB   TOOLBOX   SCENARIO
01      OK      OK    OK   OK        normal
02      OK      OK    OK   OK        normal
03      OK      OK    OK   OK        ranking-db-failure
04      OK      DOWN  OK   OK        api-down
```

---

# 47. `clublabctl resources`

Debe mostrar solo recursos ClubLab.

Ejemplo:

```text
team01 api       122 MiB / 512 MiB
team01 db        91 MiB / 640 MiB
team01 toolbox   28 MiB / 256 MiB
```

No mezclar:

```text
WhatsApp
Pelican
postgres-main
```

en la tabla principal.

---

# 48. Logs instructor-side

Comando:

```text
clublabctl logs team01 api
```

puede mostrar:

```text
technical stdout/stderr.
```

Distinto de:

```text
clublab logs api
```

del alumno.

---

# 49. Filtros

`clublabctl logs` debe aceptar solo:

```text
team válido
role válido
```

Roles:

```text
frontend
api
database
toolbox
gateway
```

No path libre.

---

# 50. Audit

Comando:

```text
clublabctl audit tail
```

Debe mostrar:

```text
timestamp
actor
action
team
result
```

No secrets.

---

# 51. Spare

Se mantiene:

```text
clublab-spare
```

Puerto:

```text
8219.
```

Debe estar:

```text
precreado y healthy
```

si los recursos del host lo permiten.

---

# 52. `clublabctl spare status`

Debe comprobar:

```text
frontend
api
DB
toolbox
login
ranking
scenario normal.
```

---

# 53. `clublabctl spare assign`

Conceptualmente:

```text
clublabctl spare assign team03
```

No necesita renombrar infraestructura.

Su función puede ser:

```text
mostrar nuevas credenciales/URL
registrar mapping temporal
marcar team03 → spare.
```

---

# 54. Cambio a spare

El alumno recibe:

```text
spare URL
spare app login
spare terminal login
spare DB student credentials.
```

El instructor puede reparar team original después.

---

# 55. Spare y datos

Spare inicia:

```text
seed limpio.
```

No se intenta migrar automáticamente:

```text
score M4
lablogs
session
```

de un team roto.

La prioridad es:

```text
continuidad pedagógica.
```

---

# 56. Spare assignment audit

Registrar:

```text
team original
spare
timestamp
reason
actor.
```

---

# 57. Audit storage

Ruta:

```text
/home/tulum/infra/clublab/audit/
```

Formato:

```text
JSONL.
```

Ejemplo:

```json
{
  "ts": "2026-09-17T22:20:00-05:00",
  "actor": "tulum",
  "action": "scenario.load",
  "team": "team03",
  "scenario": "ranking-db-failure",
  "result": "success"
}
```

---

# 58. Eventos auditables

```text
deploy
scenario load
scenario clear
recover
reset
spare assign
credential rotation
preflight fail
```

---

# 59. No auditar shell del alumno

No registrar:

```text
cada comando
cada SELECT
cada curl.
```

Solo eventos del plano operativo.

---

# 60. Entregables del Bloque C

```text
preflight matrix;
status format;
resource view;
technical logs;
spare workflow;
audit format.
```

Entregable derivado:

```text
SYS03_Preflight_Reset_Recovery.md
```

---

# BLOQUE D — Integración operativa y D04

# 61. Objetivo

Validar que la capa operativa puede ejecutar el laboratorio completo de principio a fin.

---

# 62. Flujo de preparación

Antes de clase:

```text
1. preflight
2. deploy
3. status all
4. security checks rápidos
5. smoke tests
6. spare check
7. scenario normal
8. entregar accesos
```

---

# 63. Flujo de inicio de clase

Instructor:

```text
clublabctl status all
```

Debe ver:

```text
todos READY
scenario normal.
```

---

# 64. Minuto 70

Según D01:

```text
activar incidente.
```

Comando:

```text
clublabctl scenario load all ranking-db-failure
```

Internamente:

```text
team por team
+
verify.
```

---

# 65. Resultado esperado de carga global

Ejemplo:

```text
team01 SUCCESS
team02 SUCCESS
team03 SUCCESS
team04 SUCCESS
team05 SUCCESS
team06 SUCCESS
```

Si un team falla:

```text
no revertir automáticamente los demás.
```

Reportar:

```text
partial success.
```

---

# 66. Partial scenario failure

Si:

```text
5 teams success
1 fail
```

Instructor puede:

```text
retry team
o
switch spare.
```

No romper toda la clase.

---

# 67. Flujo de recuperación alumno

Alumno:

```text
clublab recover ranking-db
```

Instructor:

```text
clublabctl status all
```

debe poder ver progresivamente:

```text
scenario normal
ranking 200.
```

---

# 68. Instructor override

Si un team no recupera:

```text
clublabctl recover teamXX
```

Si sigue fallando:

```text
reset
o
spare.
```

---

# 69. Flujo de cierre de clase

Opciones:

```text
mantener stacks para revisión
o
shutdown controlado.
```

No:

```text
prune.
```

La política concreta se cerrará en este bloque.

---

# 70. Criterio de validación operativa

Debe ser posible ejecutar sin comandos Docker manuales:

```text
deploy
status
scenario
recover
reset
spare
audit.
```

Docker manual queda reservado para:

```text
debug excepcional.
```

---

# 71. Test OP-01 — Deploy

Desde entorno limpio:

```text
clublabctl deploy team01
```

Esperado:

```text
READY.
```

---

# 72. Test OP-02 — Deploy all

```text
clublabctl deploy all
```

Esperado:

```text
teams READY;
gateway routes válidas.
```

---

# 73. Test OP-03 — Scenario

```text
scenario load team01 ranking-db-failure
```

Esperado:

```text
ranking 500;
health 200.
```

---

# 74. Test OP-04 — Clear

```text
scenario clear team01
```

Esperado:

```text
ranking 200;
score preservado.
```

---

# 75. Test OP-05 — api-down

```text
scenario load team01 api-down
```

Esperado:

```text
API stopped;
frontend up.
```

---

# 76. Test OP-06 — Recover api-down

```text
scenario clear team01
```

Esperado:

```text
API healthy.
```

---

# 77. Test OP-07 — Reset isolation

Reset Team01.

Esperado:

```text
Team02 intacto.
```

---

# 78. Test OP-08 — Guard rails

Intentar:

```text
reset postgres-main
reset ../../
scenario load team99
```

Esperado:

```text
ABORT.
```

---

# 79. Test OP-09 — Preflight

Crear una colisión controlada de puerto.

Esperado:

```text
FAIL antes de deploy.
```

---

# 80. Test OP-10 — Spare

Simular Team03 inutilizable.

Esperado:

```text
spare assign
→ nuevo acceso
→ continuidad.
```

---

# 81. Test OP-11 — Audit

Después de operaciones:

```text
audit contiene eventos
sin secrets.
```

---

# 82. Test OP-12 — Student CLI

Dentro de toolbox:

```text
whoami
status
health
logs
recover
```

funcionan.

Intentar:

```text
reset
scenario
deploy
```

debe fallar/inexistir.

---

# 83. Test OP-13 — Repetibilidad

Ejecutar:

```text
reset
normal
scenario
recover
reset
```

varias veces.

El entorno debe volver al mismo estado.

---

# 84. Test OP-14 — 4 teams

Ejecutar flujo completo con:

```text
4 teams simultáneos.
```

Objetivo:

```text
baseline de piloto.
```

---

# 85. Test OP-15 — 6 teams + spare

Ejecutar si recursos lo permiten.

Validar:

```text
RAM
CPU
latencia
WebSockets
reset
scenario.
```

Esto define el máximo real.

---

# 86. D04 — documento final

`D04_Scenario_Manager_y_Operacion_ClubLab.md` consolidará:

```text
CLI student
CLI instructor
scenario manager
state machine
reset
recovery
preflight
status
resources
logs
spare
audit
operational tests.
```

---

# 87. Qué NO pertenece a Fase 5

No hacer todavía:

```text
manual completo del alumno;
tarjetas de roles;
presentación de clase;
material impreso;
evaluación pedagógica final.
```

Eso pertenece a fases posteriores.

---

# 88. Implementación técnica probable

Se podrá usar:

```text
Bash
Python
o
TypeScript/Node
```

para `clublabctl`.

La decisión final debe priorizar:

```text
mantenibilidad;
validación de inputs;
JSON/YAML;
tests;
claridad.
```

---

# 89. Recomendación inicial

Preferencia para `clublabctl`:

```text
Python
```

porque facilita:

```text
subcommands;
validación;
JSON;
YAML;
subprocess seguro;
tests;
manejo de errores.
```

No es obligatorio hasta Bloque A.

---

# 90. Student CLI

Puede ser:

```text
Bash muy pequeño
o
Python mínimo.
```

Criterio:

```text
sin dependencias innecesarias;
salida legible;
sin eval;
sin input libre.
```

---

# 91. Interfaz con Docker

`clublabctl` puede invocar:

```text
docker
docker compose
```

desde host.

No necesita hablar con Docker SDK si CLI segura resulta suficiente.

---

# 92. Regla de comandos externos

Toda llamada deberá:

```text
usar argumentos estructurados;
validar inputs;
capturar exit codes;
capturar stderr;
timeout cuando corresponda.
```

No:

```text
shell injection;
eval;
string concat insegura.
```

---

# 93. Configuración versionada vs runtime

Versionado:

```text
team template;
scenario definitions;
gateway template;
CLI code;
validation rules.
```

Runtime:

```text
secrets;
generated team env;
state;
audit.
```

---

# 94. Estado persistente de `clublabctl`

Evitar una DB propia compleja.

Se puede utilizar:

```text
runtime JSON
```

para:

```text
spare mapping;
last expected scenario;
generation ID.
```

Docker/API siguen siendo fuentes de verdad para estado real.

---

# 95. Generation ID

Cada despliegue de clase puede tener:

```text
generation_id
```

Ejemplo:

```text
2026-09-CLUBLAB01-A
```

Sirve para:

```text
audit;
credential rotation;
logs;
reset tracking.
```

No es un secreto.

---

# 96. Criterios de éxito de Fase 5

```text
[ ] student CLI definido
[ ] instructor CLI definido
[ ] team inventory definido
[ ] scenario normal definido
[ ] ranking-db-failure operativo
[ ] api-down operativo
[ ] scenario clear definido
[ ] recover levels definidos
[ ] reset definido
[ ] state machine definida
[ ] preflight definido
[ ] status all definido
[ ] resources definido
[ ] technical logs definidos
[ ] spare workflow definido
[ ] audit definido
[ ] guard rails definidos
[ ] operational tests definidos
[ ] D04 consolidado
```

---

# 97. Primer bloque a desarrollar

# BLOQUE A — Modelo operativo + CLIs
El siguiente trabajo será cerrar exactamente:

```text
comandos;
argumentos;
salidas;
exit codes;
team inventory;
estructura de carpetas;
lenguaje de implementación;
resolución segura de recursos.
```

No se empezará por scripts sueltos.

Primero debemos definir una interfaz operativa estable para que después scenario/reset/preflight se construyan encima sin contradicciones.