# ClubLab — Fase 1 / Bloque C
## Catálogo de misiones de ClubLab #01

**Proyecto:** ClubLab v1  
**Experiencia:** ClubLab #01 — *Desarmando una aplicación*  
**Fase:** 1 — Diseño pedagógico  
**Bloque:** C  
**Dependencias:** Bloque A + Bloque B  
**Estado:** CERRADO PARA DISEÑO v1  
**Entregable principal:** `P04_Misiones_v1`

---

# 1. Propósito del Bloque C

Este bloque convierte la narrativa definida anteriormente en una secuencia concreta de actividades.

La misión de ClubLab #01 no es enseñar herramientas aisladas.

Cada misión debe provocar una pregunta y hacer que el integrante utilice una herramienta porque la necesita para responderla.

La secuencia pedagógica será:

```text
USAR
  ↓
OBSERVAR
  ↓
INVESTIGAR
  ↓
DESCUBRIR
  ↓
CONECTAR
  ↓
DIAGNOSTICAR
  ↓
RECONSTRUIR
```

---

# 2. Catálogo final de misiones

ClubLab #01 tendrá nueve misiones:

```text
M0 — Reconocimiento
M1 — ¿De dónde vienen los datos?
M2 — Habla con la API
M3 — Encuentra dónde viven los datos
M4 — Cambia el sistema
M5 — ¿Dónde se está ejecutando?
M6 — Algo se rompió
M7 — Diagnostica y recupera
M8 — Reconstruye la arquitectura
```

---

# 3. Reglas generales de diseño

Todas las misiones deben cumplir:

```text
1. Tener una pregunta clara.
2. Introducir como máximo un concepto principal nuevo.
3. Producir evidencia observable.
4. Poder completarse sin conocimiento avanzado.
5. Tener tres niveles de pista.
6. Tener extensión opcional.
7. Tener tiempo máximo.
8. No requerir acceso al host Tulum.
9. No depender de memorizar sintaxis.
10. Terminar con una breve reflexión:
    “¿Qué acabamos de descubrir?”
```

---

# 4. Estructura estándar de misión

Cada misión utiliza:

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
Extensión avanzada
Condición de salida
```

---

# 5. M0 — Reconocimiento

## Nombre

**Explora ClubLab**

## Objetivo

Familiarizar al equipo con la aplicación antes de introducir conceptos técnicos.

## Narrativa

> “Esta aplicación ya está funcionando. Antes de investigar cómo está hecha, conozcan qué hace.”

## Tiempo objetivo

```text
5–7 minutos
```

## Rol principal

```text
Explorador de Interfaz
```

## Roles secundarios

```text
Todos
```

## Herramientas

```text
Navegador
```

## Punto de partida

El equipo recibe:

```text
URL
usuario de laboratorio
contraseña de laboratorio
nombre/número de equipo
```

## Tarea

Localizar:

```text
perfil
equipo
ranking
misiones
actividad
```

Y responder:

```text
¿Cuántos puntos tiene su equipo?
¿Qué posición ocupa?
¿Cuántas misiones están disponibles?
¿Qué dato les parece más interesante investigar?
```

## Restricciones

No abrir todavía terminal ni herramientas especiales.

No se menciona DevTools.

## Descubrimiento esperado

La aplicación muestra distintos datos relacionados entre sí.

Todavía se percibe como una sola “caja”.

## Evidencia

Registrar:

```text
puntos del equipo
posición
una misión visible
un dato que quieran investigar
```

## Pista 1

> “Recorran todas las secciones disponibles.”

## Pista 2

> “El dashboard no contiene toda la información.”

## Pista 3

> “Entren a Ranking, Misiones, Equipo y Actividad.”

## Error frecuente

Querer inspeccionar código inmediatamente.

Respuesta del instructor:

> “Primero entiendan qué hace. Después veremos cómo.”

## Extensión avanzada

Encontrar:

```text
un dato repetido en dos pantallas
o
una relación entre ranking y actividad
```

## Condición de salida

El equipo conoce la aplicación y ha identificado al menos un dato que le genera curiosidad.

---

# 6. M1 — ¿De dónde vienen los datos?

## Nombre

**Sigue la pista del ranking**

## Objetivo

Descubrir que la interfaz realiza peticiones y que el navegador permite observarlas.

## Narrativa

El instructor plantea:

> “Su equipo tiene 320 puntos. ¿De dónde salió ese número?”

Si responden “de la base de datos”:

> “¿Cómo lo saben?”

## Tiempo objetivo

```text
8–10 minutos
```

## Rol principal

```text
Explorador de Interfaz
```

## Roles secundarios

```text
Investigador de API
Relator
```

## Herramientas

```text
Navegador
DevTools
Network
Fetch/XHR
```

## Punto de partida

ClubLab funcionando correctamente.

## Tarea

Encontrar qué ocurre cuando se abre o recarga el ranking.

Identificar una petición relacionada con el ranking.

## Restricciones

No consultar todavía la API con terminal.

No revelar la lista completa de endpoints.

## Descubrimiento esperado

El navegador hace una solicitud parecida a:

```http
GET /api/ranking
```

y recibe una respuesta.

## Evidencia

Registrar:

```text
método
URL o path
status HTTP
uno de los datos presentes en la respuesta
```

Ejemplo:

```text
GET
/api/ranking
200
score: 320
```

## Pista 1

> “¿Puede el navegador mostrar qué está ocurriendo cuando cambia la pantalla?”

## Pista 2

> “Busquen una herramienta que permita observar tráfico o peticiones.”

## Pista 3

> “F12 → Network → Fetch/XHR → recarguen Ranking.”

## Error frecuente

Mirar únicamente Console.

Respuesta del instructor:

> “Console muestra mensajes. ¿Dónde observarías las solicitudes?”

## Extensión avanzada

Comparar dos endpoints y responder:

```text
¿Cuál tarda más?
¿Qué código HTTP devuelve cada uno?
¿Qué cambia en Response?
```

## Condición de salida

El equipo demuestra que el dato de ranking llega mediante una petición observable.

---

# 7. M2 — Habla con la API

## Nombre

**Quita la interfaz del camino**

## Objetivo

Comprender que la API existe independientemente de la interfaz.

## Narrativa

> “Ya saben que el navegador está pidiendo datos. ¿Pueden pedirlos ustedes directamente?”

## Tiempo objetivo

```text
8–10 minutos
```

## Rol principal

```text
Investigador de API
```

## Roles secundarios

```text
Explorador de Interfaz
Relator
```

## Herramientas

```text
terminal de laboratorio
curl
navegador
JSON
```

## Punto de partida

El equipo conoce el endpoint descubierto en M1.

## Tarea

Consultar directamente el endpoint.

Ejemplo pedagógico:

```bash
curl http://api/ranking
```

La URL real dependerá de la arquitectura técnica final.

Luego identificar:

```text
qué estructura devuelve;
qué campo corresponde al equipo;
qué valor coincide con la interfaz.
```

## Restricciones

No enseñar todavía todos los endpoints.

No introducir autenticación compleja en esta misión.

## Descubrimiento esperado

La API devuelve información aunque no se utilice el frontend.

## Evidencia

Guardar:

```text
endpoint consultado
status
fragmento de JSON relevante
dato que coincide con la interfaz
```

## Pista 1

> “Si el navegador puede pedir esa información, ustedes también deberían poder.”

## Pista 2

> “Utilicen la URL que encontraron antes, pero desde la terminal.”

## Pista 3

> “Usen curl contra el endpoint del ranking.”

## Error frecuente

Copiar la URL del frontend en vez del endpoint API.

Respuesta del instructor:

> “¿La petición que encontraron iba exactamente a esa dirección?”

## Extensión avanzada

Probar:

```text
un ID válido
un ID inexistente
```

y comparar:

```text
200
404
```

## Condición de salida

El equipo obtiene datos directamente de la API y puede explicar que el frontend no es la única forma de consultarla.

---

# 8. M3 — Encuentra dónde viven los datos

## Nombre

**Rastrea el dato hasta su origen**

## Objetivo

Descubrir persistencia y relacionar la API con PostgreSQL.

## Narrativa

> “Ya sabemos quién entrega el dato. Ahora falta una pregunta: ¿dónde vive?”

## Tiempo objetivo

```text
10–12 minutos
```

## Rol principal

```text
Investigador de Datos
```

## Roles secundarios

```text
Investigador de API
Relator
```

## Herramientas

```text
terminal aislada
psql
SQL básico
```

## Punto de partida

El equipo conoce:

```text
dato visible
dato en JSON
```

## Tarea

Entrar a una base ClubLab con credenciales limitadas.

Comandos de apoyo permitidos:

```text
\dt
\d nombre_tabla
SELECT ...
```

Localizar el registro relacionado con:

```text
equipo
usuario
score
```

## Restricciones

No usar:

```text
DROP
TRUNCATE
ALTER
DELETE masivo
roles administrativos
```

La cuenta debe limitar técnicamente estas acciones.

## Descubrimiento esperado

El mismo dato aparece:

```text
UI
→ JSON
→ fila de PostgreSQL
```

## Evidencia

Registrar:

```text
tabla
columna
valor
identificador relacionado
```

Ejemplo:

```text
team_scores
score
320
team_id = 3
```

## Pista 1

> “¿Qué sistema podría guardar información aunque cierres el navegador?”

## Pista 2

> “La terminal tiene acceso a una base preparada para ustedes.”

## Pista 3

> “Entren a psql, usen \dt y busquen una tabla relacionada con equipos o puntos.”

## Error frecuente

Buscar exactamente una tabla llamada `ranking`.

Respuesta del instructor:

> “El nombre de la pantalla no tiene por qué ser el nombre de una tabla.”

## Extensión avanzada

Encontrar una relación entre dos tablas.

Ejemplo:

```text
teams
scores
```

## Condición de salida

El equipo localiza en PostgreSQL el dato que vio primero en la interfaz.

---

# 9. M4 — Cambia el sistema

## Nombre

**Haz que la interfaz cambie desde los datos**

## Objetivo

Conectar PostgreSQL → backend → API → frontend.

## Narrativa

> “Si ese dato realmente viene de la base, entonces debería ser posible cambiarlo desde su origen.”

## Tiempo objetivo

```text
10–12 minutos
```

## Rol principal

```text
Investigador de Datos
```

## Roles secundarios

```text
Investigador de API
Explorador de Interfaz
```

## Herramientas

```text
psql
curl
navegador
```

## Punto de partida

Dato localizado en M3.

## Tarea

Modificar un campo específicamente autorizado.

Ejemplo:

```sql
UPDATE team_scores
SET score = 340
WHERE team_id = 3;
```

Luego:

```text
1. consultar API;
2. recargar frontend;
3. comprobar cambio.
```

## Restricciones

Solo modificar:

```text
su propio equipo
campos autorizados
valores dentro del rango indicado
```

No modificar IDs ni relaciones.

## Descubrimiento esperado

La cadena queda visible:

```text
PostgreSQL
   ↓
Backend
   ↓
API
   ↓
Frontend
```

## Evidencia

Registrar:

```text
valor anterior
valor nuevo
respuesta API
valor final en UI
```

## Pista 1

> “Ya encontraron dónde está almacenado.”

## Pista 2

> “¿Qué pasaría si cambian únicamente ese registro?”

## Pista 3

> “Ejecuten el UPDATE indicado para su team_id y luego consulten otra vez la API.”

## Error frecuente

Cambiar el dato y no refrescar la petición.

Respuesta:

> “¿Cómo saben que el frontend volvió a pedir la información?”

## Extensión avanzada

Predecir antes de refrescar:

```text
qué cambiará
qué no cambiará
```

y comprobarlo.

## Condición de salida

El equipo demuestra un cambio de extremo a extremo desde la BD hasta la interfaz.

---

# 10. M5 — ¿Dónde se está ejecutando?

## Nombre

**Encuentra las piezas**

## Objetivo

Descubrir que frontend, API y base de datos son servicios separados.

## Narrativa

> “Ya encontraron tres partes del sistema. ¿Son realmente tres cosas distintas o todo es un solo programa?”

## Tiempo objetivo

```text
8–10 minutos
```

## Rol principal

```text
Operador de Sistemas
```

## Roles secundarios

```text
Todos
```

## Herramientas

La implementación técnica deberá ofrecer una vista segura del estado del equipo.

Puede ser:

```text
comando clublab status
panel técnico
terminal toolbox
health endpoint
```

No Docker directo del host.

## Punto de partida

El equipo ya conoce:

```text
frontend
API
database
```

## Tarea

Identificar los servicios existentes del entorno del equipo.

Ejemplo conceptual:

```text
frontend   running
api        running
database   running
toolbox    running
```

Comprobar al menos un healthcheck.

## Restricciones

No usar:

```text
docker ps del host
docker socket
sudo
systemctl del host
```

## Descubrimiento esperado

Cada componente puede tener:

```text
estado
logs
salud
ciclo de vida
```

independiente.

Aquí se introduce por primera vez el concepto de contenedor/Docker.

## Evidencia

Registrar:

```text
nombres de 3 servicios
estado
un healthcheck correcto
```

## Pista 1

> “Si son partes distintas, debería existir alguna forma de verlas por separado.”

## Pista 2

> “Utilicen la herramienta de estado del laboratorio.”

## Pista 3

> “Ejecuten `clublab status` o la alternativa definida.”

## Error frecuente

Confundir “servidor” con “backend”.

Respuesta:

> “El backend es un servicio. El servidor es la infraestructura donde puede ejecutarse.”

## Extensión avanzada

Relacionar:

```text
servicio
puerto interno
healthcheck
```

sin necesidad de entrar en redes Docker.

## Condición de salida

El equipo entiende que la aplicación está compuesta por servicios separados.

---

# 11. Punto de control antes del incidente

Antes de continuar, el instructor debe pedir al equipo que complete temporalmente:

```text
Navegador
   ↓
Frontend
   ↓
________
   ↓
________
```

Respuesta esperada:

```text
API / Backend
Database
```

No introducir todavía el fallo.

Tiempo máximo:

```text
2–3 minutos
```

---

# 12. M6 — Algo se rompió

## Nombre

**Incidente: el ranking dejó de funcionar**

## Objetivo

Provocar un cambio de modo mental:

```text
exploración
→
diagnóstico
```

## Narrativa

El instructor activa el escenario.

Mensaje visible:

> **INCIDENTE 01**
>
> El ranking dejó de cargar correctamente.
>
> El resto de la aplicación parece seguir disponible.
>
> No reinicien cosas al azar.
>
> Encuentren evidencia.

## Tiempo objetivo

```text
5–7 minutos de observación inicial
```
## Rol principal

```text
Explorador de Interfaz
```

## Roles secundarios

```text
Todos
```

## Herramientas

```text
navegador
DevTools
Network
```

## Punto de partida

El equipo acaba de comprobar que todo funcionaba.

## Tarea

Sin reparar nada todavía:

```text
1. reproducir el fallo;
2. identificar qué funciona;
3. identificar qué no funciona;
4. observar la petición fallida;
5. registrar status/respuesta.
```

## Restricciones

No ejecutar recuperación todavía.

No detener/arrancar servicios.

## Descubrimiento esperado

Un fallo localizado no implica que toda la aplicación esté caída.

## Evidencia

Completar:

```text
Frontend carga:      sí/no
Ranking carga:       sí/no
API health:          sí/no
Ranking endpoint:    status
Error observado:     ...
```

## Pista 1

> “Antes de tocar nada, ¿qué sigue funcionando?”

## Pista 2

> “Comparen una petición que funciona con la que falla.”

## Pista 3

> “Miren Network y prueben también `/api/health`.”

## Error frecuente

Ir directamente al botón de reiniciar.

Respuesta:

> “Todavía no sabemos qué componente falló. Primero demuéstrenlo.”

## Extensión avanzada

Construir una pequeña tabla:

```text
componente
evidencia a favor
evidencia en contra
```

## Condición de salida

El equipo tiene una hipótesis inicial basada en síntomas observables.

---

# 13. M7 — Diagnostica y recupera

## Nombre

**Encuentra al responsable**

## Objetivo

Utilizar evidencia de varias capas para localizar la causa del incidente y restaurar el servicio.

## Narrativa

> “Ya saben cómo se ve el problema desde el usuario. Ahora sigan la cadena hasta encontrar dónde se rompe.”

## Tiempo objetivo

```text
20–25 minutos
```

## Rol principal

```text
Operador de Sistemas
```

## Roles secundarios

```text
Investigador de API
Investigador de Datos
Explorador de Interfaz
```

Esta es la misión principal de trabajo en equipo.

## Herramientas

Dependiendo del escenario:

```text
curl
DevTools
healthchecks
logs
psql
clublab status
clublab logs
comando de recuperación controlado
```

## Punto de partida

Hipótesis de M6.

## Tarea

Investigar en orden libre.

El equipo debe obtener evidencia de al menos dos fuentes.

Ejemplo:

```text
Network
+
logs
```

o:

```text
API
+
DB
```

Después debe responder:

```text
¿Qué componente falló?
¿Qué evidencia lo demuestra?
¿Qué componentes descartaron?
¿Qué acción mínima lo recupera?
```

Finalmente ejecuta la recuperación permitida.

## Restricciones

No se permite:

```text
reset total como primera acción
reiniciar todos los servicios
borrar datos
editar infraestructura ajena al equipo
```

La recuperación debe ser específica.

## Descubrimiento esperado

Diagnosticar significa aislar un fallo usando evidencia, no probar acciones al azar.

## Evidencia

Formato obligatorio:

```text
Síntoma:
Hipótesis:
Evidencia 1:
Evidencia 2:
Componente responsable:
Acción tomada:
Resultado:
```

## Pista 1

> “Sigan el camino del dato. ¿Hasta qué punto funciona?”

## Pista 2

> “Comparen estado, API, base y logs. Una de esas capas debería dar una señal distinta.”

## Pista 3

La pista concreta dependerá del escenario final.

Ejemplo si el fallo es DB:

> “El API está vivo, pero revisen qué dice cuando intenta consultar el ranking.”

## Error frecuente

Concluir que “el backend está caído” solo porque el endpoint devuelve 500.

Respuesta:

> “Un 500 demuestra que el backend recibió la petición. ¿Qué podría estar fallando detrás?”

## Extensión avanzada

Explicar:

```text
por qué el frontend seguía funcionando;
por qué el healthcheck podía responder;
por qué solo una funcionalidad fallaba.
```

## Condición de salida

El equipo:

```text
identifica la causa;
justifica con evidencia;
ejecuta recuperación;
comprueba que el ranking vuelve.
```

---

# 14. Escenario recomendado para M6/M7

Para la primera edición se recomienda:

# **Backend operativo + conexión a base de datos del ranking rota**

Ejemplo técnico futuro:

```text
frontend = UP
api = UP
/api/health = 200
/api/ranking = 500
database = UP o inaccesible para API por configuración controlada
```

Razón pedagógica:

```text
no todo está caído;
el backend responde;
el error obliga a pensar en dependencias;
Network ayuda;
logs ayudan;
la DB ya fue descubierta;
la recuperación puede ser específica.
```

No se cierra todavía la implementación exacta; pertenece a Fase 5.

---

# 15. Alternativa de incidente simplificada

Si la prueba piloto demuestra que el escenario anterior es demasiado difícil:

```text
API completamente detenida
```

Resultado:

```text
frontend = UP
api = DOWN
database = UP
```

Es más fácil de diagnosticar, pero pedagógicamente menos interesante.

Se conservará como:

```text
PLAN B DEL INCIDENTE
```

---

# 16. M8 — Reconstruye la arquitectura

## Nombre

**Dibuja lo que acabas de descubrir**

## Objetivo

Transformar la experiencia en un modelo mental explícito.

## Narrativa

> “Hace dos horas esto era una sola aplicación. Dibujen ahora todas las piezas que saben que existen.”

## Tiempo objetivo

```text
12–15 minutos
```

## Rol principal

```text
Todo el equipo
```

## Herramientas

```text
hoja
pizarra
plantilla
diagrama incompleto
```

No terminal.

## Punto de partida

Todas las misiones anteriores completadas.

## Tarea

Completar el diagrama.

Debe incluir al menos:

```text
navegador
frontend
API/backend
base de datos
servidor
contenedores/Docker
```

Añadir flechas de comunicación.

Después responder:

```text
¿Qué pasó cuando el ranking falló?
¿Qué parte seguía funcionando?
¿Qué evidencia permitió localizar el problema?
```

## Restricciones

No copiar el diagrama del instructor.

No evaluar estética.

## Descubrimiento esperado

La aplicación deja de percibirse como un único bloque.

## Evidencia

```text
diagrama final del equipo
+
explicación oral de 60–90 segundos
```

## Pista 1

> “Empiecen por ustedes: ¿qué utilizaron primero?”

## Pista 2

> “Sigan el recorrido del dato de ranking.”

## Pista 3

> “Navegador → Frontend → API/Backend → Base de datos. Ahora agreguen dónde se ejecutan.”

## Error frecuente

Poner Docker entre frontend y backend como si fuera protocolo.

Respuesta:

> “Docker no es el mensaje que viaja entre ellos. ¿Qué función cumplía?”

## Extensión avanzada

Añadir correctamente:

```text
HTTP
JSON
logs
healthcheck
puertos
red
```

sin convertirlo en requisito.

## Condición de salida

El equipo explica correctamente el recorrido del dato y el fallo.

---

# 17. Tiempo total de misiones

Propuesta inicial:

| Misión | Tiempo |
|---|---:|
| M0 | 5–7 min |
| M1 | 8–10 min |
| M2 | 8–10 min |
| M3 | 10–12 min |
| M4 | 10–12 min |
| M5 | 8–10 min |
| Punto de control | 2–3 min |
| M6 | 5–7 min |
| M7 | 20–25 min |
| M8 | 12–15 min |

Rango total de actividad:

```text
88–111 minutos
```

El cronograma final reservará además:

```text
bienvenida
transiciones
explicaciones breves
cierre
```

por lo que en el Bloque G se ajustará todo a exactamente 120 minutos.

---

# 18. Dependencias entre misiones

```text
M0
 ↓
M1
 ↓
M2
 ↓
M3
 ↓
M4
 ↓
M5
 ↓
M6
 ↓
M7
 ↓
M8
```

No deben saltarse:

```text
M1 antes de M2
M3 antes de M4
M5 antes del incidente
```

porque cada una prepara el modelo mental de la siguiente.

---

# 19. Mapa de conceptos por misión

| Misión | Concepto principal |
|---|---|
| M0 | Sistema visible |
| M1 | Request / Network |
| M2 | API |
| M3 | Persistencia / DB |
| M4 | Flujo completo de datos |
| M5 | Servicios / contenedores |
| M6 | Síntoma vs componente |
| M7 | Diagnóstico con evidencia |
| M8 | Arquitectura |

---

# 20. Mapa de herramientas

| Herramienta | Primera aparición |
|---|---|
| Navegador | M0 |
| DevTools Network | M1 |
| curl | M2 |
| psql | M3 |
| UPDATE controlado | M4 |
| status/health | M5 |
| logs | M7 |
| diagrama | M8 |

Esto evita enseñar todas las herramientas al inicio.

---

# 21. Reglas de pistas

El instructor seguirá:

```text
P0 — esperar
P1 — pregunta conceptual
P2 — dirección
P3 — instrucción concreta
P4 — desbloqueo
```

No entregar P3 inmediatamente.

Tiempo sugerido:

```text
2–3 min sin avance
→ P1

2–3 min adicionales
→ P2

2 min adicionales
→ P3
```

Ajustar según grupo.

---

# 22. Evidencias totales del equipo

Al final el equipo habrá producido:

```text
E0 datos de reconocimiento
E1 request encontrada
E2 respuesta API
E3 registro SQL
E4 cambio extremo a extremo
E5 mapa de servicios
E6 síntomas del incidente
E7 diagnóstico y recuperación
E8 arquitectura final
```

Estas evidencias servirán posteriormente para el Cuaderno de Misiones.

---

# 23. Lo que NO se calificará

No se evaluará:

```text
velocidad
cantidad de comandos memorizados
calidad estética del diagrama
conocimiento previo
cantidad de términos técnicos usados
```

Se valorará:

```text
evidencia
razonamiento
comunicación
comprensión
```

---

# 24. Comportamiento esperado del instructor

Durante una misión:

```text
NO resolver
NO tomar el teclado salvo bloqueo total
NO revelar la siguiente capa
NO adelantar la solución del incidente
```

Sí:

```text
preguntar
observar
pedir evidencia
dar pistas progresivas
controlar tiempo
```

---

# 25. Reglas para equipos avanzados

Los retos avanzados nunca deben:

```text
alterar datos de otro equipo
tocar infraestructura
adelantar incidentes
requerir permisos extra
```

Deben ser de investigación.

---

# 26. Reglas para equipos principiantes

El camino mínimo debe poder completarse copiando comandos sencillos desde su guía.

Ejemplo:

```bash
curl <URL>
```

y:

```sql
SELECT ...
```

La dificultad debe estar en interpretar qué significa el resultado, no en recordar sintaxis.

---

# 27. Señales de que una misión está mal diseñada

Durante ensayo, revisar si:

```text
todos preguntan qué comando escribir;
nadie entiende por qué hace algo;
hay más explicación que investigación;
una sola persona monopoliza teclado;
se requiere conocimiento no introducido;
la solución depende de adivinar;
el resultado no es visible;
la misión tarda más de 15 min salvo M7.
```

Si ocurre, rediseñar.

---

# 28. Criterios de éxito del catálogo

El catálogo es válido si:

```text
cada misión responde una pregunta;
cada misión prepara la siguiente;
el incidente usa conocimientos ya descubiertos;
hay evidencia en cada etapa;
el principiante puede avanzar;
el avanzado tiene extensiones;
el flujo completo cabe en 2 horas;
```

---

# 29. Decisiones cerradas en Bloque C

### DC-01
ClubLab #01 tendrá **9 misiones**.

### DC-02
La progresión será:

```text
UI → Network → API → DB → cambio → servicios → incidente → diagnóstico → arquitectura
```

### DC-03
La primera modificación real será sobre datos controlados del propio equipo.

### DC-04
La introducción de Docker será indirecta y posterior a comprender las capas.

### DC-05
El incidente principal recomendado será:

```text
API viva + problema de acceso a datos del ranking
```

### DC-06
Existirá un incidente simplificado como plan B.

### DC-07
El diagnóstico exigirá al menos dos fuentes de evidencia.

### DC-08
No se permitirá “reiniciar todo” como primera respuesta.

### DC-09
M8 incluirá explicación oral breve, no solo diagrama.

### DC-10
Las evidencias de estas misiones serán la base del futuro Cuaderno de Misiones.

---

# 30. Entregables del Bloque C

Este bloque produce:

```text
P04_Misiones_v1
P04A_Matriz_Conceptos
P04B_Matriz_Herramientas
P04C_Evidencias_Misiones
P04D_Incidente_Recomendado
```

---

# 31. Criterios de aceptación

- [x] M0 diseñada.
- [x] M1 diseñada.
- [x] M2 diseñada.
- [x] M3 diseñada.
- [x] M4 diseñada.
- [x] M5 diseñada.
- [x] M6 diseñada.
- [x] M7 diseñada.
- [x] M8 diseñada.
- [x] Cada misión tiene objetivo.
- [x] Cada misión tiene tiempo.
- [x] Cada misión tiene rol.
- [x] Cada misión tiene herramientas.
- [x] Cada misión tiene evidencia.
- [x] Cada misión tiene tres pistas.
- [x] Cada misión tiene extensión avanzada.
- [x] Incidente principal definido conceptualmente.
- [x] Plan B del incidente definido.
- [x] Dependencias entre misiones definidas.
- [x] Flujo completo pedagógicamente coherente.

# BLOQUE C — COMPLETADO

---

# 32. Siguiente bloque

# BLOQUE D — Roles + rotación

El siguiente bloque deberá convertir los roles preliminares en responsabilidades concretas durante cada misión.

Se definirá:

```text
qué hace cada rol;
qué herramientas utiliza;
qué puede tocar;
qué no puede tocar;
qué evidencia debe aportar;
qué comandos tendrá en su tarjeta;
cómo se reparten las misiones;
cuándo rotan;
cómo funciona un equipo de 3;
cómo funciona uno de 4;
cómo funciona uno de 5;
cómo evitar que una sola persona haga todo.
```

El resultado será la especificación pedagógica que posteriormente se convertirá en las tarjetas de rol de la Fase 6.