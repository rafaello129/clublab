# ClubLab — Fase 5 / Bloque D
## Deploy, smoke tests, integración operativa y cierre

**Estado:** DISEÑO CERRADO v1 + CONTROL PLANE IMPLEMENTADO  
**Dependencias:** Bloques A–C + D02 + D03 + APP04  
**Entregable consolidado:** `D04_Scenario_Manager_y_Operacion_ClubLab.md`

---

## 1. Objetivo

Cerrar la capa operativa de ClubLab y dejar un flujo único para:

```text
preflight
→ deploy
→ smoke
→ status
→ scenario
→ recover
→ reset/spare
→ audit
```

La Fase 5 queda completa a nivel de diseño y código del control plane.

La validación end-to-end sobre Tulum queda pendiente hasta que existan las imágenes, Compose y aplicación real.

---

## 2. Comandos finales de `clublabctl`

```text
inventory list|show|validate

preflight [target]
deploy [target]
smoke [target]
status [target]
resources [target]
logs <team> <role>

scenario load <target> <scenario>
scenario clear <target>
scenario status [target]

recover <target>
reset <target> --yes

spare status
spare assign <team>
spare release

audit tail
```

---

## 3. `deploy`

`deploy` es fail-closed.

Para un team ausente:

```text
preflight team
↓
state STARTING
↓
database up
↓
wait DB
↓
bootstrap one-shot
↓
frontend + API + toolbox up
↓
wait API
↓
scenario normal
↓
ensure shared gateway
↓
attach gateway to team APP network
↓
smoke
↓
READY
```

---

## 4. Deploy idempotente

Si el team ya existe:

### READY + normal + smoke PASS

```text
deploy → SUCCESS
sin recrear containers
sin reseed
sin reset
```

### Scenario activo

```text
deploy → STATE_CONFLICT
```

El instructor debe usar:

```text
scenario clear
o
recover
```

### Team degradado

```text
deploy → STATE_CONFLICT
```

No intenta “arreglar” destructivamente el entorno.

---

## 5. Target `all` para deploy

`deploy all` utiliza únicamente:

```text
enabled_by_default=true
```

Con el inventario actual:

```text
team01
team02
team03
team04
spare
```

Team05/06 quedan disponibles para una sesión mayor, pero no se levantan por defecto.

---

## 6. Shared gateway

El gateway es un recurso global:

```text
clublab-gateway
```

Contrato esperado:

```text
infrastructure/compose/gateway.compose.yml
runtime/gateway.env
```

El gateway:

- publica exclusivamente los puertos 8211–8216 y 8219;
- pertenece a ClubLab por labels;
- tiene ingress propio;
- se conecta a la APP network de cada team desde el host;
- nunca se conecta a DATA.

---

## 7. APP network

Cada APP network debe llevar:

```text
com.clublab.project=clublab
com.clublab.team=teamXX
com.clublab.network-role=app
com.clublab.managed-by=clublab
```

`clublabctl` no conecta el gateway a una red que no cumpla estos labels.

---

## 8. Runtime env contract

Templates versionados:

```text
infrastructure/templates/team.env.example
infrastructure/templates/gateway.env.example
```

Runtime real:

```text
/home/tulum/infra/clublab/runtime/
```

No se generan secrets débiles automáticamente durante `deploy`.

Preflight exige que el runtime ya exista correctamente.

---

## 9. `smoke`

Se agrega:

```bash
clublabctl smoke team01
clublabctl smoke all
```

Checks previstos:

```text
frontend container
API container + /api/health
database container
toolbox container
/internal/health/ready
/api/ranking
scenario normal
gateway /
gateway /api/health
```

Resultado:

```text
PASS
o
FAIL
```

---

## 10. Bootstrap contract

`bootstrap` es un servicio one-shot del team Compose.

Debe ser:

```text
idempotente para deploy
destructivo solo después de reset de volúmenes
```

Responsabilidades:

```text
migrations
roles
grants
schemas app/lab
seed si DB está vacía
validación inicial
```

No debe reemplazar datos existentes durante un deploy idempotente.

---

## 11. Reset vs deploy

```text
deploy
→ conserva datos

recover
→ conserva datos y lablogs

reset
→ elimina db-data + lablogs
→ vuelve a seed
```

Esta diferencia queda congelada.

---

## 12. Smoke y seed

El smoke genérico no exige score=320 porque un team puede haber completado M4.

La validación exacta de seed inicial pertenece a:

```text
bootstrap
+
E2E fresh-deploy
```

Esto evita que `deploy` rompa la idempotencia después de una modificación legítima.

---

## 13. Flujo antes de clase

```bash
clublabctl preflight
clublabctl deploy
clublabctl smoke
clublabctl status
clublabctl spare status
```

Criterio:

```text
team01–04 READY
spare READY
scenario normal
smoke PASS
```

---

## 14. Flujo del incidente

Aproximadamente minuto 70:

```bash
clublabctl scenario load all ranking-db-failure
```

Después:

```bash
clublabctl scenario status
```

Expected:

```text
todos los teams desplegados → ranking-db-failure
```

Spare queda normal.

---

## 15. Recovery del alumno

Alumno:

```bash
clublab recover ranking-db
```

Instructor observa:

```bash
clublabctl scenario status
```

Los teams vuelven a `normal` independientemente.

---

## 16. Instructor override

Si un team falla:

```text
recover
↓
si falla:
reset explícito
o
spare assign
```

Nunca se resetean automáticamente los demás teams.

---

## 17. Flujo de contingencia

```bash
clublabctl spare status
clublabctl spare assign team03
```

El equipo recibe:

```text
spare URL
app credential
terminal credential
DB student credential
```

La distribución de credenciales será parte del material del instructor.

---

## 18. Cierre de clase

No se usa prune.

La política final será una de:

```text
mantener stacks para revisión
o
docker compose down controlado por proyecto
```

La automatización de shutdown puede añadirse después sin modificar el modelo operativo.

---

## 19. Matriz OP-01..OP-15

| ID | Prueba | Cobertura actual |
|---|---|---|
| OP-01 | Deploy team | Código + unit test; live pendiente |
| OP-02 | Deploy all | Código; live pendiente |
| OP-03 | ranking-db-failure | Código + unit test; live pendiente |
| OP-04 | Scenario clear | Código + unit test; live pendiente |
| OP-05 | api-down | Código + unit test; live pendiente |
| OP-06 | Recover api-down | Código + unit test; live pendiente |
| OP-07 | Reset isolation | Guard rails implementados; live pendiente |
| OP-08 | Invalid target/production guard | Código/inventory guard; live pendiente |
| OP-09 | Preflight port conflict | Código; live pendiente |
| OP-10 | Spare continuity | Unit test; live pendiente |
| OP-11 | Audit no-secrets | Unit test |
| OP-12 | Student CLI scope | Código definido; container live pendiente |
| OP-13 | Repetibilidad | Diseño/código; live pendiente |
| OP-14 | 4 teams | Pendiente en Tulum |
| OP-15 | 6 teams + spare | Pendiente en Tulum |

---

## 20. CI actual

GitHub Actions ejecuta:

```text
python -m unittest discover -s tests/operation -v
```

Cubre:

```text
inventory
scenario manager
recovery
reset confirmation
preflight helpers
monitor
spare
audit
deployment manager
```

CI no reemplaza las pruebas reales contra Docker/Tulum.

---

## 21. Qué significa “Fase 5 completada”

Sí está completo:

```text
contrato operativo
CLIs
state model
scenario manager
recovery
reset
preflight
status
resources
logs
spare
audit
deploy orchestration
smoke orchestration
guard rails
unit tests
documentación D04
```

No está aún validado:

```text
Compose real
gateway real
app images
DB bootstrap real
LAN access real
4-team load test
6-team + spare load test
```

Eso requiere continuar con la implementación de Fase 4/infraestructura y luego ejecutar Fase 9.

---

## 22. Decisiones finales

### DD5-01
`deploy` nunca resetea un team existente.

### DD5-02
`deploy all` usa `enabled_by_default`.

### DD5-03
Gateway es shared y se conecta solo a APP networks validadas.

### DD5-04
`smoke` es un comando explícito reutilizable.

### DD5-05
Smoke normal no exige score inicial.

### DD5-06
Bootstrap debe ser idempotente.

### DD5-07
Runtime secrets/env deben existir antes de deploy.

### DD5-08
CI y live validation se distinguen explícitamente.

---

# BLOQUE D — COMPLETADO

# FASE 5 — COMPLETADA A NIVEL DE DISEÑO Y CONTROL PLANE
