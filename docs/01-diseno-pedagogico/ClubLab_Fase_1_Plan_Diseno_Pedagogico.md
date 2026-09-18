# ClubLab — Plan de Fase 1
## Diseño pedagógico de ClubLab #01 — “Desarmando una aplicación”

**Proyecto:** ClubLab v1  
**Fase:** 1  
**Nombre:** Diseño pedagógico de la experiencia  
**Duración objetivo de la sesión final:** 2 horas  
**Estado:** PLAN DE TRABAJO  
**Entrada principal:** `D00_Estado_Base_Servidor_ClubLab.md`  
**Entregable principal:** `D01_Diseno_Experiencia_ClubLab_01.md`

---

# 1. Propósito de la Fase 1

La Fase 1 define **qué experiencia vivirán los integrantes del club**, antes de decidir cómo implementar técnicamente cada componente.

En esta fase no se desarrolla todavía la aplicación ni se configura infraestructura.

La pregunta principal es:

> **¿Qué debe descubrir una persona durante dos horas para entender cómo funciona una aplicación real sin convertir la sesión en una clase tradicional de sintaxis?**

El resultado debe permitir que, al terminar la sesión, los integrantes puedan construir por sí mismos una idea como:

```text
Usuario
  ↓
Navegador
  ↓
Frontend
  ↓
HTTP / API
  ↓
Backend
  ↓
Base de datos
```

y además entender que todo esto se ejecuta sobre:

```text
Servidor
Linux
Docker
Red
```

---

# 2. Principios pedagógicos

## 2.1 Experimentar antes de explicar

Secuencia principal:

```text
OBSERVAR
   ↓
PREGUNTAR
   ↓
PROBAR
   ↓
DESCUBRIR
   ↓
EXPLICAR
```

No:

```text
DEFINICIÓN
   ↓
TEORÍA
   ↓
SINTAXIS
   ↓
EJERCICIO
```

---

## 2.2 El integrante debe tocar el sistema

La sesión no puede ser una demostración pasiva.

Cada equipo debe poder:

```text
abrir
inspeccionar
consultar
modificar
romper
diagnosticar
recuperar
```

su propio entorno de laboratorio.

---

## 2.3 El error forma parte del aprendizaje

No se busca evitar fallos.

Se busca que los fallos sean:

```text
controlados
repetibles
diagnosticables
reversibles
```

---

## 2.4 No enseñar herramientas aisladas

No habrá bloques del tipo:

```text
20 min de React
20 min de NestJS
20 min de PostgreSQL
20 min de Docker
```

En su lugar, las herramientas aparecerán porque son necesarias para resolver una misión.

Ejemplo:

```text
“El ranking no carga”
        ↓
Network
        ↓
HTTP 500
        ↓
logs
        ↓
base de datos
```

---

# 3. Resultado de aprendizaje esperado

Al final de ClubLab #01 un integrante debería poder explicar, con sus propias palabras:

- qué diferencia hay entre frontend y backend;
- qué es una API;
- para qué sirve HTTP;
- de dónde vienen los datos que aparecen en pantalla;
- qué papel cumple una base de datos;
- qué ocurre cuando un servicio falla;
- por qué una aplicación puede tener varias partes funcionando por separado;
- qué hace un servidor;
- para qué se utiliza Docker;
- qué herramientas sirven para investigar un problema.

No se exige que pueda programar cada una de esas piezas.

---

# 4. Resultados de descubrimiento

La sesión debe producir al menos estos descubrimientos:

```text
D1. La interfaz no contiene necesariamente los datos.
D2. El frontend realiza peticiones.
D3. Las peticiones tienen método, URL, headers, status y respuesta.
D4. Una API puede usarse sin la interfaz.
D5. El backend procesa peticiones.
D6. El backend consulta datos.
D7. Los datos persisten en una base de datos.
D8. Cambiar datos puede cambiar lo que ve el usuario.
D9. Los componentes se ejecutan como servicios separados.
D10. Si un componente falla, el resto puede seguir funcionando.
D11. Logs, Network y estado de servicios ayudan a diagnosticar.
D12. Una aplicación completa es una arquitectura, no un solo programa.
```

---

# 5. Experiencia narrativa

ClubLab #01 debe sentirse como una investigación técnica.

La narrativa propuesta:

> Los integrantes reciben acceso a una aplicación del club. Funciona correctamente al inicio, pero no se les explica su arquitectura. A través de pequeñas misiones descubren progresivamente cómo está construida. Más adelante aparece un incidente realista y cada equipo debe localizar qué componente falló y recuperar el sistema.

La clase comienza con:

```text
“Esta aplicación ya está funcionando.
No les voy a decir cómo está hecha.
Su trabajo es descubrirlo.”
```

---

# 6. Estructura de la sesión

La sesión de 2 horas se dividirá en cuatro actos.

```text
ACTO 1 — DESCUBRIR
00:00 ───────────── 00:30

ACTO 2 — CONECTAR
00:30 ───────────── 01:05

ACTO 3 — INCIDENTE
01:05 ───────────── 01:40

ACTO 4 — RECONSTRUIR
01:40 ───────────── 02:00
```

Los tiempos exactos se cerrarán en el documento final de experiencia.

---

# 7. Acto 1 — Descubrir

## Objetivo

Despertar preguntas antes de presentar conceptos.

## Experiencia

Los equipos reciben:

```text
URL de ClubLab
usuario de laboratorio
número de equipo
guía breve
primera misión
```

Primero navegan la aplicación.

La aplicación debe mostrar suficiente información para provocar preguntas:

```text
perfil
equipo
ranking
misiones
actividad
mensajes
```

## Pregunta detonadora

> **¿De dónde salió el número que aparece en el ranking?**

No explicar todavía frontend, backend o base de datos.

---

# 8. Misiones preliminares

La numeración definitiva se cerrará al final de esta fase.

---

## Misión 0 — Reconocimiento

### Objetivo

Familiarizarse con la aplicación.

### Tarea

Encontrar:

```text
perfil
equipo
ranking
misiones
actividad
```

### Descubrimiento

La aplicación tiene varias vistas y datos relacionados.

### Tiempo objetivo

5–8 minutos.

---

## Misión 1 — ¿De dónde vienen los datos?

### Objetivo

Descubrir DevTools y Network.

### Tarea

Investigar qué ocurre cuando se abre el ranking.

### Herramientas

```text
F12
Network
Fetch/XHR
```

### Descubrimiento esperado

Existe una petición parecida a:

```http
GET /api/ranking
```

---

## Misión 2 — Habla con la API

### Objetivo

Separar mentalmente interfaz y API.

### Tarea

Abrir directamente una URL de API o utilizar `curl`.

Ejemplo:

```bash
curl http://api/.../ranking
```

### Descubrimiento

La información existe aunque no se utilice la interfaz gráfica.

---

## Misión 3 — Encuentra dónde viven los datos

### Objetivo

Descubrir PostgreSQL.

### Tarea

Utilizar una terminal/controlada y consultar una tabla.

Ejemplo conceptual:

```sql
SELECT * FROM scores;
```

### Descubrimiento

El número visto en la interfaz está almacenado como dato persistente.

---

## Misión 4 — Cambia el sistema

### Objetivo

Demostrar la relación BD → API → frontend.

### Tarea

Modificar un valor permitido.

Ejemplo:

```text
puntos de un usuario
estado de una misión
nombre visible del equipo
```

Luego:

```text
recargar aplicación
```

### Descubrimiento

```text
BD
 ↓
backend
 ↓
API
 ↓
frontend
```

---

## Misión 5 — ¿Dónde se está ejecutando?

### Objetivo

Introducir servicios y contenedores.

### Tarea

Consultar el entorno de laboratorio.

El alumno no recibirá acceso Docker al host.

La experiencia deberá mostrar de forma segura que existen componentes separados:

```text
frontend
api
database
toolbox
```

### Descubrimiento

Una aplicación no es un único proceso.

---

# 9. Acto 2 — Conectar

## Objetivo

Relacionar descubrimientos aislados.

Los equipos deben completar un mapa incompleto.

Inicio:

```text
NAVEGADOR
   │
   ▼
??????????
   │
   ▼
??????????
   │
   ▼
??????????
```

Conforme avanzan:

```text
NAVEGADOR
   │
   ▼
FRONTEND
   │
 HTTP
   ▼
API / BACKEND
   │
   ▼
POSTGRESQL
```

Posteriormente se añade:

```text
SERVER
  └── Docker
      ├── frontend
      ├── api
      └── database
```

La explicación formal llega **después** de que hayan encontrado las piezas.

---

# 10. Acto 3 — Incidente

## Objetivo

Hacer que los integrantes utilicen el modelo mental recién construido.

No se les dirá directamente qué se rompió.

Mensaje de incidente:

> **“El ranking dejó de funcionar. El resto de la aplicación todavía abre. Averigüen qué ocurrió.”**

---

# 11. Escenario principal recomendado

Para ClubLab #01 el fallo debe ser comprensible y producir señales claras.

Escenario inicial recomendado:

```text
frontend     → funciona
api          → funciona parcialmente
database     → inaccesible o configuración incorrecta
ranking      → falla
```

Otra opción:

```text
frontend     → funciona
api          → detenida
database     → funciona
```

La selección definitiva se hará durante esta fase según dificultad pedagógica.

---

# 12. Método de diagnóstico que queremos provocar

Idealmente los alumnos recorrerán:

```text
1. La página abre.
2. El ranking no carga.
3. DevTools muestra error.
4. Network muestra una petición fallida.
5. Se observa status HTTP.
6. Se consulta la API directamente.
7. Se revisan logs.
8. Se determina qué componente falló.
9. Se ejecuta la recuperación permitida.
10. Se comprueba que el ranking volvió.
```

Sin presentar inicialmente esta lista como receta.

---

# 13. Niveles de pistas

Cada misión tendrá tres niveles.

## Pista 1 — conceptual

Ejemplo:

> “La interfaz necesita conseguir ese dato de algún sitio.”

No revela herramienta.

---

## Pista 2 — dirección

Ejemplo:

> “Observa qué ocurre en el navegador cuando abres el ranking.”

---

## Pista 3 — operativa

Ejemplo:

> “Abre F12 → Network → Fetch/XHR y recarga la página.”

La guía del instructor determinará cuándo utilizar cada nivel.

---

# 14. Acto 4 — Reconstrucción

## Objetivo

Convertir experimentos en comprensión.

Cada equipo completa el mapa final.

Ejemplo:

```text
                         SERVIDOR
                            │
                          Docker
                            │
              ┌─────────────┼─────────────┐
              │             │             │
          Frontend         API        PostgreSQL
              │             │             │
              └──── HTTP ───┘             │
                            └───────────────┘

                            ▲
                            │
                        Navegador
```

No importa que el diagrama exacto sea perfecto.

Importa que puedan justificar:

```text
qué hace cada componente
cómo se comunican
qué ocurrió durante el incidente
```

---

# 15. Cierre de la sesión

No terminar con un examen.

Cerrar con preguntas como:

```text
¿Qué parte te dio más curiosidad?
¿Qué herramienta no conocías?
¿En qué parte te gustaría profundizar?
¿Qué fue lo más difícil de diagnosticar?
¿Preferirías trabajar con interfaz, datos, servidores, redes o seguridad?
```

Esto servirá para orientar los siguientes ClubLab.

---

# 16. Roles durante la sesión

La Fase 1 debe definir qué hace cada rol, pero los documentos de rol se producirán formalmente en la Fase 6.

Roles preliminares:

```text
Explorador de Interfaz
Investigador de API
Investigador de Datos
Operador de Sistemas
```

---

# 17. Rol — Explorador de Interfaz

Responsabilidades:

```text
usar la aplicación
observar comportamientos
usar DevTools
identificar peticiones
registrar errores visuales
```

Herramientas:

```text
Browser
DevTools
Network
Console básica
```

---

# 18. Rol — Investigador de API

Responsabilidades:

```text
probar endpoints
leer JSON
observar status HTTP
comparar respuestas
```

Herramientas:

```text
curl
HTTP
JSON
```

---

# 19. Rol — Investigador de Datos

Responsabilidades:

```text
explorar tablas permitidas
consultar datos
realizar modificaciones controladas
verificar persistencia
```

Herramientas:

```text
psql
SQL básico
```

---

# 20. Rol — Operador de Sistemas

Responsabilidades:

```text
observar servicios
consultar estado
revisar logs permitidos
ejecutar recuperación de laboratorio
```

Herramientas:

```text
terminal
health checks
logs
comandos seguros
```

---

# 21. Rotación de roles

Para evitar que cada integrante toque una sola área durante toda la sesión:

```text
Acto 1
→ roles iniciales

Acto 3
→ rotación parcial
```

Ejemplo:

```text
Interfaz ↔ Sistemas
API ↔ Datos
```

La rotación debe durar menos de dos minutos.

---

# 22. Tamaño de equipo

Hipótesis inicial:

```text
3–4 integrantes por equipo
```

Ideal:

```text
4 integrantes
1 por rol
```

Si hay tres:

```text
API + Datos
```

pueden combinarse.

Si hay cinco:

```text
Observador / Relator
```

puede documentar hipótesis y descubrimientos.

---

# 23. Información que NO debemos dar al inicio

No entregar inmediatamente:

```text
diagrama completo
nombres de todos los servicios
estructura exacta
credenciales de DB administrativa
respuesta de las misiones
lista de endpoints completa
solución del incidente
```

El objetivo es que la arquitectura sea descubierta.

---

# 24. Información que SÍ deben tener

Los integrantes necesitan:

```text
cómo entrar
qué pueden tocar
qué no pueden tocar
qué hacer si se pierden
qué herramientas tienen
credenciales exclusivamente de laboratorio
cómo pedir una pista
```

---

# 25. Nivel técnico objetivo

La clase debe funcionar para integrantes que:

```text
saben algo de programación
o
tienen poca experiencia con servidores
o
nunca han usado PostgreSQL
o
nunca han abierto Network
```

No debe depender de conocimientos avanzados previos.

---

# 26. Regla de complejidad

Cada misión debe introducir **como máximo un concepto principal nuevo**.

Ejemplo correcto:

```text
Misión 1 → Network
Misión 2 → API
Misión 3 → DB
Misión 5 → servicios
```

Evitar una misión que requiera simultáneamente:

```text
Docker
SQL
DNS
HTTP
Linux
JWT
```

sin preparación previa.

---

# 27. Diseño de evidencias

Cada misión debe terminar con una evidencia simple.

Tipos:

```text
respuesta escrita
captura
valor encontrado
URL
status HTTP
consulta ejecutada
dato modificado
hipótesis del fallo
diagrama
```

No se calificará formalmente.

La evidencia sirve para comprobar que el equipo descubrió la pieza esperada.

---

# 28. Formato estándar de una misión

Cada misión del documento final tendrá:

```text
ID
Nombre
Objetivo
Narrativa
Tiempo objetivo
Rol principal
Roles secundarios
Herramientas
Punto de partida
Tarea
Restricciones
Descubrimiento esperado
Evidencia
Pista 1
Pista 2
Pista 3
Error frecuente
Extensión para equipos rápidos
Condición de salida
```

---

# 29. Extensiones para equipos rápidos

Cada misión debe tener un reto opcional.

Ejemplos:

```text
¿Puedes encontrar otro endpoint?
¿Puedes averiguar cuánto tarda la petición?
¿Qué pasa si consultas un ID inexistente?
¿Qué código HTTP obtienes?
¿Qué tabla crees que utiliza este endpoint?
```

Esto evita que los equipos avanzados queden esperando.

---

# 30. Plan B para equipos bloqueados

Si un equipo se retrasa demasiado:

```text
Pista 1
 ↓
Pista 2
 ↓
Pista 3
 ↓
Instructor desbloquea
```

El objetivo es evitar que una sola misión consuma toda la sesión.

Tiempo máximo recomendado por bloqueo:

```text
5–7 minutos
```

antes de aumentar el nivel de ayuda.

---

# 31. Plan B si falla infraestructura

El diseño pedagógico debe sobrevivir a problemas técnicos.

Preparar alternativas:

```text
API real falla
→ respuesta JSON preparada

DB no accesible
→ terminal de demostración / snapshot

entorno de un equipo roto
→ reset inmediato

Internet falla
→ operación LAN

Tailscale falla
→ acceso local alternativo
```

La implementación técnica de estos mecanismos pertenece a fases posteriores.

---

# 32. Qué NO debe incluir ClubLab #01
Para evitar sobrecarga, la primera sesión no profundizará en:

```text
JWT internals
OAuth
TLS
CI/CD
Kubernetes
SQL avanzado
ORM profundo
inyección SQL
XSS
CSRF
WebSockets
colas
caching
microservicios
```

Pueden mencionarse como caminos futuros.

---

# 33. Conexiones con futuros ClubLab

La primera clase debe dejar “puertas abiertas”.

Ejemplos:

```text
HTTP
→ ClubLab de redes

login
→ ClubLab de autenticación

DevTools
→ ClubLab de frontend

SQL
→ ClubLab de bases de datos

logs
→ ClubLab de DevOps

endpoint manipulable
→ ClubLab de ciberseguridad

WebSockets
→ ClubLab de tiempo real
```

---

# 34. Subfases de trabajo de Fase 1

---

## Subfase 1.1 — Perfil de participantes

Definir:

```text
cantidad aproximada
nivel promedio
mínimo esperado
máximo esperado
equipos
dispositivos disponibles
```

### Resultado

`P01_Perfil_Participantes`

---

## Subfase 1.2 — Objetivos de descubrimiento

Cerrar exactamente:

```text
qué deben entender
qué no necesitan memorizar
qué conceptos solo se mencionan
```

### Resultado

`P02_Resultados_Aprendizaje`

---

## Subfase 1.3 — Narrativa

Definir:

```text
contexto
tono
situación inicial
incidente
cierre
```

### Resultado

`P03_Narrativa_ClubLab01`

---

## Subfase 1.4 — Catálogo de misiones

Diseñar todas las misiones.

Para cada una:

```text
objetivo
tiempo
herramienta
descubrimiento
evidencia
pistas
extensión
```

### Resultado

`P04_Misiones_v1`

---

## Subfase 1.5 — Flujo de dos horas

Construir cronograma real.

### Resultado

`P05_Cronograma_120min`

---

## Subfase 1.6 — Diseño de roles

Cerrar responsabilidades y rotación.

### Resultado

`P06_Roles_v1`

---

## Subfase 1.7 — Diseño del incidente

Seleccionar:

```text
componente que falla
señales visibles
logs
status
pistas
recuperación
```

### Resultado

`P07_Incidente_Principal`

---

## Subfase 1.8 — Escalado de dificultad

Definir:

```text
pista 1
pista 2
pista 3
extensión avanzada
```

para cada misión.

### Resultado

`P08_Matriz_Dificultad`

---

## Subfase 1.9 — Evidencias

Definir cómo sabremos que una misión fue comprendida.

### Resultado

`P09_Evidencias`

---

## Subfase 1.10 — Planes alternativos

Diseñar:

```text
plan B técnico
plan B pedagógico
equipo lento
equipo rápido
fallo total
```

### Resultado

`P10_Contingencias`

---

## Subfase 1.11 — Simulación de la experiencia

Ejecutar la sesión en papel.

Preguntas:

```text
¿hay tiempos muertos?
¿hay demasiadas explicaciones?
¿alguna misión depende de algo no descubierto?
¿un principiante puede seguirla?
¿un avanzado se aburrirá?
```

### Resultado

`P11_Revisión_Pedagógica`

---

## Subfase 1.12 — Documento final

Consolidar todo en:

```text
D01_Diseno_Experiencia_ClubLab_01.md
```

---

# 35. Estructura del entregable D01

```text
1. Propósito
2. Público
3. Resultados esperados
4. Principios pedagógicos
5. Narrativa
6. Arquitectura que se descubrirá
7. Roles
8. Misiones
9. Incidente
10. Cronograma
11. Pistas
12. Extensiones
13. Evidencias
14. Planes B
15. Cierre
16. Criterios de éxito
```

---

# 36. Criterios de éxito de Fase 1

La fase está terminada cuando:

- [ ] sabemos exactamente qué debe descubrir un integrante;
- [ ] todas las misiones tienen objetivo;
- [ ] todas las misiones caben en 120 minutos;
- [ ] cada misión introduce pocos conceptos;
- [ ] existe un incidente principal;
- [ ] existen pistas escalonadas;
- [ ] existen extensiones para equipos rápidos;
- [ ] existe estrategia para equipos lentos;
- [ ] los roles están definidos;
- [ ] la arquitectura no se revela demasiado pronto;
- [ ] existe una evidencia simple por misión;
- [ ] existe plan B técnico;
- [ ] existe plan B pedagógico;
- [ ] la sesión tiene principio, desarrollo, incidente y cierre;
- [ ] el documento D01 está completo.

---

# 37. Decisiones que NO corresponden todavía a esta fase

No cerrar aún:

```text
subred exacta
puertos exactos
docker-compose final
estructura exacta de contenedores
Caddy definitivo
Tailscale definitivo
esquema SQL final
UI final
código final
Scenario Manager final
```

Estas decisiones pertenecen principalmente a:

```text
Fase 2
Fase 3
Fase 4
Fase 5
```

---

# 38. Dependencias hacia fases posteriores

Fase 1 entregará requisitos a:

```text
Fase 2 — Arquitectura
    “necesitamos estas interacciones”

Fase 3 — Seguridad
    “estos son los permisos que requiere cada rol”

Fase 4 — Aplicación
    “estas vistas y datos son necesarios”

Fase 5 — Escenarios
    “este fallo debe poder provocarse”

Fase 6 — Roles
    “estas son las responsabilidades reales”

Fase 7 — Material alumno
    “estas son las herramientas y pistas”

Fase 8 — Instructor
    “este es el recorrido exacto”
```

---

# 39. Flujo completo de la Fase 1

```text
PERFIL
  ↓
OBJETIVOS
  ↓
NARRATIVA
  ↓
MISIONES
  ↓
ROLES
  ↓
INCIDENTE
  ↓
PISTAS
  ↓
CRONOGRAMA
  ↓
CONTINGENCIAS
  ↓
SIMULACIÓN
  ↓
D01 FINAL
```

---

# 40. Orden recomendado de ejecución

Para desarrollar Fase 1 sin mezclar decisiones:

```text
BLOQUE A
Perfil + objetivos

BLOQUE B
Narrativa + arquitectura a descubrir

BLOQUE C
Misiones

BLOQUE D
Roles + rotación

BLOQUE E
Incidente principal

BLOQUE F
Pistas + extensiones + evidencias

BLOQUE G
Cronograma de 120 min

BLOQUE H
Contingencias + simulación

BLOQUE I
Consolidación D01
```

---

# 41. Primer bloque a desarrollar

La ejecución formal de Fase 1 debe comenzar por:

# BLOQUE A — Perfil + objetivos

Antes de cerrar las misiones necesitamos definir:

```text
cantidad aproximada de integrantes
cantidad de equipos
nivel técnico mínimo
nivel técnico promedio
si llevan laptop propia
si todos tendrán navegador
si todos tendrán terminal
si trabajarán individualmente o por equipo
```

Con eso se podrá cerrar:

```text
duración por misión
número de roles
cantidad de entornos
nivel de dificultad
cantidad de pistas
```

---

# 42. Resultado final esperado

Al terminar la Fase 1 tendremos un diseño suficientemente preciso como para decir:

> **“Ahora sabemos exactamente qué experiencia debemos construir.”**

Solo entonces la Fase 2 transformará esa experiencia en una arquitectura técnica.