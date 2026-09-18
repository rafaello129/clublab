# P06C — Configuraciones de equipo
## ClubLab #01

**Estado:** FINAL PARA FASE 6 / BLOQUES A–B

---

# 1. Configuración de referencia — 4 personas

Antes de rotar:

~~~text
A → R1 Interfaz
B → R2 API
C → R3 Datos
D → R4 Sistemas
~~~

Después de M5:

~~~text
A → R4 Sistemas
B → R3 Datos
C → R2 API
D → R1 Interfaz
~~~

Esta es la configuración ideal.

Todos los tiempos y materiales se diseñan primero para este caso.

---

# 2. Equipo de 5 personas

Antes:

~~~text
A → R1 Interfaz
B → R2 API
C → R3 Datos
D → R4 Sistemas
E → R5 Relator
~~~

Después:

~~~text
A → R4 Sistemas
B → R3 Datos
C → R2 API
D → R1 Interfaz
E → R5 Relator
~~~

R5 añade registro y consolidación.

No sustituye a ningún rol base.

---

# 3. Equipo de 3 personas

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

Reglas:

~~~text
el bundle API+Datos cambia de persona
quien usa el bundle anuncia qué rol está ejerciendo
A verifica UI durante M3/M4 antes de la rotación
C mantiene visión de estado cuando no lidera antes de la rotación
~~~

La combinación API+Datos es operativa, no conceptual.

---

# 4. Equipo de 2 personas

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

Reglas:

~~~text
trabajo secuencial
una herramienta principal a la vez
decir en voz alta qué rol se está usando
no ejecutar UI/API o Datos/Sistemas como una sola capa
más apoyo del instructor si aparece sobrecarga
~~~

---

# 5. Contingencia individual

~~~text
M0–M1 → Interfaz
M2     → API
M3–M4 → Datos
M5     → Sistemas
M6     → volver a Interfaz
M7     → Interfaz → API → Datos → Sistemas
M8     → integrar
~~~

No existe handoff interpersonal.

La persona declara explícitamente cada cambio de “sombrero”.

El instructor pregunta y pide evidencia, pero no opera por el alumno.

---

# 6. Asignación inicial

Objetivo:

~~~text
< 2 minutos una vez formado el equipo
~~~

Proceso:

~~~text
identificar tamaño del equipo
aplicar configuración
resolver duplicidad de preferencias rápidamente
entregar acceso
iniciar
~~~

No hacer tests previos de personalidad o conocimientos.

---

# 7. Si dos personas quieren el mismo rol

Resolver mediante:

~~~text
sorteo rápido
o
decisión rápida del instructor
~~~

La primera clase busca exploración, no permanencia en el área que ya conocen.

---

# 8. Integrante avanzado

No recibe automáticamente API, Datos o Sistemas.

Puede:

~~~text
hacer preguntas
explicar una idea si se lo piden
ayudar a interpretar evidencia
~~~

No puede:

~~~text
tomar el teclado permanentemente
resolver por todos
adelantar el incidente
~~~

---

# 9. Integrante principiante

Puede ocupar cualquier rol.

Se le permite:

~~~text
cheat sheet
comandos preparados
pistas
preguntas
~~~

Su responsabilidad sigue siendo:

~~~text
predecir
observar
explicar
~~~

---

# 10. Una laptop por equipo

~~~text
función OPERAR → teclado
resto → observar/verificar/registrar
~~~

El cambio de operador debe ser visible.

---

# 11. Varias laptops

Se pueden repartir herramientas:

~~~text
Interfaz → navegador
API/Datos/Sistemas → toolbox/pestañas auxiliares
~~~

Pero todo hallazgo debe volver al equipo.

No son cuatro ejercicios individuales.

Durante M7 se priorizan rondas secuenciales por capa.

---

# 12. Handoff

El protocolo definitivo está en:

~~~text
P06B_Protocolo_Rotacion_y_Handoff.md
~~~

Tiempo máximo:

~~~text
2 minutos
~~~

Toda transferencia termina con readback.
