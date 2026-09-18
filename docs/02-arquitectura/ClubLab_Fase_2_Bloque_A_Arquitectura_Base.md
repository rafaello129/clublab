# ClubLab — Fase 2 / Bloque A
## Arquitectura base y decisiones principales

**Proyecto:** ClubLab v1  
**Fase:** 2 — Arquitectura técnica  
**Bloque:** A  
**Estado:** CERRADO PARA DISEÑO v1  
**Dependencias:** `D00_Estado_Base_Servidor_ClubLab.md` + `D01_Diseno_Experiencia_ClubLab_01.md`

---

# 1. Propósito

Este bloque cierra la forma base de un entorno ClubLab antes de diseñar redes, acceso y publicación.

Debe responder:

```text
¿Cuántos servicios tiene cada equipo?
¿Qué tecnología usa cada servicio?
¿Cómo se aíslan los datos?
¿Cómo se nombran los recursos?
¿Cómo se despliega un equipo nuevo?
¿Cuánto puede consumir?
¿Cómo se organiza el repositorio?
```

El objetivo es que los bloques posteriores no tengan que rehacer estas decisiones.

---

# 2. Decisión principal

La arquitectura base de ClubLab será:

> **Un stack independiente y desechable por equipo.**

Cada equipo tendrá:

```text
1 frontend
1 API
1 PostgreSQL
1 toolbox
```

Total:

```text
4 contenedores por equipo
```

Para la escala pedagógica prevista:

```text
4 equipos → 16 contenedores ClubLab
6 equipos → 24 contenedores ClubLab
```

El gateway y componentes de control serán compartidos y se diseñarán en los bloques siguientes.

---

# 3. Arquitectura lógica por equipo

```text
┌───────────────────────────────────────────┐
│               TEAM 01                    │
│                                           │
│  ┌──────────┐        ┌──────────────┐     │
│  │ Frontend │ ─────▶ │     API      │     │
│  └──────────┘        └──────┬───────┘     │
│                             │             │
│                             ▼             │
│                      ┌──────────────┐     │
│                      │ PostgreSQL   │     │
│                      └──────────────┘     │
│                             ▲             │
│                             │             │
│                      ┌──────────────┐     │
│                      │   Toolbox    │     │
│                      └──────────────┘     │
└───────────────────────────────────────────┘
```

El toolbox podrá comunicarse con API y DB del mismo equipo.

No tendrá acceso al host real.

---

# 4. Servicio 1 — Frontend

## Tecnología

```text
React
TypeScript
Vite
```

## Runtime

La aplicación compilada se servirá como archivos estáticos.

Imagen de runtime propuesta:

```text
nginx:alpine
```

o equivalente ligero.

## Motivo

No tiene sentido mantener Node en ejecución únicamente para servir un frontend estático.

Beneficios:

```text
menos RAM;
menos CPU;
arranque rápido;
imagen simple;
menos superficie operativa.
```

## Responsabilidades

```text
servir UI;
consumir API del equipo;
mostrar estados de carga;
mostrar error controlado del ranking;
permitir DevTools/Network.
```

---

# 5. Servicio 2 — API

## Tecnología

```text
NestJS
TypeScript
Node.js 22 LTS
```

La versión concreta de NestJS se fijará cuando se cree el proyecto.

## Runtime propuesto

```text
node:22-bookworm-slim
```

con build multi-stage.

La imagen final deberá contener únicamente:

```text
código compilado;
dependencias de producción;
configuración necesaria.
```

## Responsabilidades

```text
/api/health
/api/ranking
/api/me
/api/missions
lógica de negocio;
acceso a datos;
logs;
soporte futuro de escenarios.
```

---

# 6. Diseño interno mínimo de API

Para soportar el incidente pedagógico se evitará acoplar toda la aplicación a una única pieza inseparable.

Separación conceptual:

```text
UserController
MissionController
RankingController
        │
        ▼
UserService
MissionService
RankingService
        │
        ▼
UserRepository
MissionRepository
RankingRepository
```

No es obligatorio crear una arquitectura excesivamente compleja.

La finalidad es permitir en Fase 5:

```text
fallo de RankingRepository
```

sin derribar:

```text
/api/health
/api/me
/api/missions
```

---

# 7. Servicio 3 — PostgreSQL

## Decisión

Cada equipo tendrá:

> **su propio contenedor PostgreSQL.**

No se utilizará:

```text
postgres-main
una DB compartida entre todos los equipos
un schema compartido en producción
```

## Imagen propuesta

```text
postgres:18-bookworm
```

Razones:

```text
misma familia ya utilizada en el servidor;
comportamiento predecible;
psql compatible;
aislamiento fuerte;
reset sencillo.
```

## Resultado

```text
team01 → DB propia
team02 → DB propia
team03 → DB propia
...
```

---

# 8. Por qué no usar una sola PostgreSQL compartida

Una instancia compartida consumiría menos recursos, pero complicaría:

```text
aislamiento;
permisos;
reset;
fault injection;
errores de alumnos;
restauración;
explicación pedagógica.
```

Para ClubLab #01 priorizamos:

```text
simplicidad operativa
+
aislamiento
+
reproducibilidad
```

sobre ahorrar algunos cientos de MiB.

---

# 9. Servicio 4 — Toolbox

El toolbox será la terminal controlada del equipo.

## Base propuesta

Imagen propia:

```text
clublab/toolbox:1
```

construida a partir de una imagen Debian/PostgreSQL compatible.

## Herramientas mínimas

```text
curl
psql
jq
ping
getent
dig
ss
ip
nc
bash
```

Se podrán retirar herramientas que finalmente no tengan valor pedagógico.

## No incluir

```text
docker CLI del host;
sudo;
systemctl del host;
herramientas ofensivas;
credenciales productivas.
```

---

# 10. Ciclo de vida del toolbox

El toolbox podrá permanecer activo durante la sesión para ofrecer una experiencia consistente.

No guardará información importante.

Características:

```text
sin volumen persistente;
desechable;
recreable;
credenciales ClubLab inyectadas;
solo red de su equipo.
```

---

# 11. Persistencia por equipo

Cada PostgreSQL tendrá un volumen propio.

Convención:

```text
clublab-team01-db-data
clublab-team02-db-data
...
```

La persistencia servirá durante la sesión para que:

```text
UPDATE
→ sobreviva a recarga de UI/API
```

pero el entorno completo seguirá siendo desechable.

---

# 12. Estrategia de reset

La unidad de recuperación será:

```text
EL EQUIPO
```

No el host.

Conceptualmente:

```text
reset team01
```

debe poder devolver:

```text
frontend;
API;
DB;
toolbox;
datos;
configuración;
```

a un estado conocido.

La implementación exacta pertenece a Fase 5.

---

# 13. Seeds

Cada DB se construirá a partir de:

```text
migrations
+
seed inicial
```

Los seeds deben ser deterministas.

Ejemplo conceptual:

```text
team01
score inicial: 120

team02
score inicial: 180

team03
score inicial: 240
```

Cada entorno debe ser reconocible sin depender de datos generados aleatoriamente.

---

# 14. Identidad del equipo

Toda configuración utilizará una clave estable:

```text
TEAM_ID
```

Formato:

```text
team01
team02
team03
...
```

Además:

```text
TEAM_NUMBER=01
TEAM_NAME="Equipo 01"
```

`TEAM_ID` será la identidad técnica principal.

---

# 15. Convención de nombres

## Compose project

```text
clublab-team01
```

## Contenedores

```text
clublab-team01-frontend
clublab-team01-api
clublab-team01-db
clublab-team01-toolbox
```

## Red

```text
clublab-team01
```

## Volumen

```text
clublab-team01-db-data
```

## Credencial lógica

```text
clublab_team01
```

## Base

```text
clublab_team01
```

Todo recurso destruible deberá comenzar con:

```text
clublab-
```

o portar labels ClubLab inequívocas.

---

# 16. Labels obligatorias

Cada recurso gestionado por ClubLab deberá incluir, donde Docker lo permita:

```text
com.clublab.project=clublab
com.clublab.team=team01
com.clublab.role=frontend|api|database|toolbox
com.clublab.managed-by=clublab
com.clublab.disposable=true
```

Para recursos compartidos:

```text
com.clublab.scope=shared
```

Objetivo:

> Ningún script futuro debe operar basándose únicamente en “todos los contenedores Docker”.

---

# 17. Regla de selección de recursos

Los scripts de ClubLab únicamente podrán operar recursos que cumplan simultáneamente:

```text
prefijo esperado
+
labels esperadas
```

Ejemplo conceptual:

```text
name starts clublab-team01-
AND
com.clublab.project=clublab
AND
com.clublab.team=team01
```

Esto reduce el riesgo de tocar Pelican, WhatsApp o PostgreSQL productivo.

---

# 18. Template de despliegue

No se mantendrá un Compose manual diferente para cada equipo.

Se utilizará:

```text
1 template de Compose
+
1 archivo de configuración por equipo
```

Modelo:

```text
compose.team.yml
        +
teams/team01.env
        +
teams/team02.env
        +
...
```

Los `.env` reales con secretos no se versionarán.

---

# 19. Configuración por equipo

Variables previstas:

```text
TEAM_ID
TEAM_NUMBER
TEAM_NAME

DB_NAME
DB_USER
DB_PASSWORD

APP_ENV

NETWORK_SUBNET      # se definirá en Bloque B
ACCESS_HOSTNAME     # se definirá en Bloque B
```

Podrán añadirse:

```text
resource limits;
scenario settings;
seed profile.
```

---

# 20. Gestión de secretos

Nunca almacenar en Git:

```text
DB_PASSWORD real;
tokens;
cookies;
secrets de aplicación.
```

El repositorio incluirá:

```text
.env.example
```

y los archivos reales se generarán durante despliegue.

Las credenciales serán:

```text
exclusivas de ClubLab;
distintas de producción;
desechables.
```

---

# 21. Estructura definitiva del repositorio

```text
clublab/
│
├── app/
│   ├── frontend/
│   └── backend/
│
├── database/
│   ├── migrations/
│   ├── seeds/
│   └── init/
│
├── infrastructure/
│   ├── compose/
│   │   └── compose.team.yml
│   ├── gateway/
│   ├── toolbox/
│   │   └── Dockerfile
│   ├── templates/
│   └── teams/
│       └── .gitkeep
│
├── scenarios/
│   ├── normal/
│   ├── ranking-db-failure/
│   └── api-down/
│
├── scripts/
│   ├── deploy/
│   ├── status/
│   ├── reset/
│   └── scenario/
│
├── docs/
│   ├── architecture/
│   ├── instructor/
│   └── students/
│
├── .env.example
├── .gitignore
└── README.md
```

---

# 22. Fuente única de verdad

No duplicar:

```text
schema;
seed;
Compose;
Dockerfile;
configuración;
```

por equipo.

La regla será:

```text
un template
+
parámetros
```

Esto hará que pasar de:

```text
4 equipos
```

a:

```text
6 equipos
```

sea una operación de configuración, no una reescritura.

---

# 23. Imágenes Docker

Imágenes propias previstas:

```text
clublab/frontend:<version>
clublab/api:<version>
clublab/toolbox:<version>
```

PostgreSQL utilizará inicialmente imagen oficial:

```text
postgres:18-bookworm
```

No utilizar:

```text
latest
```

en despliegues de clase.

---

# 24. Versionado

Cada build de la aplicación deberá poder fijarse.

Ejemplo:

```text
clublab/frontend:0.1.0
clublab/api:0.1.0
clublab/toolbox:0.1.0
```

Para ensayo:

```text
0.1.0
```

Para clase:

```text
tag aprobado
```

Evitar depender de imágenes cambiantes el día de la sesión.

---

# 25. Presupuesto inicial de RAM por equipo

Se adoptan límites iniciales conservadores:

| Servicio | Límite RAM inicial |
|---|---:|
| Frontend | 128 MiB |
| API | 512 MiB |
| PostgreSQL | 640 MiB |
| Toolbox | 256 MiB |
| **Total máximo** | **1.5 GiB aprox.** |

Estos son límites iniciales, no mediciones reales.

Deberán validarse en Fase 9.

---

# 26. Presupuesto para varios equipos

Con 1.5 GiB como techo conceptual:

```text
4 equipos
≈ 6 GiB

5 equipos
≈ 7.5 GiB

6 equipos
≈ 9 GiB
```

A esto se añadirán:

```text
gateway;
control plane;
Docker overhead.
```

El host auditado tiene margen suficiente para un piloto, pero los servidores de juegos existentes pueden aumentar su consumo; no se reservará toda la RAM libre actual para ClubLab.

---

# 27. Límites iniciales de CPU

Propuesta:

| Servicio | CPU máximo inicial |
|---|---:|
| Frontend | 0.25 |
| API | 0.75 |
| PostgreSQL | 0.75 |
| Toolbox | 0.25 |
| **Equipo** | **2.0 CPU** |

Estos límites controlan picos; no representan CPU reservada.

Con seis equipos:

```text
máximo teórico configurado = 12 CPU
```

sobre un host con 32 CPUs lógicas.

---

# 28. Límites de procesos

Valores iniciales sugeridos:

```text
frontend → 64 PIDs
api      → 128 PIDs
db       → 128 PIDs
toolbox  → 64 PIDs
```

La necesidad real deberá comprobarse durante implementación.

---

# 29. Política de almacenamiento

Solo PostgreSQL necesita persistencia normal.

Frontend:

```text
sin volumen de datos.
```

API:

```text
sin volumen persistente de aplicación.
```

Toolbox:

```text
sin volumen persistente.
```

DB:

```text
named volume exclusivo.
```

No montar:

```text
/home/tulum/apps/whatsapp
/home/docker-data
/var/www/pelican
/etc
/run/docker.sock
```

---

# 30. Código del alumno

ClubLab #01 no necesita que cada equipo modifique archivos de código.

Por ello:

```text
no habrá bind mount del repositorio
dentro de los contenedores de alumnos.
```

La aplicación se ejecutará desde imágenes ya construidas.

Esto mejora:

```text
reproducibilidad;
seguridad;
reset;
consistencia.
```

---

# 31. Ciclo de construcción

La arquitectura seguirá:

```text
source
  ↓
docker build
  ↓
imagen versionada
  ↓
template Compose
  ↓
teamXX
```

Todos los equipos utilizarán la misma versión de aplicación.

Solo cambiarán:

```text
identidad;
credenciales;
red;
datos iniciales;
estado de escenario.
```

---

# 32. Dependencias de arranque

Conceptualmente:

```text
database
  ↓ healthy
api
  ↓ healthy
frontend

toolbox
```

El frontend puede existir aunque la API falle, lo cual es importante para el incidente.

No debe configurarse un sistema donde:

```text
API unhealthy
→ frontend automáticamente se detiene
```

porque destruiría el fallo parcial.

---

# 33. Healthcheck base requerido

Aunque su diseño detallado será Bloque C, la arquitectura ya exige:
```text
DB healthcheck
API /api/health
frontend reachability
```

Estos checks no deben convertir el fallo del ranking en una caída total.

---

# 34. Compatibilidad con M4

La arquitectura debe permitir:

```text
Toolbox
  ↓
PostgreSQL del mismo team
  ↓
UPDATE controlado
  ↓
API
  ↓
Frontend
```

sin acceso a ninguna DB externa.

---

# 35. Compatibilidad con M7

La arquitectura deberá permitir posteriormente:

```text
Frontend healthy
API process healthy
DB healthy
RankingRepository falla
```

Por eso se congela desde ahora:

> **El estado del contenedor API y el estado funcional del endpoint de ranking son conceptos distintos.**

Esto es clave para la experiencia.

---

# 36. Entorno de reserva

La arquitectura base soportará un equipo adicional lógico:

```text
spare
```

Nombre sugerido:

```text
clublab-spare
```

No tiene que estar siempre encendido.

Debe poder desplegarse usando exactamente el mismo template.

---

# 37. Capacidad objetivo

La arquitectura se diseñará para:

```text
mínimo operativo: 2 equipos
objetivo normal:   4 equipos
máximo inicial:    6 equipos
reserva:           1 entorno adicional temporal
```

No se diseñará todavía para decenas de equipos.

Primero se validará el modelo.

---

# 38. Qué queda compartido

Por equipo:

```text
frontend
api
database
toolbox
red
volumen
configuración
```

Compartido:

```text
imágenes Docker
gateway
control plane
scripts
repositorio
materiales
```

Esto balancea aislamiento y consumo.

---

# 39. Qué NO se comparte entre equipos

No compartir:

```text
PostgreSQL
volumen DB
credenciales DB
network namespace
scenario state
Team ID
datos mutables
```

Así:

```text
team01 rompe algo
≠
team02 se rompe
```

---

# 40. Decisiones cerradas del Bloque A

### DA2-01
Se utilizarán **4 contenedores por equipo**.

### DA2-02
Los servicios serán:

```text
frontend
api
database
toolbox
```

### DA2-03
Frontend será React/TypeScript compilado y servido estáticamente.

### DA2-04
API será NestJS/TypeScript sobre Node 22.

### DA2-05
Cada equipo tendrá PostgreSQL propio.

### DA2-06
Se parte de `postgres:18-bookworm`.

### DA2-07
Toolbox será una imagen ClubLab propia.

### DA2-08
Solo PostgreSQL tendrá persistencia normal.

### DA2-09
Los recursos utilizarán prefijo y labels `clublab`.

### DA2-10
Se utilizará un único template de despliegue parametrizado.

### DA2-11
Las credenciales reales no se versionarán.

### DA2-12
Todos los equipos ejecutarán las mismas imágenes versionadas.

### DA2-13
El presupuesto inicial será ~1.5 GiB RAM y hasta 2 CPU por equipo.

### DA2-14
La capacidad inicial objetivo será 4 equipos, escalable a 6.

### DA2-15
Existirá soporte para un entorno `spare`.

### DA2-16
La API deberá permitir fallos scoped al ranking.

### DA2-17
No habrá bind mounts del código del alumno ni acceso al host.

---

# 41. Decisiones que pasan al Bloque B

El siguiente bloque deberá decidir:

```text
rango IP exacto;
subred por equipo;
gateway;
hostnames;
LAN/Tailscale;
terminal web;
publicación de frontend/API/toolbox;
DNS;
puertos;
reglas de comunicación;
```

No es necesario reabrir la decisión de los cuatro servicios por equipo.

---

# 42. Requisitos que pasan al Bloque C

Después de definir redes deberán cerrarse:

```text
healthchecks finales;
logs filtrados;
control plane;
reset;
fault injection;
status;
operación del instructor;
Scenario Manager compatibility.
```

---

# 43. Criterios de aceptación

```text
[x] cantidad de contenedores definida
[x] frontend definido
[x] API definida
[x] PostgreSQL definido
[x] toolbox definido
[x] aislamiento de datos decidido
[x] persistencia definida
[x] seeds definidos conceptualmente
[x] naming definido
[x] labels definidas
[x] template definido
[x] secretos definidos
[x] estructura de repositorio definida
[x] imágenes/versionado definidos
[x] RAM inicial definida
[x] CPU inicial definida
[x] PIDs iniciales definidos
[x] entorno de reserva contemplado
[x] compatibilidad M4 validada
[x] compatibilidad M7 validada
```

# BLOQUE A — COMPLETADO

---

# 44. Arquitectura base congelada

```text
                         TEAM XX
┌──────────────────────────────────────────────────────┐
│                                                      │
│  clublab-teamXX-frontend                             │
│          │                                           │
│          ▼                                           │
│  clublab-teamXX-api                                  │
│          │                                           │
│          ▼                                           │
│  clublab-teamXX-db ───── named volume                │
│          ▲                                           │
│          │                                           │
│  clublab-teamXX-toolbox                              │
│                                                      │
│  Identity: TEAM_ID=teamXX                            │
│  Managed only through ClubLab resources/labels       │
└──────────────────────────────────────────────────────┘
```

El próximo bloque diseñará cómo esta caja se conecta al alumno sin abrir acceso lateral ni tocar las redes existentes del servidor.