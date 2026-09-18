# ClubLab — Fase 3 / Bloque C
## Control de acciones, secrets y aislamiento operacional

**Proyecto:** ClubLab v1  
**Fase:** 3 — Seguridad y aislamiento  
**Bloque:** C  
**Estado:** CERRADO PARA DISEÑO v1  
**Dependencias:** D00 + D01 + D02 + Fase 3/Bloques A–B

---

# 1. Propósito

Este bloque protege las operaciones que pueden cambiar el estado de ClubLab.

Hasta ahora ya se definieron:

```text
usuarios;
permisos PostgreSQL;
hardening de contenedores;
terminal restringida;
gateway endurecido.
```

Ahora toca cerrar:

```text
recovery token;
student CLI;
instructor CLI;
secrets runtime;
guard rails;
firewall;
auditoría;
aislamiento host/team;
controles de acciones destructivas.
```

La regla principal será:

> **El alumno puede diagnosticar y recuperar su escenario, pero no administrar la infraestructura.**

---

# 2. Separación de planos

Se mantienen dos herramientas distintas:

```text
clublab
clublabctl
```

No son aliases ni modos del mismo binario.

---

# 3. `clublab` — herramienta del alumno

Se ejecuta dentro de:

```text
teamXX-toolbox
```

Subcomandos permitidos:

```text
clublab whoami
clublab status
clublab health
clublab logs api
clublab recover ranking-db
clublab help
```

No incluye:

```text
deploy
reset
scenario load
scenario clear
resources
spare
docker
shell host
```

---

# 4. `clublabctl` — herramienta del instructor

Se ejecuta:

```text
host-side
```

por la cuenta operadora autorizada.

Subcomandos previstos:

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
audit
```

Nunca estará disponible dentro de:

```text
toolbox;
frontend;
api;
gateway.
```

---

# 5. No compartir binario administrativo

Aunque ambos CLI puedan compartir lógica en repositorio:

```text
student CLI
≠
admin CLI
```

El runtime del toolbox solo incluirá:

```text
clublab
```

No incluir:

```text
clublabctl
scripts admin
docker helpers
reset scripts
team inventory completo
```

---

# 6. Recovery token — propósito

M7 requiere que el alumno pueda ejecutar:

```bash
clublab recover ranking-db
```

sin obtener permisos de administración.

Por ello se define:

> **un token de recuperación scoped por team y por acción.**

---

# 7. Propiedades del recovery token

Cada token tendrá:

```text
scope = teamXX
action = recover-ranking-db
lifetime = generación de laboratorio
```

No permitirá:

```text
scenario load;
reset;
deploy;
leer otros teams;
cambiar DB;
controlar Docker.
```

---

# 8. Recovery token por team

Ejemplo conceptual:

```text
team01_recovery_token != team02_recovery_token
```

Nunca compartir:

```text
un token global
```

para todos los equipos.

---

# 9. Token no considerado secreto fuerte

Como el alumno controla su toolbox, debe asumirse que eventualmente puede leer:

```text
su propio recovery token.
```

Eso es aceptable.

La seguridad real depende de:

```text
scope;
validación server-side;
acción única;
team único.
```

No de ocultarlo.

---

# 10. Ruta de recovery

El comando:

```bash
clublab recover ranking-db
```

llamará a un endpoint interno del team.

Conceptualmente:

```text
Toolbox
  ↓
internal control endpoint
  ↓
validate token
  ↓
validate team
  ↓
validate scenario
  ↓
scenario state → normal
```

---

# 11. Recovery endpoint no público

La ruta de control:

```text
NO se publica por gateway.
```

Solo debe ser accesible desde:

```text
teamXX-app
```

o una red interna equivalente.

Así el navegador de la LAN no puede invocarla directamente.

---

# 12. Validaciones del recovery endpoint

Debe comprobar:

```text
token válido;
scope team correcto;
acción permitida;
scenario actual;
request origin/network esperado.
```

Si alguna falla:

```text
403/denied
```

sin revelar detalles sensibles.

---

# 13. Idempotencia

`recover ranking-db` será idempotente.

Si el entorno ya está:

```text
normal
```

devolver:

```text
Environment already healthy.
```

No debe:

```text
reiniciar API;
resetear DB;
crear otro escenario;
alterar datos.
```

---

# 14. Rate limiting del recovery

No se necesita un sistema complejo.

Pero se recomienda:

```text
rate limit simple
```

por team.

Ejemplo conceptual:

```text
5 requests/min
```

para evitar spam accidental.

---

# 15. Student CLI — validación local

`clublab` no aceptará parámetros arbitrarios.

Permitido:

```text
clublab logs api
```

No:

```text
clublab logs ../../etc/passwd
clublab recover team02
clublab status --host ...
```

Subcomandos y argumentos estarán en whitelist.

---

# 16. Student CLI — sin shell interpolation

No construir comandos como:

```bash
eval "$USER_INPUT"
```

ni:

```text
shell=True
```

con argumentos controlados por alumno.

La implementación debe usar:

```text
argumentos estructurados
```

y listas cerradas.

---

# 17. Student CLI — logs

`clublab logs api` leerá únicamente:

```text
lablogs del team actual.
```

No permitirá:

```text
ruta libre;
servicio arbitrario;
container name;
team ID externo.
```

---

# 18. `whoami`

Debe mostrar:

```text
TEAM_ID;
identidad de entorno;
servicios lógicos.
```

No mostrar:

```text
recovery token;
password DB;
password terminal;
Docker IDs;
host paths.
```

---

# 19. `status` y `health`

Operan mediante:

```text
checks locales de red;
HTTP;
pg_isready;
```

No acceden a:

```text
Docker API;
host;
clublabctl.
```

---

# 20. Secrets — categorías

Se definen cinco categorías:

```text
S1 — DB bootstrap/admin
S2 — DB migrator
S3 — DB app
S4 — DB student
S5 — terminal auth
S6 — recovery token
S7 — app secret/JWT si aplica
```

Cada servicio recibe únicamente lo necesario.

---

# 21. Distribución de secrets

## Frontend

```text
ninguno de DB;
ningún recovery token;
ningún secreto administrativo.
```

## API

```text
DB app credential;
app secrets mínimos;
scenario state access.
```

## Toolbox

```text
DB student credential;
recovery token scoped;
terminal identity local.
```

## Gateway

```text
terminal Basic Auth hashes/credentials;
sin DB credentials.
```

## Instructor

```text
runtime secret inventory completo;
solo fuera de contenedores alumno.
```

---

# 22. Almacenamiento host-side de secrets

Ruta propuesta:

```text
/home/tulum/infra/clublab/runtime/secrets/
```

Ejemplo:

```text
team01.env
team02.env
...
gateway.env
```

Permisos:

```text
dir 700
file 600
```

Propiedad:

```text
cuenta operadora autorizada.
```

---

# 23. Secrets fuera de Git

`.gitignore` deberá excluir explícitamente:

```text
runtime/
teams/*.env
*.secret
*.credentials
*.token
```

El repositorio contiene solo:

```text
templates;
.env.example;
generadores.
```

---

# 24. Generación de secrets

Se generarán con:

```text
CSPRNG
```

no con:

```text
fecha;
Team ID;
incrementos;
palabras previsibles.
```

Longitud inicial:

```text
>= 24 caracteres
```

para credenciales internas.

---

# 25. Rotación

Dos niveles:

```text
misma sesión
→ credenciales pueden conservarse tras reset

nueva generación/clase
→ rotar credenciales
```

El flujo de despliegue debe soportarlo automáticamente.

---

# 26. Terminal Basic Auth

Cada team tendrá:

```text
usuario/password propios
```

No reutilizar:

```text
team01 terminal credential
```

en:

```text
team02.
```

El gateway no debe imprimir esas credenciales en logs.

---

# 27. Hashes vs plaintext

Si Caddy/ttyd soporta hashes de forma sencilla:

```text
preferir hash.
```

Si ttyd requiere plaintext runtime:

```text
mantenerlo solo en runtime secret file
```

con permisos restrictivos.

No copiarlo a:

```text
README;
Caddyfile versionado;
material permanente.
```

---

# 28. Historial de shell

Evitar pasar secrets manualmente por comandos.

No instruir:

```bash
export RECOVERY_TOKEN=...
curl -H "Authorization: Bearer ..."
```

El CLI los consume internamente.

---

# 29. Variables de entorno

Se acepta usar variables runtime para secrets de servicio si:

```text
solo llegan al contenedor necesario;
no se imprimen;
no se exponen al frontend;
no se comparten con toolbox salvo student scope.
```

No ejecutar debugging que haga:

```text
printenv
```

sobre logs del alumno.

---

# 30. Protección de errores

Errores de API no deben devolver:

```text
DATABASE_URL;
password;
token;
stack trace completo;
env vars.
```

Respuesta pública:

```text
mensaje genérico.
```

Detalle técnico:

```text
solo logs instructor/pedagógicos sanitizados.
```

---

# 31. `clublabctl` — modelo de seguridad

`clublabctl` será la única capa normal que automatiza Docker para ClubLab.

No recibe input libre de contenedor.

Trabaja sobre:

```text
team whitelist;
resource labels;
resource names previstos.
```

---

# 32. Whitelist de teams

Inicial:

```text
team01
team02
team03
team04
team05
team06
spare
```

Cualquier otro valor:

```text
ABORT.
```

---

# 33. Validación de recursos

Antes de operar un contenedor:

```text
name prefix
+
project label
+
team label
+
role label
```

deben coincidir.

Ejemplo:

```text
clublab-team01-api
com.clublab.project=clublab
com.clublab.team=team01
com.clublab.role=api
```

---

# 34. Fail closed

Si falta una label:

```text
NO asumir.
```

Si hay dos recursos ambiguos:

```text
NO elegir uno arbitrariamente.
```

La herramienta debe:

```text
abortar;
reportar inconsistencia.
```

---

# 35. Guard rail de reset

`clublabctl reset team01` deberá mostrar:

```text
team;
contenedores;
redes/volúmenes que tocará;
estado actual.
```

y pedir confirmación.

---

# 36. Reset all

Una operación:

```text
reset all
```

es excepcional.

Debe requerir:

```text
flag explícito;
confirmación fuerte;
lista previa.
```

Ejemplo conceptual:

```bash
clublabctl reset all --confirm-all
```

---

# 37. Operaciones globales prohibidas

No usar:

```bash
docker system prune
docker volume prune
docker network prune
docker stop $(docker ps -q)
docker rm -f $(docker ps -aq)
```

ni equivalentes.

No se aceptan ni siquiera “porque el servidor solo tenga ClubLab”; el servidor es compartido.

---

# 38. Scenario load

`clublabctl scenario load team01 ranking-db-failure`

debe validar:

```text
team permitido;
scenario permitido;
infra healthy;
scenario actual;
endpoint baseline.
```

Solo después activa el escenario.

---

# 39. Scenario allowlist

Inicial:

```text
normal
ranking-db-failure
api-down
```

No aceptar nombres arbitrarios de scenario desde shell.

---

# 40. Scenario all

`scenario load all`

internamente será:

```text
for team in whitelist_active:
    apply individually
    validate individually
```

No una operación Docker global indiscriminada.

---

# 41. Auditoría

Archivo host-side:

```text
/home/tulum/infra/clublab/audit/clublabctl.log
```

o equivalente.

Registrar:

```text
timestamp;
actor;
command;
team;
scenario;
result.
```

No registrar:

```text
passwords;
tokens;
full env.
```

---

# 42. Eventos auditables

Obligatorios:

```text
deploy;
scenario load;
scenario clear;
recover instructor;
reset;
spare switch;
credential rotation;
preflight failure crítico.
```

---

# 43. Formato de auditoría

Ejemplo:

```text
2026-09-17T20:31:04-05:00
actor=tulum
action=scenario.load
team=team03
scenario=ranking-db-failure
result=success
```

Formato estructurado preferido:

```text
JSON Lines
```

para futura automatización.

---
# 44. Auditoría student-side

No se necesita registrar cada comando shell.

Sí puede registrarse:

```text
recover solicitado;
recover success/failure.
```

Objetivo:

```text
operación del sistema
```

no vigilancia del alumno.

---

# 45. Firewall — objetivo

Solo los puertos del gateway destinados a la clase deben ser alcanzables desde la red autorizada.

Puertos:

```text
8211–8216
8219
```

---

# 46. Binding

Primera barrera:

```text
CLUBLAB_BIND_IP
```

Los ports no se publican normalmente a:

```text
0.0.0.0.
```

---

# 47. firewalld

Se añadirá una política específica de ClubLab o reglas equivalentes durante implementación.

Objetivo:

```text
permitir puertos ClubLab desde subnet de clase;
rechazar desde interfaces/redes no previstas.
```

No modificar reglas productivas salvo necesidad explícita y reversible.

---

# 48. Red autorizada

La subnet concreta de alumnos deberá detectarse/configurarse en preflight.

No hardcodear permanentemente:

```text
10.10.100.0/22
```

sin validar que esa sigue siendo la LAN real.

---

# 49. Firewall y Docker

Se reconoce que Docker manipula networking/iptables/nftables.

Por tanto:

```text
firewalld
```

no será la única frontera.

La seguridad depende en conjunto de:

```text
published ports mínimos;
bind IP;
Docker networks;
internal networks;
auth terminal;
app auth;
PostgreSQL no publicado.
```

---

# 50. No publicar DB/API/toolbox

Regla invariable:

```text
5432 host → NO
3000 host → NO
7681 host → NO
frontend internal port → NO
```

Solo:

```text
gateway team ports.
```

---

# 51. Host access desde Toolbox

No añadir rutas especiales al host.

Debe verificarse que el toolbox no pueda acceder a servicios del host usando:

```text
gateway IP de Docker;
LAN IP del host;
Tailscale IP;
host.docker.internal.
```

---

# 52. Riesgo de host LAN IP

Aunque una red Docker sea `internal`, se deberá validar en práctica el comportamiento concreto del host y Docker.

Prueba explícita:

```text
toolbox → CLUBLAB_BIND_IP:22
toolbox → CLUBLAB_BIND_IP:9090
toolbox → Tailscale services
```

Esperado:

```text
DENIED / unreachable
```

Si no:

```text
agregar control específico.
```

---

# 53. Servicios productivos a bloquear

Desde toolbox, no debe alcanzarse:

```text
SSH 22
Cockpit 9090
Caddy/Pelican 8090
Wings 8081/2022
WhatsApp 8080/3500
Pelican game ports
postgres-main
```

La lista se actualizará con preflight real.

---

# 54. Cross-team isolation

Desde team01:

```text
team02-app subnet
team02-data subnet
team02 gateway backend aliases
```

deben ser inaccesibles.

El alumno solo puede llegar al puerto público de otro team si conoce la URL de LAN, igual que cualquier alumno de la clase.

---

# 55. Acceso a otro gateway port

Un alumno podría intentar abrir:

```text
http://LAN_IP:8212
```

desde su navegador.

Eso no debe otorgar acceso automático.

Por tanto:

```text
app auth;
terminal auth;
DB internal.
```

siguen siendo importantes.

---

# 56. Credencial de aplicación por team

La aplicación ClubLab deberá usar credenciales o sesión específica por team.

No diseñar:

```text
Team01 login funciona en Team02
```

como comportamiento normal.

La implementación concreta se cerrará en Fase 4.

---

# 57. Terminal cross-team

Credencial de terminal team01 en:

```text
:8212/terminal/
```

debe fallar.

Esto se probará explícitamente.

---

# 58. Recovery cross-team

El token team01 enviado al endpoint interno de team02 debe:

```text
403
```

aunque hipotéticamente pudiera llegar a ese endpoint.

Defensa en profundidad.

---

# 59. Secrets cross-team

No debe existir volumen/configuración compartida que contenga:

```text
todos los team passwords
```

montado en un contenedor de alumno.

Cada toolbox recibe solo:

```text
su student DB credential;
su recovery token.
```

---

# 60. Instructor environment

La cuenta operadora del host sí tendrá acceso al inventario completo.

Eso es aceptable porque pertenece a:

```text
Z1 — control instructor.
```

Se protegerá mediante permisos de filesystem.

---

# 61. No usar sudo dentro de scripts si no hace falta

Si la cuenta operadora ya tiene los permisos requeridos para Docker:

```text
clublabctl
```

no deberá ejecutar:

```text
sudo sh -c ...
```

de forma indiscriminada.

La elevación, si es necesaria, se limitará a operaciones explícitas.

---

# 62. Riesgo del grupo `docker`

En Linux:

```text
docker group ≈ privilegio root
```

Por tanto:

```text
nunca agregar student;
nunca exponer socket;
nunca compartir sesión host.
```

Solo el plano instructor autorizado puede tener acceso operativo a Docker.

---

# 63. Backup de secrets

No se necesitan backups históricos frecuentes de credenciales desechables.

Lo importante es poder:

```text
regenerar.
```

No copiar runtime secrets a:

```text
backups generales no cifrados
```

sin necesidad.

---

# 64. Destrucción de generación

Al finalizar una generación de laboratorio:

```text
detener stacks;
eliminar recursos desechables según política;
eliminar/rotar secrets;
conservar código/config/audit sin secrets.
```

No utilizar prune global.

---

# 65. Preflight de seguridad

`clublabctl preflight` deberá comprobar además:

```text
secret files mode 600;
secret dir mode 700;
no docker.sock mounts;
no privileged containers;
no host network;
gateway admin API no expuesta;
DB no published;
team ports correctos;
runtime configs existen;
```

---

# 66. Security assertions

Antes de declarar:

```text
READY
```

un team deberá pasar checks rápidos:

```text
DB port unpublished;
toolbox user non-root;
terminal auth configured;
scenario token exists;
labels correctas.
```

---

# 67. Fail secure

Si falta:

```text
terminal password;
recovery token;
DB student credential;
```

no iniciar el team en modo permisivo.

Debe:

```text
fallar el despliegue.
```

No usar defaults como:

```text
admin/admin.
```

---

# 68. Defaults prohibidos

No permitir:

```text
changeme
password
123456
team01
admin
```

como secrets de fallback.

Si generación falla:

```text
ABORT.
```

---

# 69. Manejo de archivos temporales

Los scripts administrativos que generen secrets deberán:

```text
usar permisos restrictivos;
evitar /tmp público;
limpiar temporales;
usar umask 077.
```

---

# 70. `umask`

Para generación runtime:

```bash
umask 077
```

antes de crear:

```text
env files;
tokens;
credenciales.
```

---

# 71. Integridad de configuración

Se recomienda que `clublabctl preflight` valide que:

```text
team env;
gateway config;
scenario config;
```

pertenecen al team esperado.

No hace falta firma criptográfica en v1.

Sí:

```text
consistencia y ownership.
```

---

# 72. Configuración del gateway

El archivo generado del gateway:

```text
no contendrá DB passwords;
no contendrá recovery tokens.
```

Solo:

```text
listeners;
upstreams;
terminal auth;
routes.
```

---

# 73. Sanitización de auditoría

Si un comando falla por credencial:

```text
registrar error genérico.
```

No imprimir:

```text
secret completo.
```

Ejemplo correcto:

```text
credential validation failed
```

---

# 74. Logs instructor-side

Los logs técnicos completos pueden contener más detalle que lablogs, pero igualmente se diseñará la API para no registrar:

```text
passwords;
tokens;
Authorization headers completos.
```

No confiar solo en ocultárselos al alumno.

---

# 75. Protección del scenario state

El estado de escenario no debe residir en un archivo writable por:

```text
student.
```

Opciones válidas:

```text
estado interno API;
archivo/config no writable por toolbox;
almacenamiento controlado.
```

El toolbox solo puede solicitar:

```text
recover.
```

---

# 76. Student no puede falsificar `normal`

Editar localmente una variable o archivo en toolbox no debe cambiar el escenario real.

El control debe estar:

```text
server-side.
```

---

# 77. Student no puede activar `ranking-db-failure`

El endpoint interno acepta:

```text
recover only.
```

No:

```text
set scenario.
```

Scenario load queda exclusivamente en:

```text
clublabctl.
```

---

# 78. Control de API interna

Si el endpoint de control está dentro del mismo proceso API:

```text
ruta separada;
auth separada;
no proxy pública;
logs auditables.
```

No reutilizar sesión de usuario web como permiso de recuperación.

---

# 79. CORS no es frontera de seguridad

Aunque frontend y API usen mismo origen, no considerar:

```text
CORS
```

como mecanismo para proteger endpoints internos.

La protección real es:

```text
routing;
network;
auth;
scope.
```

---

# 80. Seguridad de HTTP en LAN

ClubLab v1 utilizará HTTP.

Se acepta porque:

```text
LAN controlada;
datos ficticios;
credenciales desechables;
sin acceso remoto público.
```

Consecuencia:

```text
no reutilizar passwords personales;
no usar secrets productivos.
```

Si se habilita acceso remoto:

```text
HTTPS obligatorio.
```

---

# 81. Cambio de modelo si sale de LAN

Si ClubLab se usa posteriormente sobre:

```text
Internet;
Wi-Fi no confiable;
red pública;
acceso remoto externo;
```

se deberá reabrir esta decisión y añadir:

```text
TLS;
auth más fuerte;
posiblemente SSO/VPN.
```

No asumir que el diseño LAN es universal.

---

# 82. DoS accidental entre alumnos

El control primario será:

```text
resource limits;
PIDs;
timeouts DB;
connection limits;
gateway limits razonables.
```

No se pretende defender contra un atacante dedicado con acceso físico y tiempo ilimitado.

La amenaza principal es:

```text
curiosidad;
errores;
experimentación.
```

---

# 83. Gateway rate limits

No se requiere rate limiting complejo en v1.

Puede añadirse si el ensayo muestra:

```text
refresh loops;
terminal abuse accidental;
requests masivas.
```

Primero se probará con límites de contenedor.

---

# 84. Auditoría de incidentes accidentales

Si un team entra en:

```text
DEGRADED
```

sin scenario activo:

```text
clublabctl status
```

deberá permitir distinguirlo.

El instructor puede registrar:

```text
accidental failure
```

sin culpar al alumno.

---

# 85. Decisiones cerradas del Bloque C

### DC3-01
`clublab` y `clublabctl` serán herramientas separadas.

### DC3-02
`clublab` solo contendrá subcomandos pedagógicos en whitelist.

### DC3-03
`clublabctl` será host-side y no estará en toolbox.

### DC3-04
Recovery utilizará token scoped por team y acción.

### DC3-05
El recovery endpoint no será publicado por gateway.

### DC3-06
Recover será idempotente.

### DC3-07
Cada team tendrá secrets distintos.

### DC3-08
Runtime secrets vivirán fuera de Git con permisos restrictivos.

### DC3-09
No existirán passwords/defaults inseguros de fallback.

### DC3-10
`clublabctl` operará solo sobre whitelist + prefijo + labels.

### DC3-11
Los scripts harán fail closed ante inconsistencias.

### DC3-12
No se usarán comandos Docker globales destructivos.

### DC3-13
Se mantendrá auditoría estructurada de acciones administrativas.

### DC3-14
Solo puertos gateway serán publicados.

### DC3-15
Firewall complementará, no sustituirá, el aislamiento Docker.

### DC3-16
Toolbox no tendrá rutas especiales al host.

### DC3-17
Se probará acceso a servicios reales del host y deberá fallar.

### DC3-18
Credenciales de app/terminal/recovery serán team-scoped.

### DC3-19
Scenario state será server-side y no writable por student.

### DC3-20
HTTP solo se acepta en LAN controlada; remoto requerirá HTTPS.

---

# 86. Requisitos para Bloque D

El siguiente bloque debe probar de forma integrada:

```text
PostgreSQL permissions;
container users;
capabilities;
read-only;
terminal auth;
DB publication;
API publication;
cross-team isolation;
host isolation;
recovery scope;
clublabctl guard rails;
secrets leakage;
resource limits;
gateway lateral movement.
```

No basta con revisar configuración.

Se deberá construir:

```text
matriz PASS/FAIL
```

y consolidar:

```text
D03_Seguridad_Aislamiento_ClubLab.md
```

---

# 87. Criterios de aceptación

```text
[x] student CLI scope definido
[x] instructor CLI scope definido
[x] recovery token definido
[x] recovery endpoint protegido
[x] idempotencia definida
[x] secrets categorizados
[x] distribución de secrets definida
[x] almacenamiento runtime definido
[x] rotación definida
[x] guard rails definidos
[x] fail closed definido
[x] audit definido
[x] firewall policy definida
[x] host access tests derivados
[x] cross-team controls definidos
[x] scenario state protegido
[x] CORS descartado como frontera
[x] política HTTP/HTTPS definida
[x] cleanup de generación definido
```

# BLOQUE C — COMPLETADO

---

# 88. Modelo final del control operacional

```text
                         INSTRUCTOR
                             │
                             ▼
                        clublabctl
                             │
            whitelist + labels + audit
                             │
            ┌────────────────┼────────────────┐
            │                │                │
         Team01           Team02           TeamXX

ALUMNO
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
      internal recovery endpoint
             │
      scope=teamXX/action
             │
             ▼
      scenario → normal
```

El alumno controla únicamente la recuperación pedagógica de su propio escenario. La infraestructura permanece bajo control del instructor.