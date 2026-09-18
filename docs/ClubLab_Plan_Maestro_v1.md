# ClubLab — Plan Maestro v1

**Proyecto:** Laboratorio práctico para Club de Programación  
**Experiencia inicial:** *ClubLab #01 — Desarmando una aplicación*  
**Duración objetivo de la primera sesión:** 2 horas  
**Servidor base:** Tulum — Dell PowerEdge R440 / CentOS Stream 10  
**Documento base consultado:** `01_Manual_Administracion_Servidor_Tulum (1).docx.pdf`  
**Estado del servidor documentado en el manual:** 29 de agosto de 2026

---

## 1. Propósito del proyecto

ClubLab no será únicamente una aplicación para una clase. Será una **plataforma educativa reutilizable** para que los integrantes del club puedan experimentar con sistemas reales sin convertir las sesiones en cursos tradicionales de sintaxis.

La filosofía del club será:

> **Primero experimentar, después explicar.**

El objetivo no es enseñar React, NestJS, PostgreSQL, Docker o Linux como cursos independientes, sino permitir que los integrantes descubran cómo se relacionan las distintas áreas del desarrollo de software mediante experiencias prácticas.

ClubLab debe permitir trabajar progresivamente temas como:

- frontend;
- backend;
- APIs;
- bases de datos;
- arquitectura de software;
- redes;
- servidores;
- Linux;
- Docker;
- DevOps;
- debugging;
- ciberseguridad;
- autenticación;
- WebSockets;
- observabilidad.

La primera experiencia será:

# ClubLab #01 — Desarmando una aplicación

Pregunta central:

> **¿Qué hay detrás de una aplicación real?**

---

# 2. Objetivo de la primera clase

Al terminar la sesión, los integrantes deben poder construir mentalmente un flujo parecido a:

```text
Usuario
   │
   ▼
Navegador
   │
   ▼
Frontend
   │ HTTP
   ▼
Backend / API
   │
   ▼
Base de datos

Todo ello ejecutándose sobre:

Servidor → Linux → Docker → Red
```

No es necesario que sepan programar cada pieza.

Sí deben haber:

- utilizado la aplicación;
- inspeccionado peticiones;
- interactuado con una API;
- observado datos reales;
- modificado información;
- identificado servicios;
- investigado un fallo;
- reparado un escenario controlado;
- entendido que una aplicación es un sistema de componentes.

---

# 3. Principios de diseño

## 3.1 La experiencia es el producto

La aplicación existe para soportar la experiencia educativa.

No se debe construir funcionalidad que no aporte valor al laboratorio.

---

## 3.2 Experimentar antes de explicar

Patrón recomendado:

```text
OBSERVAR
   ↓
PREGUNTAR
   ↓
EXPERIMENTAR
   ↓
DESCUBRIR
   ↓
EXPLICAR
```

Evitar:

```text
TEORÍA
   ↓
DEFINICIÓN
   ↓
EJEMPLO
   ↓
EJERCICIO
```

---

## 3.3 Código como herramienta, no como tema central

Puede existir código prehecho.

Los alumnos pueden modificar valores o pequeñas piezas como:

```ts
const POINTS_PER_MISSION = 10;
```

pero la sesión no gira alrededor de aprender sintaxis.

---

## 3.4 Sistemas reales, riesgo controlado

Los integrantes deben poder:

- consultar;
- modificar;
- detener;
- probar;
- romper;
- investigar;
- restaurar.

Pero únicamente dentro de un entorno aislado.

---

# 4. Estado base del servidor Tulum

Según el manual técnico de agosto de 2026, Tulum dispone de:

- Dell PowerEdge R440;
- CentOS Stream 10;
- arquitectura x86-64;
- 2 × Intel Xeon Silver 4208;
- 32 CPU lógicos;
- 77 GiB de RAM;
- aproximadamente 1.3 TB en `/home`;
- Docker Engine;
- PostgreSQL central;
- Tailscale;
- Cloudflare Quick Tunnel;
- SSH;
- firewalld;
- Cockpit;
- scripts de respaldo y monitorización.

La arquitectura documentada mantiene frontend y backend sobre loopback y PostgreSQL dentro de Docker.

Ejemplo del estado documentado:

```text
Tailscale / Cloudflare
          │
          ▼
      Servidor Tulum
          │
      Docker Engine
       /    |    \
Frontend Backend PostgreSQL
```

Servicios documentados:

```text
Frontend     127.0.0.1:8080
Backend      127.0.0.1:3500
PostgreSQL   Docker interno
```

PostgreSQL no publica `5432` hacia el host.

---

# 5. Regla fundamental de infraestructura

ClubLab debe quedar **completamente separado** de los servicios reales existentes.

No utilizar directamente:

```text
whatsapp-backend
whatsapp-frontend
postgres-main
whatsapp_db
whatsapp_user
whatsapp_app-net
postgres_postgres_data
/home/docker-data de forma manual
```

ClubLab tendrá:

```text
su propia aplicación
su propia red
su propia base de datos
su propio volumen
sus propios usuarios
sus propias credenciales
sus propios scripts
sus propios escenarios
```

---

# 6. Acciones que los integrantes NO deben poder realizar sobre el host

No dar acceso normal al usuario administrativo `tulum`.

No agregar integrantes al grupo Docker del host.

No proporcionar acceso a:

```text
/home/tulum/.ssh
/home/tulum/backups
/home/docker-data
database-net productiva
Docker socket del host
servicios de producción
```

No permitir dentro del laboratorio:

```text
--privileged
montajes arbitrarios del host
Docker socket
acceso root al servidor real
```

El manual del servidor advierte particularmente sobre:

- `docker compose down -v`;
- eliminación de volúmenes;
- borrar `/home/docker-data`;
- publicar PostgreSQL;
- cambiar `eno1` remotamente;
- reiniciar NetworkManager sin plan;
- borrar llaves SSH.

---

# 7. Arquitectura conceptual objetivo

```text
                         INTEGRANTES
                              │
                              ▼
                    ┌─────────────────┐
                    │ ClubLab Gateway │
                    └────────┬────────┘
                             │
                 ┌───────────┴───────────┐
                 │                       │
          ┌──────▼──────┐         ┌──────▼──────┐
          │  Frontend   │         │     API     │
          │    React    │────────►│   NestJS    │
          └─────────────┘         └──────┬──────┘
                                        │
                                 ┌──────▼──────┐
                                 │ PostgreSQL  │
                                 │   ClubLab   │
                                 └─────────────┘

                    ┌─────────────────────┐
                    │       Toolbox       │
                    │ curl / psql / dig   │
                    │ ping / ss / etc.    │
                    └─────────────────────┘

                              Docker
                                │
                             TULUM
```

---

# 8. Modelo de equipos

Cada grupo tendrá un entorno independiente.

Ejemplo:

```text
team01
├── frontend
├── api
├── database
└── toolbox

team02
├── frontend
├── api
├── database
└── toolbox
```

Objetivo:

> Un equipo puede romper su laboratorio sin afectar a los demás.

---

# 9. Estructura general del proyecto

```text
clublab/
│
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
│   ├── networks/
│   └── toolbox/
│
├── scenarios/
│   ├── normal/
│   ├── api-down/
│   ├── db-down/
│   └── ...
│
├── scripts/
│   ├── deploy
│   ├── reset
│   ├── scenario
│   └── status
│
├── docs/
│   ├── instructor/
│   ├── students/
│   ├── roles/
│   └── architecture/
│
└── README.md
```

En Tulum se buscará respetar la organización existente:

```text
/home/tulum/apps/
```

sin administrar manualmente `/home/docker-data`.

---

# 10. Plan Maestro por fases

---

# FASE 0 — Auditoría y congelación del estado actual

## Objetivo

Verificar el estado real del servidor antes de modificarlo.

El manual corresponde al 29 de agosto de 2026, por lo que no se debe asumir que todo sigue exactamente igual.

## Revisar

```text
Sistema operativo
Kernel
CPU
RAM
Discos
/home
Docker
Contenedores
Redes Docker
Volúmenes
Puertos
firewalld
Tailscale
Cloudflare
Caddy
Servicios systemd
Rutas
```

## Comandos inicialmente permitidos

Solo consulta:

```bash
hostnamectl
df -h
free -h
ip route
sudo ss -lntup

docker ps
docker ps -a
docker network ls
docker volume ls
docker system df
docker stats

tailscale status
tailscale serve status

systemctl status docker
systemctl status tailscaled
systemctl status cloudflared-quick
```

## Entregable

`D00_Estado_Base_Servidor_ClubLab.md`

Debe incluir:

- estado real;
- diferencias respecto al manual;
- recursos disponibles;
- puertos ocupados;
- redes existentes;
- servicios que no deben tocarse;
- riesgos;
- opciones de publicación;
- decisión preliminar de acceso.

## Condición de salida

No se avanza hasta tener un mapa actualizado del servidor.

---

# FASE 1 — Diseño pedagógico de ClubLab #01

## Objetivo

Definir la experiencia antes de programar.

## Preguntas que deben poder responder al terminar

```text
¿Qué hace el frontend?
¿Qué hace el backend?
¿Qué es una API?
¿Dónde se guardan los datos?
¿Qué hace una base de datos?
¿Qué es un servidor?
¿Qué hace Docker?
¿Qué sucede si falla un componente?
¿Cómo podemos investigar un problema?
```

## Misiones preliminares

```text
M0  Conoce ClubLab
M1  ¿De dónde vienen los datos?
M2  Habla directamente con la API
M3  Encuentra dónde viven los datos
M4  Cambia el sistema
M5  Encuentra dónde se ejecuta
M6  Algo se rompió
M7  Diagnostica el incidente
M8  Reconstruye la arquitectura
```

## Entregable

`D01_Diseno_Experiencia_ClubLab_01.md`

Debe contener:

- objetivo de cada misión;
- duración;
- conocimientos implícitos;
- herramienta utilizada;
- pregunta detonadora;
- descubrimiento esperado;
- pista 1;
- pista 2;
- pista 3;
- evidencia de finalización.

---

# FASE 2 — Arquitectura técnica

## Objetivo

Diseñar la infraestructura completa antes de implementarla.

## Decisiones

Definir:

- frontend;
- backend;
- base de datos;
- gateway;
- redes;
- volúmenes;
- nombres DNS internos;
- acceso de alumnos;
- acceso del instructor;
- healthchecks;
- logs;
- límites de CPU;
- límites de RAM;
- persistencia;
- reset;
- réplicas por equipo;
- estrategia de publicación.

## Stack preliminar

```text
Frontend       React + TypeScript
Backend        NestJS + TypeScript
Database       PostgreSQL
ORM            Prisma o TypeORM
Infra          Docker Compose
```

La elección Prisma/TypeORM se hará según claridad pedagógica y mantenimiento, no únicamente por preferencia técnica.

## Entregable

`D02_Arquitectura_Tecnica_ClubLab_v1.md`

Debe incluir:

- diagrama lógico;
- diagrama de red;
- flujo HTTP;
- modelo Docker;
- persistencia;
- publicación;
- estrategia de aislamiento.

---

# FASE 3 — Seguridad, aislamiento y acceso

## Objetivo

Permitir experimentación sin poner en riesgo Tulum.

## Modelo

Cada equipo:

```text
teamXX
├── frontend
├── api
├── database
└── toolbox
```

## Toolbox

El contenedor de herramientas podrá incluir:

```text
curl
ping
dig
getent
psql
ss
traceroute
ip
```

## Restricciones

```text
sin --privileged
sin Docker socket
sin /home del host
sin ~/.ssh
sin /home/docker-data
sin database-net productiva
sin credenciales reales
sin acceso root al host
```

## Entregable

`D03_Modelo_Seguridad_Acceso_ClubLab.md`

---

# FASE 4 — Aplicación ClubLab

## Objetivo

Construir una aplicación suficientemente interesante para investigar, pero deliberadamente pequeña.

## Funciones propuestas

```text
Dashboard
Mi perfil
Integrantes
Equipos
Misiones
Ranking
Mensajes
Actividad
```

## Modelo inicial

```text
User
Team
Mission
Submission
Score
Message
ActivityLog
```

## Endpoints mínimos

```http
GET /api/health
GET /api/users
GET /api/users/:id
GET /api/ranking
GET /api/missions
POST /api/login
POST /api/messages
```

## Código organizado y legible

```text
src/
├── auth/
├── users/
├── teams/
├── missions/
├── ranking/
└── messages/
```

## Logs pedagógicos

Ejemplo:

```text
[API] GET /ranking
[DB] Query completed in 12 ms
[AUTH] User 5 authenticated
```

## Entregables

```text
APP01_ClubLab_Frontend
APP02_ClubLab_API
APP03_ClubLab_Database
APP04_Seeds_Demo
```

---

# FASE 5 — Motor de escenarios

## Objetivo

Convertir ClubLab en un laboratorio repetible.

## Escenarios iniciales

```text
00-normal
01-api-down
02-database-down
03-wrong-db-config
04-broken-endpoint
05-missing-data
06-auth-problem
07-security-preview
```

## Interfaz operativa deseada

Ejemplo conceptual:

```bash
./clublab status
./clublab start
./clublab stop

./clublab scenario load api-down

./clublab reset team01
./clublab reset all
```

## Reset

Debe restaurar:

```text
contenedores
configuración
base de datos
seeds
estado normal
```

## Entregables

```text
SYS01_ClubLab_Scenario_Manager
D04_Catalogo_Escenarios.md
```

---

# FASE 6 — Roles para integrantes

## Objetivo

Que cada alumno sepa qué investigar sin recibir un manual enorme.

## Roles iniciales

### 1. Explorador de interfaz

Herramientas:

```text
Browser
DevTools
Network
Fetch/XHR
Headers
Response
```

---

### 2. Investigador de API

Herramientas:

```text
HTTP
curl
JSON
status codes
```

---

### 3. Investigador de datos

Herramientas:

```text
PostgreSQL
psql
tablas
consultas simples
```

---

### 4. Operador de sistemas

Herramientas:

```text
terminal
red
procesos
servicios
diagnóstico
```

## Rotación

Los roles no representan profesiones permanentes.

Pueden rotarse a mitad de la sesión.

## Entregable

`D05_Tarjetas_Rol/`

```text
rol_interfaz.md
rol_api.md
rol_datos.md
rol_sistemas.md
```

---

# FASE 7 — Kit documental de integrantes

## Objetivo

Dar apoyo suficiente sin quitarles la exploración.

## Documento A — Bienvenido a ClubLab

Máximo 2–3 páginas.

Debe incluir:

```text
qué estamos haciendo
cómo entrar
cómo funciona el equipo
qué hacer si te pierdes
reglas del laboratorio
```

Archivo:

`D06_Guia_Integrante.md`

---

## Documento B — Cheat Sheet

### Navegador

```text
F12
Network
Fetch/XHR
Headers
Response
```

### HTTP

```bash
curl URL
curl -i URL
```

### Linux

```bash
pwd
ls
cd
cat
clear
```

### Red

```bash
ping
getent hosts
ss
```

### PostgreSQL

```text
\dt
\d tabla
SELECT ...
\q
```

Archivo:

`D07_Cheat_Sheet_ClubLab.md`

---

## Documento C — Cuaderno de misiones

Ejemplo:

```text
MISIÓN 03
Encuentra la fuente de los puntos

Sabemos:
La interfaz muestra 320 puntos.

No sabemos:
¿Dónde está almacenado ese número?

Objetivo:
Encuentra su origen y modifícalo.

Evidencia:
________________________
```

Archivo:

`D08_Cuaderno_Misiones.md`

---

## Documento D — Mapa incompleto

Inicio:

```text
NAVEGADOR
   │
   ▼
¿?????????
   │
   ▼
¿?????????
   │
   ▼
¿?????????
```

Final esperado:

```text
Browser
   ↓
Frontend
   ↓
API
   ↓
Backend
   ↓
PostgreSQL
```

El mapa no debe entregarse resuelto.

---

# FASE 8 — Guía privada del instructor

## Objetivo

Permitir impartir la sesión sin improvisar.

## Documento principal

`D09_Manual_Instructor.md`

Debe incluir:

- cronograma;
- qué decir;
- qué preguntar;
- qué observar;
- qué no revelar;
- respuestas esperadas;
- errores frecuentes;
- pistas escalonadas;- cuándo intervenir;
- cuándo dejar que fallen;
- cuándo cambiar de misión;
- tiempos máximos.

## Estructura ejemplo

```text
00:00 Bienvenida
00:05 Abrir ClubLab
00:10 Primera pregunta
00:15 Misión 1
...
01:20 Inyectar fallo
01:25 Investigación
...
01:55 Reconstrucción
02:00 Cierre
```

## Documento técnico separado

`D10_Runbook_Tecnico.md`

Debe incluir:

```text
cómo levantar ClubLab
cómo detenerlo
cómo comprobar salud
cómo cargar escenarios
cómo resetear equipos
cómo restaurar la BD
cómo consultar logs
qué hacer si falla Tailscale
qué hacer si falla Cloudflare
qué hacer si falla Docker
qué hacer si el laboratorio no inicia
```

---

# FASE 9 — Ensayos

## Ensayo A — Técnico

Probar desde cero:

```text
deploy
↓
seed
↓
login
↓
frontend
↓
API
↓
BD
↓
toolbox
↓
scenario
↓
reset
```

Escenarios mínimos:

```text
API caída
DB caída
frontend caído
configuración incorrecta
reinicio de un servicio
reset completo
```

## Ensayo B — Pedagógico

Simular:

- alumno avanzado;
- alumno principiante;
- alumno sin experiencia en Linux;
- alumno que termina rápido;
- equipo bloqueado;
- equipo que rompe más de lo previsto.

## Entregable

`D11_Checklist_Clase_Lista.md`

---

# FASE 10 — Ejecución de ClubLab #01

## Estructura general

```text
DESCUBRIR
0:00 ─────────────── 0:35

TOCAR
0:35 ─────────────── 1:15

ROMPER / INVESTIGAR
1:15 ─────────────── 1:45

RECONSTRUIR
1:45 ─────────────── 2:00
```

## Experiencia esperada

Los integrantes deben:

1. usar la aplicación;
2. descubrir peticiones;
3. inspeccionar JSON;
4. hablar con la API;
5. encontrar datos;
6. modificar información;
7. observar el cambio;
8. conocer el servidor;
9. identificar servicios;
10. investigar un fallo;
11. restaurar el sistema;
12. reconstruir la arquitectura completa.

---

# FASE 11 — Evaluación y evolución

## Objetivo

Medir interés y calidad de la experiencia, no memorizar conceptos.

## Preguntas

```text
¿Qué entendiste?
¿Qué te confundió?
¿Qué área te interesó?
¿Qué actividad disfrutaste?
¿Qué fue demasiado fácil?
¿Qué fue demasiado difícil?
¿Qué te gustaría tocar después?
```

## Perfil de interés

No es una calificación.

Ejemplo:

```text
Frontend        ██░░░
Backend         █████
Bases de datos  ████░
Redes           ███░░
DevOps          █████
Seguridad       ████░
```

## Posibles siguientes experiencias

```text
ClubLab #02 — Atacando una aplicación
ClubLab #03 — Cómo viaja una petición
ClubLab #04 — La base de datos tiene un problema
ClubLab #05 — Producción se cayó
ClubLab #06 — Autenticación y sesiones
ClubLab #07 — Tiempo real y WebSockets
```

---

# 11. Flujo completo del proyecto

```text
FASE 0
Auditoría servidor
   ↓
FASE 1
Diseño pedagógico
   ↓
FASE 2
Arquitectura
   ↓
FASE 3
Seguridad / acceso
   ↓
FASE 4
Aplicación
   ↓
FASE 5
Escenarios
   ↓
FASE 6
Roles
   ↓
FASE 7
Material integrantes
   ↓
FASE 8
Material instructor
   ↓
FASE 9
Ensayos
   ↓
FASE 10
Clase
   ↓
FASE 11
Evaluación
```

---

# 12. Entregables maestros

```text
D00  Estado Base del Servidor
D01  Diseño de Experiencia ClubLab #01
D02  Arquitectura Técnica ClubLab v1
D03  Modelo de Seguridad y Acceso
D04  Catálogo de Escenarios
D05  Tarjetas de Rol
D06  Guía del Integrante
D07  Cheat Sheet ClubLab
D08  Cuaderno de Misiones
D09  Manual del Instructor
D10  Runbook Técnico
D11  Checklist de Clase Lista

APP01 Frontend
APP02 API
APP03 Database
APP04 Seeds

SYS01 Scenario Manager
```

---

# 13. Criterios de éxito

ClubLab v1 está terminado cuando:

- el laboratorio se despliega de forma reproducible;
- no depende de servicios de producción;
- cada equipo puede tener un entorno aislado;
- existe un reset confiable;
- las misiones están documentadas;
- los roles están documentados;
- el instructor dispone de guía completa;
- los alumnos disponen de material breve;
- los escenarios se pueden cargar bajo demanda;
- la clase puede ejecutarse aun si un equipo rompe completamente su entorno;
- existe un plan B técnico;
- toda la sesión puede completarse en 2 horas.

---

# 14. Próximo paso

El siguiente paso oficial del proyecto es:

# FASE 0 — Auditoría del servidor

Primero se ejecutarán únicamente comandos de consulta.

No se modificará:

- Docker;
- redes;
- firewall;
- PostgreSQL;
- Tailscale;
- Cloudflare;
- NetworkManager;
- servicios productivos.

La salida de la auditoría se comparará con el manual de agosto de 2026 y se creará:

`D00_Estado_Base_Servidor_ClubLab.md`

A partir de ese documento se cerrará la arquitectura real de ClubLab.

---

# 15. Nota de continuidad

Este archivo debe considerarse el **documento maestro de contexto de ClubLab v1**.

Cuando se tome una decisión importante sobre:

- arquitectura;
- seguridad;
- stack;
- roles;
- experiencia;
- escenarios;
- infraestructura;
- documentación;

debe actualizarse este archivo o registrar el cambio en un documento derivado.

El objetivo es que el proyecto pueda retomarse posteriormente sin depender únicamente del historial del chat.