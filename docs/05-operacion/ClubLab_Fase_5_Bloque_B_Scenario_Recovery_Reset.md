# ClubLab — Fase 5 / Bloque B
## Scenario Manager, recovery y reset

**Estado:** DISEÑO CERRADO v1 + IMPLEMENTACIÓN BASE  
**Dependencias:** Fase 5/Bloque A + D02 + D03 + APP04

---

## 1. Objetivo

Convertir los escenarios pedagógicos en operaciones reproducibles y seguras desde `clublabctl`.

Comandos implementados en este bloque:

```text
clublabctl scenario load <target> <scenario>
clublabctl scenario clear <target>
clublabctl scenario status [target]
clublabctl recover <target>
clublabctl reset <target> --yes
```

Escenarios soportados:

```text
normal
ranking-db-failure
api-down
```

---

## 2. Separación de estado

El control operativo distingue:

```text
infra_state
expected_scenario
observed_scenario
```

Estados de infraestructura:

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

El estado esperado vive en:

```text
$CLUBLAB_RUNTIME_DIR/state/teamXX.json
```

No contiene secrets.

---

## 3. Target `all`

`all` significa:

> todos los teams ClubLab actualmente desplegados.

No significa:

```text
todos los contenedores Docker
```

ni incluye el `spare` por defecto.

La detección se realiza mediante labels ClubLab.

---

## 4. Guard rails Docker

Un contenedor solo se considera operable si coincide simultáneamente con:

```text
com.clublab.project=clublab
com.clublab.team=<team>
com.clublab.role=<role>
com.clublab.managed-by=clublab
com.clublab.disposable=true
```

y además su nombre pertenece al `compose_project` del inventario.

Si falta una condición:

```text
ABORT
```

---

## 5. Scenario `ranking-db-failure`

Flujo:

```text
clublabctl
   ↓
docker exec en API del team
   ↓
Node 22 / fetch localhost:3000
   ↓
POST /internal/lab/scenario
   ↓
ranking-db-failure
```

El token de control se lee desde el environment del propio contenedor API.

El host no necesita imprimirlo ni pasarlo como argumento de shell.

Validación posterior:

```text
/api/health  = 200
/api/ranking = 500
```

---

## 6. Scenario `api-down`

Se implementa como fallo real de infraestructura:

```text
docker stop <API validada del team>
```

No se simula mediante una variable de la aplicación.

Validación:

```text
API container running = false
```

Frontend, DB y Toolbox no son detenidos.

---

## 7. Scenario clear

`scenario clear` siempre busca regresar a:

```text
scenario=normal
health=200
ranking=200
```

Para `api-down`:

```text
start API
→ wait /api/health
→ set normal
→ validate
```

Para `ranking-db-failure`:

```text
set normal
→ validate
```

---

## 8. Recovery del instructor

Se refina el plan inicial para evitar pérdida accidental de trabajo.

`clublabctl recover teamXX` utiliza:

### R1 — Scenario clear

```text
no destructivo
conserva DB
conserva M4
conserva lablogs
```

### R2 — Restart de API

Solo si R1 falla:

```text
restart API
→ wait health
→ scenario normal
→ validate
```

### R3 — Reset

**No se ejecuta automáticamente.**

Si R1 y R2 fallan, el CLI termina indicando:

```text
Explicit reset required.
```

El instructor debe ejecutar de forma deliberada:

```bash
clublabctl reset teamXX --yes
```

Esto evita que un comando de recovery borre el trabajo del alumno.

---

## 9. Reset

Reset es la única operación destructiva de este bloque.

Requiere:

```text
target válido
+
--yes
```

Para `reset all` además requiere:

```text
--confirm RESET-ALL
```

---

## 10. Contrato de reset

El runtime espera un Compose futuro:

```text
infrastructure/compose/team.compose.yml
```

Servicios runtime:

```text
database
api
frontend
toolbox
```

Servicio one-shot:

```text
bootstrap
```

`bootstrap` deberá ejecutar:

```text
migrations
roles/grants
lab schema
seed
validation inicial
```

---

## 11. Algoritmo de reset implementado

```text
validate target
↓
state = RESETTING
↓
docker compose down --remove-orphans
↓
descubrir volúmenes por labels
↓
validar prefijo + labels + allowlist
↓
eliminar únicamente db-data / lablogs
↓
docker compose up -d database
↓
esperar DB
↓
docker compose run --rm bootstrap
↓
docker compose up -d frontend api toolbox
↓
esperar API
↓
scenario normal
↓
health/ranking validation
↓
state = READY
```

---

## 12. Seguridad de volúmenes

Solo pueden eliminarse volúmenes que cumplan:

```text
project=clublab
team=<target>
managed-by=clublab
disposable=true
```

y cuyo nombre pertenezca al proyecto Compose esperado.

Sufijos permitidos:

```text
db-data
lablogs
```

Cualquier volumen inesperado provoca:

```text
Security guard → ABORT
```

No existe:

```text
docker volume prune
docker system prune
```

---

## 13. Internal control transport

La API no publica `/internal/*` en el gateway.

Para el instructor, `clublabctl` ejecuta una petición HTTP **desde dentro del propio contenedor API** usando Node 22 y `fetch` hacia:

```text
127.0.0.1:3000
```

Ventajas:

```text
no publicar admin port
no montar Docker socket en otro contenedor
no copiar control token al toolbox
no depender de IP interna del container
```

---

## 14. Validaciones de scenario

### normal

```text
health 200
ranking 200
```

### ranking-db-failure

```text
health 200
ranking 500
```

### api-down

```text
API stopped
```

Un scenario no se marca como exitoso sin validar el estado observado.

---

## 15. Partial success

Cuando se utiliza `all`, cada team se procesa individualmente.

Ejemplo:

```text
team01 SUCCESS
team02 SUCCESS
team03 FAIL
team04 SUCCESS
```

Exit code:

```text
7 PARTIAL_SUCCESS
```

No se revierte automáticamente el resto de teams.

---

## 16. Tests

Se agregaron pruebas unitarias para:

```text
ranking-db-failure
api-down
clear api-down
R2 recovery
reset confirmation
all excludes spare
inventory validation
```

La suite de operación utiliza únicamente la librería estándar de Python.

Workflow:

```text
.github/workflows/operations-tests.yml
```

---

## 17. Estado de implementación

Funcional a nivel de código:

```text
scenario manager
runtime state
Docker resource guard
ranking-db-failure control
api-down control
scenario clear
instructor recovery R1/R2
reset orchestration
unit tests
```

Pendiente para ejecución real:

```text
team.compose.yml
backend internal endpoints
images
runtime env generation
bootstrap service
deployment real en Tulum
```

Por lo tanto el código es **fail-closed**: reset no puede ejecutarse accidentalmente antes de existir el manifiesto y environment esperados.

---

## 18. Decisiones cerradas

### DB5-01
`ranking-db-failure` se activa mediante API interna dentro del contenedor API.

### DB5-02
`api-down` detiene realmente el API del team.

### DB5-03
`all` solo opera sobre teams desplegados.

### DB5-04
Spare no entra en scenario `all` por defecto.

### DB5-05
Expected state se persiste en JSON runtime.

### DB5-06
Scenario siempre se valida después de aplicarlo.

### DB5-07
Recover R1/R2 es no destructivo.

### DB5-08
Recover nunca ejecuta reset automáticamente.

### DB5-09
Reset requiere confirmación explícita.

### DB5-10
Reset all requiere `--yes --confirm RESET-ALL`.

### DB5-11
Solo `db-data` y `lablogs` pueden borrarse durante reset.

### DB5-12
No se utilizan operaciones Docker globales.

---

# BLOQUE B — COMPLETADO

El siguiente bloque implementará:

```text
preflight
status
resources
technical logs
spare
audit
```

y cerrará la operación cotidiana antes de la integración final.
