# ClubLab — Fase 6 / Bloque C
## Incidente colaborativo, participación y contingencias

**Proyecto:** ClubLab v1  
**Fase:** 6 — Roles y dinámica de equipos  
**Bloque:** C  
**Estado:** CERRADO PARA v1  
**Dependencias:** Bloques A–B + D01 + D04  
**Entregable:** P06D_Protocolo_Incidente_Colaborativo.md

---

# 1. Propósito

Este bloque define cómo debe comportarse el equipo cuando aparece el incidente de M6/M7 y qué hacer cuando la dinámica humana se desvía del flujo previsto.

Problemas que este bloque debe evitar:

~~~text
adivinar la causa
ejecutar recover demasiado pronto
reiniciar por reflejo
una persona haciendo todo
principiantes quedándose fuera
varias investigaciones desconectadas
equipos rápidos adelantándose
equipos lentos perdiendo el objetivo
una ausencia rompiendo la asignación
una laptop bloqueando toda la clase
~~~

La prioridad no es “resolver más rápido”.

La prioridad es:

> **Construir un diagnóstico compartido a partir de evidencia.**

---

# 2. Condición de inicio del incidente

M6 comienza únicamente cuando:

~~~text
M0–M5 cerradas
checkpoint completado
rotación realizada
handoff terminado
instructor activa el escenario
~~~

El alumnado no debe saber de antemano la implementación exacta del fallo.

Sí debe saber que:

~~~text
algo cambió
debe observar primero
debe comparar capas
no debe ejecutar recovery inmediatamente
~~~

---

# 3. Primera regla del incidente

Durante M6:

> **No se arregla nada. Solo se observa.**

Permitido:

~~~text
reproducir
mirar Network
consultar status
consultar health
anotar síntomas
~~~

No permitido:

~~~text
recover
reset
reiniciar
cambiar datos
probar comandos al azar
~~~

---

# 4. Objetivo de M6

M6 debe producir un contraste mínimo:

~~~text
algo falla
+
algo sigue funcionando
~~~

Salida esperada:

~~~text
Ranking no carga
pero aplicación general sigue viva
~~~

No se exige todavía conocer la causa.

---

# 5. Entrada a M7

El equipo entra a M7 con una primera pregunta:

> **¿Qué capa explica mejor que falle solo esta parte?**

No se pide una respuesta correcta.

Se pide una primera hipótesis comprobable.

---

# 6. Protocolo de diagnóstico en siete preguntas

Durante M7 el equipo debe responder, en orden:

~~~text
1. ¿Qué falla exactamente?
2. ¿Qué sigue funcionando?
3. ¿Qué evidencia tenemos desde Interfaz?
4. ¿Qué evidencia tenemos desde API?
5. ¿Qué evidencia tenemos desde Datos?
6. ¿Qué evidencia tenemos desde Sistemas?
7. ¿Qué explicación encaja mejor con todo lo anterior?
~~~

Después de recovery se agrega:

~~~text
8. ¿Qué cambió?
9. ¿Qué se preservó?
~~~

---

# 7. Estado de hipótesis

Cada equipo mantiene como máximo:

~~~text
1 hipótesis principal
1 hipótesis alternativa
~~~

No se crea una lista infinita.

Formato:

~~~text
H1 — Principal
“Creemos que ____________________”

H2 — Alternativa
“También podría ser ____________________”
~~~

Una hipótesis debe poder conectarse con una observación concreta.

---

# 8. Regla para descartar

Una hipótesis se descarta solo con evidencia.

Ejemplo:

~~~text
Hipótesis:
“PostgreSQL completo está caído.”

Evidencia:
psql sigue accediendo a lab.my_team_score.

Resultado:
hipótesis descartada.
~~~

No se acepta:

~~~text
“no creo que sea eso”
~~~

como descarte.

---

# 9. Barrera pedagógica previa al recover

Antes de ejecutar:

~~~bash
clublab recover ranking-db
~~~

el equipo debe poder decir:

~~~text
Causa propuesta:
________________________

Evidencia 1:
________________________

Evidencia 2:
________________________

Hipótesis descartada:
________________________

Qué esperamos que cambie después del recover:
________________________
~~~

Mínimos obligatorios:

~~~text
>= 2 evidencias
>= 2 capas diferentes
>= 1 hipótesis descartada
>= 1 predicción de recuperación
~~~

---

# 10. Quién autoriza el recover

El Operador de Sistemas propone la ejecución.

El equipo confirma que la barrera está completa.

El instructor:

~~~text
no necesita aprobar verbalmente cada recover
~~~

si el material y la dinámica ya dejaron clara la regla.

Pero puede detenerlo si observa:

~~~text
diagnóstico vacío
copia mecánica
equipo saltando rondas
~~~

---

# 11. Evidencia mínima por capa

## Interfaz

~~~text
vista afectada
request asociada
status visible
~~~

## API

~~~text
/api/ranking
status
comparación con /api/health u otro endpoint sano
~~~

## Datos

~~~text
DB accesible
lab.my_team_score consultable
score preservado
~~~

## Sistemas

~~~text
componentes vivos
health
lablog relevante
~~~

Una misma observación no cuenta como dos evidencias solo por escribirla dos veces.

---

# 12. Evidencia fuerte vs evidencia débil

## Fuerte

~~~text
status HTTP
respuesta JSON
consulta SQL
health
lablog
cambio antes/después
~~~

## Débil

~~~text
“parece que”
“creo que”
“seguro es”
“la pantalla se ve rara”
~~~

La evidencia débil puede iniciar una hipótesis, pero no cerrar el diagnóstico.

---

# 13. Criterio de causa aceptable

No es necesario que el alumno reproduzca el nombre interno exacto de la clase o adapter.

Es suficiente una explicación técnicamente coherente como:

> **“La API sigue viva y la base también, pero el flujo del ranking está intentando usar una dependencia de base de datos que no puede resolver.”**

No se exige memorizar:

~~~text
RankingFaultAdapter
ScenarioAwareRankingRepository
ENOTFOUND
~~~

aunque pueden aparecer como evidencia.

---

# 14. Recovery como experimento

El recovery no es “el botón correcto”.

Es una última prueba.

Antes:

~~~text
predicción
~~~

Acción:

~~~bash
clublab recover ranking-db
~~~

Después:

~~~text
observar
verificar
registrar
~~~

---

# 15. Verificación posterior obligatoria

No se considera recuperado solo porque el comando respondió “success”.

Debe comprobarse:

~~~text
R4 → health sano
R2 → /api/ranking 200
R3 → score modificado en M4 sigue presente
R1 → ranking visible otra vez
~~~

Resultado:

~~~text
servicio recuperado
+
estado del alumno preservado
~~~

---

# 16. Recovery falla

Si el recovery del alumno no funciona:

~~~text
1. detener nuevas acciones
2. conservar evidencia
3. avisar al instructor
~~~

El alumno no escala a:

~~~text
docker
sudo
reset
clublabctl
~~~

El instructor decide:

~~~text
clublabctl recover
o
reset explícito
o
spare
~~~

Esto no penaliza al equipo.

---

# 17. Participación obligatoria en M7

En equipos de cuatro o cinco:

~~~text
R1 aporta >= 1 evidencia
R2 aporta >= 1 evidencia
R3 aporta >= 1 evidencia
R4 aporta >= 1 evidencia
~~~

R5, si existe:

~~~text
conecta >= 2 evidencias
o
formula/descarta una hipótesis
~~~

No basta con que una persona encuentre todo y las demás asientan.

---

# 18. Regla anti-monopolio

Se congela la regla:

> **Quien ya encontró una respuesta no puede quitar el teclado; debe convertir su conocimiento en una pregunta.**

Ejemplos:

No:

~~~text
“Dame, yo sé hacerlo.”
~~~

Sí:

~~~text
“¿Qué endpoint podrías comparar con ranking?”
“¿Qué comando te permite comprobar si DB sigue viva?”
“¿Qué esperas ver antes de ejecutar eso?”
~~~

---

# 19. Intervención ante un integrante muy avanzado

Si un integrante resuelve mentalmente el incidente muy pronto:

Su tarea cambia a:

~~~text
formular preguntas
proponer una hipótesis alternativa
buscar evidencia que pueda falsar su propia idea
explicar por qué una evidencia importa
~~~

No puede:

~~~text
dictar toda la secuencia
tomar el teclado
usar endpoints internos
adelantar recover
~~~

---

# 20. Intervención ante un principiante bloqueado

Secuencia de apoyo:

~~~text
1. recordar la pregunta del rol
2. señalar la herramienta
3. ofrecer dos opciones
4. proporcionar el comando
5. pedir interpretación del resultado
~~~

Ejemplo:

~~~text
“Tu pregunta es si la API sigue viva.”
→
“¿Qué herramienta usaste en M2?”
→
“¿Compararías ranking con health o con SQL?”
→
dar curl si sigue bloqueado
→
“¿Qué demuestra ese 200?”
~~~

El comando puede ser entregado.

La interpretación no.

---

# 21. Principiante que teme romper algo

Mensaje operativo:

~~~text
“Tu entorno está diseñado para experimentar.
Tus permisos están limitados.
Sigue la misión y verifica antes de modificar.”
~~~

Para M4 se refuerza:

~~~text
SELECT antes
UPDATE controlado
SELECT después
~~~

---

# 22. Dos principiantes bloqueados simultáneamente

El instructor no resuelve ambos pasos.

Debe dividir:

~~~text
Persona A → ejecutar
Persona B → predecir/verificar
~~~

y después intercambiar.

Si persiste el bloqueo:

~~~text
usar siguiente nivel de pista
~~~

---

# 23. Escalera de pistas

Se congela una escala de cinco niveles:

## P0 — Sin pista

~~~text
solo objetivo de misión
~~~

## P1 — Pregunta guía

~~~text
“¿Qué sigue funcionando?”
~~~

## P2 — Señalar capa/herramienta

~~~text
“Compara desde API.”
~~~

## P3 — Acción concreta

~~~text
“Consulta /api/health y /api/ranking.”
~~~

## P4 — Comando/evidencia de desbloqueo

~~~text
se entrega comando exacto
o una evidencia parcial
~~~

Regla:

~~~text
subir un nivel a la vez
~~~

---

# 24. Uso de P4

P4 no significa “dar la respuesta”.

Puede entregar:

~~~text
comando
endpoint
consulta
línea de log relevante
~~~

Pero todavía se pide:

~~~text
¿Qué significa?
¿Qué hipótesis apoya?
¿Qué hipótesis descarta?
~~~

---

# 25. Equipo demasiado rápido antes del incidente

No se adelanta M6.

Extensiones seguras:

~~~text
E1 — identificar requestId y seguirlo en evidencia
E2 — comparar /api/team con /api/ranking
E3 — explicar por qué health no equivale a “todo funciona”
E4 — encontrar otra relación entre datos y UI
E5 — mejorar el diagrama de arquitectura
~~~

No permitido:

~~~text
buscar el escenario
leer documentación del fallo
probar recover
usar /internal/*
~~~

---

# 26. Equipo rápido durante M7

Si diagnostica correctamente antes del tiempo esperado:

Antes de recover debe realizar una de estas extensiones:

~~~text
buscar una tercera evidencia
formular una hipótesis alternativa
explicar por qué “DB caída” es incorrecto
explicar qué preservará recover
~~~

Después de recover:

~~~text
demostrar que M4 sobrevivió
explicar qué capa cambió y cuál no
~~~

---

# 27. Equipo demasiado lento

Objetivo:

~~~text
preservar los descubrimientos centrales
~~~

No se elimina:

~~~text
M4 — persistencia/propagación
M7 — diagnóstico
M8 — reconstrucción
~~~

Se puede simplificar:

~~~text
cantidad de vistas en M0
número de endpoints explorados
cantidad de objetos SQL inspeccionados
detalle de M5
extensiones
~~~

---

# 28. Orden de intervención para equipo lento

~~~text
1. P1 pregunta
2. P2 herramienta
3. P3 acción
4. P4 comando
5. instructor elimina una tarea secundaria
~~~

No saltar directamente a la causa.

---

# 29. Umbral de retraso

El instructor considera que un equipo necesita intervención cuando:

~~~text
lleva > 3 minutos sin producir nueva evidencia
o
repite la misma acción sin una hipótesis nueva
~~~

No se usa solamente “va una misión atrás” como criterio.

---

# 30. Rol termina antes que los demás

Si una persona termina su parte:

Puede asumir temporalmente:

~~~text
OBSERVAR
VERIFICAR
REGISTRAR
~~~

No asume automáticamente OPERAR.

También puede:

~~~text
preparar una pregunta
comprobar consistencia
actualizar diagrama
~~~

---

# 31. Una persona ausente antes de empezar

Se aplica inmediatamente la configuración del tamaño real:

~~~text
5 → 4
4 → 3
3 → 2
~~~

No se mantiene un “rol fantasma”.

---

# 32. Una persona se retira durante M0–M5

Procedimiento:

~~~text
1. pausar máximo 60 s
2. identificar roles restantes
3. aplicar configuración inferior
4. transferir evidencia mínima
5. continuar
~~~

No reiniciar la clase del team.

---

# 33. Una persona se retira después de la rotación

No se intenta reconstruir la asignación original.

Se redistribuyen los **roles actuales**.

Prioridad:

~~~text
mantener R1
mantener R4
combinar R2+R3 si hace falta
~~~

Motivo:

~~~text
UI y Sistemas marcan inicio/fin del diagnóstico
API+Datos pueden secuenciarse
~~~

---

# 34. Laptop principal falla

Primera respuesta:

~~~text
no tocar servidor
~~~

Opciones en orden:

~~~text
1. otra laptop del mismo team
2. navegador en otra máquina + mismo URL
3. spare si el problema es del entorno y no del equipo local
~~~

El fallo físico de laptop no justifica reset.

---

# 35. Solo una laptop y falla

El instructor distingue:

~~~text
problema local
vs
problema ClubLab
~~~

Si es local:

~~~text
cambiar dispositivo
~~~

Si el stack también está comprometido:

~~~text
usar protocolo de recovery/spare
~~~

---

# 36. Varias laptops y resultados diferentes

Antes de asumir un bug:

~~~text
verificar mismo team
misma URL/puerto
misma sesión
misma vista
~~~

El Relator o REGISTRAR conserva cuál máquina produjo cada evidencia.

---

# 37. Equipo usa el team equivocado

Se detiene inmediatamente.

Procedimiento:

~~~text
1. no continuar modificaciones
2. confirmar team asignado
3. volver a URL/terminal correctos
4. informar instructor si hubo UPDATE
~~~

El instructor decide si requiere reset del team afectado.

No se oculta el error.

---

# 38. Equipo intenta acceder a otro team

Se trata como problema pedagógico y de seguridad.

~~~text
detener
recordar alcance
registrar si hubo acceso efectivo
informar instructor
~~~

La infraestructura debería bloquearlo.

Si no lo bloquea:

~~~text
hallazgo de seguridad
→ no continuar clase normal
→ escalar para corrección
~~~

---

# 39. Equipo ejecuta recover antes de tiempo

No se reinicia la misión automáticamente.

Procedimiento:

~~~text
1. marcar “recover prematuro”
2. registrar qué evidencia faltaba
3. instructor puede recargar escenario
4. repetir diagnóstico desde la evidencia faltante
~~~

No se castiga con pérdida de puntos.

---

# 40. Equipo ejecuta UPDATE incorrecto en M4

Si el permiso lo bloquea:

~~~text
usarlo como evidencia de least privilege
~~~

Si modificó score permitido pero valor no previsto:

~~~text
comprobar antes/después
continuar con el valor real
~~~

No hace falta reset salvo que impida la misión.

---

# 41. Equipo pierde el score inicial

No se inventa.

Debe recuperarlo desde evidencia previa o consultar el estado actual.

Si necesita demostrar cambio y no registró el valor anterior:

~~~text
el instructor puede proporcionar el seed esperado
~~~

pero se marca como evidencia faltante, no como fallo técnico.

---

# 42. Equipo no logra formular hipótesis

Usar plantilla de contraste:

> **“Sabemos que ____ funciona, pero ____ falla. Entonces el problema probablemente está entre ____ y ____.”**

Esta plantilla guía sin dar la causa.

---

# 43. Equipo formula una causa demasiado específica

Ejemplo:

~~~text
“Se cayó Docker DNS.”
~~~

Respuesta del instructor:

> **“¿Qué evidencia demuestra Docker DNS y no solamente una dependencia del ranking?”**

Se empuja a una formulación soportada por evidencia.

---

# 44. Equipo formula una causa demasiado vaga

Ejemplo:

~~~text
“Falla el backend.”
~~~

Respuesta:

> **“¿Todo el backend? ¿Qué endpoint contradice esa idea?”**

Objetivo:

~~~text
acotar
sin entregar respuesta
~~~

---

# 45. Discusión sin ejecutar

Si pasan más de 2 minutos debatiendo sin prueba:

El rol VERIFICAR debe proponer:

~~~text
la acción más barata que pueda distinguir H1 de H2
~~~

Ejemplo:

~~~text
H1 DB caída
H2 solo ranking roto

Prueba barata:
psql o /api/health
~~~

---

# 46. Ejecución sin discutir

Si encadenan comandos sin explicar:

El instructor detiene con:

> **“Antes del siguiente comando: ¿qué esperan ver y qué significaría?”**

No se permite continuar hasta obtener una predicción breve.

---

# 47. Conflicto entre integrantes

Si hay dos explicaciones:

~~~text
no votar
no elegir por experiencia
~~~

Se escribe:

~~~text
H1
H2
~~~

y se busca una prueba discriminante.

La evidencia decide.

---

# 48. R5 domina la discusión

R5 coordina, no sentencia.

Debe preguntar:

~~~text
“¿Qué evidencia tiene Interfaz?”
“¿Qué evidencia tiene API?”
~~~

No:

~~~text
“la causa es esta”
~~~

sin recoger las otras capas.

---

# 49. R5 queda pasivo

Se le asigna inmediatamente una tarea:

~~~text
identificar contradicción
resumir dos evidencias
formular H2
preparar M8
~~~

---

# 50. M8 después de un equipo muy asistido

Aunque recibió P3/P4, el equipo debe explicar:

~~~text
qué hizo
qué vio
qué significa
qué descartó
~~~

El objetivo final sigue siendo comprensión, no independencia absoluta.

---

# 51. M8 después de un fallo técnico real

Si el stack no pudo recuperarse y se usó spare:

El equipo puede explicar:

~~~text
evidencia reunida
causa que estaba investigando
qué parte no pudo validar
por qué se cambió a spare
~~~

No se finge un resultado que no ocurrió.

---

# 52. Papel del instructor durante M7

El instructor actúa como:

~~~text
facilitador
control temporal
gestor de pistas
observador de seguridad
gestor de contingencias
~~~

No como:

~~~text
operador principal
debugger del equipo
persona que revela causa
~~~

---

# 53. Qué debe escuchar el instructor

Indicadores positivos:

~~~text
“esperamos que…”
“esto descarta…”
“pero health sigue 200…”
“veamos desde otra capa…”
“el score sigue ahí…”
~~~

Indicadores de intervención:

~~~text
“prueba esto a ver”
“reinicia”
“dame el teclado”
“seguro es Docker”
“ya funcionó, vámonos”
~~~

---

# 54. Nivel de intervención

El instructor intenta siempre:

~~~text
pregunta
antes que pista

pista
antes que comando

comando
antes que explicación

explicación parcial
antes que respuesta completa
~~~

---

# 55. Seguridad durante contingencias

Nunca se usa una contingencia que requiera:

~~~text
dar clublabctl al alumno
dar SSH al host
dar Docker socket
dar credencial migrator/owner
desactivar aislamiento
compartir tokens administrativos
~~~

La contingencia debe mantener el modelo de seguridad.

---

# 56. Continuidad con spare

Si el equipo pasa a spare:

Se informa claramente:

~~~text
“Este es un entorno limpio de reemplazo.”
~~~

No se promete:

~~~text
score anterior
lablogs anteriores
misma sesión
~~~

El equipo reconstruye solamente el mínimo necesario para continuar.

---

# 57. Prioridad de contingencias

Orden oficial:

~~~text
C1 — pista pedagógica
C2 — cambio de operador/configuración
C3 — recovery del alumno
C4 — recovery del instructor
C5 — reset explícito del team
C6 — spare
~~~

No saltar a reset/spare por un bloqueo conceptual.

---

# 58. Antipatrones cerrados

## CP-01 — Recover como primer diagnóstico

Mitigación:

~~~text
barrera de evidencia
~~~

## CP-02 — Avanzado toma control

Mitigación:

~~~text
convertir respuesta en pregunta
~~~

## CP-03 — Principiante solo copia

Mitigación:

~~~text
pedir predicción e interpretación
~~~

## CP-04 — Equipo rápido adelanta escenario

Mitigación:

~~~text
extensiones seguras
~~~

## CP-05 — Equipo lento pierde M7

Mitigación:

~~~text
recortar tareas secundarias
~~~

## CP-06 — Ausencia deja rol vacío

Mitigación:

~~~text
reconfigurar tamaño real
~~~

## CP-07 — Error técnico se trata como error del alumno

Mitigación:

~~~text
separar problema pedagógico de infraestructura
~~~

## CP-08 — Se finge una validación que no ocurrió

Mitigación:

~~~text
M8 declara límites reales de evidencia
~~~

---

# 59. Decisiones cerradas

### DC6-01
M6 es solo observación; no recovery.

### DC6-02
M7 usa una hipótesis principal y una alternativa como máximo.

### DC6-03
Toda hipótesis descartada requiere evidencia.

### DC6-04
Recover requiere dos evidencias de al menos dos capas, una hipótesis descartada y una predicción.

### DC6-05
El success del comando recover no basta; la recuperación se verifica en cuatro capas.

### DC6-06
Se adopta escalera de pistas P0–P4.

### DC6-07
P4 puede dar comando, pero nunca elimina la interpretación.

### DC6-08
Un equipo rápido usa extensiones; no adelanta M6.

### DC6-09
Un equipo lento conserva M4, M7 y M8.

### DC6-10
Tres minutos sin evidencia nueva es señal de intervención.

### DC6-11
Una ausencia provoca reconfiguración inmediata al tamaño real.

### DC6-12
Una laptop rota no justifica reset del stack.

### DC6-13
Un recover prematuro puede corregirse recargando el escenario.

### DC6-14
Conflictos de hipótesis se resuelven con una prueba discriminante, no por votación.

### DC6-15
Las contingencias nunca relajan seguridad.

---

# 60. Criterios de aceptación

~~~text
[x] protocolo M6
[x] protocolo M7
[x] barrera de recovery
[x] verificación post-recover
[x] evidencia mínima por capa
[x] evidencia fuerte/débil
[x] regla anti-monopolio
[x] apoyo a principiantes
[x] escalera P0–P4
[x] equipos rápidos
[x] equipos lentos
[x] rol que termina antes
[x] ausencia antes/durante
[x] laptop fallida
[x] team equivocado
[x] recover prematuro
[x] error M4
[x] conflicto de hipótesis
[x] papel del instructor
[x] contingencias seguras
[x] prioridad C1–C6
~~~

# BLOQUE C — COMPLETADO

El siguiente bloque validará la dinámica completa para equipos de 2, 3, 4 y 5 personas y consolidará D05.
