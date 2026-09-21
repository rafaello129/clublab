# D05 — Roles y Dinámica de Equipos de ClubLab

**Proyecto:** ClubLab v1  
**Fase:** 6  
**Versión:** v1  
**Estado:** FINAL DE DISEÑO  
**Validación empírica:** pendiente en Fase 9

---

# 1. Propósito

D05 consolida el modelo humano de ClubLab #01.

Define:

~~~text
roles
responsabilidades
herramientas
evidencia
rotación
handoff
participación
diagnóstico
pistas
contingencias
validación de dinámica
~~~

La meta es impedir que la práctica dependa de una sola persona y convertir la investigación en una actividad de equipo.

---

# 2. Roles oficiales

~~~text
R1 — Explorador de Interfaz
R2 — Investigador de API
R3 — Investigador de Datos
R4 — Operador de Sistemas
R5 — Relator / Analista opcional
~~~

R1–R4 son los roles base.

R5 se recomienda con equipos de cinco.

---

# 3. R1 — Explorador de Interfaz

Pregunta:

> **¿Qué ve el usuario y qué ocurre cuando interactúa?**

Herramientas:

~~~text
Browser
DevTools
Network
Fetch/XHR
Headers
Response
~~~

Lidera principalmente:

~~~text
M0
M1
M6
~~~

Evidencia:

~~~text
pantalla
request
método
status
dato/error
~~~

No utiliza:

~~~text
/internal
clublabctl
infraestructura administrativa
~~~

---

# 4. R2 — Investigador de API

Pregunta:

> **¿Qué pide la aplicación y qué responde el backend?**

Herramientas:

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

Lidera:

~~~text
M2
ronda API de M7
~~~

Evidencia:

~~~text
URL
método
status
JSON
comparación
~~~

No utiliza:

~~~text
/internal/*
control token
otros teams
~~~

---

# 5. R3 — Investigador de Datos

Pregunta:

> **¿Dónde vive la información?**

Herramientas:

~~~text
psql
\dt
\d
SELECT
lab.my_team_score
UPDATE controlado
~~~

Lidera:

~~~text
M3
M4
ronda Datos de M7
~~~

Secuencia de modificación:

~~~text
SELECT
→ verificar
→ predecir
→ UPDATE
→ SELECT
→ comprobar API/UI
~~~

No utiliza roles administrativos ni DDL.

---

# 6. R4 — Operador de Sistemas

Pregunta:

> **¿Qué componentes funcionan y dónde aparece la evidencia del fallo?**

Herramientas:

~~~bash
clublab whoami
clublab status
clublab health
clublab logs api
clublab recover ranking-db
~~~

Lidera:

~~~text
M5
ronda Sistemas de M7
recovery
~~~

No utiliza:

~~~text
docker
sudo
clublabctl
host shell
reset
~~~

---

# 7. R5 — Relator / Analista

Pregunta:

> **¿Qué sabemos y qué estamos suponiendo?**

Responsabilidades:

~~~text
registrar evidencia
mantener hipótesis
detectar contradicciones
conectar capas
coordinar M8
~~~

No debe ser:

~~~text
secretario pasivo
operador permanente
persona que decide la causa por todos
~~~

---

# 8. Funciones momentáneas

Cada misión reparte:

~~~text
OPERAR
OBSERVAR
VERIFICAR
REGISTRAR
~~~

Los roles definen perspectiva.

Las funciones definen qué hace cada persona en ese momento.

---

# 9. POE

Se adopta:

~~~text
Predicción
→ Observación
→ Evidencia
~~~

Antes:

> **“Si hacemos X, esperamos Y.”**

Después:

> **“Observamos Z; esto apoya/contradice nuestra idea porque…”**

---

# 10. Regla del teclado

> **La persona que OPERA controla la herramienta principal.**

Los demás:

~~~text
sugieren
preguntan
observan
verifican
registran
~~~

No deben ejecutar acciones paralelas que adelanten la misión.

---

# 11. Configuración ideal

~~~text
4 personas
~~~

Antes:

~~~text
A → R1
B → R2
C → R3
D → R4
~~~

Después de M5:

~~~text
A → R4
B → R3
C → R2
D → R1
~~~

---

# 12. Equipo de cinco

~~~text
A → R1
B → R2
C → R3
D → R4
E → R5
~~~

R5 permanece durante la rotación.

---

# 13. Equipo de tres

Antes:

~~~text
A → R1
B → R2 + R3
C → R4
~~~

Después:

~~~text
A → R4
B → R1
C → R2 + R3
~~~

API y Datos se mantienen como capas separadas aunque las opere la misma persona.

---

# 14. Equipo de dos

Antes:

~~~text
A → R1 + R2
B → R3 + R4
~~~

Después:

~~~text
A → R3 + R4
B → R1 + R2
~~~

Es una configuración de contingencia.

Trabajo secuencial.

---

# 15. Handoff

Momento:

~~~text
después de M5
antes de M6
~~~

Plantilla:

> **“Yo usé ____. Encontré ____. Recuerda ____. Evita ____.”**

Readback:

> **“Entonces, lo importante para mí es ____.”**

Máximo:

~~~text
2 minutos
~~~

---

# 16. Matriz base M0–M5

| Misión | OPERAR | OBSERVAR | VERIFICAR | REGISTRAR |
|---|---|---|---|---|
| M0 | R1 | R2 | R4 | R3 |
| M1 | R1 | R2 | R4 | R3 |
| M2 | R2 | R1 | R4 | R3 |
| M3 | R3 | R2 | R1 | R4 |
| M4 | R3 | R1 | R2 | R4 |
| M5 | R4 | R1 | R2 | R3 |

---

# 17. M6

Objetivo:

~~~text
observar el incidente
no arreglarlo
~~~

Salida:

~~~text
qué falla
qué sigue funcionando
primer contraste
~~~

Recover está prohibido durante esta fase exploratoria.

---

# 18. M7

Rondas:

~~~text
1. Interfaz
2. API
3. Datos
4. Sistemas
~~~

El incidente se diagnostica por capas.

No por intuición.

---

# 19. Hipótesis

Máximo:

~~~text
H1 principal
H2 alternativa
~~~

No se descarta una hipótesis sin evidencia.

---

# 20. Barrera de recovery

Antes de:

~~~bash
clublab recover ranking-db
~~~

se requiere:

~~~text
>= 2 evidencias
>= 2 capas
>= 1 hipótesis descartada
>= 1 predicción
~~~

---

# 21. Recovery

Se trata como experimento.

Después se valida:

~~~text
R4 → health
R2 → ranking 200
R3 → score preservado
R1 → UI recuperada
~~~

El mensaje de success del comando no basta.

---

# 22. M8

Todos participan.

Salida:

~~~text
diagrama final
explicación oral
~~~

Cada integrante debe explicar al menos una relación entre capas.

---

# 23. Regla anti-monopolio

> **Quien conoce la respuesta la convierte en una pregunta; no toma el teclado.**

El avanzado ayuda con:

~~~text
preguntas
hipótesis alternativa
falsación
interpretación
~~~

No con sustitución del operador.

---

# 24. Principiantes

Pueden recibir:

~~~text
cheat sheet
preguntas
pistas
comandos preparados
~~~

No se evalúa memoria de sintaxis.

Se evalúa:

~~~text
predicción
interpretación
evidencia
~~~

---

# 25. Escalera de pistas

~~~text
P0 — sin pista
P1 — pregunta guía
P2 — señalar capa/herramienta
P3 — acción concreta
P4 — comando/evidencia parcial
~~~

Se sube un nivel a la vez.

P4 no elimina la necesidad de interpretar.

---

# 26. Equipo rápido

No adelanta M6.

Extensiones:

~~~text
requestId
comparación de endpoints
health vs funcionalidad
relaciones DB/UI
diagrama
hipótesis alternativa
~~~

---

# 27. Equipo lento

No se eliminan:

~~~text
M4
M7
M8
~~~

Se simplifican primero tareas secundarias.

Intervenir cuando:

~~~text
> 3 min sin evidencia nueva
o
misma acción sin hipótesis nueva
~~~

---

# 28. Ausencias

Se usa la configuración del tamaño real.

Si alguien se retira:

~~~text
pausa <= 60 s
redistribución
handoff mínimo
continuar
~~~

No hay roles fantasma.

---

# 29. Problemas de laptop

Primero separar:

~~~text
fallo local
vs
fallo ClubLab
~~~

Un problema local no justifica reset.

---

# 30. Team equivocado

~~~text
detener
corregir team
informar si hubo modificación
~~~

No se continúa sobre un entorno ajeno.

---

# 31. Recover prematuro

~~~text
registrar
identificar evidencia faltante
recargar escenario si hace falta
repetir desde la capa faltante
~~~

No tiene penalización.

---

# 32. Contingencias

Orden:

~~~text
C1 pista pedagógica
C2 cambio de operador/configuración
C3 recovery alumno
C4 recovery instructor
C5 reset explícito
C6 spare
~~~

Nunca se relajan controles de seguridad.

---

# 33. Seguridad

Ningún rol o contingencia requiere:

~~~text
SSH
sudo
Docker socket
clublabctl alumno
control token
owner/migrator
producción
otro team
~~~

---

# 34. Validación por tamaño

## 4 personas

~~~text
configuración recomendada
carga baja
rotación simétrica
~~~

## 5 personas

~~~text
válida
R5 debe mantenerse activo
~~~

## 3 personas

~~~text
válida
carga media
bundle API+Datos controlado
~~~

## 2 personas

~~~text
válida como contingencia
carga alta
posible riesgo temporal
~~~

---

# 35. Cronograma

La dinámica conserva el diseño de 120 minutos.

Puntos protegidos:

~~~text
rotación <= 2 min
M7 = 23 min
M8 = 13 min
~~~

---

# 36. Evidencia final mínima

Cada equipo debe terminar con:

~~~text
request identificada
API consultada
dato localizado
modificación extremo a extremo
mapa de componentes
hipótesis descartada
diagnóstico con evidencia
recovery validado
diagrama final
~~~

---

# 37. Métricas para Fase 9

Medir:

~~~text
tiempo de asignación
tiempo de handoff
tiempo por misión
pista máxima
intervenciones del instructor
cambios de operador
evidencias por persona
recover prematuro
errores de team
tiempo de recovery
~~~

---

# 38. Umbrales de revisión

Revisar este diseño si:

~~~text
handoff > 3 min
M7 queda con < 15 min
una persona ejecuta > 60% de acciones
dos o más integrantes no aportan evidencia
> 50% equipos necesita P4 en una misión
recover prematuro es mayoritario
M8 queda con < 8 min
~~~

---

# 39. Estado de validación

Completado:

~~~text
validación de diseño
trazabilidad de roles
configuraciones
rotación
incidente
contingencias
seguridad conceptual
~~~

Pendiente:

~~~text
ensayo con infraestructura real
medición real de tiempos
observación con participantes
ajustes derivados de evidencia
~~~

---

# 40. Estado final

~~~text
Fase 6 / Bloque A ✅
Fase 6 / Bloque B ✅
Fase 6 / Bloque C ✅
Fase 6 / Bloque D ✅
~~~

# FASE 6 — CERRADA A NIVEL DE DISEÑO
