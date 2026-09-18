# ClubLab — Fase 1 / Bloque B
## Narrativa + arquitectura a descubrir

**Proyecto:** ClubLab v1  
**Experiencia:** ClubLab #01 — *Desarmando una aplicación*  
**Fase:** 1 — Diseño pedagógico  
**Bloque:** B  
**Dependencia:** Bloque A — Perfil + objetivos  
**Estado:** CERRADO PARA DISEÑO v1

---

# 1. Propósito del Bloque B

Este bloque define **cómo se presenta ClubLab #01**, qué sabe el integrante al comenzar, qué información se mantiene oculta y cómo se revela progresivamente la arquitectura durante la sesión.

No se diseñan todavía las misiones en detalle.

La intención es que el alumno no reciba esta arquitectura:

```text
Navegador
  ↓
Frontend
  ↓
API
  ↓
Backend
  ↓
PostgreSQL
```

como explicación inicial.

Debe **descubrirla**.

---

# 2. Idea narrativa central

ClubLab #01 se presenta como una investigación técnica.

El sistema ya existe y está funcionando.

Los integrantes reciben acceso a una aplicación del club, pero no reciben su diagrama, código fuente completo ni explicación de infraestructura.

La consigna inicial será:

> **“La aplicación ya está funcionando. Su trabajo no es programarla: su trabajo es descubrir cómo funciona.”**

Esto cambia la dinámica de:

```text
“te voy a explicar una arquitectura”
```

a:

```text
“vas a encontrar la arquitectura”
```

---

# 3. Nombre visible de la experiencia

Nombre principal:

# ClubLab #01 — Desarmando una aplicación

Subtítulo opcional:

> **¿Qué hay detrás de lo que ves en pantalla?**

Evitar nombres como:

```text
Curso de arquitectura web
Introducción a APIs
Clase de backend
Docker básico
```

porque revelan demasiado pronto el contenido y hacen que la sesión se perciba como clase tradicional.

---

# 4. Estado inicial del participante

Al comenzar, el integrante solo debe saber:

```text
1. Existe una aplicación.
2. Tiene una URL.
3. Tiene una cuenta de laboratorio.
4. Trabaja en un equipo.
5. Puede investigar.
6. Puede pedir pistas.
7. Puede romper únicamente su entorno.
```

No debe conocer todavía:

```text
frameworks;
estructura del backend;
tipo de base de datos;
cantidad de contenedores;
redes Docker;
endpoints disponibles;
diagrama completo;
incidente futuro.
```

---

# 5. Lo primero que verá

La aplicación deberá parecer una herramienta real del club.

Pantalla inicial propuesta:

```text
┌───────────────────────────────────────────────┐
│ ClubLab                                      │
├───────────────────────────────────────────────┤
│ Hola, Equipo 03                              │
│                                               │
│ Puntos                      320                │
│ Misiones completadas         4                │
│ Posición                     2                │
│                                               │
│ Actividad reciente                            │
│ • Ana completó Misión 2                       │
│ • Equipo 01 ganó 20 puntos                    │
│ • Nueva misión disponible                     │
│                                               │
│ [Ranking] [Misiones] [Equipo] [Actividad]    │
└───────────────────────────────────────────────┘
```

La interfaz debe contener datos suficientemente visibles como para provocar preguntas.

---

# 6. Primera pregunta detonadora

Después de unos minutos explorando:

> **“Ese número de 320 puntos, ¿de dónde salió?”**

No se acepta de inmediato:

```text
“de la base de datos”
```

como respuesta final.

La siguiente pregunta será:

> **“¿Cómo lo sabes?”**

Esto establece desde el principio la regla de ClubLab:

> **Las respuestas deben apoyarse en evidencia.**

---

# 7. Narrativa general de la sesión

La experiencia tendrá cuatro momentos narrativos.

```text
ACTO I
EL SISTEMA FUNCIONA

ACTO II
DESCUBRIMOS SUS CAPAS

ACTO III
ALGO FALLA

ACTO IV
RECONSTRUIMOS EL SISTEMA
```

---

# 8. Acto I — El sistema funciona

## Estado narrativo

Todo funciona correctamente.

Los integrantes navegan la aplicación sin explicación previa.

La sensación buscada:

```text
“Esto parece una app normal.”
```

Luego aparecen preguntas:

```text
¿de dónde viene este dato?
¿quién lo calcula?
¿qué pasa cuando doy clic?
¿por qué tarda?
¿dónde se guarda?
```

---

# 9. Acto II — Descubrimos sus capas

Cada descubrimiento debe responder una pregunta anterior.

Secuencia conceptual:

```text
Veo un dato
    ↓
Descubro una petición
    ↓
Descubro una API
    ↓
Descubro un backend
    ↓
Descubro una base de datos
    ↓
Descubro que cada componente se ejecuta por separado
```

El instructor no presenta esta secuencia como temario.

La experiencia la provoca.

---

# 10. Acto III — Algo falla

Cuando el equipo ya tiene un modelo mental parcial:

> **“Hay un incidente. El ranking dejó de responder correctamente.”**

No se revela:

```text
qué servicio falló;
qué comando ejecutar;
qué archivo revisar;
qué contenedor tocar.
```

El sistema deberá proporcionar suficiente evidencia para investigar.

---

# 11. Acto IV — Reconstruimos el sistema

Después de reparar o identificar el incidente:

> **“Ahora dibujen el sistema que acaban de investigar.”**

El grupo debe reconstruirlo sin copiar un diagrama proporcionado.

El instructor consolida al final.

---

# 12. Arquitectura conceptual que deben descubrir

La arquitectura pedagógica central será:

```text
USUARIO
   │
   ▼
NAVEGADOR
   │
   ▼
FRONTEND
   │
   │ HTTP
   ▼
API / BACKEND
   │
   ▼
POSTGRESQL
```

Luego se añade la infraestructura:

```text
                    SERVIDOR
                       │
                     Docker
                       │
        ┌──────────────┼──────────────┐
        │              │              │
    Frontend          API        PostgreSQL
```

---

# 13. Nivel de precisión esperado

El objetivo no es que un principiante salga diciendo:

```text
reverse proxy
bridge network
container namespace
ORM
connection pool
```

La comprensión mínima correcta es:

```text
El navegador usa el frontend.

El frontend pide información.

El backend recibe la petición.

El backend consulta o modifica datos.

La base de datos guarda esos datos.

Las partes se ejecutan como servicios separados.
```

---

# 14. Capas de descubrimiento

La arquitectura se revelará en seis capas.

---

## Capa 0 — “La aplicación”

Modelo inicial:

```text
┌─────────────────┐
│   APLICACIÓN    │
└─────────────────┘
```

Es deliberadamente incompleto.

---

## Capa 1 — Navegador e interfaz

Después de explorar:

```text
USUARIO
   │
   ▼
NAVEGADOR
   │
   ▼
INTERFAZ
```

Conceptos asociados:

```text
UI
navegador
DevTools
```

---

## Capa 2 — Peticiones

Después de observar Network:

```text
NAVEGADOR
   │
   │ GET /api/ranking
   ▼
????????
```

Conceptos asociados:

```text
HTTP
request
response
status
```

---

## Capa 3 — API / backend

Después de consultar directamente la API:

```text
FRONTEND
   │
   ▼
API / BACKEND
```

Conceptos asociados:

```text
endpoint
JSON
lógica
```

---

## Capa 4 — Datos

Después de consultar PostgreSQL:

```text
FRONTEND
   │
   ▼
BACKEND
   │
   ▼
DATABASE
```

Conceptos asociados:

```text
persistencia
tabla
registro
consulta
```

---

## Capa 5 — Infraestructura

Después de observar servicios:

```text
SERVER
  │
Docker
  │
  ├── frontend
  ├── api
  └── database
```

Conceptos asociados:

```text
servicio
contenedor
aislamiento
estado
logs
```

---

# 15. Diagrama inicial entregado al equipo

Los integrantes recibirán un mapa incompleto.

Versión propuesta:

```text
┌──────────────┐
│   USUARIO    │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  NAVEGADOR   │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│      ?       │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│      ?       │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│      ?       │
└──────────────┘
```

A un lado:

```text
¿Dónde se ejecuta todo esto?

┌──────────────────────────────┐
│              ?               │
│                              │
│   [?]       [?]       [?]    │
└──────────────────────────────┘
```

---

# 16. Diagrama final esperado

Una versión correcta al final podría ser:

```text
┌──────────────┐
│   USUARIO    │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  NAVEGADOR   │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   FRONTEND   │
└──────┬───────┘
       │ HTTP
       ▼
┌──────────────┐
│ API/BACKEND  │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ POSTGRESQL   │
└──────────────┘
```

Infraestructura:

```text
┌───────────────────────────────────┐
│             SERVIDOR              │
│                                   │
│              Docker               │
│                                   │
│  ┌────────┐ ┌────────┐ ┌───────┐ │
│  │Frontend│ │  API   │ │  DB   │ │
│  └────────┘ └────────┘ └───────┘ │
└───────────────────────────────────┘
```

---

# 17. El diagrama no será una prueba de dibujo

Se aceptan variaciones.

Ejemplos válidos:

```text
Browser → Web → API → DB

Cliente → Front → Backend → PostgreSQL

Usuario → Navegador → React → Nest → Postgres
```

Lo importante es que expliquen correctamente la relación.

---

# 18. Información que se mantiene oculta al inicio

Ocultar deliberadamente:

```text
React
NestJS
PostgreSQL
Docker Compose
nombres de contenedores
esquema completo
lista de endpoints
diagrama técnico
código fuente
credenciales de servicios
```

---

# 19. Información que puede revelarse progresivamente

## Después de descubrir frontend

Se puede revelar:

```text
“Sí, esta parte está hecha con React.”
```

No antes.

---

## Después de descubrir API

Se puede revelar:

```text
“Este servicio está construido con NestJS.”
```

---

## Después de descubrir DB

Se puede revelar:

```text
“La base es PostgreSQL.”
```

---

## Después de descubrir infraestructura

Se puede revelar:

```text
“Cada componente está ejecutándose en un contenedor.”
```

La tecnología se utiliza para nombrar algo que ya entendieron conceptualmente.

---

# 20. Regla de revelación

Orden:

```text
CONCEPTO
   ↓
EVIDENCIA
   ↓
NOMBRE TÉCNICO
   ↓
EXPLICACIÓN BREVE
```

No:

```text
NOMBRE TÉCNICO
   ↓
DEFINICIÓN
   ↓
EJEMPLO
```

---

# 21. Cómo introducir HTTP

No comenzar con:

> “HTTP es un protocolo de capa de aplicación…”

Primero:

```text
GET /api/ranking
Status: 200
Response: [...]
```

Luego preguntar:

> “¿Qué creen que acaba de pasar?”

Después se nombra:

```text
request
response
HTTP
```

---

# 22. Cómo introducir API

Primero deben descubrir que una URL responde datos sin la interfaz.

Entonces:

> **“Acaban de usar la API directamente.”**

Explicación breve:

```text
La API es una forma definida para que
una parte del sistema pida información
o ejecute acciones en otra.
```

---

# 23. Cómo introducir backend

No definirlo como “servidor”.

Explicación objetivo:

```text
El backend es la parte que recibe peticiones,
aplica lógica y se comunica con los datos
u otros servicios.
```

Aclarar posteriormente:

```text
backend ≠ máquina física
server puede referirse a varias cosas según contexto
```

Sin profundizar demasiado.

---

# 24. Cómo introducir base de datos

Primero:

```text
320 puntos en UI
        ↓
320 en JSON
        ↓
320 en una fila SQL
```

Después:

> **“Este dato persiste aquí aunque el navegador se cierre.”**

Así se introduce persistencia.

---

# 25. Cómo introducir Docker

Docker aparece tarde.

Primero deben entender que existen:

```text
frontend
backend
database
```

Luego se pregunta:

> **“¿Dónde están corriendo estas tres cosas?”**

Después se muestra el concepto:

```text
contenedores
```

No profundizar todavía en imágenes, layers, namespaces o cgroups.

---

# 26. Cómo introducir logs

Los logs aparecerán principalmente durante el incidente.

No enseñar un bloque teórico de logging.

Primero:

```text
“Sabemos que algo falló.
¿Cómo preguntamos al servicio qué ocurrió?”
```

Luego se presentan los logs como evidencia.

---

# 27. Frases recomendadas para el instructor

Inicio:

> **“Hoy no vamos a construir una aplicación. Vamos a desarmar una que ya funciona.”**

Después de abrir la app:

> **“No den por hecho cómo funciona. Demuéstrenlo.”**

Cuando alguien diga “está en la base”:

> **“¿Qué evidencia tienes?”**

Cuando aparezca Network:

> **“Eso que están viendo es parte de la conversación entre componentes.”**

Antes del incidente:

> **“Hasta ahora el sistema les ha estado ayudando. Ahora vamos a ver qué pasa cuando deja de hacerlo.”**

Cierre:

> **“Hace dos horas esto era una sola aplicación. ¿Cuántas piezas ven ahora?”**

---

# 28. Lenguaje que conviene evitar

Evitar:

```text
“Esto es muy fácil.”
“Esto ya deberían saberlo.”
“Simplemente hagan…”
“Obviamente…”
“Solo es Docker.”
```

Usar:

```text
“¿Qué observan?”
“¿Qué evidencia tienen?”
“¿Qué hipótesis explica esto?”
“¿Qué componente descartarían?”
```

---

# 29. Estado emocional buscado

La experiencia debe generar esta progresión:

```text
CURIOSIDAD
“¿de dónde viene eso?”

DESCUBRIMIENTO
“ah, hay una petición”

CONEXIÓN
“entonces la API habla con la DB”

TENSIÓN
“el ranking dejó de funcionar”

INVESTIGACIÓN
“veamos qué sigue vivo”

RESOLUCIÓN
“ya sabemos qué falló”

COMPRENSIÓN
“ahora entiendo las piezas”
```

---

# 30. Uso del código fuente

El código fuente no debe ser el primer recurso.

Orden recomendado:

```text
1. comportamiento
2. Network
3. API
4. DB
5. servicios
6. código
```

Solo después de entender el flujo se puede mostrar:

```text
frontend/
backend/
database/
```

y dentro del backend:

```text
controller
service
repository / ORM
```

El código sirve para conectar lo observado con una implementación real.

---

# 31. Nivel de código permitido en ClubLab #01

El alumno puede tocar fragmentos simples como:

```ts
const POINTS_PER_MISSION = 20;
```

o identificar algo como:

```ts
@Get('ranking')
```

pero no debe depender de comprender NestJS o React para avanzar.

---

# 32. Arquitectura del sistema vs arquitectura del laboratorio

Es importante separar dos conceptos.

## Arquitectura que el alumno descubre

```text
Frontend
Backend
Database
```

## Arquitectura real de seguridad del laboratorio

Puede incluir además:

```text
gateway
toolbox
red por equipo
scenario manager
proxy
healthchecks
```

Estos componentes no necesariamente deben enseñarse en ClubLab #01.

La infraestructura educativa puede ser más compleja que la arquitectura visible.

---

# 33. Qué NO se mostrará aunque exista técnicamente

No es necesario revelar en la primera sesión:

```text
redes Docker internas;
nombres de bridges;
Tailscale;
Cloudflare;
Caddy del host;
firewalld;
Pelican;
Wings;
infraestructura real de Tulum;
Scenario Manager interno.
```

Todo eso pertenece al funcionamiento de ClubLab, no a la experiencia principal.

---

# 34. Separación entre “real” y “seguro”

La experiencia debe ser real en el sentido de que:

```text
las peticiones son reales;la API es real;
la DB es real;
los cambios son reales;
los logs son reales;
los fallos son reales.
```

Pero segura porque:

```text
todo ocurre en recursos ClubLab;
nada afecta producción;
cada equipo está aislado;
todo puede resetearse.
```

---

# 35. Metáfora opcional para principiantes

Solo si un equipo está completamente perdido:

```text
Frontend = mostrador
Backend  = cocina
Database = almacén
API      = forma de hacer pedidos
```

No usarla como explicación principal.

Debe ser apoyo, no sustituto de la arquitectura real.

---

# 36. Puntos de revelación

Se establecen seis momentos.

| Momento | Lo que descubren | Lo que puede nombrarse |
|---|---|---|
| R0 | App visible | “interfaz” |
| R1 | Petición | HTTP / request |
| R2 | JSON directo | API |
| R3 | Procesamiento | backend |
| R4 | Persistencia | PostgreSQL / database |
| R5 | Servicios separados | Docker / contenedores |

---

# 37. Arquitectura mínima obligatoria al final

Todos los equipos deben llegar al menos a:

```text
Navegador
   ↓
Frontend
   ↓
API / Backend
   ↓
Base de datos
```

---

# 38. Arquitectura extendida para equipos avanzados

Pueden agregar:

```text
usuario
DNS / hostname
HTTP
puertos
contenedores
logs
healthcheck
servidor
red
```

Sin convertirlos en requisitos para los demás.

---

# 39. Relación narrativa con el incidente

El incidente debe depender directamente de la arquitectura descubierta.

No introducir algo completamente nuevo como:

```text
certificado TLS roto
DNS externo
problema de kernel
firewall
```

porque el alumno no tendría modelo mental para diagnosticarlo.

El fallo debe estar dentro de:

```text
frontend
API/backend
database
comunicación entre backend y DB
```

---

# 40. Criterio para elegir el incidente final

El escenario deberá cumplir:

```text
1. El síntoma es visible.
2. No rompe absolutamente todo.
3. Produce evidencia en Network.
4. Produce evidencia en logs.
5. Puede aislarse por razonamiento.
6. Puede restaurarse rápido.
7. No requiere conocimiento nuevo.
```

La elección concreta se hará en el Bloque E.

---

# 41. Resultado narrativo deseado al finalizar

Antes:

> **“Es una página.”**

Después:

> **“El navegador carga un frontend, el frontend pide datos a una API, el backend procesa la petición y consulta PostgreSQL. Esos componentes están ejecutándose por separado y podemos diagnosticar cuál falla.”**

Ese cambio de modelo mental es el principal producto de ClubLab #01.

---

# 42. Decisiones cerradas en Bloque B

### DB-01

La experiencia se presenta como una **investigación**, no como una clase tradicional.

### DB-02

La arquitectura completa estará oculta al inicio.

### DB-03

La primera pregunta detonadora será sobre el origen de un dato visible.

### DB-04

La arquitectura se revelará progresivamente.

### DB-05

Los nombres técnicos se introducen después de observar el concepto.

### DB-06

Docker aparece después de frontend/backend/database.

### DB-07

El código fuente aparece después de comprender el flujo.

### DB-08

El incidente solo utilizará conceptos ya descubiertos.

### DB-09

La infraestructura real de Tulum permanecerá invisible para los alumnos.

### DB-10

El alumno recibirá un diagrama incompleto y construirá el final.

---

# 43. Entregables del Bloque B

Este bloque produce:

```text
P03_Narrativa_ClubLab01
P03A_Arquitectura_Descubrimiento
P03B_Reglas_Revelacion
P03C_Diagrama_Inicial
P03D_Diagrama_Final_Esperado
```

---

# 44. Criterios de aceptación

- [x] Narrativa principal definida.
- [x] Estado inicial definido.
- [x] Información oculta definida.
- [x] Secuencia de revelación definida.
- [x] Arquitectura mínima definida.
- [x] Arquitectura extendida definida.
- [x] Diagrama inicial definido.
- [x] Diagrama final esperado definido.
- [x] Regla de introducción de conceptos definida.
- [x] Uso del código fuente definido.
- [x] Relación con incidente definida.
- [x] Límites de contenido definidos.

# BLOQUE B — COMPLETADO

---

# 45. Siguiente bloque

# BLOQUE C — Catálogo de misiones

El siguiente bloque convertirá esta narrativa en actividades concretas.

Se diseñarán, una por una:

```text
M0 — Reconocimiento
M1 — ¿De dónde vienen los datos?
M2 — Habla con la API
M3 — Encuentra dónde viven los datos
M4 — Cambia el sistema
M5 — ¿Dónde se está ejecutando?
M6 — Incidente
M7 — Diagnóstico
M8 — Reconstrucción
```

Para cada misión se definirá:

```text
objetivo;
narrativa;
tiempo;
rol principal;
herramientas;
tarea;
restricciones;
descubrimiento esperado;
evidencia;
pistas;
error frecuente;
reto opcional;
condición de salida.
```

El Bloque C será el núcleo pedagógico de ClubLab #01.