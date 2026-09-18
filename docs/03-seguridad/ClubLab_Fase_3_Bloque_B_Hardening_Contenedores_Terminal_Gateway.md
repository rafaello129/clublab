# ClubLab — Fase 3 / Bloque B
## Hardening de contenedores, terminal y gateway

**Proyecto:** ClubLab v1  
**Fase:** 3 — Seguridad y aislamiento  
**Bloque:** B  
**Estado:** CERRADO PARA DISEÑO v1  
**Dependencias:** D00 + D01 + D02 + Fase 3/Bloque A  

---

# 1. Propósito

Este bloque convierte las fronteras arquitectónicas de ClubLab en controles concretos dentro de los contenedores.

Debe responder:

```text
¿Con qué usuario corre cada servicio?
¿Qué capabilities conserva?
¿Qué puede escribir?
¿Qué puede montar?
¿Qué puede ejecutar el alumno?
¿Cómo se endurece la terminal web?
¿Cómo se evita que Caddy se vuelva un puente entre equipos?
¿Cómo se limitan CPU, RAM y procesos?
```

La regla principal será:

> **Un contenedor accesible por el alumno debe asumirse potencialmente hostil.**

Por tanto, su diseño debe impedir que una acción dentro del contenedor se convierta en acceso al host o a otro team.

---

# 2. Baseline de seguridad común

Todos los contenedores ClubLab deberán intentar cumplir:

```text
usuario no-root;
capabilities mínimas;
no-new-privileges;
sin privileged;
sin host network;
sin Docker socket;
sin mounts del host;
resource limits;
PIDs limitados;
seccomp por defecto de Docker;
filesystem read-only cuando sea viable.
```

Excepciones deberán documentarse.

---

# 3. Matriz de hardening por servicio

| Servicio | Usuario | read-only | Capabilities | Escritura necesaria |
|---|---|---:|---|---|
| Frontend | no-root | Sí | ninguna | tmp/cache mínimo |
| API | no-root | Sí | ninguna | `/tmp` + lablogs |
| PostgreSQL | usuario oficial postgres | No | mínimas imagen oficial | data directory |
| Toolbox | no-root | Parcial | ninguna | home/tmp efímero |
| Gateway | no-root si viable | Sí | mínima para bind | config/runtime mínimo |

---

# 4. Frontend

## Runtime

Frontend estático:

```text
React build
→ servidor web ligero
```

Preferencia:

```text
nginx-unprivileged
```

o imagen equivalente que no requiera root para escuchar.

Puerto interno recomendado:

```text
8080
```

en lugar de:

```text
80
```

si eso permite ejecución no-root.

El gateway ocultará este detalle al alumno.

---

# 5. Usuario del frontend

El frontend deberá correr como:

```text
UID/GID no-root
```

sin shell administrativa necesaria.

No debe tener:

```text
sudo;
package manager operativo;
SSH;
Docker CLI;
credenciales DB;
recovery token.
```

---

# 6. Filesystem del frontend

Objetivo:

```text
read_only: true
```

Escrituras temporales, si la imagen las necesita:

```text
/tmp
/var/cache/nginx
/var/run
```

mediante:

```text
tmpfs
```

No volúmenes persistentes.

---

# 7. Frontend — capabilities

Se parte de:

```yaml
cap_drop:
  - ALL
```

y no se añade ninguna capability salvo prueba técnica que lo exija.

Si el servidor elegido necesita bind a puerto privilegiado:

```text
NO se añadirá NET_BIND_SERVICE como primera opción;
se preferirá puerto >1024.
```

---

# 8. API

La API es un servicio sensible porque contiene:

```text
credencial DB de aplicación;
lógica;
lab logging;
scenario-aware repository.
```

Debe ejecutarse como:

```text
usuario Node no-root
```

o usuario propio ClubLab.

---

# 9. Filesystem de API

Objetivo:

```text
read_only: true
```

Permitido:

```text
/tmp
```

como `tmpfs`.

El log pedagógico será la única escritura persistente/compartida necesaria.

Montaje:

```text
lablogs volume
```

con:

```text
API → read/write
Toolbox → read-only
```

No escribir código/configuración durante runtime.

---

# 10. API — capabilities

Configurar:

```yaml
cap_drop:
  - ALL
security_opt:
  - no-new-privileges:true
```

No necesita:

```text
NET_ADMIN;
SYS_ADMIN;
SYS_PTRACE;
DAC_OVERRIDE;
CHOWN;
SETUID;
SETGID;
```

si la imagen/build están preparados correctamente.

---

# 11. API — señales y procesos

El proceso Node será:

```text
PID 1 o init mínimo
```

Se evaluará:

```text
init: true
```

para reap de procesos/zombies si fuera necesario.

No ejecutar:

```text
nodemon;
ts-node dev;
shell watchers;
```

en una clase.

Runtime:

```text
build de producción.
```

---

# 12. PostgreSQL

PostgreSQL utilizará la imagen oficial y su usuario interno:

```text
postgres
```

No se forzará `read_only: true` porque necesita escritura real en:

```text
PGDATA
```

El aislamiento principal será:

```text
volumen propio;
red DATA propia;
sin published port;
credenciales únicas;
grants;
resource limits.
```

---

# 13. PostgreSQL — filesystem

Persistente:

```text
PGDATA
```

Temporal:

```text
/tmp
/run/postgresql
```

No montar:

```text
filesystem host;
backups productivos;
sockets host;
configuración externa sensible.
```

---

# 14. PostgreSQL — capabilities

No se concederán capabilities adicionales arbitrarias.

Se utilizará el comportamiento compatible con la imagen oficial y se probará si puede operar con:

```text
cap_drop: ALL
```

más únicamente capacidades realmente requeridas por la imagen.

La decisión final se basará en prueba técnica, no en suposición.

---

# 15. Toolbox — componente de mayor riesgo

El toolbox permite al alumno:

```text
shell;
curl;
psql;
jq;
ping;
dig/getent;
ss/ip;
clublab.
```

Por tanto, será el contenedor más restringido.

Debe asumirse que el alumno intentará:

```text
explorar filesystem;
listar procesos;
ver variables;
hacer conexiones;
probar comandos no previstos.
```

Eso es parte natural de un laboratorio.

---

# 16. Usuario del toolbox

Se define:

```text
username: student
```

con UID/GID no-root dedicado.

No pertenecerá a:

```text
sudo;
wheel;
docker;
adm;
systemd-journal;
shadow;
```

No tendrá password de root utilizable.

---

# 17. `sudo` y `su`

Preferencia:

```text
sudo no instalado
```

y:

```text
su inutilizable
```

porque no existe credencial root conocida.

No depender únicamente de “no revelar la password de root”.

---

# 18. Package managers

El alumno no necesita instalar software durante la sesión.

Preferencia:

```text
no incluir apt/dnf/apk en la imagen final
```

si la construcción multi-stage permite removerlos.

Si técnicamente permanecen:

```text
usuario no-root
```

impide instalación global.

Objetivo:

```text
imagen inmutable y predecible.
```

---

# 19. Toolbox — filesystem

El root filesystem será preferentemente:

```text
read_only: true
```

con áreas efímeras:

```text
/home/student
/tmp
```

mediante:

```text
tmpfs
```

Ventajas:

```text
el alumno puede crear archivos;
el contenedor sigue siendo desechable;
no modifica la imagen;
reset es inmediato.
```

---

# 20. Home del alumno

Se permitirá escribir en:

```text
/home/student
```

pero será efímero.

Puede guardar durante la sesión:

```text
notas;
salidas;
pequeños JSON;
comandos.
```

No se conserva después de recrear el toolbox.

---

# 21. Toolbox — capabilities

Partir de:

```yaml
cap_drop:
  - ALL
```

Las herramientas elegidas deben funcionar sin:

```text
NET_ADMIN;
SYS_ADMIN;
SYS_PTRACE.
```

Nota:

```text
ping
```

puede requerir comportamiento especial según imagen/kernel.

Preferencias, en orden:

```text
1. usar ping con soporte no privilegiado del sistema;
2. eliminar ping si exige capability peligrosa;
3. nunca añadir NET_ADMIN solo para conservar ping.
```

---

# 22. Herramientas de red permitidas

Mantener:

```text
curl
getent
dig
nc
ss
ip
```

cuando funcionen sin privilegios.

No incluir en v1:

```text
nmap;
tcpdump;
scapy;
ettercap;
metasploit;
masscan;
iptables/nft;
```

No porque sean “malas”, sino porque no aportan a ClubLab #01 y amplían innecesariamente la superficie.

---

# 23. Visibilidad de procesos

El toolbox verá procesos de:

```text
su propio contenedor.
```

Nunca utilizar:

```text
pid: host
```

ni compartir PID namespace con API/DB.

---

# 24. Dispositivos

No montar:

```text
/dev
```

del host ni dispositivos físicos adicionales.

No:

```text
USB;
GPU;
serial;
KVM;
```

para ClubLab #01.

---

# 25. ttyd — terminal web

La terminal será servida por:

```text
ttyd
```

o equivalente.

La shell objetivo:

```text
/bin/bash
```

como usuario:

```text
student
```

No lanzar ttyd como root para luego hacer `su student` si puede evitarse.

---

# 26. Autenticación de ttyd

Se selecciona para v1:

> **Basic Auth con credenciales únicas por team, sobre LAN controlada.**

Motivos:

```text
simple;
compatible;
fácil de resetear;
no introduce SSO;
suficiente para laboratorio local.
```

Esta credencial es distinta de:

```text
DB student password;
app login;
recovery token.
```

---

# 27. Alcance de Basic Auth

Basic Auth protege únicamente:

```text
/terminal/
```

No debe utilizarse como autenticación de:

```text
la aplicación ClubLab;
PostgreSQL;
recover token.
```

Separar credenciales reduce impacto.

---

# 28. Exposición de ttyd

`ttyd` escucha únicamente dentro de:

```text
teamXX-app
```

No publica puerto al host.

Acceso externo:

```text
Alumno
→ gateway
→ /terminal/
→ ttyd
```

---

# 29. WebSocket

El gateway deberá permitir WebSocket para ttyd.

Pero solo para la ruta definida:

```text
/terminal/*
```

No crear:

```text
proxy websocket genérico.
```

---

# 30. Terminal timeout

Se recomienda:

```text
idle timeout
```

o cierre de sesión cuando el contenedor se recrea.

No se necesita persistencia de sesiones entre clases.

Durante el ensayo se validará un valor que no moleste una clase de 120 minutos.

---

# 31. Credenciales visibles en entorno

El toolbox necesita:

```text
student DB credential;
recovery token limitado;
TEAM_ID.
```

Pero se debe reducir exposición innecesaria.

Preferencia:

```text
.pgpass con 0600
+
config específica de clublab
```

en vez de múltiples passwords visibles en:

```bash
env
```

si es sencillo implementarlo.

---

# 32. Recovery token en toolbox

El token no debe mostrarse en:

```text
clublab whoami;
logs;
help;
history.
```

`clublab recover` lo consume internamente.

El alumno puede llegar a leerlo si controla su propio toolbox, por lo que la seguridad no puede depender de que sea secreto absoluto.

Debe ser seguro incluso si lo conoce porque:

```text
scope=team actual;
action=recover-ranking-db;
sin reset;
sin scenario load;
sin cross-team.
```

---

# 33. Shell history

Evitar que secretos queden en:

```text
~/.bash_history
```

No pedir al alumno comandos como:

```bash
curl -H "Authorization: Bearer SECRET..."
```

El CLI `clublab` manejará tokens internamente.

---

# 34. Gateway — función de seguridad

`clublab-gateway` conecta:

```text
LAN
```

con múltiples redes APP.

Por ello es el único punto compartido entre todos los equipos y merece controles específicos.

---

# 35. Gateway — usuario

Preferencia:

```text
usuario no-root
```

El gateway escuchará internamente en un puerto:

```text
>1024
```

y Docker publicará:

```text
8211–8216
8219
```

hacia ese puerto o conjunto de listeners.

No necesita escuchar en:

```text
80/443
```

dentro del contenedor.

---

# 36. Gateway — filesystem

Objetivo:

```text
read_only: true
```

Permitir únicamente runtime mínimo mediante:

```text
tmpfs
```

si Caddy lo requiere.

La configuración se monta:

```text
read-only
```

No debe poder reescribirla desde dentro.

---

# 37. Gateway — capabilities

Configurar:

```text
cap_drop:
  - ALL
```

y:

```text
no-new-privileges:true
```

Sin:

```text
NET_ADMIN;
SYS_ADMIN;
NET_RAW
```

si no son necesarias.

---

# 38. Gateway — sin API Docker

Prohibido:

```text
/var/run/docker.sock
```

Prohibido también:

```text
Docker socket proxy
```

en v1.

El gateway no necesita descubrir contenedores dinámicamente.

Su configuración se genera antes de iniciar.

---

# 39. Gateway — configuración estática/generada

El archivo Caddy se construirá desde el inventario de teams.

Ejemplo conceptual:

```text
8211 → team01
8212 → team02
...
```

No habrá service discovery con privilegios Docker.

Ventaja:

```text
menos magia;
menos superficie;
fácil auditar.
```

---

# 40. Gateway — aliases únicos

Como ya definió D02:

```text
team01-frontend
team01-api
team01-toolbox
```

No usar desde Caddy:

```text
frontend
api
toolbox
```

porque esos nombres existen en varias redes.

---

# 41. Gateway — destinos permitidos
Por team:

```text
/terminal → teamXX-toolbox
/api      → teamXX-api
/         → teamXX-frontend
```

No debe existir configuración que acepte:

```text
upstream por parámetro;
URL elegida por cliente;
hostname arbitrario;
CONNECT.
```

---

# 42. Gateway — error behavior

Un upstream caído debe producir:

```text
502/503
```

normal.

No debe redirigir al alumno hacia:

```text
otro team;
servicio fallback compartido.
```

---

# 43. Gateway — administración

No exponer hacia LAN:

```text
Caddy Admin API
```

El puerto administrativo, si existe:

```text
deshabilitado
```

o:

```text
solo loopback dentro del contenedor
```

según configuración final.

---

# 44. `clublab-ingress`

El gateway será el único servicio conectado a:

```text
clublab-ingress
```

Además participa en redes APP.

No se habilita:

```text
IP forwarding
```

como función del contenedor.

Su trabajo es:

```text
L7 reverse proxy
```

no router.

---

# 45. `internal: true`

Las redes:

```text
teamXX-app
teamXX-data
```

seguirán configuradas como internas cuando Docker lo permita en la implementación real.

Resultado:

```text
API/toolbox/DB no salen libremente hacia LAN/Internet.
```

El gateway proporciona únicamente tráfico HTTP explícito.

---

# 46. Resolución DNS del toolbox

El toolbox podrá resolver:

```text
api
database
frontend
```

por Docker DNS de su team.

No se añadirá:

```text
DNS externo custom
```

salvo necesidad demostrada.

`dig` puede utilizarse sobre DNS de Docker para observar resolución interna.

---

# 47. Acceso al host desde toolbox

No añadir:

```yaml
extra_hosts:
  - "host.docker.internal:host-gateway"
```

No utilizar:

```text
network_mode: host
```

No montar sockets host.

---

# 48. Acceso a metadata del host

El alumno puede observar información normal proporcionada por el kernel/container, pero no debe recibir mounts que expongan:

```text
/proc del host;
/sys del host;
/etc del host.
```

Usar namespaces Docker por defecto.

---

# 49. Variables sensibles

Frontend:

```text
ninguna credencial DB.
```

Gateway:

```text
ninguna credencial DB.
```

Toolbox:

```text
solo student/recovery scope.
```

API:

```text
app DB credential + secretos mínimos.
```

DB:

```text
bootstrap/configuración propia.
```

---

# 50. Resource limits

Se mantienen los techos de Fase 2:

| Servicio | RAM | CPU | PIDs |
|---|---:|---:|---:|
| Frontend | 128 MiB | 0.25 | 64 |
| API | 512 MiB | 0.75 | 128 |
| PostgreSQL | 640 MiB | 0.75 | 128 |
| Toolbox | 256 MiB | 0.25 | 64 |

Deben aplicarse realmente en Compose/engine, no quedar solo documentados.

---

# 51. Gateway — recursos

Propuesta inicial:

```text
RAM: 128–256 MiB
CPU: 0.5
PIDs: 64
```

Se validará con:

```text
6 teams
+
WebSockets de terminal.
```

---

# 52. `ulimits`

Se evaluarán límites razonables.

Ejemplo conceptual:

```text
nofile
nproc
```

Sin valores excesivamente bajos que rompan Node/PostgreSQL.

La prueba real decidirá los números definitivos.

---

# 53. Logging del runtime

Docker seguirá utilizando la política del host:

```text
json-file
```

con rotación ya configurada globalmente.

ClubLab no cambiará la configuración del daemon.

Los logs técnicos completos son instructor-side.

---

# 54. Imágenes fijadas

No usar:

```text
latest
```

en la clase.

Idealmente, después del piloto se fijarán:

```text
tag exacto
```

y, para la sesión final, se podrá fijar también:

```text
digest
```

de imágenes críticas.

Objetivo:

```text
misma imagen ensayada
=
misma imagen en clase.
```

---

# 55. Build multi-stage

Frontend/API/toolbox se construirán mediante:

```text
builder stage
→ runtime stage
```

El runtime no debe contener innecesariamente:

```text
compiladores;
headers;
source completo;
cache npm;
devDependencies;
package managers si pueden eliminarse.
```

---

# 56. `.dockerignore`

Obligatorio para imágenes propias.

Excluir:

```text
.git
node_modules local
.env
runtime secrets
backups
docs innecesarios
tests de gran tamaño
```

Esto reduce riesgo de incluir secretos accidentalmente en la imagen.

---

# 57. Escaneo básico de imágenes

Antes del piloto se recomienda revisar:

```text
dependencias;
CVEs conocidas;
tamaño;
usuario runtime.
```

No se necesita construir un pipeline de seguridad empresarial.

La validación puede integrarse más adelante en CI.

---

# 58. Root shell de contingencia

El instructor puede necesitar troubleshooting.

No se habilitará root para alumnos.

El instructor podrá usar desde host:

```text
docker exec
```

sobre recursos ClubLab únicamente cuando sea necesario.

Ese acceso pertenece al plano de instructor.

---

# 59. Debug vs producción

No mantener herramientas debug de alto privilegio en runtime simplemente para facilitar troubleshooting.

Preferencia:

```text
toolbox controlado
+
docker exec instructor
```

antes que:

```text
dar privilegios adicionales a API/gateway.
```

---

# 60. Read-only — política final

## Obligatorio si pruebas pasan

```text
frontend
api
gateway
```

## Preferido y sujeto a prueba

```text
toolbox
```

con home/tmp en `tmpfs`.

## No aplicable de forma global

```text
database
```

porque PGDATA debe escribir.

---

# 61. `tmpfs` previsto

Frontend:

```text
/tmp
cache/runtime del servidor web
```

API:

```text
/tmp
```

Toolbox:

```text
/tmp
/home/student
```

Gateway:

```text
/tmp
runtime mínimo requerido
```

Datos importantes nunca viven en estos `tmpfs`.

---

# 62. Seguridad del volumen `lablogs`

API:

```text
read-write
```

Toolbox:

```text
read-only
```

No compartir con:

```text
frontend;
gateway;
otros teams.
```

El alumno puede leer logs pedagógicos pero no alterarlos.

---

# 63. Seguridad del volumen DB

Solo:

```text
database
```

monta:

```text
db-data
```

Ni:

```text
API
Toolbox
Gateway
```

montan el volumen físicamente.

El acceso es exclusivamente SQL.

---

# 64. Pruebas técnicas del Bloque B

Antes de considerar implementación segura deberán existir pruebas para verificar:

```text
container user != root;
sudo falla;
Docker socket no existe;
capabilities peligrosas ausentes;
read-only funciona;
tmpfs permite operación normal;
API escribe lablogs;
toolbox solo lee lablogs;
gateway no llega a DATA;
toolbox no llega al host;
terminal requiere auth;
terminal abre shell student;
resource limits se aplican.
```

---

# 65. Prueba de usuario

Dentro de:

```text
frontend
api
toolbox
gateway
```

ejecutar:

```bash
id
```

Esperado:

```text
uid != 0
```

PostgreSQL:

```text
usuario postgres de la imagen
```

esperado y documentado.

---

# 66. Prueba de capabilities

Inspeccionar desde host:

```text
CapAdd
CapDrop
SecurityOpt
```

Esperado:

```text
ALL dropped
+
solo excepciones justificadas.
```

Cualquier `SYS_ADMIN`:

```text
FAIL inmediato.
```

---

# 67. Prueba de filesystem

Intentar en frontend/API/gateway:

```text
touch /archivo
```

Esperado:

```text
read-only filesystem
```

En `/tmp`:

```text
OK
```

En toolbox:

```text
/home/student → OK
/etc → FAIL
```

---

# 68. Prueba de terminal

Sin credenciales:

```text
/terminal/
→ DENIED
```

Con credenciales team01:

```text
→ shell de team01
```

Credenciales team01 en team02:

```text
→ DENIED
```

---

# 69. Prueba de host

Desde toolbox:

```text
host.docker.internal
gateway host special
Docker socket
LAN services productivos
```

deben ser:

```text
inaccesibles
```

salvo alguna ruta explícitamente aprobada.

---

# 70. Prueba de gateway

Intentar usarlo como proxy hacia:

```text
team02 desde puerto team01;
database;
host;
URL arbitraria.
```

Esperado:

```text
no existe ruta.
```

---

# 71. Prueba de agotamiento básico

Con una carga controlada dentro de toolbox:

```text
procesos;
memoria;
CPU.
```

Verificar:

```text
team limitado;
otros teams healthy;
host healthy.
```

No realizar pruebas destructivas indiscriminadas.

---

# 72. Riesgos residuales

## RB3-01 — alumno puede leer su propio recovery token

Aceptable si:

```text
token está scoped
y
solo puede recover propio.
```

No tratarlo como secreto de alta confianza.

## RB3-02 — Basic Auth via HTTP en LAN

Aceptable para v1 debido a:

```text
LAN controlada;
credenciales desechables;
sin datos reales.
```

Si el acceso se vuelve remoto:

```text
HTTPS obligatorio.
```

## RB3-03 — Gateway multihomed

Se mitiga con:

```text
L7 proxy;
sin forwarding;
sin NET_ADMIN;
routes estáticas;
pruebas laterales.
```

## RB3-04 — Toolbox permite exploración amplia dentro del team

Es intencional.

La frontera importante es:

```text
team / host / otros teams.
```

---

# 73. Decisiones cerradas del Bloque B

### DB3-01
Frontend, API, Toolbox y Gateway operarán como usuarios no-root.

### DB3-02
PostgreSQL conservará el usuario previsto por la imagen oficial.

### DB3-03
Se aplicará `cap_drop: ALL` como baseline.

### DB3-04
No se añadirá `NET_ADMIN` ni `SYS_ADMIN`.

### DB3-05
Se aplicará `no-new-privileges`.

### DB3-06
Frontend, API y Gateway usarán filesystem read-only si las pruebas pasan.

### DB3-07
Toolbox usará root filesystem read-only preferentemente con `/home/student` y `/tmp` efímeros.

### DB3-08
No existirán bind mounts del host en servicios accesibles al alumno.

### DB3-09
Toolbox no tendrá sudo, Docker socket ni host network.

### DB3-10
No se incluirán herramientas ofensivas innecesarias en Toolbox v1.

### DB3-11
La terminal será `ttyd` o equivalente con Basic Auth único por team.

### DB3-12
La terminal siempre abrirá una shell no-root del contenedor.

### DB3-13
Gateway no tendrá Docker socket ni service discovery privilegiado.

### DB3-14
Gateway utilizará configuración estática/generada con upstreams explícitos.

### DB3-15
Caddy Admin API no será accesible desde LAN.

### DB3-16
No se añadirá `host.docker.internal`.

### DB3-17
Solo API monta `lablogs` RW; Toolbox lo monta RO.

### DB3-18
Solo PostgreSQL monta `db-data`.

### DB3-19
Los límites RAM/CPU/PIDs definidos en D02 deberán aplicarse realmente.

### DB3-20
Las imágenes propias utilizarán builds multi-stage y no `latest`.

---

# 74. Requisitos para Bloque C

El próximo bloque deberá cerrar:

```text
recovery token;
secrets runtime;
permisos de clublab;
permisos de clublabctl;
firewall;
guard rails;
auditoría;
protección cross-team;
host isolation operativo.
```

En particular, ya queda establecido:

```text
Toolbox = ambiente potencialmente hostil
```

por lo que ningún secreto que permita administración real del stack puede estar disponible allí.

---

# 75. Criterios de aceptación

```text
[x] usuarios runtime definidos
[x] frontend hardening definido
[x] API hardening definido
[x] PostgreSQL hardening base definido
[x] toolbox hardening definido
[x] terminal auth definida
[x] gateway hardening definido
[x] capabilities policy definida
[x] no-new-privileges definido
[x] read-only policy definida
[x] tmpfs definidos
[x] mounts prohibidos definidos
[x] Docker socket prohibido
[x] host network prohibido
[x] lablogs RW/RO definido
[x] resource limits exigidos
[x] image build policy definida
[x] pruebas de hardening definidas
[x] riesgos residuales documentados
```

# BLOQUE B — COMPLETADO

---

# 76. Modelo final

```text
                     LAN
                      │
                      ▼
            ┌──────────────────┐
            │ clublab-gateway  │
            │ no-root          │
            │ read-only        │
            │ cap_drop ALL     │
            └────────┬─────────┘
                     │
                teamXX-app
                     │
       ┌─────────────┼─────────────┐
       │             │             │
   Frontend         API         Toolbox
   no-root          no-root     student
   read-only        read-only   restricted
   no secrets       app secret  DB-student
       │             │             │
       │             └──────┬──────┘
       │                    │
       │               teamXX-data
       │                    │
       │                PostgreSQL
       │                 db-data
       │
       └── sin acceso DB

Shared operational volume:
API RW ── lablogs ── Toolbox RO
```

El siguiente bloque protege las acciones y secretos que todavía pueden cambiar estado: `recover`, `reset`, `scenario`, `clublab`, `clublabctl` y firewall.