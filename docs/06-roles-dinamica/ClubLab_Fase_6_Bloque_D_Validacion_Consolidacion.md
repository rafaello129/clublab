# ClubLab — Fase 6 / Bloque D
## Validación de dinámica y consolidación D05

**Proyecto:** ClubLab v1  
**Fase:** 6 — Roles y dinámica de equipos  
**Bloque:** D  
**Estado:** CERRADO PARA v1  
**Dependencias:** Bloques A–C + D01 + D04  
**Entregable consolidado:** D05_Roles_y_Dinamica_Equipos_ClubLab.md

---

# 1. Propósito

Este bloque valida que la dinámica diseñada en Fase 6:

~~~text
cabe en el cronograma
funciona con equipos de distintos tamaños
mantiene participación real
no rompe el modelo de seguridad
preserva el objetivo pedagógico
~~~

La validación de este bloque es de **mesa y diseño**.

No sustituye:

~~~text
ensayo real
prueba sobre Tulum
medición con alumnos
validación de tiempos con infraestructura real
~~~

Eso pertenece a Fase 9.

---

# 2. Configuraciones a validar

Se revisan cuatro configuraciones:

~~~text
V2 — equipo de 2 personas
V3 — equipo de 3 personas
V4 — equipo de 4 personas
V5 — equipo de 5 personas
~~~

Configuración de referencia:

~~~text
V4
~~~

---

# 3. Criterios comunes

Cada configuración debe cumplir:

~~~text
todos tienen responsabilidad clara
todos operan al menos una herramienta
todos producen al menos una evidencia
la rotación cambia la capa principal
M7 no queda concentrada en una sola persona
M8 puede explicarse como equipo
ningún rol requiere privilegios adicionales
~~~

---

# 4. Validación V4 — cuatro personas

## Inicio

~~~text
A → R1 Interfaz
B → R2 API
C → R3 Datos
D → R4 Sistemas
~~~

## Después de M5

~~~text
A → R4
B → R3
C → R2
D → R1
~~~

## Resultado esperado

~~~text
4/4 personas operan
4/4 roles base cubiertos
4/4 capas cubiertas
rotación simétrica
M7 distribuida en cuatro rondas
~~~

## Evaluación

~~~text
VALIDADO EN DISEÑO
~~~

Es la configuración más limpia y se mantiene como referencia oficial.

---

# 5. Validación V5 — cinco personas

## Inicio

~~~text
A → R1
B → R2
C → R3
D → R4
E → R5
~~~

## Rotación

~~~text
A ↔ D
B ↔ C
E permanece R5
~~~

## Riesgo principal

~~~text
R5 se vuelve pasivo
~~~

## Control

R5 debe:

~~~text
mantener evidencia
conectar al menos dos capas
formular o descartar hipótesis
coordinar M8
~~~

## Evaluación

~~~text
VALIDADO EN DISEÑO
~~~

La quinta persona añade capacidad de síntesis sin alterar el flujo base.

---

# 6. Validación V3 — tres personas

## Inicio

~~~text
A → R1
B → R2 + R3
C → R4
~~~

## Rotación

~~~text
A → R4
B → R1
C → R2 + R3
~~~

## Riesgo principal

~~~text
persona con R2+R3 monopoliza demasiadas acciones
~~~

## Control

~~~text
API y Datos se ejecutan en rondas separadas
se anuncia cambio de rol
registro se reparte cuando la persona combinada opera
~~~

## Evaluación

~~~text
VALIDADO EN DISEÑO CON CARGA ADICIONAL
~~~

Es viable, pero requiere más disciplina que V4/V5.

---

# 7. Validación V2 — dos personas

## Inicio

~~~text
A → R1 + R2
B → R3 + R4
~~~

## Rotación

~~~text
A → R3 + R4
B → R1 + R2
~~~

## Riesgo principal

~~~text
sobrecarga cognitiva
~~~

## Control

~~~text
trabajo secuencial
una herramienta principal a la vez
declarar el rol activo
más apoyo de pistas si se estanca
~~~

## Evaluación

~~~text
VALIDADO COMO CONTINGENCIA
~~~

No es la configuración objetivo, pero puede conservar los objetivos centrales.

---

# 8. Validación temporal

Se mantiene el cronograma de D01:

| Tramo | Duración |
|---|---:|
| Bienvenida | 5 min |
| Equipos + acceso | 5 min |
| M0 | 6 min |
| M1 | 9 min |
| M2 | 9 min |
| M3 | 11 min |
| M4 | 11 min |
| M5 | 9 min |
| Checkpoint | 3 min |
| Rotación + handoff | 2 min |
| M6 | 6 min |
| M7 | 23 min |
| Buffer | 2 min |
| M8 | 13 min |
| Cierre | 6 min |

Total:

~~~text
120 minutos
~~~

---

# 9. Validación de asignación

Objetivo:

~~~text
formar equipo + asignar roles + acceso <= 5 min
~~~

La parte de roles debe consumir:

~~~text
<= 2 min
~~~

Condición:

~~~text
sin tests previos
sin explicación extensa de cada especialidad
sin negociación larga
~~~

---

# 10. Validación de handoff

Objetivo oficial:

~~~text
90–100 s
~~~

Máximo:

~~~text
2 min
~~~

Si el handoff excede dos minutos:

~~~text
usar plantilla de cuatro campos
eliminar historia secundaria
hacer readback breve
~~~

No se roba tiempo a M7.

---

# 11. Validación de M7

M7 conserva:

~~~text
23 minutos
~~~

Distribución orientativa:

~~~text
Ronda Interfaz   3–4 min
Ronda API        3–4 min
Ronda Datos      3–4 min
Ronda Sistemas   4–5 min
Hipótesis        2–3 min
Recover          1–2 min
Verificación     3–4 min
~~~

No es un cronómetro rígido.

Sirve para detectar si una ronda monopoliza el incidente.

---

# 12. Validación de participación — V4

Al terminar M7:

~~~text
A operó antes y después de rotar
B operó antes y después de rotar
C operó antes y después de rotar
D operó antes y después de rotar
~~~

Cada integrante debe haber:

~~~text
usado al menos una herramienta
aportado al menos una evidencia
explicado al menos una relación causal
~~~

---

# 13. Validación de participación — V5

Además de lo anterior para R1–R4:

R5 debe haber:

~~~text
registrado evidencia
conectado dos capas
intervenido en hipótesis
participado en M8
~~~

Si R5 solo toma notas:

~~~text
validación fallida
~~~

---

# 14. Validación de participación — V3

Se comprueba:

~~~text
A opera Interfaz y después Sistemas
B opera API/Datos y después Interfaz
C opera Sistemas y después API/Datos
~~~

La persona con bundle doble no puede encadenar ambas capas sin pausa verbal.

---

# 15. Validación de participación — V2

Se comprueba:

~~~text
A opera al menos una acción de cada bundle que recibe
B opera al menos una acción de cada bundle que recibe
~~~

El objetivo no es cubrir la misma cantidad de acciones que V4.

El objetivo es conservar:

~~~text
UI
API
Datos
Sistemas
rotación
diagnóstico
recovery
reconstrucción
~~~

---

# 16. Validación de evidencia

Antes de recover:

~~~text
>= 2 evidencias
>= 2 capas
>= 1 hipótesis descartada
>= 1 predicción
~~~

Después:

~~~text
health validado
ranking validado
score preservado
UI recuperada
~~~

---

# 17. Validación de M8

M8 debe producir:

~~~text
diagrama final
+
explicación oral
~~~

Para V4/V5:

~~~text
cada integrante explica >= 1 relación entre capas
~~~

Para V2/V3:

~~~text
cada integrante explica >= 2 relaciones
~~~

No se acepta:

~~~text
una sola persona explica todo
~~~

---

# 18. Validación de comprensión del rol

Cada rol base debe poder explicarse en:

~~~text
<= 60 segundos
~~~

Debe responder solo:

~~~text
qué pregunta responde
qué herramienta usa
qué evidencia produce
qué no debe tocar
~~~

Si necesita explicar arquitectura completa:

~~~text
el contrato del rol es demasiado complejo
~~~

---

# 19. Validación de seguridad

Ninguna configuración necesita:

~~~text
SSH
sudo
docker
clublabctl
host shell
control token
migrator
owner
otro team
~~~

Herramientas del alumno:

~~~text
Browser
DevTools
curl
psql
clublab
~~~

Resultado:

~~~text
VALIDADO EN DISEÑO
~~~

La validación empírica depende de Fase 3 + implementación real.

---

# 20. Validación de contingencias

La dinámica conserva el objetivo ante:

~~~text
equipo rápido
equipo lento
integrante avanzado
principiante bloqueado
ausencia
laptop fallida
recover prematuro
fallo de recovery
uso de spare
~~~

Condición:

> **La contingencia modifica el camino, no el objetivo de aprendizaje.**

---

# 21. Qué se preserva siempre

No se elimina de la experiencia normal o reducida:

~~~text
M4
M7
M8
rotación
evidencia
diagnóstico
~~~

Son el núcleo de ClubLab #01.

---

# 22. Qué puede comprimirse

Si falta tiempo:

~~~text
exploración de M0
endpoints secundarios
objetos SQL secundarios
explicación detallada de M5
extensiones
~~~

---

# 23. Validación de carga del instructor

El instructor no debería necesitar:

~~~text
operar terminal por cada team
dictar comandos permanentemente
autorizar manualmente cada acción
resolver cada hipótesis
~~~

Debe poder circular entre equipos usando:

~~~text
estado
evidencia
nivel de pista
cronograma
~~~

Esto queda como criterio para Fase 9.

---

# 24. Validación de autonomía

Un equipo ideal debe poder avanzar M0–M5 con:

~~~text
material de misión
cheat sheet
rol
acceso preparado
~~~

y recurrir al instructor principalmente para:

~~~text
pistas
bloqueos
contingencias
seguridad
~~~

---

# 25. Tabla de validación de diseño

| ID | Criterio | V2 | V3 | V4 | V5 |
|---|---|---|---|---|---|
| VD6-01 | Todas las capas cubiertas | PASS diseño | PASS diseño | PASS diseño | PASS diseño |
| VD6-02 | Rotación viable | PASS contingencia | PASS | PASS | PASS |
| VD6-03 | Handoff <=2 min | PASS previsto | PASS previsto | PASS previsto | PASS previsto |
| VD6-04 | Todos operan | PASS previsto | PASS previsto | PASS previsto | PASS previsto |
| VD6-05 | M7 distribuida | PASS secuencial | PASS controlado | PASS | PASS |
| VD6-06 | Recovery con evidencia | PASS | PASS | PASS | PASS |
| VD6-07 | M8 colaborativa | PASS | PASS | PASS | PASS |
| VD6-08 | Seguridad sin privilegios | PASS diseño | PASS diseño | PASS diseño | PASS diseño |
| VD6-09 | Compatible 120 min | RIESGO | PASS con control | PASS | PASS |
| VD6-10 | Carga cognitiva | ALTA | MEDIA | BAJA | BAJA |

La palabra PASS en esta tabla significa:

~~~text
coherencia de diseño
~~~

No significa:

~~~text
prueba empírica ejecutada
~~~

---

# 26. Riesgos que pasan a Fase 9

## R6-01 — Equipo de dos

Puede necesitar más de 120 min.

## R6-02 — Handoff

Puede extenderse si las tarjetas son demasiado verbosas.

## R6-03 — M7

Los alumnos pueden querer ejecutar recover antes de completar evidencia.

## R6-04 — R5

Puede quedar pasivo si el material no le asigna acciones concretas.

## R6-05 — Pistas

El instructor puede subir niveles demasiado rápido.

## R6-06 — Varias laptops

Puede fragmentar al equipo.

## R6-07 — psql

Puede consumir demasiado tiempo en principiantes.

---

# 27. Métricas para el ensayo

Fase 9 deberá medir:

~~~text
tiempo real de asignación
tiempo real de handoff
tiempo M0–M8
pista máxima usada por misión
número de intervenciones del instructor
número de veces que cambia OPERAR
número de evidencias por integrante
recover prematuros
errores de team
tiempo de recovery
tiempo de contingencia
~~~

---

# 28. Umbrales de revisión

Revisar Fase 6 si en ensayo ocurre alguno:

~~~text
handoff > 3 min
M7 < 15 min por retrasos previos
una persona opera > 60% de acciones
dos o más personas no aportan evidencia
> 50% equipos necesita P4 en la misma misión
recover prematuro en mayoría de equipos
M8 se reduce a < 8 min
~~~

---

# 29. Resultado del bloque

La dinámica es coherente para:

~~~text
3–5 integrantes
~~~

y utilizable como contingencia para:

~~~text
2 integrantes
1 integrante
~~~

La configuración recomendada continúa siendo:

~~~text
4 integrantes
~~~

---

# 30. Decisiones cerradas

### DD6-01
La validación de Bloque D es de diseño, no empírica.

### DD6-02
V4 sigue siendo configuración de referencia.

### DD6-03
V2 se acepta como contingencia con riesgo temporal.

### DD6-04
M4, M7 y M8 no se eliminan.

### DD6-05
Handoff mantiene máximo de dos minutos.

### DD6-06
M7 conserva 23 minutos en versión normal.

### DD6-07
M8 exige participación distribuida.

### DD6-08
PASS de diseño no equivale a prueba real.

### DD6-09
Los riesgos abiertos se transfieren a Fase 9.

### DD6-10
Las métricas de ensayo se congelan en este bloque.

---

# 31. Criterios de aceptación

~~~text
[x] validación V2
[x] validación V3
[x] validación V4
[x] validación V5
[x] validación temporal
[x] validación de handoff
[x] validación M7
[x] validación de participación
[x] validación de M8
[x] validación de seguridad
[x] validación de contingencias
[x] riesgos para Fase 9
[x] métricas de ensayo
[x] umbrales de revisión
[x] consolidación D05
~~~

# BLOQUE D — COMPLETADO

# FASE 6 — CERRADA A NIVEL DE DISEÑO
