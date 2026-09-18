# P06D — Protocolo de incidente colaborativo
## ClubLab #01

**Estado:** FINAL PARA FASE 6 / BLOQUE C

---

# 1. Regla principal

> **Primero evidencia. Después recovery.**

Durante M6:

~~~text
observar
comparar
registrar
~~~

No:

~~~text
recover
reset
reiniciar
~~~

---

# 2. Diagnóstico

Responder:

~~~text
1. ¿Qué falla?
2. ¿Qué funciona?
3. ¿Qué muestra Interfaz?
4. ¿Qué muestra API?
5. ¿Qué muestra Datos?
6. ¿Qué muestra Sistemas?
7. ¿Qué explicación encaja mejor?
~~~

---

# 3. Hipótesis

Máximo:

~~~text
H1 principal
H2 alternativa
~~~

Formato:

~~~text
H1: creemos que __________________
H2: también podría ser ___________
~~~

No se descarta una hipótesis sin evidencia.

---

# 4. Evidencia mínima antes de recover

~~~text
>= 2 evidencias
>= 2 capas distintas
>= 1 hipótesis descartada
>= 1 predicción sobre qué cambiará
~~~

Plantilla:

~~~text
Causa propuesta:
____________________

Evidencia 1:
____________________

Evidencia 2:
____________________

Hipótesis descartada:
____________________

Después del recover esperamos:
____________________
~~~

---

# 5. Evidencia por capa

## Interfaz

~~~text
vista
request
status
~~~

## API

~~~text
ranking
health/endpoint sano
comparación de status
~~~

## Datos

~~~text
DB accesible
score consultable
score preservado
~~~

## Sistemas

~~~text
status
health
lablog
~~~

---

# 6. Recovery

Acción:

~~~bash
clublab recover ranking-db
~~~

Después se comprueba:

~~~text
R4 → health
R2 → ranking 200
R3 → score preservado
R1 → UI recuperada
~~~

Un mensaje “success” del comando no es suficiente por sí solo.

---

# 7. Si recovery falla

Alumno:

~~~text
detiene nuevas acciones
conserva evidencia
avisa al instructor
~~~

Instructor decide:

~~~text
clublabctl recover
reset explícito
spare
~~~

Nunca se entrega control del host al alumno.

---

# 8. Escalera de pistas

~~~text
P0 sin pista
P1 pregunta guía
P2 señalar capa/herramienta
P3 acción concreta
P4 comando o evidencia parcial
~~~

Regla:

~~~text
subir un nivel a la vez
~~~

Aunque reciba P4, el alumno debe explicar el resultado.

---

# 9. Regla anti-monopolio

> **Quien sabe la respuesta debe convertirla en una pregunta, no quitar el teclado.**

Permitido:

~~~text
“¿Qué endpoint compararías?”
“¿Qué evidencia descartaría DB caída?”
~~~

No permitido:

~~~text
“Dame, yo lo hago.”
~~~

---

# 10. Principiante bloqueado

Secuencia:

~~~text
recordar pregunta del rol
→ señalar herramienta
→ ofrecer dos opciones
→ dar comando
→ pedir interpretación
~~~

Se puede entregar el comando.

No se entrega automáticamente la explicación.

---

# 11. Equipo rápido

Antes de M6:

~~~text
requestId
comparar endpoints
explicar health
mejorar diagrama
relaciones DB/UI
~~~

Nunca:

~~~text
adelantar incidente
buscar /internal
probar recover
~~~

Durante M7:

~~~text
tercera evidencia
hipótesis alternativa
falsar su propia causa
explicar preservación de M4
~~~

---

# 12. Equipo lento

No eliminar:

~~~text
M4
M7
M8
~~~

Simplificar primero:

~~~text
M0
endpoints extra
exploración SQL extra
detalle secundario de M5
~~~

Intervenir si:

~~~text
> 3 min sin evidencia nueva
o
repiten la misma acción sin hipótesis nueva
~~~

---

# 13. Ausencias

Antes de empezar:

~~~text
usar configuración del tamaño real
~~~

Durante la actividad:

~~~text
pausar <= 60 s
redistribuir roles actuales
transferir evidencia mínima
continuar
~~~

Prioridad si faltan manos:

~~~text
mantener R1
mantener R4
combinar R2+R3
~~~

---

# 14. Laptop falla

No tocar servidor por defecto.

Orden:

~~~text
otra laptop
→ mismo team
→ comprobar URL/puerto/sesión
→ spare solo si el entorno también falla
~~~

---

# 15. Team equivocado

~~~text
detener
confirmar asignación
volver al team correcto
informar si hubo modificación
~~~

Nunca continuar “porque ya estamos aquí”.

---

# 16. Recover prematuro

~~~text
registrar recover prematuro
identificar evidencia faltante
instructor puede recargar escenario
repetir desde la capa faltante
~~~

No penalización.

---

# 17. Hipótesis en conflicto

No votar.

~~~text
H1
H2
→ buscar prueba discriminante
→ ejecutar la más barata
→ conservar la que sobreviva
~~~

---

# 18. Equipo discute sin ejecutar

Después de 2 minutos sin prueba:

~~~text
VERIFICAR propone la prueba más barata
que diferencie H1 y H2
~~~

---

# 19. Equipo ejecuta sin pensar

Antes del siguiente comando:

> **“¿Qué esperan ver y qué significaría?”**

Sin predicción, no se encadena otra acción.

---

# 20. Contingencias — orden oficial

~~~text
C1 pista pedagógica
C2 cambio de operador/configuración
C3 recovery del alumno
C4 recovery del instructor
C5 reset explícito
C6 spare
~~~

No usar una contingencia técnica para resolver un bloqueo conceptual.

---

# 21. Papel del instructor

Debe actuar como:

~~~text
facilitador
gestor de pistas
control temporal
observador de seguridad
gestor de contingencias
~~~

No como operador principal.

---

# 22. Frases que indican buena dinámica

~~~text
“esperamos que…”
“esto descarta…”
“health sigue 200…”
“vamos a comprobarlo desde otra capa…”
“el score sigue ahí…”
~~~

Frases que requieren intervención:

~~~text
“prueba esto a ver”
“reinicia”
“dame el teclado”
“seguro es Docker”
“ya funcionó”
~~~

---

# 23. M8 si hubo problemas reales

Si se usó spare o no pudo validarse algo:

El equipo declara:

~~~text
qué evidencia sí obtuvo
qué no pudo comprobar
qué contingencia se usó
~~~

No se inventa una validación.

---

# 24. Seguridad

Ninguna contingencia permite:

~~~text
SSH al host
sudo
Docker socket
clublabctl al alumno
control token
credenciales administrativas
~~~

El modelo de seguridad permanece intacto.
