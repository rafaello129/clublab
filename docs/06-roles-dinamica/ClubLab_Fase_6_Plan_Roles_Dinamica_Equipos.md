# ClubLab — Plan de Fase 6
## Roles, rotación y dinámica de equipos

**Proyecto:** ClubLab v1  
**Fase:** 6  
**Nombre:** Roles y dinámica de equipos  
**Estado:** PLAN DE TRABAJO  
**Entradas principales:**  
- D01_Diseno_Experiencia_ClubLab_01.md
- ClubLab_Fase_1_Bloque_D_Roles_y_Rotacion.md
- D04_Scenario_Manager_y_Operacion_ClubLab.md
- SYS01_CLI_clublab.md
- APP04_Aplicacion_Integrada.md

**Entregable principal previsto:**  
- D05_Roles_y_Dinamica_Equipos_ClubLab.md

**Entregables auxiliares previstos:**  
- P06_Roles_v1.md
- P06A_Matriz_Roles_Misiones.md
- P06B_Protocolo_Rotacion_y_Handoff.md
- P06C_Configuraciones_de_Equipo.md
- P06D_Protocolo_Incidente_Colaborativo.md

---

# 1. Propósito de la Fase 6

La Fase 1 ya definió los roles pedagógicos conceptuales.

La Fase 6 **no vuelve a inventar los roles**.

Su función es convertirlos en un sistema operativo para la clase:

~~~text
quién hace qué
cuándo toma el teclado
qué evidencia debe aportar
cómo rota
cómo transfiere contexto
cómo participa durante el incidente
qué ocurre si el equipo tiene 2, 3, 4 o 5 personas
cómo evitar que una persona monopolice la sesión
~~~

La pregunta principal será:

> **¿Cómo conseguimos que todos los integrantes investiguen, aporten evidencia y conecten capas distintas del sistema durante los 120 minutos?**

---

# 2. Objetivo general

Al finalizar la fase debe existir un protocolo de colaboración que permita formar un equipo y asignar roles en menos de dos minutos, ejecutar M0–M8 sin ambigüedades y rotar antes del incidente sin perder contexto.

El sistema debe funcionar para grupos mixtos:

~~~text
principiantes
intermedios
avanzados
~~~

sin convertir al integrante avanzado en “el operador de todo”.

---

# 3. Roles congelados

ClubLab #01 mantiene cuatro roles base:

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

R5 se utiliza principalmente con equipos de cinco.

---

# 4. Herramientas reales disponibles por rol

La Fase 6 debe actualizar las definiciones originales usando las herramientas que ya quedaron cerradas en Fases 4–5.

## R1 — Interfaz

~~~text
Browser
DevTools
Network
Fetch/XHR
Headers
Response
~~~

## R2 — API

~~~text
curl
HTTP
JSON
/api/health
/api/ranking
/api/team
/api/missions
/api/activity
~~~

## R3 — Datos

~~~text
psql
\dt
\d
SELECT
lab.my_team_score
UPDATE controlado
~~~

## R4 — Sistemas

~~~text
clublab whoami
clublab status
clublab health
clublab logs api
clublab recover ranking-db
~~~

## R5 — Relator

~~~text
registro de evidencia
matriz hipótesis/evidencia
diagrama
línea de tiempo
conclusión del equipo
~~~

---

# 5. Principios obligatorios

La dinámica deberá respetar:

~~~text
1. El rol principal controla el teclado.
2. Antes de ejecutar, se expresa una predicción.
3. Después de ejecutar, se registra evidencia.
4. Una misión nunca pertenece completamente a una sola persona.
5. Los roles rotan antes del incidente.
6. El incidente exige evidencia de varias capas.
7. El avanzado no sustituye al principiante.
8. Pedir ayuda no penaliza.
9. Ningún rol obtiene privilegios adicionales.
10. El equipo produce una sola explicación final.
~~~

---

# 6. División de la fase

La Fase 6 se trabajará en **cuatro bloques**:

~~~text
BLOQUE A
Contrato final de roles y configuraciones de equipo

BLOQUE B
Matriz misión/rol + rotación + handoff

BLOQUE C
Dinámica del incidente + participación + contingencias

BLOQUE D
Validación de la dinámica + consolidación D05
~~~

---

# BLOQUE A — Contrato final de roles y configuraciones

# 7. Objetivo

Cerrar la versión definitiva de cada rol después de conocer ya:

~~~text
frontend real previsto
API real prevista
superficie SQL
student CLI
scenario/recovery
limitaciones de seguridad
~~~

---

# 8. Contrato por rol

Cada rol deberá quedar definido con exactamente estas secciones:

~~~text
nombre
pregunta principal
objetivo
herramientas
acciones permitidas
acciones prohibidas
evidencia mínima
misiones donde lidera
riesgos de comportamiento
preguntas guía
~~~

---

# 9. R1 — Explorador de Interfaz

Debe liderar especialmente:

~~~text
M0
M1
M6 síntoma inicial
~~~

Evidencia mínima esperada:

~~~text
pantalla afectada
request relevante
método
status
respuesta visible
~~~

Riesgo a evitar:

~~~text
“solo hacer clic”
~~~

---

# 10. R2 — Investigador de API

Debe liderar especialmente:

~~~text
M2
comparación de endpoints en M7
~~~

Evidencia mínima:

~~~text
URL
método
status
JSON
comparación sano/fallido
~~~

Riesgo:

~~~text
copiar comandos sin interpretar
~~~

---

# 11. R3 — Investigador de Datos

Debe liderar:

~~~text
M3
M4
~~~

Evidencia mínima:

~~~text
tabla/vista
registro
valor anterior
valor nuevo
consulta
~~~

Riesgo:

~~~text
hacer UPDATE sin comprobar primero
~~~

Regla obligatoria:

~~~text
SELECT
→ verificar
→ predecir
→ UPDATE
→ comprobar
~~~

---

# 12. R4 — Operador de Sistemas

Debe liderar:

~~~text
M5
M7
recover
~~~

Herramientas definitivas:

~~~bash
clublab status
clublab health
clublab logs api
clublab recover ranking-db
~~~

Evidencia mínima:

~~~text
servicios vivos
health
ranking status
fragmento de lablog
resultado del recover
~~~

Riesgo:

~~~text
“reiniciar por reiniciar”
~~~

---

# 13. R5 — Relator / Analista

Solo cuando ayude a la dinámica.

No debe ser un rol pasivo.

Durante M7 será responsable de mantener:

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

Durante M8 coordina la explicación de 60–90 segundos.

---

# 14. Configuración ideal

~~~text
4 integrantes
1 rol base por integrante
~~~

Es la configuración de referencia para todos los tiempos y materiales.

---

# 15. Equipos de cinco

~~~text
R1 Interfaz
R2 API
R3 Datos
R4 Sistemas
R5 Relator
~~~

R5 permanece como relator después de la rotación, pero debe participar activamente en M7.

---

# 16. Equipos de tres

Configuración inicial:

~~~text
A → Interfaz
B → API + Datos
C → Sistemas
~~~

La combinación API+Datos debe considerarse temporal, no indicar que ambas áreas son “lo mismo”.

---

# 17. Equipos de dos

Configuración de contingencia:

~~~text
A → Interfaz + API
B → Datos + Sistemas
~~~

Después intercambian.

La Fase 6 deberá identificar qué partes pueden simplificarse para evitar sobrecarga.

---

# 18. Equipo individual

Solo contingencia.

El alumno cambia explícitamente de “sombrero” entre:

~~~text
Interfaz
API
Datos
Sistemas
~~~

El instructor funciona como interlocutor, no como operador.

---

# 19. Salidas del Bloque A

~~~text
P06_Roles_v1
P06C_Configuraciones_de_Equipo
~~~

---

# BLOQUE B — Matriz misión/rol, rotación y handoff

# 20. Objetivo

Convertir M0–M8 en una secuencia donde siempre quede claro:

~~~text
quién opera
quién verifica
quién observa
quién registra
~~~

---

# 21. Matriz base

Referencia inicial:

| Misión | Lidera | Apoyo principal |
|---|---|---|
| M0 | Interfaz | Todos |
| M1 | Interfaz | API |
| M2 | API | Interfaz |
| M3 | Datos | API |
| M4 | Datos | API + Interfaz |
| M5 | Sistemas | Todos |
| M6 | Interfaz | Todos |
| M7 | Sistemas | API + Datos + Interfaz |
| M8 | Todos | Relator si existe |

El bloque deberá convertir esta tabla en protocolo operativo.

---

# 22. Cuatro funciones de participación

En cada misión deben existir:

~~~text
OPERAR
OBSERVAR
VERIFICAR
REGISTRAR
~~~

No son nuevos roles.

Son funciones momentáneas dentro de la misión.

---

# 23. Regla de predicción

Antes de una acción relevante:

> **“Voy a hacer X. Si nuestra hipótesis es correcta, espero Y.”**

Ejemplo:

> “Voy a consultar /api/ranking. Si la API está funcionando pero falla solo el ranking, espero recibir un 500 y que /api/health siga en 200.”

---

# 24. Regla posterior a la acción

Después:

> **“Observamos Z; esto apoya/contradice nuestra hipótesis porque…”**

La Fase 7 convertirá esta regla en una plantilla breve para alumnos.

---

# 25. Rotación oficial

Ocurre:

~~~text
después de M5
antes de M6
~~~

Para cuatro personas:

~~~text
Interfaz  ↔ Sistemas
API       ↔ Datos
~~~

---

# 26. Motivo de la rotación

El incidente debe obligar a observar otra capa.

Ejemplo:

~~~text
quien vio la UI
→ pasa a Sistemas

quien usó API
→ pasa a Datos

quien investigó DB
→ pasa a API

quien observó servicios
→ pasa a Interfaz
~~~

---

# 27. Protocolo de handoff

Cada persona dispone de:

~~~text
30–45 segundos
~~~

para transferir:

~~~text
1. herramienta principal
2. hallazgo más importante
3. dato/endpoint/tabla a recordar
4. error que debe evitar
~~~

Tiempo máximo de toda la rotación:

~~~text
2 minutos
~~~

---

# 28. Tarjeta verbal de handoff

Formato:

> **“Yo usé ____. Encontré ____. Lo importante es ____. Evita ____.”**

Debe poder hacerse sin leer un manual.

---

# 29. Control del teclado

Regla base:

> **El rol principal de la misión controla el teclado.**

Excepciones:

~~~text
demostración breve
accesibilidad
bloqueo técnico
rotación
indicación del instructor
~~~

La excepción no debe convertir al avanzado en operador permanente.

---

# 30. Salidas del Bloque B

~~~text
P06A_Matriz_Roles_Misiones
P06B_Protocolo_Rotacion_y_Handoff
~~~

---

# BLOQUE C — Incidente colaborativo, participación y contingencias

# 31. Objetivo

Definir cómo trabaja el equipo durante M6/M7 para evitar:

~~~text
adivinanzas
reinicios aleatorios
una persona haciendo todo
varias investigaciones desconectadas
~~~

---

# 32. Regla del incidente

Nadie puede ejecutar recovery hasta que el equipo pueda expresar:

~~~text
qué cree que falló
+
dos evidencias
+
una hipótesis descartada
~~~

El software puede permitir el comando, pero pedagógicamente el instructor no autoriza su uso antes de este punto.

---

# 33. Aportación mínima por rol en M7

## Interfaz

~~~text
síntoma
request fallida
~~~

## API

~~~text
status/respuesta
comparación con endpoint sano
~~~

## Datos

~~~text
DB accesible
dato consultable
~~~

## Sistemas

~~~text
health/status
lablog
acción de recuperación
~~~

## Relator

~~~text
hipótesis consolidada
evidencias
hipótesis descartada
~~~

---

# 34. Protocolo de diagnóstico

El equipo debe poder responder:

~~~text
1. ¿Qué funciona?
2. ¿Qué falla?
3. ¿Dónde aparece la primera evidencia?
4. ¿Qué componente podemos descartar?
5. ¿Qué evidencia apoya la causa?
6. ¿Qué acción mínima la recupera?
7. ¿Cómo comprobamos que volvió?
~~~

---

# 35. Dinámica para principiantes

El instructor debe impedir que la actividad se vuelva una prueba de memoria.

Permitido:

~~~text
cheat sheets
comandos preparados
preguntas guía
pistas progresivas
~~~

No se evalúa:

~~~text
memorizar curl
memorizar SQL
memorizar flags
~~~

Se evalúa comprensión de la evidencia.

---

# 36. Dinámica para avanzados

Si una persona termina antes:

~~~text
debe formular una hipótesis
ayudar con preguntas
comparar evidencia
mejorar el diagrama
~~~

No debe:

~~~text
tomar el teclado de otros
adelantar el escenario
buscar endpoints internos
explorar otros teams
~~~

---

# 37. Equipos desbalanceados

La fase deberá definir respuesta a:

~~~text
un alumno muy avanzado
dos principiantes bloqueados
una persona ausente
una laptop que falla
un rol que termina demasiado pronto
un equipo demasiado rápido
un equipo muy lento
~~~

El objetivo es ajustar participación, no cambiar los objetivos de aprendizaje.

---

# 38. Una laptop por equipo

Con una sola laptop:

~~~text
regla del teclado = estricta
handoff visible
relator usa papel/hoja separada si existe
~~~

---

# 39. Varias laptops

Recomendación:

~~~text
Interfaz → navegador principal
API/Datos/Sistemas → toolbox o pestañas separadas
~~~

Pero el equipo debe seguir compartiendo hallazgos.

No se convierte en cuatro ejercicios individuales.

---

# 40. Equipos rápidos

Extensiones permitidas:

~~~text
comparar request sana/fallida
encontrar otra relación SQL
explicar requestId
mejorar diagrama
formular una variante del fallo
~~~

No avanzar el incidente antes del minuto definido.

---

# 41. Equipos lentos

Orden de reducción:

~~~text
1. dar pista
2. proporcionar comando
3. señalar herramienta
4. entregar evidencia parcial
5. desbloqueo P4
~~~

No eliminar:

~~~text
M4
M7
M8
~~~

porque contienen los descubrimientos centrales.

---

# 42. Salida del Bloque C

~~~text
P06D_Protocolo_Incidente_Colaborativo
~~~

---

# BLOQUE D — Validación y consolidación D05

# 43. Objetivo

Comprobar que la dinámica puede ejecutarse en los formatos previstos antes de producir los materiales finales.

---

# 44. Validaciones de mesa

Simular al menos:

~~~text
2 personas
3 personas
4 personas
5 personas
~~~

Para cada configuración se revisará:

~~~text
asignación inicial
M0–M5
rotación
M6/M7
M8
~~~

---

# 45. Validación de tiempos

Comprobar que:

~~~text
formar equipos + asignar roles <= 5 min
explicar roles <= 2 min
rotación + handoff <= 2 min
M7 conserva 23 min
M8 conserva 13 min
~~~

No se debe robar tiempo al incidente para explicar roles demasiado complejos.

---

# 46. Validación de comprensión

Cada rol debe poder explicarse en:

~~~text
menos de 60 segundos
~~~

Una tarjeta futura no deberá requerir más de:

~~~text
1 cara / bloque visual breve
~~~

---

# 47. Validación de participación

Para cuatro integrantes, al terminar M7:

~~~text
todos operaron al menos una herramienta
todos aportaron al menos una evidencia
al menos dos personas utilizaron una capa distinta tras rotación
~~~

---

# 48. Validación del incidente

Antes de recover:

~~~text
>= 2 evidencias
>= 1 hipótesis descartada
causa formulada por el equipo
~~~

Después:

~~~text
validación de ranking
validación de health
explicación de por qué recover funcionó
~~~

---

# 49. Validación de seguridad

Ningún rol requiere:

~~~text
host shell
sudo
Docker socket
clublabctl
control token
app DB password
otro team
~~~

---

# 50. Salida hacia Fase 7

Fase 6 produce **contenido y contratos**, no todavía el paquete final del alumno.

Fase 7 transformará este contenido en:

~~~text
tarjetas de rol
hojas de misión
cheat sheets
hoja de evidencias
hoja/diagrama final
~~~

Esto evita mezclar diseño de dinámica con diseño gráfico/material.

---

# 51. Salida hacia Fase 8

Fase 8 recibirá:

~~~text
reglas de participación
criterios de intervención
rotación
pistas por rol
contingencias de equipos
~~~

y lo convertirá en guía operativa del instructor.

---

# 52. D05 — Documento consolidado

D05_Roles_y_Dinamica_Equipos_ClubLab.md reunirá:

~~~text
roles definitivos
herramientas definitivas
límites
matriz misión/rol
funciones operar/observar/verificar/registrar
rotación
handoff
configuraciones de 2–5 personas
protocolo M6/M7
reglas anti-monopolio
contingencias
validaciones
~~~

---

# 53. Qué NO pertenece a Fase 6

No implementar aquí:

~~~text
diseño gráfico final de tarjetas
manual completo del alumno
presentación del instructor
app/infra real
ensayo sobre Tulum
~~~

Eso pertenece respectivamente a:

~~~text
Fase 7
Fase 8
implementación técnica
Fase 9
~~~

---

# 54. Criterios de éxito de Fase 6

~~~text
[ ] contratos R1–R5 actualizados
[ ] herramientas definitivas por rol
[ ] límites definitivos por rol
[ ] configuraciones 2/3/4/5 personas
[ ] matriz M0–M8/roles
[ ] funciones operar/observar/verificar/registrar
[ ] regla del teclado
[ ] regla de predicción
[ ] protocolo de evidencia
[ ] rotación oficial
[ ] handoff definido
[ ] protocolo M6/M7
[ ] reglas para avanzados/principiantes
[ ] contingencias de participación
[ ] validación temporal
[ ] validación de seguridad
[ ] D05 consolidado
~~~

---

# 55. Primer bloque a desarrollar

# BLOQUE A — Contrato final de roles y configuraciones

El siguiente paso será actualizar formalmente R1–R5 con las herramientas reales que ya existen en el diseño actual y cerrar las configuraciones de equipos de 2, 3, 4 y 5 integrantes.

No se crearán todavía las tarjetas visuales; primero se cerrará el contenido que esas tarjetas deberán contener.
