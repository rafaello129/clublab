# D04 — Scenario Manager y Operación de ClubLab

**Versión:** v1  
**Estado:** FINAL DE DISEÑO + CONTROL PLANE IMPLEMENTADO  
**Fase:** 5  
**Live validation:** pendiente

---

## 1. Propósito

D04 define cómo se opera ClubLab sin exponer Docker ni infraestructura administrativa a los alumnos.

Existen dos planos:

```text
Alumno
→ clublab

Instructor
→ clublabctl
```

---

## 2. Student CLI

```text
clublab whoami
clublab status
clublab health
clublab logs api
clublab recover ranking-db
```

No contiene:

```text
deploy
reset
scenario load
Docker access
host access
```

---

## 3. Instructor CLI

```text
inventory
preflight
deploy
smoke
status
resources
logs
scenario
recover
reset
spare
audit
```

---

## 4. Estados

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

Se distingue:

```text
infra_state
expected_scenario
observed_scenario
```

---

## 5. Escenarios

```text
normal
ranking-db-failure
api-down
```

### ranking-db-failure

```text
API health 200
DB real healthy
ranking 500
otros endpoints 200
```

### api-down

```text
API container detenido
frontend/DB/toolbox permanecen activos
```

---

## 6. Scenario transport

El control de escenario de aplicación se realiza desde el host:

```text
clublabctl
→ docker exec API
→ Node fetch 127.0.0.1:3000/internal/...
```

El control token permanece dentro del API.

No se publica una ruta administrativa por gateway.

---

## 7. Recovery

```text
R1 scenario clear
R2 API restart
R3 explicit reset
```

R3 nunca es automático.

---

## 8. Reset

```text
validate
→ RESETTING
→ team compose down
→ remove only labelled db-data/lablogs
→ database up
→ bootstrap
→ services up
→ normal
→ smoke
→ READY
```

Solo se eliminan recursos del target validado.

---

## 9. Preflight

Comprueba:

```text
inventory
Docker
Compose
bind IP
RAM
disk
runtime permissions
ports
IPAM
container hardening
spare presence
```

Fail-closed.

---

## 10. Status

Vista operativa:

```text
TEAM
FRONT
API
DB
TOOLBOX
SCENARIO
STATE
```

---

## 11. Resources

Solo recursos ClubLab:

```text
CPU
RAM
PIDs
network I/O
```

No mezcla servicios productivos.

---

## 12. Logs

Alumno:

```text
lab-events.jsonl sanitizado
```

Instructor:

```text
docker logs del role validado
```

---

## 13. Spare

```text
port 8219
independent clean stack
normal scenario
```

Asignación:

```text
original team → spare
```

No migra DB ni logs.

---

## 14. Audit

```text
runtime/audit/clublabctl.jsonl
```

Registra acciones del plano instructor.

No registra secrets ni comandos individuales del alumno.

---

## 15. Deploy

Para un entorno ausente:

```text
preflight
→ database
→ bootstrap
→ frontend/API/toolbox
→ gateway
→ APP network attachment
→ smoke
→ READY
```

Para un entorno existente:

```text
normal + healthy → idempotent success
scenario/degraded → refuse
```

---

## 16. Gateway

Shared resource:

```text
clublab-gateway
```

Publica:

```text
8211 team01
8212 team02
8213 team03
8214 team04
8215 team05
8216 team06
8219 spare
```

Solo se conecta a APP networks.

---

## 17. Smoke

Comprueba:

```text
frontend
API
database
toolbox
readiness
ranking
scenario normal
gateway frontend
gateway API
```

No modifica estado.

---

## 18. Runtime

Servidor:

```text
/home/tulum/infra/clublab/runtime/
```

Versionado:

```text
templates
inventario
CLI
tests
scenario contracts
```

No versionado:

```text
env
passwords
tokens
state
audit
```

---

## 19. Seguridad operacional

Guard rails:

```text
target allowlist
resource labels
project prefix
role allowlist
network labels
volume suffix allowlist
no shell=True
no prune global
no Docker socket student
no direct DB/API publish
```

---

## 20. Default class deployment

```text
team01
team02
team03
team04
spare
```

Presupuesto inicial aproximado:

```text
1.5 GiB/team
+
host reserve
```

Team05/06 se habilitan deliberadamente para sesiones mayores.

---

## 21. Flujo operativo de clase

### Antes

```text
preflight
deploy
smoke
status
spare status
```

### Incidente

```text
scenario load all ranking-db-failure
```

### Recuperación

```text
student recover
instructor status
```

### Contingencia

```text
instructor recover
reset explicit
or spare
```

---

## 22. Implementación en repo

```text
scripts/clublabctl/
infrastructure/toolbox/bin/clublab
infrastructure/teams/teams.json
infrastructure/templates/
tests/operation/
.github/workflows/operations-tests.yml
```

---

## 23. Validación

### Automatizada

Unit tests + GitHub Actions.

### Pendiente física

```text
real Compose
real images
Tulum runtime
LAN routes
security gate
4-team rehearsal
6-team + spare load test
```

No se considera que estas pruebas hayan ocurrido hasta ejecutarlas en el servidor.

---

## 24. Estado final

```text
Fase 5 / Bloque A ✅
Fase 5 / Bloque B ✅
Fase 5 / Bloque C ✅
Fase 5 / Bloque D ✅
```

# FASE 5 — CERRADA

El control plane está diseñado e implementado.

La siguiente etapa debe conectar este control plane con la aplicación e infraestructura reales antes de producir el ensayo completo.
