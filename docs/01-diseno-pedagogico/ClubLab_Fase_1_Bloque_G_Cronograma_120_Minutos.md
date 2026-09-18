# ClubLab — Fase 1 / Bloque G
## Cronograma exacto de 120 minutos

**Proyecto:** ClubLab v1  
**Experiencia:** ClubLab #01 — *Desarmando una aplicación*  
**Fase:** 1 — Diseño pedagógico  
**Bloque:** G  
**Dependencias:** Bloques A–F  
**Estado:** CERRADO PARA DISEÑO v1  
**Entregable principal:** `P05_Cronograma_120min`

---

# 1. Propósito del Bloque G

Este bloque demuestra que toda la experiencia diseñada hasta ahora cabe dentro de una sesión real de dos horas.

El cronograma debe proteger tres cosas:

```text
1. tiempo de exploración;
2. tiempo suficiente para el incidente;
3. cierre y reconstrucción.
```

La sesión no debe convertirse en una carrera para terminar misiones.

La prioridad es:

```text
comprensión
>
cantidad de contenido
```

---

# 2. Duración total

```text
120 minutos
```

Distribución general:

```text
00–10    Preparación
10–34    Descubrir
34–68    Conectar
68–101   Incidente
101–120  Reconstruir y cerrar
```

---

# 3. Cronograma maestro

| Tiempo | Actividad | Duración |
|---|---|---:|
| 00:00–00:05 | Bienvenida + reglas | 5 min |
| 00:05–00:10 | Equipos + roles + acceso | 5 min |
| 00:10–00:16 | M0 — Reconocimiento | 6 min |
| 00:16–00:25 | M1 — ¿De dónde vienen los datos? | 9 min |
| 00:25–00:34 | M2 — Habla con la API | 9 min |
| 00:34–00:45 | M3 — Encuentra dónde viven los datos | 11 min |
| 00:45–00:56 | M4 — Cambia el sistema | 11 min |
| 00:56–01:05 | M5 — ¿Dónde se está ejecutando? | 9 min |
| 01:05–01:08 | Punto de control | 3 min |
| 01:08–01:10 | Rotación de roles | 2 min |
| 01:10–01:16 | M6 — Algo se rompió | 6 min |
| 01:16–01:39 | M7 — Diagnostica y recupera | 23 min |
| 01:39–01:41 | Buffer técnico/pedagógico | 2 min |
| 01:41–01:54 | M8 — Reconstruye la arquitectura | 13 min |
| 01:54–02:00 | Cierre + intereses + conclusión | 6 min |

Total:

```text
120 minutos exactos
```

---

# 4. 00:00–00:05 — Bienvenida

## Objetivo

Establecer el tono sin explicar arquitectura.

## Mensaje del instructor

> “Hoy no vamos a construir una aplicación. Vamos a desarmar una que ya funciona.”

Luego:

> “No den por hecho cómo funciona. Demuéstrenlo.”

## Explicar únicamente

```text
qué es ClubLab;
duración;
trabajo por equipos;
regla de evidencia;
cómo pedir pistas;
qué NO tocar.
```

No explicar:

```text
React;
NestJS;
PostgreSQL;
Docker;
arquitectura;
incidente.
```

---

# 5. 00:05–00:10 — Equipos, roles y acceso

## Actividades

```text
formar equipos;
asignar Team ID;
entregar credenciales;
asignar roles;
abrir aplicación;
confirmar acceso.
```

## Regla

A los 10 minutos todos deben estar dentro.

Si un equipo tiene problema de acceso:

```text
el instructor resuelve;
no convertirlo en misión.
```

---

# 6. 00:10–00:16 — M0

## Objetivo

Explorar la aplicación.

## Ritmo

```text
min 10–14 → exploración
min 14–16 → evidencia + “¿qué dato investigarían?”
```

## Señal para cerrar

Todos deben conocer:

```text
puntos;
posición;
misiones;
actividad.
```

---

# 7. 00:16–00:25 — M1

## Objetivo

Descubrir Network.

## Ritmo

```text
16–18 → pregunta detonadora
18–23 → investigación
23–25 → registrar request/status
```

## Pregunta clave

> “¿De dónde salió ese número?”

## Condición de salida

```text
request identificada
+
status observado
```

---

# 8. 00:25–00:34 — M2

## Objetivo

Consultar la API sin interfaz.

## Ritmo

```text
25–27 → conectar hallazgo M1
27–32 → curl
32–34 → comparar JSON con UI
```

## Condición de salida

El equipo puede decir:

> “La API existe aunque no usemos la interfaz.”

---

# 9. 00:34–00:45 — M3

## Objetivo

Encontrar persistencia.

## Ritmo

```text
34–36 → pregunta “¿dónde vive?”
36–42 → psql / exploración
42–45 → localizar registro y documentar
```

## Condición de salida

```text
tabla
columna
valor
```

---

# 10. 00:45–00:56 — M4

## Objetivo

Demostrar flujo extremo a extremo.

## Ritmo

```text
45–48 → SELECT y predicción
48–51 → UPDATE autorizado
51–54 → consultar API
54–56 → verificar UI
```

## Condición de salida

```text
DB
→ API
→ UI
```

visible.

---

# 11. 00:56–01:05 — M5

## Objetivo

Descubrir servicios separados.

## Ritmo

```text
56–58 → pregunta “¿dónde corre?”
58–63 → status/health
63–65 → nombrar servicios
```

## Condición de salida

El equipo identifica al menos:

```text
frontend
api
database
```

como componentes diferentes.

---

# 12. 01:05–01:08 — Punto de control

El instructor detiene a todos.

Pregunta:

> “Hasta ahora, ¿qué piezas sabemos que existen?”

Los equipos completan:

```text
Navegador
   ↓
Frontend
   ↓
________
   ↓
________
```

Respuesta esperada:

```text
API / Backend
Database
```

No mostrar todavía el diagrama final.

---

# 13. 01:08–01:10 — Rotación de roles

Rotación estándar:

```text
Interfaz ↔ Sistemas
API      ↔ Datos
```

Cada persona dispone de:

```text
30–45 segundos
```

para transferir:

```text
herramienta;
hallazgo;
dato importante;
error a evitar.
```

Máximo:

```text
2 minutos
```

---

# 14. 01:10 — Momento del incidente

A las:

```text
01:10
```

el instructor activa:

# INCIDENTE 01

No antes.

Esto evita que equipos rápidos descubran el fallo mientras otros aún están aprendiendo.

---

# 15. 01:10–01:16 — M6

## Objetivo

Observar sin reparar.

## Regla

Durante los primeros minutos:

```text
NO recover
NO reset
NO restart
```

## Ritmo

```text
70–72 → reproducir fallo
72–74 → comparar qué funciona
74–76 → Network + hipótesis inicial
```

## Salida

Cada equipo debe tener:

```text
qué funciona;
qué falla;
request;
status;
hipótesis.
```

---

# 16. 01:16–01:39 — M7

## Objetivo

Diagnóstico y recuperación.

Este es el bloque más importante de la sesión.

## Distribución interna

```text
01:16–01:21
Exploración inicial

01:21–01:27
Comparación API / DB / servicios

01:27–01:32
Logs + hipótesis

01:32–01:35
Validar causa

01:35–01:37
Recuperación

01:37–01:39
Validación final
```

---

# 17. Checkpoints dentro de M7

## 01:21

El instructor pregunta:

```text
¿qué hipótesis tienen?
```

No exige solución.

---

## 01:27

Si un equipo no ha llegado a evidencia útil:

```text
dar P2
```

---

## 01:32

Si un equipo aún no localiza la dependencia:

```text
dar P3
```

---

## 01:35

Todos los equipos deberían estar en recuperación o muy cerca.

Si no:

```text
usar P4
```

para proteger el cierre de la sesión.

---

# 18. 01:39–01:41 — Buffer

Este bloque existe deliberadamente.

Puede utilizarse para:

```text
reset tardío;
equipo con dificultad;
problema de acceso;
explicación breve;
transición.
```

Si no se necesita:

```text
se añade a M8.
```

Nunca utilizarlo para introducir contenido nuevo.

---

# 19. 01:41–01:54 — M8

## Objetivo

Reconstruir la arquitectura.

## Ritmo

```text
101–106 → completar diagrama
106–111 → relacionar incidente con diagrama
111–114 → explicación rápida de equipos
```

No todos tienen que presentar formalmente.

Opciones según número de equipos:

```text
2–3 equipos
→ todos presentan

4–6 equipos
→ 2 presentan y el resto compara
```

---

# 20. 01:54–02:00 — Cierre

## Primera pregunta

> “Hace dos horas esto era una sola aplicación. ¿Cuántas piezas ven ahora?”

## Preguntas de salida

```text
¿Qué parte te dio más curiosidad?
¿Qué herramienta no conocías?
¿Qué rol disfrutaste más?
¿Qué tema te gustaría explorar después?
```

## Mensaje final

> “Hoy no aprendieron a construir todas estas piezas. Aprendieron a reconocerlas, conectarlas y seguir evidencia cuando algo falla.”

---

# 21. Distribución por actos

## ACTO I — Descubrir

```text
00:00–00:34
```

Incluye:

```text
bienvenida;
M0;
M1;
M2.
```

---

## ACTO II — Conectar

```text
00:34–01:10
```

Incluye:

```text
M3;
M4;
M5;
punto de control;
rotación.
```

---

## ACTO III — Incidente

```text
01:10–01:41
```

Incluye:

```text
M6;
M7;
buffer.
```

---

## ACTO IV — Reconstruir

```text
01:41–02:00
```

Incluye:

```text
M8;
cierre.
```

---

# 22. Porcentaje aproximado de sesión

```text
Instructor / transiciones
≈ 25%

Trabajo activo
≈ 60%

Discusión / reconstrucción
≈ 15%
```

Cumple el objetivo de evitar una sesión basada en exposición.

---

# 23. Señales para acelerar

El instructor debe acelerar si:

```text
M0 supera minuto 16;
M1 supera minuto 25;
M3 no termina al 45;
M5 supera 65;
incidente no empieza al 70;
M7 sigue sin hipótesis al 92;
M8 no inicia al 101.
```

Acciones:

```text
subir pista;
eliminar extensión;
entregar comando base;
hacer cierre de misión más breve.
```

---

# 24. Señales para frenar

Se puede dar más tiempo si:

```text
todos van adelantados;
hay discusión productiva;
apareció una hipótesis interesante;
la mayoría está cerca del descubrimiento;
el buffer sigue intacto.
```

No adelantar el incidente antes de:

```text
01:10
```

aunque equipos terminen antes.

---

# 25. Regla de sincronización

M0–M5 permiten pequeñas diferencias de ritmo.

Antes del incidente:

```text
todos deben sincronizarse.
```

Esto evita que:

```text
un equipo vea el escenario roto
mientras otro todavía hace M4.
```

El punto de control y la rotación sirven como barrera de sincronización.

---

# 26. Qué hacen los equipos rápidos antes del incidente

Si terminan M5 temprano:

```text
hacer extensión M5;
revisar evidencias;
actualizar diagrama parcial;
responder “¿qué descubrimos?”;
```

No:

```text
explorar logs del incidente;
activar escenarios;
consultar soluciones.
```

---

# 27. Margen de contingencia real

El cronograma tiene:

```text
2 minutos de buffer explícito
+
varios minutos recuperables de extensiones
+
M8 adaptable
```

Margen efectivo:

```text
aprox. 7–10 minutos
```

sin destruir el núcleo.

---

# 28. Prioridades si se pierde tiempo

Orden de protección:

```text
1. M7 — Diagnóstico
2. M6 — Observación
3. M4 — Flujo extremo a extremo
4. M3 — Persistencia
5. M2 — API
6. M1 — Network
7. M8 — Reconstrucción
8. M5 — Servicios
9. M0 — Exploración
```

No significa eliminar M0/M5, sino comprimirlos primero.

---

# 29. Regla de “no sacrificar el cierre”

Aunque exista retraso:

```text
reservar mínimo 5 minutos finales.
```

Una sesión sin cierre deja experimentos sueltos.

El instructor debe detener el laboratorio a más tardar:

```text
01:55
```

para cerrar.

---

# 30. Versión de contingencia — 105 minutos

Si por problemas logísticos la sesión comienza 15 minutos tarde:

```text
M0   4 min
M1   7 min
M2   7 min
M3   9 min
M4   9 min
M5   7 min
Checkpoint + rotación 4 min
M6   5 min
M7   22 min
M8   10 min
Cierre 6 min
```

Sin extensiones.

---

# 31. Versión comprimida — 90 minutos

Solo para contingencia seria.

| Bloque | Tiempo |
|---|---:|
| Inicio + roles | 5 min |
| M0 | 3 min |
| M1 | 7 min |
| M2 | 7 min |
| M3 | 8 min |
| M4 | 8 min |
| M5 | 6 min |
| Checkpoint + rotación | 3 min |
| M6 | 5 min |
| M7 | 20 min |
| M8 | 10 min |
| Cierre | 8 min |

Total:

```text
90 min
```

---

# 32. Qué desaparece en versión comprimida

Eliminar:

```text
extensiones;
presentaciones largas;
comparaciones opcionales;
preguntas avanzadas;
exploración libre adicional.
```

Mantener:

```text
evidencia principal;
incidente;
reconstrucción;
cierre.
```

---

# 33. Checklist del instructor antes de iniciar

Antes del minuto 0:

```text
[ ] entornos healthy
[ ] cuentas disponibles
[ ] seeds correctos
[ ] URL accesible
[ ] API responde
[ ] DB responde
[ ] Scenario Manager listo
[ ] incidente probado
[ ] reset probado
[ ] tarjetas preparadas
[ ] cuadernos preparados
[ ] reloj visible
```

---

# 34. Checklist antes del incidente

En minuto 65:

```text
[ ] equipos terminaron M4
[ ] entienden API
[ ] localizaron DB
[ ] observaron servicios
[ ] sistema está sano
[ ] evidencias básicas completas
```

Si falta algo:

```text
dar apoyo directo
```

antes de activar el fallo.

---

# 35. Checklist después del incidente

Antes de M8:

```text
[ ] ranking volvió
[ ] /api/health = 200
[ ] /api/ranking = 200
[ ] equipo tiene 2 evidencias
[ ] hipótesis descartada
[ ] causa identificada
[ ] recuperación explicada
```

---

# 36. Reloj del instructor

El instructor debe tener visibles cinco hitos:

```text
00:10 → iniciar M0
00:34 → iniciar M3
01:10 → activar incidente
01:41 → iniciar M8
01:54 → iniciar cierre
```

Si esos cinco hitos se respetan, la sesión es muy difícil que se descontrole.

---

# 37. Señales de buen ritmo

```text
equipos hablan entre sí;
se escuchan preguntas;
DevTools/terminal se usan con intención;
las pistas no son automáticas;
M7 ocupa la mayor energía;
queda tiempo para explicar el diagrama.
```

---

# 38. Señales de mal ritmo

```text
20 minutos de explicación inicial;
todos esperan al instructor;
M1 consume 20 minutos;
M7 empieza después del minuto 85;
el cierre se elimina;
los avanzados van dos misiones adelante.
```

Ante cualquiera:

```text
recortar;
sincronizar;
subir pistas.
```

---

# 39. Cronograma visual compacto

```text
00      10      20      30      40      50      60
|-------|-------|-------|-------|-------|-------|
 Intro   M0   M1     M2      M3      M4      M5

60      70      80      90      100     110     120|-------|-------|-------|-------|-------|-------|
 M5/CP   M6        M7           M8          Cierre
          ↑
       INCIDENTE
```

---

# 40. Decisiones cerradas en Bloque G

### DG-01
La sesión durará 120 minutos exactos.

### DG-02
El incidente se activa en el minuto 70.

### DG-03
M7 tendrá 23 minutos.

### DG-04
Existirá una barrera de sincronización antes del incidente.

### DG-05
La rotación ocurrirá inmediatamente antes de M6.

### DG-06
Se reservarán 2 minutos de buffer explícito.

### DG-07
El cierre tendrá mínimo 6 minutos en versión normal.

### DG-08
No se adelanta el incidente para equipos rápidos.

### DG-09
Las extensiones son lo primero que se elimina si hay retraso.

### DG-10
Se mantendrán versiones de contingencia de 105 y 90 minutos.

### DG-11
Los hitos críticos serán 10, 34, 70, 101 y 114 minutos.

### DG-12
M7 será el bloque individual más largo.

---

# 41. Entregables

Este bloque produce:

```text
P05_Cronograma_120min
P05A_Hitos_Instructor
P05B_Reglas_Aceleracion
P05C_Reglas_Sincronizacion
P05D_Cronograma_105min
P05E_Cronograma_90min
P05F_Checklists_Ejecucion
```

---

# 42. Criterios de aceptación

- [x] 120 minutos distribuidos.
- [x] Bienvenida incluida.
- [x] Roles incluidos.
- [x] M0–M8 incluidas.
- [x] Punto de control incluido.
- [x] Rotación incluida.
- [x] Incidente con hora exacta.
- [x] Diagnóstico con tiempo protegido.
- [x] Buffer incluido.
- [x] Cierre protegido.
- [x] Señales de acelerar definidas.
- [x] Señales de frenar definidas.
- [x] Barrera de sincronización definida.
- [x] Contingencia 105 min definida.
- [x] Contingencia 90 min definida.
- [x] Checklists definidos.
- [x] Hitos del instructor definidos.

# BLOQUE G — COMPLETADO

---

# 43. Siguiente bloque

# BLOQUE H — Contingencias + simulación pedagógica

El siguiente bloque comprobará qué pasa cuando la sesión no sale como se planeó.

Se diseñará:

```text
fallo de internet;
fallo de LAN/Tailscale;
entorno de un equipo roto;
DB no disponible;
API no disponible;
Scenario Manager falla;
un equipo se adelanta;
un equipo se retrasa;
faltan laptops;
faltan integrantes;
incidente no se activa;
incidente no se recupera;
```

Después se hará una simulación completa “en papel” de los 120 minutos para detectar dependencias, tiempos muertos y puntos frágiles antes de cerrar el D01.