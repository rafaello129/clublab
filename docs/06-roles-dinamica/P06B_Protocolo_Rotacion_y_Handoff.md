# P06B — Protocolo de rotación y handoff
## ClubLab #01

**Estado:** FINAL PARA FASE 6 / BLOQUE B

---

# 1. Momento de rotación

~~~text
después de M5
antes de M6
~~~

Objetivo:

> Entrar al incidente desde una capa distinta a la utilizada durante el descubrimiento inicial.

---

# 2. Handoff mínimo

Toda transferencia usa:

> **“Yo usé ____. Encontré ____. Recuerda ____. Evita ____.”**

Campos:

~~~text
herramienta
hallazgo
dato clave
precaución
~~~

---

# 3. Readback

Quien recibe termina con:

> **“Entonces, lo importante para mí es ____.”**

Si no puede completar la frase:

~~~text
aclaración máxima 20 s
~~~

---

# 4. Cuatro personas

Rotación:

~~~text
R1 ↔ R4
R2 ↔ R3
~~~

Las dos parejas trabajan simultáneamente.

~~~text
45 s transferencia
30 s readback
15 s cambio físico/herramienta
~~~

Objetivo:

~~~text
90 s
~~~

Máximo:

~~~text
2 min
~~~

---

# 5. Cinco personas

R1–R4 usan el mismo protocolo.

R5 permanece como Relator.

Durante handoff:

~~~text
escucha
detecta omisiones
resume checkpoint
~~~

Resumen R5 máximo:

~~~text
20 s
~~~

---

# 6. Tres personas

Antes:

~~~text
A R1
B R2+R3
C R4
~~~

Después:

~~~text
A R4
B R1
C R2+R3
~~~

Transferencia:

~~~text
A → B: Interfaz    25 s
B → C: API/Datos   25 s
C → A: Sistemas    25 s
readback conjunto  25 s
~~~

Total:

~~~text
100 s
~~~

---

# 7. Dos personas

Antes:

~~~text
A R1+R2
B R3+R4
~~~

Después:

~~~text
A R3+R4
B R1+R2
~~~

Transferencia:

~~~text
A → B: UI/API         40 s
B → A: Datos/Sistemas 40 s
readback              20 s
~~~

Total:

~~~text
100 s
~~~

---

# 8. Una persona

No hay handoff interpersonal.

Debe declarar el cambio de capa en voz alta o por escrito.

Ejemplo:

> “Ahora dejo Sistemas y vuelvo a observar desde Interfaz.”

---

# 9. Evidencia mínima a transferir

## Interfaz

~~~text
request principal
status normal
pantalla
~~~

## API

~~~text
endpoint
campo JSON
status normal
~~~

## Datos

~~~text
objeto SQL
score actual
consulta segura clave
~~~

## Sistemas

~~~text
comandos clublab
estado normal
dónde mirar logs
~~~

---

# 10. Qué no transferir

~~~text
cada click
todos los comandos
JSON completo
historia larga de la misión
~~~

Handoff no es una mini-clase.

---

# 11. Regla de teclado después de rotar

El nuevo responsable obtiene control operativo real.

No se considera rotación si el anterior continúa:

~~~text
escribiendo comandos
moviendo el mouse
dictando cada paso
~~~

Puede responder preguntas, pero no operar por el nuevo responsable.

---

# 12. Checkpoint previo

Antes del handoff, el equipo debe recordar:

~~~text
request del ranking
endpoint
objeto SQL
score actual
componentes
~~~

Si el contexto está incompleto:

~~~text
máximo 60 s para reconstruirlo
~~~

---

# 13. Condición de éxito

El handoff está completo si el nuevo responsable puede decir:

~~~text
qué herramienta utilizar
qué evidencia normal espera
qué dato debe recordar
qué acción no debe ejecutar
~~~

sin que el dueño anterior tome el teclado.
