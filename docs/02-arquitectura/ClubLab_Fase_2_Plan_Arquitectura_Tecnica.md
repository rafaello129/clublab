# ClubLab — Plan de Fase 2
## Arquitectura técnica de ClubLab

**Proyecto:** ClubLab v1  
**Fase:** 2  
**Nombre:** Arquitectura técnica e infraestructura base  
**Estado:** PLAN DE TRABAJO  
**Entradas principales:**  
- `D00_Estado_Base_Servidor_ClubLab.md`
- `D01_Diseno_Experiencia_ClubLab_01.md`

**Entregable principal:**  
`D02_Arquitectura_Tecnica_ClubLab.md`

---

# 1. Propósito de la Fase 2

La Fase 2 transforma la experiencia pedagógica ya definida en una arquitectura técnica concreta.

La pregunta principal deja de ser:

> **¿Qué queremos que descubran los alumnos?**

y pasa a ser:

> **¿Cómo construimos esa experiencia de forma segura, aislada, repetible y fácil de operar?**

En esta fase se decidirá:

```text
qué servicios existen;
cómo se conectan;
cómo se aísla cada equipo;
cómo acceden los alumnos;
qué recursos consume cada entorno;
cómo se observan los servicios;
cómo se preparará la futura inyección de fallos.
```

No se desarrollará todavía toda la aplicación ni el Scenario Manager final.

---

# 2. Condiciones heredadas de Fase 0 y Fase 1

La arquitectura debe respetar obligatoriamente:

```text
no tocar postgres-main;
no usar redes Docker existentes;
no usar volúmenes existentes;
no usar Docker socket del host;
no dar sudo;
no dar acceso SSH al usuario tulum;
no exponer PostgreSQL al host o Internet;
no reutilizar puertos productivos;
no conectar ClubLab con Pelican, WhatsApp o producción;
cada equipo debe poder romperse sin afectar a otro;
cada equipo debe poder resetearse;
el laboratorio debe funcionar con 2–6 equipos;
el incidente debe poder aislarse por equipo;
el alumno debe tener acceso a frontend, API, DB y toolbox;
```

Además, debe conservarse el comportamiento pedagógico:

```text
/api/health      → puede seguir en 200
/api/ranking     → puede fallar de forma controlada
DB               → puede seguir viva
logs             → accesibles y filtrados
```

---

# 3. Arquitectura conceptual objetivo

La arquitectura base propuesta para cada equipo será:

```text
                       CLUBLAB
                          │
                   Gateway / acceso
                          │
          ┌───────────────┼───────────────┐
          │               │               │
       Team 01         Team 02         Team XX
          │               │               │
     ┌────┼────┐      ┌───┼────┐      ┌───┼────┐
     │    │    │      │   │    │      │   │    │
  Front  API  DB   Front API   DB   Front API   DB
     │    │    │      │   │    │      │   │    │
     └────┴─Toolbox    └───┴─Toolbox    └───┴─Toolbox
```

Cada equipo tendrá su propio dominio técnico.

---

# 4. Componentes mínimos por equipo

## Frontend

Responsabilidades:

```text
servir la aplicación;
mostrar estados normales/error;
consumir API del equipo;
ser accesible desde navegador.
```

## API

Responsabilidades:

```text
exponer endpoints;
procesar lógica;
consultar DB;
generar logs;
exponer healthcheck;
permitir fallo parcial controlado.
```

## PostgreSQL

Responsabilidades:

```text
persistencia aislada por equipo;
datos iniciales reproducibles;
credenciales exclusivas;
reset sencillo.
```

## Toolbox

Responsabilidades:

```text
curl;
psql;
ping/getent/ss según necesidad;
herramientas de diagnóstico;
acceso limitado al entorno del equipo.
```

No tendrá acceso al host real.

---

# 5. Decisión preliminar de aislamiento

La opción preferida para la primera versión será:

> **Un stack independiente por equipo.**

Ejemplo:

```text
clublab-team01-frontend
clublab-team01-api
clublab-team01-db
clublab-team01-toolbox
```

Ventajas:

```text
aislamiento;
reset simple;
fallos independientes;
datos independientes;
logs claros;
fácil relación mental equipo ↔ entorno;
```

Desventaja principal:

```text
mayor consumo de RAM.
```

Aun así, con el presupuesto preliminar de Fase 0, sigue siendo razonable para 4–6 equipos ligeros.

---

# 6. Red por equipo

Cada equipo deberá tener una red propia.

Ejemplo:

```text
clublab-team01
clublab-team02
clublab-team03
```

Dentro de una red:

```text
frontend
api
database
toolbox
```

podrán comunicarse únicamente según necesidad.

No habrá conexión con:

```text
database-net
whatsapp_app-net
pelican_nw
```

---

# 7. Subredes

No utilizar:

```text
172.17.0.0/16
172.18.0.0/16
172.19.0.0/16
172.20.0.0/16
10.10.100.0/22
```

Durante Fase 2 se seleccionará un rango explícito para ClubLab.

Ejemplo conceptual:

```text
172.30.0.0/16
```

dividido por equipo.

La elección final debe comprobar que no exista conflicto con:

```text
Docker default-address-pools;
VPN;
LAN;
otras redes futuras.
```

---

# 8. Gateway y acceso

La arquitectura deberá evitar publicar un puerto distinto para cada componente de cada equipo.

Se evaluará preferentemente un acceso del tipo:

```text
http(s)://clublab/.../team01
```

o:

```text
team01.clublab.local
team02.clublab.local
```

El gateway deberá enrutar:

```text
frontend
API
terminal/toolbox si aplica
```

sin exponer PostgreSQL.

---

# 9. Acceso recomendado para la primera versión

Orden de preferencia:

```text
1. LAN local
2. Tailscale
3. combinación LAN + Tailscale
```

Cloudflare Quick Tunnel no será requisito para ClubLab #01.

La primera sesión debe poder ejecutarse aunque Internet público falle.

---

# 10. Exposición de puertos

Regla:

```text
publicar el mínimo posible.
```

Idealmente:

```text
gateway único
+
sin puertos directos por DB
+
sin Docker API
```

PostgreSQL solo será visible dentro de la red del equipo.

El toolbox llegará a DB desde dentro de esa red.

---

# 11. Persistencia

Cada DB tendrá un volumen propio:

```text
clublab-team01-db-data
clublab-team02-db-data
...
```

Los datos deberán poder volver al estado inicial mediante:

```text
seed
o
restore
```

No se dependerá de backups manuales durante la clase.

La filosofía será:

```text
reproducible
>
permanente
```

---

# 12. Datos iniciales

Cada equipo deberá tener datos identificables.

Ejemplo:

```text
Team 01
score 120

Team 02
score 180

Team 03
score 240
```

Los seeds deberán generar:

```text
usuarios;
equipos;
ranking;
misiones;
actividad;
datos suficientes para M0–M4.
```

---

# 13. Healthchecks

Se deberán diseñar al menos:

```text
frontend reachability
API health
DB health
```

Pero deben distinguirse:

```text
health técnico
vs
health pedagógico
```

El alumno no debe recibir una respuesta automática como:

```text
“DB_HOST está mal”
```

El healthcheck debe indicar estado, no resolver el incidente.

---

# 14. Logs

Los logs del alumno deberán ser:

```text
del equipo;
filtrados;
legibles;
sin secretos;
sin variables completas;
sin acceso a otros servicios.
```

La interfaz futura deberá permitir algo como:

```bash
clublab logs api
```

sin ejecutar:

```bash
docker logs
```

directamente.

---

# 15. Preparación para el Scenario Manager

Aunque el Scenario Manager se implementa en Fase 5, la arquitectura debe dejar preparado:

```text
nombres predecibles;
labels;
redes aisladas;
servicios independientes;
configuración sustituible;
healthchecks;
reset por equipo.
```

Labels recomendadas:

```text
project=clublab
team=team01
role=api
managed-by=clublab
```

---

# 16. Convención de nombres

Contenedores:

```text
clublab-team01-frontend
clublab-team01-api
clublab-team01-db
clublab-team01-toolbox
```

Red:

```text
clublab-team01
```

Volumen:

```text
clublab-team01-db-data
```

Proyecto Compose:

```text
clublab-team01
```

Esto permitirá operar únicamente sobre recursos ClubLab.

---

# 17. Límites de recursos

Presupuesto preliminar por equipo:

| Componente | RAM objetivo |
|---|---:|
| Frontend | 64–128 MiB |
| API | 256–512 MiB |
| PostgreSQL | 384–512 MiB |
| Toolbox | 128–256 MiB |
| Margen | 128–256 MiB |
| **Total** | **~1–1.6 GiB** |

Presupuesto del piloto:

```text
4 equipos → ~4–6.5 GiB
6 equipos → ~6–10 GiB
```

Los límites exactos se validarán en ensayo.

---

# 18. CPU

ClubLab debe usar límites razonables.

Ejemplo conceptual:

```text
frontend  0.25 CPU
api       0.50 CPU
db        0.50 CPU
toolbox   0.25 CPU
```

No se cerrarán los valores definitivos hasta medir la aplicación real.

---

# 19. Arquitectura de acceso del alumno

El alumno debe tener únicamente:

```text
navegador
+
terminal/toolbox
```

Desde ahí podrá realizar:

```text
curl
psql
health
logs
diagnóstico
```

No necesitará:

```text
SSH al host
Docker CLI del host
sudo
```

---

# 20. Terminal del laboratorio

Se deberá elegir una de estas opciones:

```text
A. terminal web dentro del toolbox
B. terminal SSH aislada a un contenedor/VM
C. CLI local conectada al entorno
```

Preferencia para la primera versión:

> **Terminal web o sesión aislada directamente al toolbox.**

Reduce instalaciones y evita cuentas del host.

---

# 21. Separación pedagógica y de infraestructura

El alumno verá:

```text
frontend
api
database
toolbox
```

Pero la infraestructura puede tener además:

```text
gateway
control plane
scenario manager
health service
```

Estos componentes no tienen por qué ser visibles en ClubLab #01.

---

# 22. Fallo parcial del ranking

La arquitectura debe permitir un escenario donde:

```text
frontend = healthy
api = healthy
database = healthy
/api/ranking = 500
```

sin romper:

```text
/api/health
/api/me
/api/missions
```

Por tanto, el fallo no puede depender obligatoriamente de una única conexión global a DB si eso tumba toda la API.

Fase 2 debe dejar una arquitectura compatible con:

```text
fault injection scoped;
configuración de dependencia específica;
proxy interno;
adapter/repository específico;
```

La implementación exacta quedará para Fase 5.

---

# 23. Estrategia recomendada para la capa de datos

La API debería separar al menos conceptualmente:

```text
RankingRepository
MissionRepository
UserRepository
```

o equivalente.

Esto permitirá que el escenario de ranking pueda afectar:

```text
RankingRepository
```

sin destruir todo el backend.

No obliga todavía a una arquitectura compleja.

---

# 24. Estructura de repositorio objetivo

```text
clublab/
├── app/
│   ├── frontend/
│   └── backend/
│
├── database/
│   ├── migrations/
│   └── seeds/
│
├── infrastructure/
│   ├── compose/
│   ├── gateway/
│   ├── toolbox/
│   └── templates/
│
├── scenarios/
│   ├── normal/
│   ├── ranking-db-failure/
│   └── api-down/
│
├── scripts/
│   ├── deploy/
│   ├── reset/
│   ├── status/
│   └── scenario/
│
└── docs/
```

En Fase 2 solo se cierra la arquitectura de esta estructura; la implementación completa vendrá después.

---

# 25. Estructura de despliegue por equipo

Modelo:

```text
template
   │
   ├── team01
   ├── team02
   ├── team03
   └── teamXX
```

La configuración por equipo debe variar únicamente en:

```text
Team ID
credenciales
subred
hostname/ruta
seeds
labels
límites
```

No mantener seis Compose completamente distintos a mano.

---

# 26. Estrategia de configuración

Se preferirá:

```text
template
+
variables por equipo
```

Ejemplo conceptual:

```text
TEAM_ID=team01
TEAM_NAME=Equipo 01
NETWORK_SUBNET=...
DB_NAME=...
DB_USER=...
```

Las credenciales se generan exclusivamente para ClubLab.

---

# 27. Seguridad mínima que debe soportar la arquitectura

Aunque la implementación detallada será Fase 3, Fase 2 debe hacer posible:

```text
network isolation;
DB isolation;
no host mounts peligrosos;
read-only filesystem donde aplique;
capabilities mínimas;
sin privileged;
sin Docker socket;
sin host network;
límites CPU/RAM/PIDs.
```

---

# 28. Backups

Para los entornos de alumnos:

```text
seed/reset
```

será la principal estrategia de recuperación.

No se necesita backup individual por equipo durante una sesión.

Sí puede existir backup de:

```text
configuración base;
seeds;
migrations;
escenarios.
```

todo versionado en Git.

---

# 29. Operación del instructor

El instructor necesitará una capa de administración separada.

Conceptualmente:

```text
clublab status all
clublab status team01
clublab reset team01
clublab scenario load team01 ranking-db-failure
clublab scenario clear team01
```

Estos comandos no estarán disponibles para estudiantes salvo versiones limitadas.

---

# 30. Observabilidad del instructor

Debe poder ver rápidamente:

```text
qué equipos están activos;
qué servicio está unhealthy;
qué escenario está cargado;
cuánta RAM consume cada equipo;
si un equipo necesita reset.
```

La forma concreta puede ser:

```text
CLI
dashboard
ambos
```

No es necesario construir dashboard en Fase 2.

---

# 31. Disponibilidad de entorno de reserva

La arquitectura debe contemplar:

```text
clublab-spare
```

o equivalente.

Debe poder sustituir rápidamente a un equipo roto.

Puede estar:

```text
precreado y detenido
o
desplegable en segundos.
```

---

# 32. Bloques de trabajo de la Fase 2

Para evitar demasiadas subfases, la Fase 2 se divide solo en **cuatro bloques**.

---

# BLOQUE A — Arquitectura base y decisiones principales

Cerrar:

```text
stack por equipo;
frontend/api/db/toolbox;
PostgreSQL por equipo;
convenciones de nombres;
estructura de repositorio;
estrategia de templates;
presupuesto de recursos.
```

Resultado:

```text
arquitectura lógica aprobada.
```

---

# BLOQUE B — Redes, acceso y aislamiento

Cerrar:

```text
subredes;
red por equipo;
gateway;
LAN/Tailscale;
terminal del alumno;
puertos;
DNS/hostnames;
qué se expone;
qué queda interno.
```

Resultado:

```text
arquitectura de conectividad aprobada.
```

---

# BLOQUE C — Observabilidad, fallos y operación

Cerrar:

```text
healthchecks;
logs;
fault injection;
compatibilidad con incidente M7;
reset;
entorno reserva;
operación del instructor;
requisitos del Scenario Manager.
```

Resultado:

```text
arquitectura operativa aprobada.
```

---

# BLOQUE D — Validación y D02 final

Realizar:

```text
revisión contra D00;
revisión contra D01;
estimación de recursos;
mapa de puertos;
mapa de redes;
mapa de servicios;
riesgos;
decisiones finales;
diagrama definitivo.
```

Resultado:

```text
D02_Arquitectura_Tecnica_ClubLab.md
```

---

# 33. Entregable D02

El documento final deberá incluir:

```text
1. Objetivo
2. Restricciones heredadas
3. Arquitectura general
4. Arquitectura por equipo
5. Redes
6. Acceso
7. Gateway
8. PostgreSQL
9. Toolbox
10. Persistencia
11. Healthchecks
12. Logs
13. Preparación para escenarios
14. Límites de recursos
15. Nombres y labels
16. Operación del instructor
17. Entorno de reserva
18. Seguridad estructural
19. Diagramas
20. Riesgos
21. Decisiones cerradas
22. Requisitos para Fases 3–5
```

---

# 34. Diagramas obligatorios

D02 deberá contener al menos:
## Diagrama 1 — Vista global

```text
Alumno
  ↓
Gateway
  ↓
Team XX
```

## Diagrama 2 — Stack por equipo

```text
Frontend
   ↓
API
   ↓
DB

Toolbox
 ↘ API / DB
```

## Diagrama 3 — Redes

```text
team01 network
team02 network
team03 network
```

sin conexión lateral.

## Diagrama 4 — Operación

```text
Instructor
  ↓
Control plane / scripts
  ↓
status / scenario / reset
```

---

# 35. Riesgos a resolver en Fase 2

## R1 — Demasiados contenedores

Mitigación:

```text
imágenes ligeras;
límites;
toolbox simple;
frontend servido estáticamente.
```

## R2 — Colisiones de red

Mitigación:

```text
IPAM explícito.
```

## R3 — Puertos difíciles de administrar

Mitigación:

```text
gateway único.
```

## R4 — Acceso complejo para alumnos

Mitigación:

```text
terminal web / toolbox;
URLs simples.
```

## R5 — Incidente demasiado acoplado a la API

Mitigación:

```text
fault injection scoped.
```

## R6 — Reset lento

Mitigación:

```text
seeds;
volúmenes pequeños;
template reproducible.
```

---

# 36. Decisiones que deben salir cerradas de Fase 2

Al terminar esta fase debe existir respuesta concreta para:

```text
¿cuántos contenedores tiene cada equipo?
¿qué red usa?
¿qué subred usa?
¿qué puertos se publican?
¿cómo entra el alumno?
¿cómo accede a terminal?
¿cómo llega a PostgreSQL?
¿cómo se limita RAM/CPU?
¿cómo se nombran recursos?
¿cómo se observa el estado?
¿cómo se soporta el fallo del ranking?
¿cómo se resetea un equipo?
¿cómo se crea un equipo nuevo?
```

---

# 37. Qué NO corresponde todavía

No implementar aún completamente:

```text
UI final;
backend completo;
schema definitivo;
Scenario Manager final;
tarjetas del alumno;
manual instructor;
automatización total;
monitorización avanzada.
```

Estas piezas vendrán después.

---

# 38. Criterios de éxito de Fase 2

La fase se considera completa cuando:

```text
[ ] arquitectura por equipo definida;
[ ] redes aisladas definidas;
[ ] acceso del alumno definido;
[ ] gateway definido;
[ ] terminal/toolbox definido;
[ ] PostgreSQL por equipo definido;
[ ] persistencia definida;
[ ] nombres y labels definidos;
[ ] límites de recursos definidos;
[ ] healthchecks definidos;
[ ] estrategia de logs definida;
[ ] soporte para incidente definido;
[ ] reset conceptual definido;
[ ] entorno reserva definido;
[ ] operación del instructor definida;
[ ] diagramas terminados;
[ ] riesgos documentados;
[ ] D02 final consolidado.
```

---

# 39. Flujo de trabajo

```text
BLOQUE A
Arquitectura base
      ↓
BLOQUE B
Redes + acceso
      ↓
BLOQUE C
Observabilidad + escenarios + operación
      ↓
BLOQUE D
Validación + D02
```

Solo cuatro bloques.

---

# 40. Primer bloque a desarrollar

# BLOQUE A — Arquitectura base y decisiones principales

El primer trabajo será cerrar:

```text
stack exacto por equipo;
PostgreSQL por equipo;
toolbox;
cantidad de contenedores;
nombres;
labels;
estructura del repo;
template por equipo;
presupuesto CPU/RAM.
```

Una vez cerrado, podremos diseñar redes y acceso sin rehacer decisiones básicas.