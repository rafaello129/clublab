# ClubLab — Fase 5 / Bloque A
## Modelo operativo, CLIs e inventario de teams

**Estado:** DISEÑO CERRADO v1 + SCAFFOLD IMPLEMENTADO  
**Dependencias:** D02 + D03 + APP04 + Plan de Fase 5

---

## 1. Propósito

Este bloque fija la interfaz operativa antes de implementar escenarios, reset y preflight completos.

Se separan dos planos:

```text
Alumno      → clublab
Instructor  → clublabctl
```

La separación es deliberada: el alumno puede observar y recuperar su propio escenario, pero no administrar Docker ni cambiar el estado global del laboratorio.

---

## 2. Decisiones cerradas

### DA5-01 — Lenguaje

`clublab` y `clublabctl` se implementarán en **Python 3.11+** usando primero la librería estándar.

Motivos:

- argparse y subcomandos claros;
- JSON sin dependencias;
- subprocess con argumentos estructurados;
- tests con unittest;
- fácil mantenimiento en CentOS;
- evita shell interpolation.

### DA5-02 — Inventario

El inventario versionado será:

```text
infrastructure/teams/teams.json
```

Se elige JSON en lugar de YAML para evitar una dependencia runtime de PyYAML en la capa operativa.

El inventario **no contiene secrets**.

### DA5-03 — Targets

Targets permitidos:

```text
team01
team02
team03
team04
team05
team06
spare
```

`all` es una palabra operativa, no un team real.

### DA5-04 — Escenarios

Allowlist inicial:

```text
normal
ranking-db-failure
api-down
```

### DA5-05 — Roles operativos

Roles de contenedor reconocidos:

```text
frontend
api
database
toolbox
gateway
```

---

## 3. CLI del alumno

Ubicación prevista en la imagen toolbox:

```text
/usr/local/bin/clublab
```

Código fuente:

```text
infrastructure/toolbox/bin/clublab
```

Comandos:

```text
clublab whoami
clublab status
clublab health
clublab logs api
clublab recover ranking-db
clublab help
```

No existen:

```text
clublab reset
clublab deploy
clublab scenario
clublab docker
```

---

## 4. `clublab whoami`

Muestra únicamente información lógica del propio entorno:

```text
Team: team01
Name: Equipo 01
API: api:3000
Database: database:5432
Toolbox user: student
```

No muestra tokens, passwords, IDs Docker, paths del host ni otros teams.

---

## 5. `clublab status`

Ejecuta checks directos desde toolbox:

```text
frontend → HTTP
api      → /api/health
database → pg_isready
toolbox  → proceso local
```

Durante `ranking-db-failure` los cuatro componentes deben seguir apareciendo sanos.

---

## 6. `clublab health`

Añade una comprobación funcional:

```text
API health
Ranking endpoint
Database accepting
```

Durante el incidente es correcto observar:

```text
API health       200
Database         OK
Ranking endpoint 500
```

La herramienta no imprime el nombre del escenario activo.

---

## 7. `clublab logs api`

Solo lee:

```text
/var/log/clublab/lab-events.jsonl
```

y renderiza las últimas líneas en formato humano.

No acepta paths arbitrarios.

Límite inicial:

```text
1..100 líneas
default 40
```

---

## 8. `clublab recover ranking-db`

Utiliza el token scoped del propio team desde:

```text
/run/secrets/clublab_recovery_token
```

y llama:

```text
POST http://api:3000/internal/lab/recover/ranking-db
```

No recibe `teamId`.

Es idempotente.

---

## 9. CLI del instructor

Código fuente:

```text
scripts/clublabctl/clublabctl.py
```

Interfaz final reservada:

```text
clublabctl preflight [target]
clublabctl deploy <target>
clublabctl status [target]
clublabctl resources [target]
clublabctl logs <target> <role>

clublabctl scenario load <target> <scenario>
clublabctl scenario clear <target>
clublabctl scenario status <target>

clublabctl recover <target>
clublabctl reset <target>

clublabctl spare status
clublabctl spare assign <team>

clublabctl audit tail
```

Además Block A implementa:

```text
clublabctl inventory list
clublabctl inventory show <target>
clublabctl inventory validate
```

---

## 10. Estado del scaffold

En este bloque se implementan de forma funcional:

```text
inventory list
inventory show
inventory validate
version
```

Los comandos de operación quedan registrados en el parser, pero devolverán `NOT_IMPLEMENTED` hasta los Bloques B y C.

Esto evita implementar reset/scenario antes de cerrar sus contratos.

---

## 11. Inventario

Cada team contiene:

```text
display_name
access_port
app_subnet
data_subnet
compose_project
enabled_by_default
```

Mapa congelado:

| Target | Puerto | APP | DATA | Default |
|---|---:|---|---|---|
| team01 | 8211 | 10.77.1.0/24 | 10.77.101.0/24 | sí |
| team02 | 8212 | 10.77.2.0/24 | 10.77.102.0/24 | sí |
| team03 | 8213 | 10.77.3.0/24 | 10.77.103.0/24 | sí |
| team04 | 8214 | 10.77.4.0/24 | 10.77.104.0/24 | sí |
| team05 | 8215 | 10.77.5.0/24 | 10.77.105.0/24 | no |
| team06 | 8216 | 10.77.6.0/24 | 10.77.106.0/24 | no |
| spare | 8219 | 10.77.9.0/24 | 10.77.109.0/24 | sí |

Gateway ingress:

```text
10.77.250.0/24
```

---

## 12. Validación del inventario

`clublabctl inventory validate` debe detectar:

- target inválido;
- puerto duplicado;
- puerto privilegiado;
- subnet inválida;
- subnet duplicada;
- overlap entre APP/DATA;
- overlap con ingress;
- compose project duplicado;
- falta de campos requeridos.

El comando es fail-closed.

---

## 13. Exit codes

Se congelan:

```text
0   OK
2   USAGE
3   CONFIG
4   CHECK_FAILED
5   OPERATION_FAILED
6   STATE_CONFLICT
7   PARTIAL_SUCCESS
8   DEPENDENCY_UNAVAILABLE
9   SECURITY_GUARD
10  NOT_IMPLEMENTED
```

`argparse` puede producir 2 automáticamente para sintaxis inválida.

---

## 14. Formato de salida

Para uso humano se prioriza texto estable y corto.

Más adelante los comandos administrativos podrán incorporar:

```text
--json
```

cuando sea útil para tests/automatización.

Block A no obliga a JSON para el CLI del alumno.

---

## 15. Estructura del repo

```text
infrastructure/
└── teams/
    ├── README.md
    └── teams.json

infrastructure/
└── toolbox/
    └── bin/
        └── clublab

scripts/
└── clublabctl/
    ├── README.md
    └── clublabctl.py

tests/
└── operation/
    └── test_inventory.py
```

---

## 16. Guard rails de implementación

Toda futura llamada externa de `clublabctl` debe:

- usar arrays de argumentos;
- no usar `shell=True`;
- validar target antes de tocar Docker;
- comprobar labels antes de operaciones destructivas;
- aplicar timeout;
- capturar exit code y stderr;
- no imprimir secrets.

---

## 17. Datos runtime vs versionados

Versionado:

```text
teams.json
CLI source
scenario definitions
templates
tests
```

Runtime:

```text
generated env
secrets
audit
expected state
generation id
spare assignment
```

Runtime no entra a Git.

---

## 18. Criterios de aceptación

```text
[x] separación student/instructor cerrada
[x] lenguaje de implementación cerrado
[x] inventario definido
[x] targets definidos
[x] scenarios allowlist definidos
[x] roles definidos
[x] comandos student definidos
[x] comandos instructor definidos
[x] exit codes definidos
[x] inventory validation definida
[x] scaffold de clublab creado
[x] scaffold de clublabctl creado
[x] test de inventario creado
```

# BLOQUE A — COMPLETADO

El siguiente bloque implementará el comportamiento real de `scenario`, `recover` instructor-side y `reset`.
