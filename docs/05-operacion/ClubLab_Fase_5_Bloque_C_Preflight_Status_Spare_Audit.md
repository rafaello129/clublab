# ClubLab — Fase 5 / Bloque C
## Preflight, status, resources, logs, spare y auditoría

**Estado:** DISEÑO CERRADO v1 + IMPLEMENTACIÓN BASE  
**Dependencias:** Fase 5/Bloques A–B + D02 + D03 + APP04

---

## 1. Objetivo

Este bloque hace que ClubLab sea operable antes y durante una clase sin depender de inspección manual de Docker.

Se implementan:

```text
clublabctl preflight [target]
clublabctl status [target]
clublabctl resources [target]
clublabctl logs <team> <role> [--lines N]

clublabctl spare status
clublabctl spare assign <team>
clublabctl spare release

clublabctl audit tail [--lines N]
```

`deploy` permanece reservado para el Bloque D, porque necesita el Compose real, generación de environment y smoke tests integrados.

---

## 2. Preflight

`preflight` es **fail-closed**.

Categorías:

```text
CONFIG
HOST
NETWORK
PORTS
SECRETS
SECURITY
SPARE
```

Estados:

```text
PASS
WARN
FAIL
```

Un `FAIL` crítico produce exit code 4.

---

## 3. Checks implementados

### CONFIG

- inventario válido;
- existencia de `infrastructure/compose/team.compose.yml`.

### HOST

- Docker daemon disponible;
- `MemAvailable`;
- espacio libre en `/home` o filesystem operativo.

### NETWORK

- `CLUBLAB_BIND_IP` definido;
- IP sintácticamente válida;
- IP realmente asignada al host;
- APP/DATA subnets sin overlap con redes Docker extranjeras.

### PORTS

Por target:

- puerto libre antes de despliegue; o
- puerto publicado por `clublab-gateway` validado por labels/nombre.

Un puerto ocupado por un proceso o contenedor ajeno a ClubLab produce `FAIL`.

### SECRETS

- `runtime/teams` modo `0700`;
- `runtime/secrets` modo `0700`;
- `runtime/teams/teamXX.env` modo `0600`.

### SECURITY

Para teams ya desplegados:

- `privileged=false`;
- sin host network/PID/IPC;
- sin capabilities peligrosas;
- frontend/API/toolbox no-root;
- `no-new-privileges`;
- frontend/API con root filesystem read-only;
- límites de RAM/PIDs/CPU;
- sin mounts productivos sensibles;
- sin published ports directos en servicios del team.

### SPARE

La ausencia del spare produce `WARN`, no bloquea por sí sola el preflight.

---

## 4. Presupuesto de capacidad

Los thresholds viven en:

```text
infrastructure/teams/teams.json
```

Valores iniciales:

```text
memory_per_absent_team_mib = 1536
memory_host_reserve_mib    = 4096

disk_per_absent_team_gib   = 2
disk_host_reserve_gib      = 5
```

Así el código no contiene el presupuesto como una constante oculta.

---

## 5. `status`

Formato:

```text
TEAM     FRONT    API      DB       TOOLBOX  SCENARIO                 STATE
team01   OK       OK       OK       OK       normal                   READY
team02   OK       OK       OK       OK       ranking-db-failure       SCENARIO
team03   OK       DOWN     OK       OK       api-down                 SCENARIO
team04   ABSENT   ABSENT   ABSENT   ABSENT   absent                   ABSENT
```

`status all` muestra todos los targets del inventario, incluido el spare.

Estados funcionales:

```text
READY
SCENARIO
DEGRADED
ABSENT
```

No confunde un fallo pedagógico esperado con una degradación inesperada.

---

## 6. `resources`

Muestra únicamente contenedores ClubLab validados:

```text
TEAM
ROLE
CPU
MEMORY
PIDS
NET I/O
```

La fuente es:

```text
docker stats --no-stream
```

No mezcla Pelican, WhatsApp ni otros servicios productivos.

---

## 7. Logs técnicos

Instructor:

```bash
clublabctl logs team01 api --lines 100
```

Roles permitidos:

```text
frontend
api
database
toolbox
```

El container se resuelve mediante labels + prefijo antes de ejecutar:

```text
docker logs
```

No se aceptan:

```text
container IDs libres
paths
nombres arbitrarios
```

Estos logs son distintos de:

```text
clublab logs api
```

que muestra el log pedagógico sanitizado al alumno.

---

## 8. Spare

El spare sigue siendo un stack real independiente:

```text
spare
port 8219
APP  10.77.9.0/24
DATA 10.77.109.0/24
```

Antes de asignarse debe estar:

```text
READY
scenario=normal
```

---

## 9. `spare assign`

Ejemplo:

```bash
clublabctl spare assign team03
```

La asignación:

- no renombra infraestructura;
- no copia DB;
- no copia lablogs;
- no copia session state;
- no revela credenciales en audit;
- registra el mapping runtime.

Estado:

```text
runtime/state/spare.json
```

Solo puede haber una asignación activa.

Asignar de nuevo al mismo team es idempotente.

Asignar a otro team requiere primero:

```bash
clublabctl spare release
```

---

## 10. Continuidad pedagógica

El objetivo del spare es:

> restaurar la clase rápidamente, no clonar el entorno roto.

Por tanto el alumno continúa con un seed limpio.

La pérdida de un cambio M4 en un team roto es aceptable frente a detener toda la actividad.

---

## 11. Auditoría

Archivo:

```text
$CLUBLAB_RUNTIME_DIR/audit/clublabctl.jsonl
```

Permisos:

```text
dir  0700
file 0600
```

Formato:

```text
JSON Lines
```

Campos permitidos:

```text
ts
actor
action
result
team
scenario
meta restringido
```

No se aceptan dumps arbitrarios de environment o stderr.

---

## 12. Eventos auditados

Ya se registran:

```text
scenario.load
scenario.clear
recover
reset
preflight
spare.assign
spare.release
```

El audit no registra:

```text
passwords
control token
recovery token
DB URL
cada comando del alumno
```

---

## 13. `audit tail`

Ejemplo:

```bash
clublabctl audit tail --lines 30
```

Salida humana:

```text
timestamp actor action team result
```

El archivo JSONL permanece disponible para automatización posterior.

---

## 14. Runtime observado

La capa de observación se implementa en:

```text
OperationalRuntime
OperationalMonitor
PreflightRunner
SpareManager
AuditLogger
```

Esto mantiene separadas:

```text
mutaciones
observación
preflight
audit
```

del parser CLI.

---

## 15. Preflight y estado actual del repo

Aún no existe:

```text
team.compose.yml
runtime env real
gateway real
images de aplicación
```

Por tanto un preflight real **debe fallar actualmente**.

Eso es comportamiento correcto.

El comando no se diseñó para producir un falso PASS antes de que exista infraestructura.

---

## 16. Tests

Se añadieron tests para:

```text
audit write/tail
filtrado de metadata sensible
monitor READY
monitor api-down
monitor ABSENT
logs scoped
spare assign/release
spare idempotency
spare conflict
preflight helpers
inventory/scenario tests existentes
```

GitHub Actions continúa ejecutando:

```text
python -m unittest discover -s tests/operation -v
```

---

## 17. Decisiones cerradas

### DC5-01
Preflight crítico es fail-closed.

### DC5-02
La IP de bind debe existir realmente en el host.

### DC5-03
Un puerto ocupado solo es válido si pertenece al gateway ClubLab esperado.

### DC5-04
Los thresholds de capacidad se versionan en el inventario.

### DC5-05
`status all` incluye targets ausentes para dar una vista operativa completa.

### DC5-06
Resources solo muestra recursos ClubLab.

### DC5-07
Technical logs requieren team + role validado.

### DC5-08
Spare usa mapping operativo; no migración de estado.

### DC5-09
Solo una asignación spare puede estar activa.

### DC5-10
Audit usa JSONL, permisos restrictivos y schema limitado.

### DC5-11
Preflight verifica hardening de containers ya desplegados.

### DC5-12
`deploy` queda para integración del Bloque D.

---

# BLOQUE C — COMPLETADO

El siguiente bloque cerrará Fase 5 con:

```text
deploy
integración operacional completa
smoke tests
matriz OP-01..OP-15
D04 final
```
