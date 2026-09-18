# ClubLab — Fase 3 / Bloque D
## Pruebas de seguridad + consolidación de D03

**Proyecto:** ClubLab v1  
**Fase:** 3 — Seguridad y aislamiento  
**Bloque:** D  
**Estado:** DISEÑO COMPLETADO — EJECUCIÓN DE PRUEBAS PENDIENTE  
**Dependencias:** D00 + D01 + D02 + Fase 3/Bloques A–C  

---

# 1. Propósito

Este bloque cierra el diseño de seguridad de ClubLab y transforma todas las decisiones de los Bloques A–C en una matriz de pruebas verificables.

La regla de cierre es:

> **No considerar un control seguro solo porque está documentado; debe existir una prueba concreta que demuestre su comportamiento.**

Sin embargo, ClubLab todavía no está implementado.

Por tanto, este bloque produce:

```text
la matriz completa de validación;
los criterios PASS/FAIL;
los comandos/pruebas esperadas;
los gates de seguridad;
el documento D03 consolidado.
```

La ejecución real ocurrirá cuando exista una implementación funcional de los contenedores, redes, usuarios y CLI.

---

# 2. Estados de validación

Cada prueba tendrá uno de estos estados:

```text
PENDIENTE
PASS
FAIL
BLOCKED
N/A
```

Significado:

```text
PENDIENTE
→ diseño existe, implementación todavía no probada

PASS
→ comportamiento observado coincide con requisito

FAIL
→ el control no funciona como se diseñó

BLOCKED
→ no pudo probarse por dependencia técnica

N/A
→ control no aplica a la implementación final
```

No utilizar:

```text
“parece seguro”
“debería funcionar”
```

como equivalente a PASS.

---

# 3. Severidad de pruebas

Las pruebas se clasifican:

```text
CRÍTICA
ALTA
MEDIA
```

## CRÍTICA

Un FAIL bloquea el piloto.

Ejemplos:

```text
Docker socket accesible;
root en toolbox;
cross-team DB;
DB publicada;
token cross-team válido;
host accesible.
```

## ALTA

Debe corregirse antes de clase.

## MEDIA

Puede aceptarse temporalmente con mitigación documentada.

---

# 4. Matriz maestra

| ID | Prueba | Severidad | Estado inicial |
|---|---|---|---|
| T01 | Toolbox no-root | CRÍTICA | PENDIENTE |
| T02 | sudo/su no permiten escalado | CRÍTICA | PENDIENTE |
| T03 | Docker socket inaccesible | CRÍTICA | PENDIENTE |
| T04 | Host filesystem no montado | CRÍTICA | PENDIENTE |
| T05 | Capabilities peligrosas ausentes | CRÍTICA | PENDIENTE |
| T06 | no-new-privileges aplicado | ALTA | PENDIENTE |
| T07 | Filesystem read-only donde aplica | ALTA | PENDIENTE |
| T08 | Resource limits activos | ALTA | PENDIENTE |
| T09 | Team01 no alcanza Team02 | CRÍTICA | PENDIENTE |
| T10 | Gateway no alcanza DATA | CRÍTICA | PENDIENTE |
| T11 | DB no publicada al host | CRÍTICA | PENDIENTE |
| T12 | API interna no publicada | ALTA | PENDIENTE |
| T13 | Terminal protegida | CRÍTICA | PENDIENTE |
| T14 | Credenciales terminal no sirven cross-team | CRÍTICA | PENDIENTE |
| T15 | Student DB SELECT autorizado | ALTA | PENDIENTE |
| T16 | Student UPDATE score propio | ALTA | PENDIENTE |
| T17 | Student no modifica team_id | CRÍTICA | PENDIENTE |
| T18 | Student no modifica otra fila | CRÍTICA | PENDIENTE |
| T19 | Student no DROP/ALTER/TRUNCATE | CRÍTICA | PENDIENTE |
| T20 | Student no CREATE ROLE | CRÍTICA | PENDIENTE |
| T21 | App runtime no es owner | ALTA | PENDIENTE |
| T22 | App no administra schema | ALTA | PENDIENTE |
| T23 | Credenciales DB únicas por team | ALTA | PENDIENTE |
| T24 | Token recovery cross-team falla | CRÍTICA | PENDIENTE |
| T25 | Recover solo limpia escenario propio | CRÍTICA | PENDIENTE |
| T26 | Recover es idempotente | ALTA | PENDIENTE |
| T27 | Student no puede scenario load | CRÍTICA | PENDIENTE |
| T28 | Student no puede reset | CRÍTICA | PENDIENTE |
| T29 | clublabctl rechaza team inválido | CRÍTICA | PENDIENTE |
| T30 | clublabctl exige labels/prefix | CRÍTICA | PENDIENTE |
| T31 | reset team01 no toca team02 | CRÍTICA | PENDIENTE |
| T32 | scenario team01 no toca team02 | CRÍTICA | PENDIENTE |
| T33 | Secrets no aparecen en lablogs | CRÍTICA | PENDIENTE |
| T34 | Secrets no aparecen en errores HTTP | CRÍTICA | PENDIENTE |
| T35 | Toolbox no contiene app DB password | CRÍTICA | PENDIENTE |
| T36 | Gateway no contiene DB secrets | ALTA | PENDIENTE |
| T37 | Gateway no funciona como proxy abierto | CRÍTICA | PENDIENTE |
| T38 | Caddy Admin API no accesible desde LAN | ALTA | PENDIENTE |
| T39 | Toolbox no accede a SSH/Cockpit host | CRÍTICA | PENDIENTE |
| T40 | Toolbox no accede a servicios productivos | CRÍTICA | PENDIENTE |
| T41 | Scenario no desactiva controles | CRÍTICA | PENDIENTE |
| T42 | Reset recrea permisos correctamente | ALTA | PENDIENTE |
| T43 | Secrets runtime con permisos 600/700 | ALTA | PENDIENTE |
| T44 | No secrets versionados en Git | CRÍTICA | PENDIENTE |
| T45 | Audit no registra secrets | ALTA | PENDIENTE |
| T46 | Stress básico no afecta otro team | ALTA | PENDIENTE |
| T47 | Stress básico no degrada host | ALTA | PENDIENTE |
| T48 | Spare respeta mismos controles | ALTA | PENDIENTE |

---

# 5. T01 — Toolbox no-root

Ejecutar:

```bash
id
whoami
```

Esperado:

```text
user=student
uid != 0
```

PASS si:

```text
el proceso de shell no corre como root.
```

FAIL si:

```text
uid=0
```

Severidad:

```text
CRÍTICA
```

---

# 6. T02 — Escalado local

Probar:

```bash
sudo -n true
su -
```

Esperado:

```text
sudo inexistente/denegado;
su no permite root.
```

También comprobar:

```text
student no pertenece a wheel/sudo/docker.
```

---

# 7. T03 — Docker socket

Dentro de toolbox:

```bash
test -S /var/run/docker.sock
```

Esperado:

```text
FALSE
```

También:

```bash
docker ps
```

debe:

```text
no existir
o
no tener daemon accesible.
```

Cualquier acceso funcional al Docker del host:

```text
FAIL CRÍTICO.
```

---

# 8. T04 — Filesystem host

Comprobar mounts:

```bash
mount
cat /proc/mounts
```

No debe aparecer:

```text
/home/tulum
/home/docker-data
/etc del host
/var/www/pelican
Docker socket
```

---

# 9. T05 — Capabilities

Desde host:

```text
docker inspect <container>
```

Validar:

```text
CapDrop incluye ALL
```

y que no existan:

```text
SYS_ADMIN
NET_ADMIN
SYS_PTRACE
SYS_MODULE
```

sin justificación explícita.

---

# 10. T06 — no-new-privileges

Desde host:

```text
SecurityOpt
```

Esperado:

```text
no-new-privileges:true
```

para:

```text
frontend
api
toolbox
gateway
```

y donde sea compatible.

---

# 11. T07 — Read-only filesystem

Frontend/API/Gateway:

```bash
touch /security-test
```

Esperado:

```text
Read-only file system
```

Pero:

```bash
touch /tmp/security-test
```

debe funcionar si `/tmp` está habilitado.

Toolbox:

```text
/home/student → writable
/etc → read-only
```

---

# 12. T08 — Límites de recursos

Desde instructor:

```text
inspect limits
```

Comprobar:

```text
Memory
NanoCPUs/CPU quota
PidsLimit
```

contra D02.

No basta documentarlos en Compose si Docker no los aplica realmente.

---

# 13. T09 — Cross-team network

Desde:

```text
team01-toolbox
```

intentar alcanzar:

```text
team02 API
team02 DB
team02 toolbox
```

mediante:

```text
DNS;
subnet IP;
puerto.
```

Esperado:

```text
unreachable / timeout / no route.
```

---

# 14. T10 — Gateway no llega a DATA

Desde `clublab-gateway`:

```text
team01 database:5432
```

debe ser:

```text
inaccesible.
```

El gateway no debe formar parte de:

```text
teamXX-data.
```

---

# 15. T11 — DB no publicada

Desde LAN:

```text
<host>:5432
```

Esperado:

```text
no listener ClubLab.
```

Desde:

```bash
docker inspect
```

PostgreSQL TeamXX debe tener:

```text
sin published ports.
```

---

# 16. T12 — API no publicada directamente

Desde LAN:

```text
<host>:3000
```

no debe corresponder a una API ClubLab.

La única ruta debe ser:

```text
gateway /api.
```

---

# 17. T13 — Terminal protegida

Sin Basic Auth:

```text
/team-port/terminal/
```

Esperado:

```text
401 / denied.
```

Con credencial correcta:

```text
shell student.
```

---

# 18. T14 — Terminal cross-team

Usar credencial terminal de team01 en:

```text
team02 /terminal/
```

Esperado:

```text
DENIED.
```

---

# 19. T15 — SELECT pedagógico

Como student:

```sql
SELECT * FROM app.teams;
SELECT * FROM app.scores;
SELECT * FROM lab.my_team_score;
```

según objetos autorizados.

Esperado:

```text
PASS.
```

Esto demuestra que M3 es posible.

---

# 20. T16 — UPDATE pedagógico

Como student:

```sql
UPDATE lab.my_team_score
SET score = <valor válido>;
```

Esperado:

```text
1 fila modificada.
```

Luego:

```text
API refleja dato;
UI refleja dato.
```

Esto valida M4.

---

# 21. T17 — Cambio de identidad

Intentar:

```sql
UPDATE lab.my_team_score
SET team_id = ...;
```

Esperado:

```text
permission denied
o
view no permite columna.
```

---

# 22. T18 — Otra fila

Intentar modificar un team distinto.

Esperado:

```text
0 filas
o
DENIED.
```

Nunca:

```text
UPDATE exitoso.
```

---

# 23. T19 — DDL destructivo

Como student:

```sql
DROP TABLE app.scores;
ALTER TABLE app.scores ...;
TRUNCATE app.scores;
CREATE TABLE test (...);
```

Todos:

```text
DENIED.
```

---

# 24. T20 — Administración de roles

Como student:

```sql
CREATE ROLE attacker;
ALTER ROLE ...;
GRANT ...;
```

Esperado:

```text
DENIED.
```

---

# 25. T21 — API no es owner

Consultar metadata administrativa desde plano instructor.

Esperado:

```text
owner de objetos = clublab_teamXX_owner
```

No:

```text
clublab_teamXX_app.
```

---

# 26. T22 — App runtime no administra schema

Usando la identidad app:

```text
operaciones funcionales → OK
DROP/ALTER/CREATE ROLE → DENIED
```

---

# 27. T23 — Credenciales únicas

Validar:

```text
team01_student_password != team02_student_password
team01_app_password != team02_app_password
terminal01 != terminal02
recovery01 != recovery02
```

No registrar valores completos en resultado.

---

# 28. T24 — Token cross-team

Intentar utilizar:

```text
token team01
```

contra control endpoint Team02.

Esperado:

```text
403.
```

---

# 29. T25 — Scope de recover

Con scenario activo en Team01:

```bash
clublab recover ranking-db
```

Esperado:

```text
Team01 → normal
Team02 → sin cambios
```

---

# 30. T26 — Recover idempotente

Ejecutar dos veces.

Primera:

```text
scenario → normal
```

Segunda:

```text
already healthy / no-op
```

No debe resetear datos.

---

# 31. T27 — Student no puede scenario load

Intentar:

```text
clublab scenario ...
```

Esperado:

```text
comando inexistente/denegado.
```

Intentar endpoint interno de set scenario:

```text
DENIED.
```

---

# 32. T28 — Student no puede reset

No debe existir:

```text
clublab reset
```

ni credencial capaz de invocarlo.

---

# 33. T29 — Team inválido en clublabctl

Ejemplos:

```text
prod
postgres-main
../../etc
team99
```

Resultado:

```text
ABORT
```

antes de cualquier operación Docker.

---

# 34. T30 — Labels/prefix

Preparar caso controlado con recurso inconsistente.

Si:

```text
prefijo correcto
pero label incorrecta
```

o al revés:

```text
clublabctl no opera el recurso.
```

---

# 35. T31 — Reset aislado

Registrar estado Team02.

Ejecutar:

```text
reset Team01
```

Después:

```text
Team01 → seed
Team02 → estado anterior intacto
```

---

# 36. T32 — Scenario aislado

Activar:

```text
ranking-db-failure Team01
```

Esperado:

```text
Team01 ranking = 500
Team02 ranking = 200
```

---

# 37. T33 — Secrets en lablogs

Buscar:

```text
password patterns
DATABASE_URL
Authorization
Bearer
token
secret
```

Resultado:

```text
ningún secret real.
```

---

# 38. T34 — Secrets en HTTP

Forzar errores de:

```text
DB;
ranking;
auth.
```

La respuesta pública no debe incluir:

```text
password;
DATABASE_URL;
stack trace sensible;
token.
```

---

# 39. T35 — Toolbox no contiene APP password

Dentro de toolbox revisar:

```text
env
/home/student
/etc accesible
config clublab
```

No debe aparecer:

```text
DB_APP_PASSWORD.
```

---

# 40. T36 — Gateway sin DB secrets

Revisar:

```text
env;
config;
mounts.
```

Debe contener únicamente lo requerido para routing/terminal auth.

---

# 41. T37 — Gateway no es proxy abierto

Intentar usar rutas/headers manipulados para alcanzar:

```text
database;
host;
Team02 desde Team01;
URL arbitraria.
```

Resultado:

```text
sin ruta.
```

---

# 42. T38 — Caddy Admin API

Desde LAN:

```text
:2019
```

del ClubLab gateway no debe estar publicada.

Si Admin API está habilitada internamente:

```text
solo loopback interno.
```

---

# 43. T39 — Servicios host críticos

Desde toolbox intentar alcanzar:

```text
host SSH
Cockpit
```

Resultado:

```text
FAIL de conexión.
```

---

# 44. T40 — Servicios productivos

Probar de forma controlada conectividad hacia:

```text
WhatsApp frontend/backend;
Pelican;
Wings;
Playit;postgres-main.
```

Esperado:

```text
inaccesible.
```

No enviar operaciones destructivas; solo connectivity checks.

---

# 45. T41 — Scenario conserva seguridad

Comparar:

```text
normal
vs
ranking-db-failure
```

Debe mantenerse idéntico:

```text
users;
mounts;
networks;
capabilities;
secrets;
published ports.
```

El escenario solo cambia:

```text
estado funcional previsto.
```

---

# 46. T42 — Reset conserva hardening

Después de reset:

```text
roles;
grants;
read-only;
terminal auth;
labels;
limits;
network isolation
```

deben seguir iguales.

---

# 47. T43 — Permisos de secret files

Host-side:

```text
runtime/secrets dir → 700
secret files        → 600
```

No deben ser world-readable.

---

# 48. T44 — Git secret scan

Antes del piloto revisar:

```text
tracked files;
history relevante;
.env;
tokens;
password patterns.
```

No debe existir secret runtime versionado.

Si aparece uno:

```text
rotar inmediatamente.
```

---

# 49. T45 — Audit sin secretos

Revisar:

```text
clublabctl audit log
```

Debe contener:

```text
actor;
acción;
team;
resultado.
```

No:

```text
password;
token;
env completo.
```

---

# 50. T46 — Stress de team

Dentro del toolbox, carga controlada hasta límites.

Validar:

```text
Team01 limitado;
Team02 healthy.
```

No intentar afectar deliberadamente al host más allá del test seguro.

---

# 51. T47 — Host bajo stress controlado

Durante prueba anterior:

```text
Docker;
SSH instructor;
servicios productivos
```

deben continuar operativos.

Si el host se degrada:

```text
reducir limits/cambiar prueba.
```

---

# 52. T48 — Spare

El entorno spare debe pasar los mismos controles que:

```text
Team01–Team06.
```

No crear un spare “menos seguro” por ser contingencia.

---

# 53. Gates de seguridad

## Gate S1 — Database

Debe pasar:

```text
T15–T23
```

antes de permitir M3/M4.

## Gate S2 — Container Isolation

Debe pasar:

```text
T01–T08
```

antes de entregar terminal a alumnos.

## Gate S3 — Network Isolation

Debe pasar:

```text
T09–T14
T37–T40
```

antes de conectar la LAN de alumnos.

## Gate S4 — Control Plane

Debe pasar:

```text
T24–T32
```

antes de habilitar escenarios/resets.

## Gate S5 — Secrets

Debe pasar:

```text
T33–T45
```

antes del piloto.

---

# 54. Gate final

Para piloto:

```text
TODAS las pruebas CRÍTICAS = PASS
```

Además:

```text
ninguna ALTA = FAIL sin mitigación aprobada.
```

No se permite iniciar clase real con:

```text
FAIL crítico conocido.
```

---

# 55. Evidencia a conservar

Por prueba:

```text
ID;
fecha;
build/tag;
team;
comando/procedimiento;
resultado;
PASS/FAIL;
nota.
```

No conservar:

```text
secrets;
passwords;
tokens completos.
```

---

# 56. Formato de reporte

```text
T09
Build: 0.1.0
Team: team01
Expected: no connectivity to team02
Observed: timeout
Result: PASS
Notes: tested API + DB
```

---

# 57. Automatización

No todas las pruebas deben ser manuales.

Candidatas a automatizar:

```text
T01
T03
T05
T06
T08
T09
T10
T11
T12
T17–T23
T24
T29–T35
T41–T45
```

Las pruebas de experiencia:

```text
terminal;
gateway;
stress;
```

pueden combinar automatización y revisión manual.

---

# 58. Ubicación futura

Propuesta:

```text
tests/security/
├── container/
├── database/
├── network/
├── control-plane/
└── secrets/
```

Runner conceptual:

```bash
./scripts/security/check-all.sh
```

No se implementa todavía en este bloque.

---

# 59. Riesgos que la prueba debe buscar activamente

No limitarse a “happy path”.

Buscar:

```text
credencial cruzada;
nombre de team inválido;
fila fuera de scope;
route inesperada;
host IP directa;
token reutilizado;
reset parcial;
secret en error;
resource sin label.
```

---

# 60. Resultado del Bloque D

Con los controles definidos en A–C y la matriz de pruebas de este documento:

```text
el DISEÑO de seguridad queda consolidado.
```

Pero:

> **La validación empírica permanece PENDIENTE hasta que exista una implementación ejecutable.**

No se marcarán pruebas ficticiamente como PASS.

---

# 61. Estado de Fase 3

```text
[A] Identidad + PostgreSQL                  ✅ Diseño cerrado
[B] Hardening + terminal + gateway          ✅ Diseño cerrado
[C] Control + secrets + aislamiento         ✅ Diseño cerrado
[D] Matriz de pruebas + D03                 ✅ Diseño cerrado

Ejecución real de tests                      ⏳ Pendiente implementación
```

Por tanto:

# **FASE 3 — DISEÑO COMPLETADO**

La fase no se considerará **validada técnicamente** hasta ejecutar la matriz sobre el sistema real.

---

# 62. Próximo paso

La siguiente fase puede diseñar/construir la aplicación, pero la implementación de infraestructura deberá respetar D03 y luego pasar los gates de seguridad.

La pregunta pasa a ser:

> **¿Qué aplicación concreta vamos a construir para materializar las misiones de ClubLab #01 sin romper estas fronteras?**