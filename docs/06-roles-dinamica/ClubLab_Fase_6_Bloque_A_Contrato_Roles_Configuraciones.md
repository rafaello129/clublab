# ClubLab — Fase 6 / Bloque A
## Contrato final de roles y configuraciones de equipo

**Proyecto:** ClubLab v1  
**Fase:** 6 — Roles y dinámica de equipos  
**Bloque:** A  
**Estado:** CERRADO PARA v1  
**Dependencias:** D01 + D04 + APP04 + Plan de Fase 6  
**Entregables:** P06_Roles_v1 + P06C_Configuraciones_de_Equipo

---

# 1. Propósito

Este bloque toma los roles conceptuales definidos en Fase 1 y los actualiza con las herramientas, endpoints, comandos y límites reales definidos en Fases 4 y 5.

No se crean profesiones ni especialidades permanentes.

Los roles existen para repartir investigación, teclado y evidencia durante ClubLab #01.

Regla principal:

> **Cada integrante investiga una parte distinta, pero el equipo construye una sola explicación.**

---

# 2. Roles oficiales de ClubLab #01

Se congelan cuatro roles base:

~~~text
R1 — Explorador de Interfaz
R2 — Investigador de API
R3 — Investigador de Datos
R4 — Operador de Sistemas
~~~

Rol opcional:

~~~text
R5 — Relator / Analista
~~~

R5 se utiliza principalmente con equipos de cinco integrantes.

---

# 3. Propiedades comunes de todos los roles

Todo rol debe:

~~~text
tener una pregunta principal
usar herramientas concretas
producir evidencia
poder explicarse en menos de un minuto
no requerir privilegios del host
no monopolizar la solución
poder transferirse a otra persona
~~~

Los roles describen responsabilidades temporales.

No significan:

~~~text
“esta persona es frontend”
“esta persona es DBA”
“esta persona es DevOps”
~~~

---

# 4. R1 — Explorador de Interfaz

## Pregunta principal

> **¿Qué está viendo el usuario y qué ocurre cuando interactúa con la aplicación?**

## Objetivo

Observar el sistema desde el navegador y conectar síntomas visuales con requests reales.

## Herramientas

~~~text
Browser
DevTools
Network
Fetch/XHR
Headers
Response
Console básica
~~~

## Acciones permitidas

~~~text
navegar la aplicación
recargar vistas
abrir DevTools
filtrar requests Fetch/XHR
inspeccionar URL, método y status
leer headers y respuestas
comparar estado normal y estado con incidente
~~~

## Acciones prohibidas

~~~text
modificar infraestructura
usar clublabctl
buscar endpoints /internal
usar credenciales administrativas
intentar entrar a otros teams
~~~

## Evidencia mínima

~~~text
pantalla observada
request relevante
método
status
dato o error visible
~~~

## Misiones donde lidera

~~~text
M0 — Reconocimiento
M1 — ¿De dónde vienen los datos?
M6 — observación inicial del incidente
~~~

## Riesgo de comportamiento

Convertirse en la persona que solamente hace clic.

## Mitigación

Debe entregar siempre al menos una evidencia técnica desde Network o Response.

## Preguntas guía

~~~text
¿Qué cambió en pantalla?
¿Qué request corresponde a esa vista?
¿Qué status obtuvo?
¿Qué sigue funcionando?
¿La respuesta contiene el dato que vemos?
~~~

---

# 5. R2 — Investigador de API

## Pregunta principal

> **¿Qué está pidiendo la aplicación y qué responde el backend?**

## Objetivo

Repetir y comparar requests fuera de la interfaz para entender la API como una capa independiente.

## Herramientas

~~~text
curl
HTTP
JSON
/api/health
/api/me
/api/team
/api/ranking
/api/missions
/api/activity
~~~

## Acciones permitidas

~~~text
consultar endpoints públicos de su team
comparar endpoints sanos y fallidos
leer status HTTP
leer JSON
repetir una request encontrada por R1
usar health para comprobar liveness
~~~

## Acciones prohibidas

~~~text
usar /internal/*
usar control token
usar recovery token directamente
consultar otros teams
forzar métodos no necesarios
realizar fuzzing o exploración ofensiva
~~~

## Evidencia mínima

~~~text
URL
método
status
campo JSON relevante
comparación con UI o con otro endpoint
~~~

## Misiones donde lidera

~~~text
M2 — Habla con la API
M7 — comparación funcional de endpoints
~~~

## Riesgo de comportamiento

Copiar un comando sin saber qué demuestra.

## Mitigación

Después de cada request debe responder:

> **¿Qué demuestra esta respuesta?**

## Preguntas guía

~~~text
¿Responde la API?
¿Responde solo este endpoint?
¿Qué status devuelve?
¿Qué JSON coincide con la UI?
¿Qué endpoint sano sirve como comparación?
~~~

---

# 6. R3 — Investigador de Datos

## Pregunta principal

> **¿Dónde vive la información que la aplicación muestra?**

## Objetivo

Relacionar el dato visible con PostgreSQL y comprobar persistencia mediante una modificación controlada.

## Herramientas

~~~text
psql
\dt
\d
SELECT
lab.my_team_score
UPDATE controlado
~~~

## Acciones permitidas

~~~text
conectarse con la credencial student del propio team
listar objetos visibles
consultar datos autorizados
consultar lab.my_team_score
actualizar únicamente score mediante la superficie permitida
comprobar el resultado después del cambio
~~~

## Acciones prohibidas

~~~text
usar usuario app/migrator/owner
crear o borrar tablas
crear roles
cambiar grants
consultar otras bases
usar archivos del servidor
modificar registros fuera de la superficie pedagógica
~~~

## Evidencia mínima

~~~text
objeto consultado
registro local
valor anterior
consulta ejecutada
valor nuevo
~~~

## Misiones donde lidera

~~~text
M3 — Encuentra dónde viven los datos
M4 — Cambia el sistema
~~~

## Regla obligatoria

~~~text
SELECT
→ verificar
→ predecir
→ UPDATE
→ volver a SELECT
→ comprobar API/UI
~~~

## Riesgo de comportamiento

Ejecutar UPDATE antes de confirmar qué registro se está modificando.

## Mitigación

No se ejecuta UPDATE sin mostrar primero el valor actual al equipo.

## Preguntas guía

~~~text
¿Dónde aparece este dato?
¿Es el team correcto?
¿Qué valor tiene antes?
¿Qué esperamos que cambie?
¿La API y la UI reflejan el nuevo valor?
~~~

---

# 7. R4 — Operador de Sistemas

## Pregunta principal

> **¿Qué componentes están funcionando y dónde aparece la evidencia del fallo?**

## Objetivo

Observar estado y logs de forma segura y ejecutar una recuperación específica cuando el diagnóstico esté justificado.

## Herramientas definitivas

~~~bash
clublab whoami
clublab status
clublab health
clublab logs api
clublab recover ranking-db
~~~

Herramientas de apoyo disponibles en toolbox cuando la misión lo requiera:

~~~text
curl
pg_isready
getent
ss
~~~

## Acciones permitidas

~~~text
consultar identidad lógica del team
consultar estado de componentes
consultar health
leer lablogs sanitizados
comparar ranking con health
ejecutar recover ranking-db cuando corresponda
~~~

## Acciones prohibidas

~~~text
usar clublabctl
usar docker
usar sudo
usar systemctl del host
acceder a Tulum directamente
reiniciar todos los servicios
ejecutar reset
ver logs técnicos del instructor
~~~

## Evidencia mínima

~~~text
estado de servicios
resultado de health
estado del ranking
fragmento relevante del lablog
resultado de recover
~~~

## Misiones donde lidera

~~~text
M5 — ¿Dónde se está ejecutando?
M7 — Diagnostica y recupera
~~~

## Riesgo de comportamiento

Intentar solucionar antes de diagnosticar.

## Mitigación

Recovery se considera una acción final, no una herramienta de exploración.

## Preguntas guía

~~~text
¿Qué servicios están vivos?
¿Qué healthcheck sigue sano?
¿Qué endpoint está fallando?
¿Qué dice el lablog?
¿Cuál es la acción mínima para recuperar?
~~~

---

# 8. R5 — Relator / Analista

## Pregunta principal

> **¿Qué sabemos realmente, qué estamos suponiendo y cómo se conecta la evidencia?**

## Objetivo

Mantener una explicación coherente del equipo y evitar que los hallazgos queden aislados.

## Herramientas

~~~text
hoja de evidencia
matriz hipótesis/evidencia
diagrama
línea de tiempo
notas del equipo
~~~

## Acciones permitidas

~~~text
registrar hallazgos
pedir que una afirmación se acompañe de evidencia
actualizar el diagrama
resumir hipótesis
coordinar la explicación final
~~~

## Acciones prohibidas

~~~text
convertirse en observador pasivo
hacer todas las tareas de escritura sin participar
tomar permanentemente el teclado de otro rol
decidir el diagnóstico sin escuchar las otras capas
~~~

## Evidencia mínima

Durante M7 debe mantener:

~~~text
Síntoma
Hipótesis
Evidencia 1
Evidencia 2
Hipótesis descartada
Causa
Acción
Resultado
~~~

## Misiones donde participa especialmente

~~~text
todas como registro
M7 como consolidación del diagnóstico
M8 como coordinación de la explicación
~~~

## Riesgo de comportamiento

Quedar fuera de la parte técnica.

## Mitigación

Debe hacer preguntas de evidencia y explicar al menos una relación entre dos capas durante M8.

## Preguntas guía

~~~text
¿Qué sabemos?
¿Qué estamos asumiendo?
¿Qué evidencia falta?
¿Qué hipótesis ya podemos descartar?
¿Cómo explicaríamos esto a otro equipo?
~~~

---

# 9. Fronteras de seguridad por rol

Ningún rol obtiene acceso adicional por su nombre.

Todos trabajan con las mismas fronteras del team.

~~~text
sin host shell
sin sudo
sin Docker socket
sin clublabctl
sin control token
sin credenciales productivas
sin acceso a otros teams
~~~

El rol únicamente determina responsabilidad pedagógica.

---

# 10. Configuración ideal — 4 integrantes

Configuración oficial de referencia:

~~~text
Persona A → R1 Interfaz
Persona B → R2 API
Persona C → R3 Datos
Persona D → R4 Sistemas
~~~

Ventajas:

~~~text
un rol base por persona
todas las capas representadas
rotación simple
ninguna combinación de responsabilidades
~~~

Todos los tiempos de ClubLab #01 se calculan pensando primero en esta configuración.

---

# 11. Configuración — 5 integrantes

~~~text
Persona A → R1 Interfaz
Persona B → R2 API
Persona C → R3 Datos
Persona D → R4 Sistemas
Persona E → R5 Relator
~~~

R5 no sustituye a ningún rol base.

Su presencia añade:

~~~text
mejor registro
mejor control de hipótesis
mejor explicación final
~~~

No debe convertir al resto en operadores mientras él solamente escribe.

---

# 12. Configuración — 3 integrantes

Configuración inicial oficial:

~~~text
Persona A → R1 Interfaz
Persona B → R2 API + R3 Datos
Persona C → R4 Sistemas
~~~

Motivo:

API y Datos se combinan porque M2, M3 y M4 son secuenciales y permiten que la misma persona siga el dato desde JSON hasta PostgreSQL.

Esto **no significa** que API y Datos sean la misma capa.

Reglas:

~~~text
Persona B cambia explícitamente de “modo API” a “modo Datos”
Persona A verifica UI en M3/M4
Persona C comprueba estado general y registra evidencia cuando no lidera
~~~

---

# 13. Configuración — 2 integrantes

Configuración de contingencia:

~~~text
Persona A → R1 Interfaz + R2 API
Persona B → R3 Datos + R4 Sistemas
~~~

Motivo:

~~~text
A sigue el flujo Browser → HTTP
B sigue el flujo Persistencia → Estado
~~~

La experiencia será más secuencial.

Reglas:

~~~text
solo una herramienta principal a la vez
no ejecutar tareas en paralelo
decir en voz alta qué rol se está usando
el instructor interviene antes si aparece sobrecarga
~~~

---

# 14. Configuración — 1 integrante

No es la modalidad objetivo.

Si ocurre:

~~~text
M0–M1 → sombrero Interfaz
M2 → sombrero API
M3–M4 → sombrero Datos
M5 → sombrero Sistemas
M6–M7 → alterna evidencias por capa
M8 → integra todo
~~~

El instructor actúa como interlocutor:

~~~text
pregunta
pide predicción
pide evidencia
~~~

pero no ejecuta las tareas.

---

# 15. Método de asignación inicial

La asignación debe tardar poco.

Orden recomendado:

~~~text
1. formar equipos
2. identificar número de integrantes
3. repartir roles según la configuración correspondiente
4. entregar acceso del team
5. iniciar M0
~~~

No se recomienda consumir tiempo haciendo un test de personalidad o de conocimientos.

---

# 16. Elección vs asignación

Para la primera clase:

> **Priorizar una asignación rápida y balanceada sobre “cada quien elige lo que ya conoce”.**

Si varias personas quieren el mismo rol:

~~~text
sorteo simple
o
decisión rápida del instructor
~~~

Motivo:

ClubLab busca que los alumnos descubran áreas, no que permanezcan únicamente en la capa que ya dominan.

---

# 17. Integrante avanzado

Un integrante avanzado no recibe automáticamente Sistemas, Datos o API.

La asignación debe evitar:

~~~text
“él sabe más, que haga lo difícil”
~~~

Su experiencia puede aprovecharse como apoyo verbal, pero el rol principal mantiene el teclado.

---

# 18. Integrante principiante

Un principiante puede ocupar cualquiera de los cuatro roles base.

No necesita memorizar comandos.

Se permitirá:

~~~text
cheat sheet
copiar un comando preparado
preguntar
pedir una pista
~~~

La responsabilidad sigue siendo explicar qué esperaba y qué observó.

---

# 19. Una laptop por equipo

Todos los roles siguen siendo válidos.

Regla:

~~~text
la persona cuyo rol lidera la misión controla la laptop
~~~

Los demás:

~~~text
observan
verifican
registran
formulan preguntas
~~~

La rotación física del teclado debe ser visible.

---

# 20. Varias laptops por equipo

Permitido:

~~~text
R1 → navegador
R2/R3/R4 → toolbox/pestañas auxiliares
~~~

Pero no deben convertirse en investigaciones aisladas.

Antes de avanzar, cada hallazgo relevante debe comunicarse al equipo.

---

# 21. Qué no se define todavía

Este bloque no cierra:

~~~text
rotación exacta por configuración
handoff
funciones Operar/Observar/Verificar/Registrar por misión
protocolo detallado de M7
contingencias de equipos rápidos/lentos
~~~

Eso pertenece a Bloques B y C.

---

# 22. Decisiones cerradas

### DA6-01
Se conservan R1–R4 como roles base.

### DA6-02
R5 es opcional y se usa principalmente en equipos de cinco.

### DA6-03
Cuatro integrantes es la configuración ideal.

### DA6-04
Con tres integrantes se combinan API + Datos.

### DA6-05
Con dos integrantes se combinan Interfaz + API y Datos + Sistemas.

### DA6-06
Un integrante individual utiliza los cuatro roles secuencialmente.

### DA6-07
Los roles no cambian permisos ni credenciales.

### DA6-08
El avanzado no obtiene automáticamente el rol técnicamente más complejo.

### DA6-09
El principiante puede ocupar cualquier rol base con apoyo de material.

### DA6-10
La asignación inicial debe ser rápida y no convertirse en una evaluación previa.

### DA6-11
Los comandos definitivos de Sistemas son los proporcionados por `clublab`, no comandos Docker.

### DA6-12
El rol API no utiliza rutas `/internal/*`.

### DA6-13
El rol Datos modifica únicamente la superficie pedagógica autorizada.

---

# 23. Criterios de aceptación

~~~text
[x] R1 actualizado
[x] R2 actualizado
[x] R3 actualizado
[x] R4 actualizado
[x] R5 actualizado
[x] herramientas reales por rol
[x] acciones permitidas/prohibidas
[x] evidencia mínima por rol
[x] preguntas guía
[x] configuración 5 personas
[x] configuración 4 personas
[x] configuración 3 personas
[x] configuración 2 personas
[x] contingencia individual
[x] reglas para avanzados
[x] reglas para principiantes
[x] fronteras de seguridad
~~~

# BLOQUE A — COMPLETADO

El siguiente bloque definirá la matriz M0–M8, las funciones momentáneas de participación, la rotación y el protocolo de handoff.
