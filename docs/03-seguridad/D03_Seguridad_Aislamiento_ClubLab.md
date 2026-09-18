# D03 — Seguridad y Aislamiento de ClubLab
## Modelo de seguridad para ClubLab #01

**Proyecto:** ClubLab v1  
**Fase:** 3 — Seguridad y aislamiento  
**Estado:** FINAL DE DISEÑO — VALIDACIÓN EMPÍRICA PENDIENTE  
**Entradas:** D00 + D01 + D02  
**Ámbito:** Host Tulum + entornos Team01–Team06 + Spare

---

# 1. Objetivo

Definir los controles que permiten que un participante:

```text
explore;
consulte;
modifique datos limitados;
diagnostique;
recupere su escenario;
```

sin poder:

```text
administrar el host;
administrar Docker;
obtener root;
afectar otro team;
administrar PostgreSQL;
acceder a producción;
usar secretos administrativos.
```

La seguridad se basa en controles técnicos, no únicamente en instrucciones.

---

# 2. Modelo de confianza

```text
Z0 — HOST TULUM
     Docker Engine
     filesystem
     servicios productivos

Z1 — CONTROL INSTRUCTOR
     clublabctl
     runtime secrets
     deploy/reset/scenario

Z2 — TEAM CLUBLAB
     frontend
     api
     database
     toolbox

Z3 — ALUMNO
     navegador
     terminal web
```

Regla principal:

```text
Z3 no accede directamente a Z0.
```

---

# 3. Activos protegidos

Host:

```text
Docker;
filesystem;
SSH;
Cockpit;
systemd;
NetworkManager;
firewall;
Tailscale.
```

Producción:

```text
WhatsApp;
postgres-main;
Pelican;
Wings;
Playit;
Caddy existente.
```

ClubLab:

```text
otros teams;
secrets;
scenario state;
audit;
control plane.
```

---

# 4. Identidades PostgreSQL

Por team:

```text
clublab_teamXX_owner
clublab_teamXX_migrator
clublab_teamXX_app
clublab_teamXX_student
```

`owner`:

```text
NOLOGIN;
propietario lógico.
```

`migrator`:

```text
deploy/reset.
```

`app`:

```text
runtime API.
```

`student`:

```text
M3/M4.
```

---

# 5. PostgreSQL por team

Cada team dispone de:

```text
instancia PostgreSQL propia;
DB propia;
red DATA propia;
volumen propio;
credenciales propias.
```

No existe:

```text
DB compartida;
usuario compartido;
5432 publicado.
```

---

# 6. Schemas

```text
app
lab
```

`app`:

```text
modelo funcional.
```

`lab`:

```text
superficie pedagógica controlada.
```

`public`:

```text
sin CREATE para PUBLIC;
no usado para objetos principales.
```

---

# 7. Permisos Student

Permitido:

```text
SELECT sobre objetos pedagógicos;
SELECT metadata básica;
UPDATE(score) sobre lab.my_team_score.
```

Prohibido:

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
SUPERUSER;
BYPASSRLS.
```

---

# 8. M4 — UPDATE seguro

No se concede:

```text
UPDATE directo sobre app.scores.
```

Se utiliza:

```text
lab.my_team_score
```

que expone:

```text
solo fila del team;
solo campos pedagógicos.
```

Permiso:

```text
UPDATE(score)
```

Si la vista no es automáticamente actualizable:

```text
INSTEAD OF UPDATE trigger
```

con scope fijo.

---

# 9. Credenciales PostgreSQL

Por team:

```text
bootstrap/admin;
migrator;
app;
student.
```

Todas diferentes entre sí y entre teams.

Autenticación:

```text
SCRAM-SHA-256.
```

Passwords runtime:

```text
>= 24 caracteres;
generados por CSPRNG.
```

---

# 10. Student DB hardening

Valores iniciales:

```text
CONNECTION LIMIT 4
statement_timeout 10s
lock_timeout 3s
idle_in_transaction_session_timeout 30s
temp_file_limit ~64 MB
```

Se validan durante implementación.

---

# 11. Runtime users

Frontend:

```text
no-root.
```

API:

```text
no-root.
```

Toolbox:

```text
student no-root.
```

Gateway:

```text
no-root cuando sea viable.
```

PostgreSQL:

```text
usuario oficial de imagen.
```

---

# 12. Capabilities

Baseline:

```text
cap_drop: ALL
```

No añadir:

```text
SYS_ADMIN
NET_ADMIN
SYS_PTRACE
SYS_MODULE
```

sin justificación formal.

---

# 13. Privilege escalation

Aplicar:

```text
no-new-privileges:true
```

donde sea compatible.

Toolbox:

```text
sin sudo;
sin docker group;
sin root password utilizable.
```

---

# 14. Filesystems

Frontend:

```text
read-only + tmpfs.
```

API:

```text
read-only + /tmp + lablogs RW.
```

Toolbox:

```text
read-only preferido;
home/tmp efímeros.
```

Gateway:

```text
read-only + runtime tmpfs.
```

DB:

```text
PGDATA writable.
```

---

# 15. Mount policy

Prohibido:

```text
/var/run/docker.sock
/home/docker-data
/home/tulum
/etc host
/proc host
/sys host
/var/www/pelican
host devices
```

Solo mounts explícitos ClubLab.

---

# 16. Volúmenes

DB:

```text
db-data
→ solo PostgreSQL.
```

Logs pedagógicos:

```text
lablogs
→ API RW
→ Toolbox RO.
```

No compartir entre teams.

---

# 17. Toolbox

Contiene únicamente herramientas necesarias:

```text
bash;
curl;
psql;
jq;
getent;
dig;
nc;
ss;
ip;
clublab;
ttyd.
```

No incluir en v1:

```text
Docker CLI;
sudo;
nmap;
tcpdump;
metasploit;
iptables;
nft.
```

si no son necesarias.

---

# 18. Terminal web

Tecnología:

```text
ttyd o equivalente.
```

Acceso:

```text
Gateway /terminal/
```

Auth v1:

```text
Basic Auth único por team.
```

Shell:

```text
student no-root.
```

No publicación directa del puerto 7681.

---

# 19. Gateway

```text
clublab-gateway
Caddy
```

Hardening:

```text
no-root;
read-only;
cap_drop ALL;
no-new-privileges;
sin Docker socket;
sin DATA networks;
sin NET_ADMIN;
config estática/generada.
```

---

# 20. Gateway no es router

Su función:

```text
reverse proxy L7.
```

No:

```text
forwarding L3;
SOCKS;
CONNECT;
proxy abierto;
destinos arbitrarios.
```

---

# 21. Caddy Admin API

No accesible desde LAN.

Preferencia:

```text
disabled
```

o:

```text
loopback interno.
```

---

# 22. Student CLI

Herramienta:

```text
clublab
```

Permitido:

```text
whoami
status
health
logs api
recover ranking-db
help
```

No permite:

```text
reset;
scenario load;
deploy;
Docker.
```

Arguments:

```text
whitelist.
```

No usar input libre en shell.

---

# 23. Instructor CLI

Herramienta:

```text
clublabctl
```

Host-side.

Funciones:

```text
preflight;
deploy;
status;
resources;
logs;
scenario;
recover;
reset;
spare;
audit.
```

No se instala en toolbox.

---

# 24. Recovery token

Por team:

```text
scope=teamXX;
action=recover-ranking-db.
```

No permite:

```text
reset;
scenario load;
cross-team.
```

Se asume que el alumno podría leerlo.

Por eso la seguridad depende de:

```text
scope + validación server-side.
```

---

# 25. Recovery endpoint

Características:

```text
interno;
no publicado por gateway;
auth scoped;
idempotente;
team-bound.
```

Si escenario está normal:

```text
no-op.
```

---

# 26. Scenario state

Server-side.

No writable por toolbox.

El alumno puede:

```text
recover.
```

No puede:

```text
set scenario.
```

---

# 27. Secrets

Categorías:

```text
DB bootstrap
DB migrator
DB app
DB student
terminal auth
recovery token
app secret
```

Cada servicio recibe solo lo necesario.

---

# 28. Distribución de secrets

Frontend:

```text
ninguno de backend/DB.
```

API:

```text
DB app + app secrets.
```

Toolbox:

```text
DB student + recovery token.
```

Gateway:

```text
terminal auth.
```

Instructor:

```text
inventario runtime completo.
```

---

# 29. Almacenamiento de secrets

Host-side:

```text
/home/tulum/infra/clublab/runtime/secrets/
```

Permisos:

```text
directory 700
files 600
umask 077
```

Fuera de Git.

---

# 30. Git

Prohibido versionar:

```text
runtime env;
passwords;
tokens;
credentials.
```

Repositorio:

```text
templates;
examples;
generators.
```

---

# 31. Logs

Lablogs no contienen:

```text
passwords;
DATABASE_URL completa;
tokens;
Authorization completo;
cookies;
host paths.
```

Errores HTTP:

```text
genéricos.
```

Audit:

```text
sin secrets.
```

---

# 32. Guard rails de clublabctl

Toda operación requiere:

```text
team whitelist;
prefijo esperado;
project label;
team label;
role label.
```

Ante inconsistencia:

```text
ABORT.
```

---

# 33. Teams válidos

```text
team01
team02
team03
team04
team05
team06
spare
```

No aceptar identificadores arbitrarios.

---

# 34. Comandos destructivos globales

Prohibidos:

```text
docker system prune
docker volume prune
docker network prune
stop/remove all
```

o equivalentes.

---

# 35. Reset

`reset teamXX`:

```text
solo team;
confirmación;
seed;
grants;
hardening;
scenario normal.
```

`reset all`:

```text
flag y confirmación fuerte.
```

---

# 36. Auditoría

Eventos:

```text
deploy
scenario load
scenario clear
recover instructor
reset
spare
credential rotation
```

Formato preferido:

```text
JSON Lines.
```

Campos:

```text
timestamp
actor
action
team
result
```

---

# 37. Network isolation

Cada team:

```text
APP network
DATA network
```

sin compartir con otros teams.

Gateway:

```text
solo APP.
```

DB:

```text
solo DATA.
```

No añadir:

```text
host.docker.internal
host network
extra host gateway
```

---

# 38. Firewall

Solo gateway publica:

```text
8211–8216
8219
```

Binding:

```text
CLUBLAB_BIND_IP.
```

Firewall:

```text
permite red de clase;
bloquea exposición innecesaria.
```

Docker networks siguen siendo la frontera principal.

---

# 39. Servicios del host
Toolbox no debe alcanzar:

```text
SSH 22
Cockpit 9090
WhatsApp 8080/3500
Pelican/Wings
Playit
postgres-main
Tailscale services
```

Esto se valida, no se asume.

---

# 40. HTTP / HTTPS

v1:

```text
HTTP permitido únicamente en LAN controlada.
```

Condiciones:

```text
datos ficticios;
credenciales desechables;
sin secretos productivos.
```

Acceso remoto/no confiable:

```text
HTTPS obligatorio.
```

---

# 41. Resource limits

Por team:

| Servicio | RAM | CPU | PIDs |
|---|---:|---:|---:|
| Frontend | 128 MiB | 0.25 | 64 |
| API | 512 MiB | 0.75 | 128 |
| PostgreSQL | 640 MiB | 0.75 | 128 |
| Toolbox | 256 MiB | 0.25 | 64 |

Deben verificarse en runtime.

---

# 42. Security gates

## S1 — Database

Pruebas de:

```text
SELECT;
UPDATE autorizado;
DDL prohibido;
cross-team credentials.
```

## S2 — Container Isolation

```text
no-root;
capabilities;
filesystem;
Docker socket;
limits.
```

## S3 — Network Isolation

```text
cross-team;
host;
gateway;
DB publication;
terminal auth.
```

## S4 — Control Plane

```text
recovery token;
reset;
scenario;
labels;
whitelist.
```

## S5 — Secrets

```text
logs;
Git;
env;
audit;
file permissions.
```

---

# 43. Matriz de pruebas

Se define una suite de 48 pruebas.

Las pruebas CRÍTICAS incluyen:

```text
no root;
no Docker socket;
no host mounts;
no cross-team;
DB no publicada;
student DB limitado;
token cross-team inválido;
reset aislado;
secrets no expuestos;
gateway no proxy abierto;
host/producción inaccesible.
```

Documento fuente:

```text
ClubLab_Fase_3_Bloque_D_Pruebas_y_Cierre.md
```

---

# 44. Criterio de piloto

Antes de un piloto:

```text
TODAS las pruebas CRÍTICAS = PASS.
```

Además:

```text
ninguna prueba ALTA = FAIL sin mitigación aprobada.
```

---

# 45. Estado de validación actual

A la fecha de cierre de diseño:

```text
matriz definida;
implementación todavía no construida;
tests reales no ejecutados.
```

Por tanto:

```text
SEGURIDAD DISEÑADA
≠
SEGURIDAD EMPÍRICAMENTE VALIDADA.
```

No se inventan resultados PASS.

---

# 46. Riesgos residuales aceptados de v1

```text
Basic Auth sobre HTTP en LAN controlada;
recovery token legible por su propio alumno;
toolbox con shell amplia dentro de su propio team;
sin Vault/KMS;
sin custom seccomp;
sin stack SIEM/observabilidad pesada.
```

Se aceptan porque:

```text
datos ficticios;
entorno local;
credenciales desechables;
scope fuerte;
objetivo educativo.
```

---

# 47. Controles deliberadamente no añadidos

No se requiere inicialmente:

```text
Kubernetes
Vault
Prometheus/Grafana
SELinux custom policy
custom seccomp profile
SSO
mTLS
SIEM
WAF
```

Se añadirán solo si una necesidad real lo justifica.

---

# 48. Decisiones congeladas

```text
PostgreSQL por team
roles owner/migrator/app/student
vista lab.my_team_score
SCRAM-SHA-256
student no-root
cap_drop ALL
no-new-privileges
read-only donde aplique
ttyd Basic Auth por team
gateway sin Docker socket
student CLI separado
instructor CLI separado
recovery token scoped
runtime secrets fuera de Git
guard rails prefix+labels
firewall como capa adicional
48 pruebas de seguridad
```

---

# 49. Requisitos para implementación

Cuando se construyan Fases 4–5 y la infraestructura:

```text
Compose debe expresar hardening;
Dockerfiles deben utilizar users no-root;
migrations deben crear roles/grants;
toolbox debe contener clublab;
API debe implementar recovery control;
gateway config debe ser generada;
clublabctl debe aplicar guard rails.
```

---

# 50. Requisitos antes de clase

Ejecutar:

```text
security suite;
preflight;
cross-team tests;
DB permission tests;
secret scan;
stress controlado.
```

Registrar:

```text
build;
fecha;
resultado;
excepciones.
```

---

# 51. Criterios de cierre de diseño

```text
[x] modelo de confianza
[x] identidades
[x] PostgreSQL
[x] UPDATE seguro
[x] credenciales
[x] hardening contenedores
[x] terminal
[x] gateway
[x] student CLI
[x] instructor CLI
[x] recovery token
[x] secrets
[x] firewall
[x] auditoría
[x] resource limits
[x] matriz de pruebas
[x] security gates
```

# FASE 3 — DISEÑO COMPLETADO

---

# 52. Validación pendiente

La fase solo podrá cambiar a:

```text
FASE 3 — VALIDADA
```

cuando:

```text
implementación exista;
tests CRÍTICOS pasen;
gates S1–S5 sean aprobados.
```

---

# 53. Próximo paso

El siguiente trabajo puede avanzar a la aplicación de ClubLab, manteniendo este documento como contrato de seguridad.

La siguiente pregunta es:

> **¿Qué aplicación concreta, modelo de datos y endpoints debemos construir para ejecutar M0–M8 exactamente como se diseñaron?**