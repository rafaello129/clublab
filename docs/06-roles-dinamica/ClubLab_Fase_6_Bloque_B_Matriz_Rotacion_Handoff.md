# ClubLab — Fase 6 / Bloque B
## Matriz misión/rol, rotación y handoff

**Proyecto:** ClubLab v1  
**Fase:** 6 — Roles y dinámica de equipos  
**Bloque:** B  
**Estado:** CERRADO PARA v1  
**Dependencias:** Bloque A + D01 + D04  
**Entregables:** P06A_Matriz_Roles_Misiones + P06B_Protocolo_Rotacion_y_Handoff

---

# 1. Propósito

Este bloque convierte los roles definidos en Bloque A en una dinámica ejecutable durante M0–M8.

Debe quedar claro en cada misión:

~~~text
quién opera
quién observa
quién verifica
quién registra
~~~

Estas cuatro funciones no sustituyen los roles R1–R5.

Son responsabilidades momentáneas.

---

# 2. Regla general de participación

En cada acción relevante:

~~~text
1. PREDICCIÓN
2. OPERACIÓN
3. OBSERVACIÓN
4. VERIFICACIÓN
5. REGISTRO
~~~

La secuencia evita convertir la práctica en una colección de comandos.

---

# 3. Protocolo POE

Se congela una versión breve del ciclo pedagógico:

## P — Predicción

Antes de ejecutar:

> **“Voy a hacer ____. Si nuestra idea es correcta, espero ____.”**

## O — Observación

Después de ejecutar:

> **“Observamos ____.”**

## E — Evidencia

Para cerrar:

> **“Esto apoya/contradice nuestra idea porque ____.”**

Nombre operativo:

~~~text
POE
Predicción → Observación → Evidencia
~~~

No requiere una hoja larga.

Fase 7 lo convertirá en una plantilla visual.

---

# 4. Función OPERAR

Responsabilidad:

~~~text
controlar la herramienta principal
ejecutar la acción acordada
explicar qué está haciendo
no adelantarse al equipo
~~~

La persona que OPERA controla el teclado de la misión.

---

# 5. Función OBSERVAR

Responsabilidad:

~~~text
mirar resultado inmediato
detectar cambios
identificar errores
comparar antes/después
~~~

No debe convertirse en “solo mirar”.

Debe verbalizar al menos un hallazgo.

---

# 6. Función VERIFICAR

Responsabilidad:

~~~text
comprobar el hallazgo desde otra capa
buscar consistencia
intentar descartar una explicación incorrecta
~~~

Ejemplos:

~~~text
UI cambia
→ verificar API

API responde
→ verificar DB

ranking falla
→ verificar health
~~~

---

# 7. Función REGISTRAR

Responsabilidad:

~~~text
guardar la evidencia mínima
anotar valor/status relevante
registrar hipótesis
conservar contexto para el handoff
~~~

Con R5 presente, el Relator asume la mayor parte de REGISTRAR.

Sin R5, la función rota.

---

# 8. Regla del teclado

Regla oficial:

> **La persona en función OPERAR controla el teclado o la herramienta principal.**

Los demás pueden:

~~~text
sugerir
preguntar
señalar
comparar
verificar
~~~

No deben ejecutar en paralelo una acción que invalide o adelante el experimento.

---

# 9. Excepciones a la regla del teclado

Permitidas únicamente por:

~~~text
accesibilidad
demostración breve
bloqueo técnico
rotación
indicación del instructor
~~~

Si otra persona toma el teclado para demostrar algo:

~~~text
máximo 60 segundos
→ devuelve control
→ el operador original explica qué ocurrió
~~~

---

# 10. Matriz M0–M5 — configuración ideal de cuatro

Antes de la rotación:

~~~text
A → R1 Interfaz
B → R2 API
C → R3 Datos
D → R4 Sistemas
~~~

| Misión | OPERAR | OBSERVAR | VERIFICAR | REGISTRAR |
|---|---|---|---|---|
| M0 | R1 Interfaz | R2 API | R4 Sistemas | R3 Datos |
| M1 | R1 Interfaz | R2 API | R4 Sistemas | R3 Datos |
| M2 | R2 API | R1 Interfaz | R4 Sistemas | R3 Datos |
| M3 | R3 Datos | R2 API | R1 Interfaz | R4 Sistemas |
| M4 | R3 Datos | R1 Interfaz | R2 API | R4 Sistemas |
| M5 | R4 Sistemas | R1 Interfaz | R2 API | R3 Datos |

La matriz distribuye teclado y evidencia antes del incidente.

---

# 11. M0 — Reconocimiento

## OPERAR — R1

~~~text
navega
identifica vistas
localiza ranking
~~~

## OBSERVAR — R2

Busca:

~~~text
qué datos parecen dinámicos
qué acciones podrían requerir API
~~~

## VERIFICAR — R4

Comprueba que el entorno inicial no muestra síntomas obvios de fallo.

## REGISTRAR — R3

Anota:

~~~text
score visible
posición visible
team visible
vistas principales
~~~

---

# 12. M1 — Network

## OPERAR — R1

~~~text
abre DevTools
Network
Fetch/XHR
recarga ranking
~~~

## OBSERVAR — R2

Identifica:

~~~text
GET /api/ranking
status
response
~~~

## VERIFICAR — R4

Confirma que la aplicación general continúa sana.

## REGISTRAR — R3

Anota:

~~~text
método
URL
status
dato reconocible
~~~

---

# 13. M2 — API directa

## OPERAR — R2

Repite la request con curl.

## OBSERVAR — R1

Compara JSON con lo que se ve en pantalla.

## VERIFICAR — R4

Comprueba que el endpoint se consulta dentro del team correcto.

## REGISTRAR — R3

Anota:

~~~text
endpoint
status
campo JSON
relación con UI
~~~

---

# 14. M3 — PostgreSQL

## OPERAR — R3

~~~text
entra a psql
inspecciona objetos
consulta lab.my_team_score
~~~

## OBSERVAR — R2

Relaciona SQL con JSON.

## VERIFICAR — R1

Relaciona el dato con la UI.

## REGISTRAR — R4

Anota:

~~~text
objeto consultado
team
score actual
~~~

---

# 15. M4 — Modificación controlada

## OPERAR — R3

Secuencia obligatoria:

~~~text
SELECT
→ predicción
→ UPDATE
→ SELECT
~~~

## OBSERVAR — R1

Recarga/refetch de la UI después del cambio.

## VERIFICAR — R2

Consulta API y comprueba nuevo score/posición.

## REGISTRAR — R4

Guarda:

~~~text
antes
acción
después
efecto en API
efecto en UI
~~~

---

# 16. M5 — Componentes y estado

## OPERAR — R4

~~~bash
clublab whoami
clublab status
clublab health
~~~

## OBSERVAR — R1

Relaciona nombres de componentes con la aplicación.

## VERIFICAR — R2

Compara health con endpoints utilizados.

## REGISTRAR — R3

Anota el mapa:

~~~text
Frontend
API
Database
Toolbox
~~~

y sus estados.

---

# 17. Checkpoint antes de rotar

Antes de cambiar roles, el equipo debe poder responder sin investigar de nuevo:

~~~text
¿Qué request carga el ranking?
¿Qué endpoint responde?
¿Dónde está el score?
¿Qué cambió en M4?
¿Qué componentes existen?
~~~

Si no puede responder al menos cuatro de cinco:

~~~text
no se inicia handoff
→ se recupera contexto durante máximo 60 segundos
~~~

---

# 18. Rotación oficial — cuatro integrantes

Después de M5:

~~~text
A: R1 Interfaz  → R4 Sistemas
B: R2 API       → R3 Datos
C: R3 Datos     → R2 API
D: R4 Sistemas  → R1 Interfaz
~~~

Visual:

~~~text
Interfaz ↔ Sistemas
API      ↔ Datos
~~~

---

# 19. Resultado pedagógico de la rotación

~~~text
quien observó UI
→ ahora diagnostica servicios

quien consultó API
→ ahora trabaja persistencia

quien modificó DB
→ ahora prueba endpoints

quien observó estado
→ ahora experimenta el síntoma como usuario
~~~

El incidente empieza con herramientas nuevas para todos los integrantes base.

---

# 20. M6 — Descubrir el incidente

Después de rotar, los nombres R1–R4 se refieren al **nuevo responsable**.

| Función | Responsable |
|---|---|
| OPERAR | R1 Interfaz |
| OBSERVAR | R2 API |
| VERIFICAR | R4 Sistemas |
| REGISTRAR | R3 Datos |

## OPERAR — R1

Reproduce el síntoma en ranking.

## OBSERVAR — R2

Identifica request/status.

## VERIFICAR — R4

Ejecuta únicamente checks de observación:

~~~bash
clublab status
clublab health
~~~

No recover todavía.

## REGISTRAR — R3

Anota:

~~~text
qué falla
qué sigue funcionando
primer contraste
~~~

---

# 21. M7 — Diagnóstico como secuencia colaborativa

M7 no tiene un solo operador.

Se divide en cuatro rondas de evidencia.

---

# 22. M7 / Ronda 1 — Interfaz

**Lidera R1**

~~~text
reproducir síntoma
identificar request
confirmar status
~~~

Aporta:

~~~text
síntoma
request fallida
~~~

R2 observa, R4 verifica estado general y R3 registra.

---

# 23. M7 / Ronda 2 — API

**Lidera R2**

Compara:

~~~text
/api/ranking
vs
/api/health
y otro endpoint sano
~~~

Aporta:

~~~text
ranking 500
health 200
endpoint sano 200
~~~

R1 verifica impacto visual.

---

# 24. M7 / Ronda 3 — Datos

**Lidera R3**

Comprueba:

~~~text
DB accesible
lab.my_team_score consultable
score M4 preservado
~~~

Aporta evidencia de que:

~~~text
la base completa no está caída
los datos siguen presentes
~~~

R2 compara con el fallo del ranking.

---

# 25. M7 / Ronda 4 — Sistemas

**Lidera R4**

~~~bash
clublab status
clublab health
clublab logs api
~~~

Aporta:

~~~text
servicios vivos
ranking fallido
error relevante del lablog
~~~

Solo después de la barrera de evidencia puede ejecutar:

~~~bash
clublab recover ranking-db
~~~

---

# 26. Barrera previa al recover

Antes de recover, el equipo debe verbalizar:

~~~text
Hipótesis actual:
____________________

Evidencia 1:
____________________

Evidencia 2:
____________________

Hipótesis descartada:
____________________
~~~

El Bloque C definirá con más detalle esta barrera.

Este bloque congela que el recover **no pertenece a la fase exploratoria**.

---

# 27. Verificación posterior al recover

Después de recovery:

## R4

Comprueba:

~~~bash
clublab health
~~~

## R2

Comprueba:

~~~text
/api/ranking → 200
~~~

## R3

Comprueba que el score de M4 sigue presente.

## R1

Comprueba que la UI vuelve a mostrar ranking.

Resultado esperado:

~~~text
recuperación funcional
+
datos preservados
~~~

---

# 28. M8 — Reconstrucción

M8 pertenece a todos.

Requisito:

> **Cada integrante debe explicar al menos una relación entre dos capas.**

Ejemplos:

~~~text
UI → request
request → API
API → DB
logs → causa
recover → API sana
~~~

Para cuatro integrantes:

~~~text
R1 → síntoma y UI
R2 → API
R3 → DB
R4 → estado, logs y recovery
~~~

No es obligatorio mantener exactamente este orden al presentar.

---

# 29. Equipos de cinco

Antes de rotar:

~~~text
A → R1
B → R2
C → R3
D → R4
E → R5
~~~

Después:

~~~text
A → R4
B → R3
C → R2
D → R1
E → R5
~~~

R5 permanece como Relator porque su valor está en conservar contexto entre ambas mitades.

Durante handoff:

~~~text
R5 escucha ambas transferencias
→ verifica que no se pierda evidencia
~~~

Durante M7:

~~~text
R5 mantiene matriz de diagnóstico
~~~

Durante M8:

~~~text
R5 coordina
pero no sustituye las explicaciones técnicas de R1–R4
~~~

---

# 30. Equipos de tres — rotación oficial

Antes:

~~~text
A → R1 Interfaz
B → R2 API + R3 Datos
C → R4 Sistemas
~~~

Después:

~~~text
A → R4 Sistemas
B → R1 Interfaz
C → R2 API + R3 Datos
~~~

Interpretación:

~~~text
A cambia UI → Sistemas
B cambia API/Datos → UI
C cambia Sistemas → API/Datos
~~~

Todos cambian de capa principal.

---

# 31. Equipos de tres — reparto M6/M7

Después de rotar:

~~~text
B/R1 → reproduce UI
C/R2 → compara API
C/R3 → comprueba DB
A/R4 → estado, logs, recovery
~~~

Para evitar que C monopolice M7:

~~~text
R2 y R3 se ejecutan como rondas separadas
C debe anunciar explícitamente el cambio:
“Ahora cambio de API a Datos.”
~~~

Registro:

~~~text
A o B registra cuando C opera
C registra cuando A/B operan
~~~

---

# 32. Equipos de dos — rotación oficial

Antes:

~~~text
A → R1 Interfaz + R2 API
B → R3 Datos + R4 Sistemas
~~~

Después:

~~~text
A → R3 Datos + R4 Sistemas
B → R1 Interfaz + R2 API
~~~

Se intercambian los dos bundles completos.

---

# 33. Equipos de dos — ejecución

No se utilizan las cuatro funciones simultáneamente.

Cada ronda usa:

~~~text
1 OPERAR
1 VERIFICAR/REGISTRAR
~~~

La segunda persona verbaliza y registra.

Después cambian.

Ejemplo M7:

~~~text
B/R1 → UI
B/R2 → API
A/R3 → DB
A/R4 → logs/recover
~~~

Aunque B tenga R1+R2, debe tratar UI y API como dos rondas distintas.

---

# 34. Equipo individual

No existe handoff interpersonal.

La “rotación” se hace declarando el cambio de capa.

Después de M5:

~~~text
“Terminé Sistemas.
Ahora vuelvo a observar el incidente desde Interfaz.”
~~~

Durante M7:

~~~text
Interfaz
→ API
→ Datos
→ Sistemas
~~~

Debe registrar una evidencia por capa antes de recover.

---

# 35. Protocolo de handoff — objetivo

Handoff no significa explicar todo lo que ocurrió.

Solo debe transferir:

~~~text
herramienta
hallazgo
dato clave
precaución
~~~

Plantilla:

> **“Yo usé ____. Encontré ____. Recuerda ____. Evita ____.”**

---

# 36. Handoff — cuatro personas

Las transferencias son por pareja:

~~~text
R1 ↔ R4
R2 ↔ R3
~~~

Se hacen en paralelo.

## Ronda 1 — 45 segundos

Cada responsable saliente explica a quien recibe su rol.

## Ronda 2 — 30 segundos

Quien recibe responde:

~~~text
“Entendí que…”
+
una pregunta si hace falta
~~~

## Cambio físico/herramienta — 15 segundos

Total objetivo:

~~~text
90 segundos
~~~

Margen máximo:

~~~text
2 minutos
~~~

---

# 37. Handoff — cinco personas

Mismo protocolo de cuatro.

R5:

~~~text
escucha
detecta omisión
hace una sola pregunta aclaratoria si es necesaria
~~~

No extiende el handoff más de dos minutos.

---

# 38. Handoff — tres personas

La rotación es circular:

~~~text
R1 → nuevo R1
R2+R3 → nuevo R2+R3
R4 → nuevo R4
~~~

Protocolo:

~~~text
Turno 1 — 25 s
A transfiere Interfaz a B

Turno 2 — 25 s
B transfiere API/Datos a C

Turno 3 — 25 s
C transfiere Sistemas a A

Readback conjunto — 25 s
~~~

Objetivo:

~~~text
100 segundos
~~~

---

# 39. Handoff — dos personas

Cada persona transfiere su bundle.

~~~text
A → Interfaz/API a B   40 s
B → Datos/Sistemas a A 40 s
readback               20 s
~~~

Total:

~~~text
100 segundos
~~~

---

# 40. Readback

Toda transferencia termina con:

> **“Entonces, lo importante para mí es ____.”**

Si el nuevo responsable no puede completar la frase:

~~~text
handoff incompleto
→ aclaración de máximo 20 segundos
~~~

---

# 41. Qué información NO se transfiere

No se debe perder tiempo con:

~~~text
historia completa de cada click
todos los comandos usados
cada respuesta JSON
detalles irrelevantes
~~~

Solo contexto suficiente para continuar.

---

# 42. Evidencia mínima para handoff

## Interfaz

~~~text
request principal
status normal
pantalla asociada
~~~

## API

~~~text
endpoint principal
campo JSON
status normal
~~~

## Datos

~~~text
objeto SQL
score actual
comando seguro clave
~~~

## Sistemas

~~~text
comandos clublab
estado normal esperado
dónde mirar logs
~~~

---

# 43. R5 y handoff

R5 no recibe un nuevo rol base.

Su propio handoff interno es:

~~~text
“Antes de la rotación sabemos…”
~~~

y debe resumir en máximo 20 segundos:

~~~text
score actual
posición actual
request del ranking
estado de servicios
~~~

Esto crea un checkpoint compartido.

---

# 44. Regla de no adelantarse

Durante M0–M5:

~~~text
no ejecutar comandos del incidente
no probar recover
no buscar fallo futuro
~~~

Durante handoff:

~~~text
no abrir nuevas investigaciones
~~~

Durante M6:

~~~text
observar primero
no recover
~~~

---

# 45. Varias laptops

Aunque existan varias laptops:

> **Las funciones siguen existiendo.**

No se permite:

~~~text
R1 navega
R2 hace curl
R3 hace SQL
R4 mira logs
todos al mismo tiempo
sin compartir resultados
~~~

Se permite trabajo paralelo únicamente cuando la misión lo indique explícitamente.

M7 prioriza rondas secuenciales para que todo el equipo entienda cada evidencia.

---

# 46. Una laptop

La matriz se aplica literalmente.

Cuando cambia OPERAR:

~~~text
cambia la persona frente al teclado
~~~

No basta con que otra persona “dicte”.

---

# 47. Ritmo esperado

La colaboración no debe añadir tiempos extra sustanciales.

Se integra dentro de las misiones.

Único bloque temporal explícito:

~~~text
checkpoint + rotación + handoff
≈ 2 minutos
~~~

Esto coincide con la ventana ya reservada entre M5 y M6.

---

# 48. Antipatrones cerrados

## BP-01 — Todos dan instrucciones al operador

Respuesta:

~~~text
solo una sugerencia a la vez
operador repite lo que va a hacer
~~~

## BP-02 — El operador ejecuta sin explicar

Respuesta:

~~~text
no hay acción sin predicción breve
~~~

## BP-03 — El registrador copia todo

Respuesta:

~~~text
solo evidencia mínima
~~~

## BP-04 — Verificar significa repetir lo mismo

Respuesta:

~~~text
verificación debe usar otra capa cuando sea posible
~~~

## BP-05 — Handoff se convierte en mini-clase

Respuesta:

~~~text
usar plantilla de cuatro campos
límite temporal
~~~

## BP-06 — Varias laptops fragmentan al equipo

Respuesta:

~~~text
hallazgo no cuenta hasta comunicarse
~~~

---

# 49. Decisiones cerradas

### DB6-01
Se utilizan cuatro funciones momentáneas: OPERAR, OBSERVAR, VERIFICAR y REGISTRAR.

### DB6-02
Se adopta POE: Predicción → Observación → Evidencia.

### DB6-03
La persona que OPERA controla la herramienta principal.

### DB6-04
M0–M5 tienen una matriz base para cuatro integrantes.

### DB6-05
M7 se divide en rondas por capa.

### DB6-06
Recover solo ocurre después de las rondas de evidencia.

### DB6-07
La rotación de cuatro personas sigue siendo R1↔R4 y R2↔R3.

### DB6-08
En equipos de tres se rota A→R4, B→R1, C→R2+R3.

### DB6-09
En equipos de dos se intercambian los bundles completos.

### DB6-10
R5 permanece como Relator durante la rotación.

### DB6-11
Handoff debe terminar en máximo dos minutos.

### DB6-12
Todo handoff incluye readback.

### DB6-13
M8 exige una relación entre capas por integrante.

---

# 50. Criterios de aceptación

~~~text
[x] matriz M0–M5
[x] M6 definido
[x] M7 por rondas
[x] M8 colaborativo
[x] OPERAR definido
[x] OBSERVAR definido
[x] VERIFICAR definido
[x] REGISTRAR definido
[x] POE definido
[x] regla del teclado cerrada
[x] rotación 4 personas
[x] rotación 5 personas
[x] rotación 3 personas
[x] rotación 2 personas
[x] contingencia individual
[x] handoff por configuración
[x] readback
[x] barrera previa a recover
[x] antipatrones
~~~

# BLOQUE B — COMPLETADO

El siguiente bloque definirá el protocolo detallado del incidente colaborativo, las reglas para equipos rápidos/lentos y las contingencias de participación.
