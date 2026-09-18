# P06A — Matriz de roles y misiones
## ClubLab #01

**Estado:** FINAL PARA FASE 6 / BLOQUE B

---

# 1. Roles

~~~text
R1 Interfaz
R2 API
R3 Datos
R4 Sistemas
R5 Relator opcional
~~~

---

# 2. Funciones momentáneas

~~~text
OPERAR    → ejecuta la acción principal
OBSERVAR  → identifica el resultado inmediato
VERIFICAR → contrasta desde otra capa
REGISTRAR → conserva evidencia mínima
~~~

No son roles nuevos.

---

# 3. Protocolo POE

Toda acción relevante sigue:

~~~text
PREDICCIÓN
“Si hacemos X, esperamos Y.”

OBSERVACIÓN
“Vimos Z.”

EVIDENCIA
“Esto apoya/contradice la idea porque…”
~~~

---

# 4. Matriz base M0–M5

| Misión | OPERAR | OBSERVAR | VERIFICAR | REGISTRAR | Evidencia de salida |
|---|---|---|---|---|---|
| M0 | R1 | R2 | R4 | R3 | vistas + score/posición inicial |
| M1 | R1 | R2 | R4 | R3 | request, método, status, response |
| M2 | R2 | R1 | R4 | R3 | API directa + JSON relacionado |
| M3 | R3 | R2 | R1 | R4 | objeto SQL + score |
| M4 | R3 | R1 | R2 | R4 | antes/después DB→API→UI |
| M5 | R4 | R1 | R2 | R3 | componentes + health |

---

# 5. Rotación

Después de M5 y antes de M6.

## Cuatro personas

~~~text
A R1 → R4
B R2 → R3
C R3 → R2
D R4 → R1
~~~

## Cinco personas

Misma rotación y R5 permanece.

## Tres personas

~~~text
A R1       → R4
B R2 + R3  → R1
C R4       → R2 + R3
~~~

## Dos personas

~~~text
A R1 + R2 → R3 + R4
B R3 + R4 → R1 + R2
~~~

---

# 6. M6

~~~text
OPERAR    R1
OBSERVAR  R2
VERIFICAR R4
REGISTRAR R3
~~~

Salida:

~~~text
síntoma
request/status
qué sigue funcionando
~~~

No recover.

---

# 7. M7

M7 se ejecuta por rondas.

## Ronda UI

~~~text
R1 opera
→ síntoma + request fallida
~~~

## Ronda API

~~~text
R2 opera
→ ranking fallido vs endpoints sanos
~~~

## Ronda Datos

~~~text
R3 opera
→ DB accesible + dato preservado
~~~

## Ronda Sistemas

~~~text
R4 opera
→ status + health + lablog
~~~

Después:

~~~text
hipótesis
>= 2 evidencias
>= 1 hipótesis descartada
→ recover
~~~

---

# 8. Verificación post-recover

~~~text
R4 → health
R2 → ranking 200
R3 → score preservado
R1 → UI recuperada
~~~

---

# 9. M8

Todos participan.

Mínimo:

~~~text
cada integrante explica una relación entre dos capas
~~~

Con R5:

~~~text
R5 coordina
R1–R4 conservan explicación técnica
~~~

---

# 10. Regla de avance

Una misión no se considera cerrada únicamente porque “funcionó”.

Debe existir:

~~~text
resultado
+
interpretación
+
evidencia
~~~
