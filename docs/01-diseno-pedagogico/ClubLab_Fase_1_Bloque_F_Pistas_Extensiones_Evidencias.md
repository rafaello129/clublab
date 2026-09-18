# ClubLab — Fase 1 / Bloque F
## Pistas + extensiones + evidencias

**Proyecto:** ClubLab v1  
**Experiencia:** ClubLab #01 — *Desarmando una aplicación*  
**Fase:** 1 — Diseño pedagógico  
**Bloque:** F  
**Dependencias:** Bloques A–E  
**Estado:** CERRADO PARA DISEÑO v1  
**Entregables:** `P08_Matriz_Dificultad` + `P09_Evidencias`

---

# 1. Propósito

Definir cómo ayudar sin resolver, cómo mantener activos a los equipos rápidos y qué evidencia demostrará que hubo comprensión.

> **La ayuda debe desbloquear el razonamiento, no sustituirlo.**

> **Una evidencia solo vale si el equipo puede explicar qué demuestra.**

---

# 2. Sistema de pistas

```text
P0 — Sin ayuda
P1 — Pregunta conceptual
P2 — Dirección hacia herramienta/capa
P3 — Instrucción concreta
P4 — Desbloqueo excepcional
```

Secuencia recomendada:

```text
2–3 min sin progreso → P1
2–3 min más          → P2
2 min más            → P3
riesgo de perder ritmo → P4
```

P4 no aparecerá en la guía normal del alumno.

Una buena pista reduce el espacio de búsqueda, pero no revela la causa.

---

# 3. Pistas por misión

## M0 — Reconocimiento
- **P1:** “Recorran todas las secciones disponibles.”
- **P2:** “El dashboard no contiene toda la información.”
- **P3:** “Entren a Ranking, Misiones, Equipo y Actividad.”
- **P4:** El instructor señala las secciones y devuelve el control.

## M1 — ¿De dónde vienen los datos?
- **P1:** “¿Puede el navegador mostrar qué ocurre cuando cambia la pantalla?”
- **P2:** “Busquen una herramienta para observar solicitudes.”
- **P3:** “F12 → Network → Fetch/XHR → recarguen Ranking.”
- **P4:** El instructor abre DevTools una vez y devuelve el teclado.

## M2 — Habla con la API
- **P1:** “Si el navegador puede pedir esa información, ustedes también.”
- **P2:** “Utilicen la URL encontrada en Network.”
- **P3:** “Prueben `curl -i <URL>`.”
- **P4:** Se entrega la URL exacta; el alumno debe interpretar la salida.

## M3 — Encuentra dónde viven los datos
- **P1:** “¿Qué sistema conserva el dato aunque cierres el navegador?”
- **P2:** “La terminal tiene acceso a una base preparada.”
- **P3:** “Entren a `psql`, usen `\dt` y busquen una tabla relacionada con equipos o puntuación.”
- **P4:** Se indica la tabla, no el registro.

## M4 — Cambia el sistema
- **P1:** “Ya encontraron dónde está almacenado.”
- **P2:** “¿Qué pasaría si modifican solo el registro de su equipo?”
- **P3:** “Primero `SELECT`, luego `UPDATE`, después consulten API y UI.”
- **P4:** Se entrega el `WHERE` correcto.

## M5 — ¿Dónde se está ejecutando?
- **P1:** “Si son partes distintas, debería poder observarse por separado.”
- **P2:** “Usen la herramienta de estado del laboratorio.”
- **P3:** “Ejecuten `clublab status` o equivalente.”
- **P4:** El instructor muestra una ejecución y pide interpretarla.

## M6 — Algo se rompió
- **P1:** “Antes de tocar nada, ¿qué sigue funcionando?”
- **P2:** “Comparen una petición sana con la que falla.”
- **P3:** “Revisen Network y `/api/health`.”
- **P4:** Se entrega la matriz Frontend / API / Ranking / DB para llenarla.

## M7 — Diagnostica y recupera
- **P1:** “Sigan el recorrido del dato. ¿Hasta qué punto funciona?”
- **P2:** “Comparen estado, API, base y logs.”
- **P3:** “La API está viva. Revisen qué reporta al obtener el ranking.”
- **P4:** “Está intentando resolver un host de base de datos que no existe.”

## M8 — Reconstruye la arquitectura
- **P1:** “Empiecen por ustedes: ¿qué utilizaron primero?”
- **P2:** “Sigan el recorrido del dato del ranking.”
- **P3:** “Navegador → Frontend → API/Backend → Base de datos; ahora agreguen dónde se ejecutan.”
- **P4:** Se entregan bloques con nombres para ordenarlos y justificar flechas.

---

# 4. Registro de pistas

Pedir una pista no tiene penalización.

El instructor registra únicamente:

```text
equipo
misión
nivel máximo utilizado
bloqueo observado
```

Después del ensayo:

```text
VERDE    mayoría termina con P0–P1
AMARILLO mayoría necesita P2
ROJO     mayoría necesita P3–P4
```

Una misión ROJA deberá revisarse, salvo M7, que intencionalmente es la más exigente.

---

# 5. Extensiones para equipos rápidos

Las extensiones son opcionales y no otorgan permisos adicionales.

| Misión | Extensión |
|---|---|
| M0 | Encontrar un mismo dato en dos pantallas |
| M1 | Comparar dos requests y sus tiempos/respuestas |
| M2 | Probar un ID válido y uno inexistente; comparar 200/404 |
| M3 | Encontrar relación entre dos tablas |
| M4 | Predecir qué cambiará antes de refrescar |
| M5 | Relacionar servicio, puerto y healthcheck |
| M6 | Crear tabla de hipótesis a favor/en contra |
| M7 | Explicar por qué frontend y health seguían vivos |
| M8 | Añadir HTTP, JSON, logs, puertos, red y healthchecks |

Reglas:

```text
no adelantar el incidente
no afectar otros equipos
no requerir privilegios extra
no modificar producción
no bloquear el flujo principal
```

Un equipo rápido primero explica su evidencia y luego recibe una extensión.

---

# 6. Evidencia mínima por misión

| Misión | Evidencia mínima |
|---|---|
| M0 | puntos, posición y dato a investigar |
| M1 | método + endpoint + status + dato |
| M2 | consulta directa + JSON relevante |
| M3 | tabla + columna + registro |
| M4 | valor antes/después en DB/API/UI |
| M5 | servicios + estado + healthcheck |
| M6 | qué funciona + qué falla + hipótesis |
| M7 | hipótesis + 2 evidencias + recuperación |
| M8 | diagrama + explicación oral |

---

# 7. Formatos de evidencia

## M0
```text
Equipo:
Puntos:
Posición:
Misión visible:
Dato a investigar:
```

## M1
```text
Método:
Endpoint:
Status:
Dato observado:
```

## M2
```text
Comando:
Status:
Campo JSON:
Valor coincidente con UI:
```

## M3
```text
Tabla:
Columna:
Identificador:
Valor:
```

## M4
```text
Valor anterior:
Valor nuevo:
Respuesta API:
Valor final en UI:
```

## M5
```text
Frontend:
API:
Database:
Healthcheck:
```

## M6
```text
¿Qué funciona?
¿Qué falla?
Request fallida:
Status:
Hipótesis inicial:
```

## M7
```text
Síntoma:
Hipótesis:
Evidencia 1:
Evidencia 2:
Hipótesis descartada:
Componente responsable:
Causa:
Acción mínima:
Resultado:
```

## M8
```text
Diagrama final
+
explicación oral de 60–90 segundos
```

---

# 8. “¿Qué descubrimos?”

Cada misión termina con una frase breve que el equipo completa.

Ejemplos:

```text
M1: “Descubrimos que el navegador ____________.”
M2: “Descubrimos que la API ____________.”
M3: “Descubrimos que los datos ____________.”
M5: “Descubrimos que una aplicación ____________.”
M7: “Descubrimos que diagnosticar significa ____________.”
```

Esto evita que la evidencia sea solo mecánica.

---

# 9. Ejecución vs comprensión

Ejemplo:

```bash
curl /api/ranking
```

**Ejecución:**

> “Me devolvió JSON.”

**Comprensión:**

> “La API responde sin pasar por la interfaz; frontend y API son piezas distintas.”

Preguntas de verificación:

```text
¿Qué demuestra?
¿Qué descarta?
¿Qué esperabas?
¿Qué pasaría si esta capa estuviera caída?
¿Cómo sabes que no fue casualidad?
```

---

# 10. Escala de comprensión

No es una calificación académica.

```text
C0 — Ejecuta sin entender
C1 — Describe lo que ocurrió
C2 — Relaciona causa y efecto
C3 — Predice una variante
```

Objetivo mínimo al terminar ClubLab #01:

```text
C2
```

Los alumnos avanzados pueden alcanzar C3.

---

# 11. Evidencia de predicción

Antes de acciones importantes el alumno debe anticipar el resultado.

M4:

> “Si cambio el dato en DB, espero que cambien API y UI.”

M7:

> “Si la conexión API→DB es la causa, restaurarla debe devolver `/api/ranking` a 200.”

Esto transforma comandos en experimentos.

---

# 12. Evidencia de descarte

Durante el incidente el equipo debe descartar al menos una hipótesis.

Ejemplo:

```text
Hipótesis descartada:
API completamente caída

Evidencia:
/api/health = 200
```

Encontrar la causa no basta; deben demostrar por qué otras explicaciones no encajan.

---

# 13. Cuaderno de Misiones

El futuro `D08_Cuaderno_de_Misiones` utilizará por misión:

```text
Nombre
Pregunta
Tarea
Espacio de evidencia
Pista 1
Pista 2
Pista 3
Reto extra
¿Qué descubrimos?
```

Debe ser breve y operativo, no un manual teórico.

---

# 14. Hoja del instructor

El instructor observará:

```text
participación
tiempo por misión
pista máxima usada
error recurrente
concepto confuso
herramienta problemática
monopolio de teclado
evidencia incompleta
```

Formato:

| Equipo | Misión | Tiempo | Pista máx. | Bloqueo principal | Nota |
|---|---|---:|---:|---|---|
| 01 | M1 | | | | |
| 01 | M2 | | | | |

La prioridad sigue siendo facilitar, no llenar formularios.

---

# 15. Evidencia que se conserva

Conservar:

```text
diagrama final
plantilla del incidente
respuestas “¿Qué descubrimos?”
tiempos aproximados
pistas máximas utilizadas
```

No es necesario conservar:

```text
cada captura
todos los comandos
logs completos
datos temporales
```

Nunca guardar en evidencias:

```text
contraseñas
tokens
credenciales
datos personales reales
IPs/rutas sensibles del host
logs de producción
```

---

# 16. Qué recortar si falta tiempo

Orden:

```text
1. extensiones avanzadas
2. detalles extra de M0
3. extensión de M3
4. parte avanzada de M5
5. exposición larga de M8
```

No eliminar, salvo emergencia:

```text
M1
M2
M3
M4
M6
M7
```

porque forman la cadena central.

---

# 17. Versión comprimida

Si la sesión debe comprimirse aproximadamente a 90 minutos:

| Misión | Tiempo |
|---|---:|
| M0 | 3 min |
| M1 | 7 min |
| M2 | 7 min |
| M3 | 8 min |
| M4 | 8 min |
| M5 | 6 min |
| M6 | 5 min |
| M7 | 20 min |
| M8 | 10 min |

El resto queda para transiciones y cierre.

---

# 18. Equipos lentos y principiantes

Si un equipo se retrasa:

```text
subir nivel de pista
eliminar extensión
entregar comando base
mantener la pregunta conceptual
```

Para principiantes puede existir una caja:

```text
COMANDOS DISPONIBLES

curl -i <URL>
\dt
SELECT ...
clublab status
```

El reto es elegir e interpretar, no memorizar sintaxis.

---

# 19. Equipos avanzados

Preguntas adicionales:

```text
¿Qué otra arquitectura produciría el mismo síntoma?
¿Qué evidencia adicional buscarías?
¿Cómo mejorarías el healthcheck?
¿Qué información no debería exponerse al usuario?
```

No deben recibir permisos especiales.

---

# 20. Matriz de dificultad inicial

| Misión | Dificultad |
|---|---|
| M0 | Baja |
| M1 | Baja-media |
| M2 | Media |
| M3 | Media |
| M4 | Media |
| M5 | Media |
| M6 | Media |
| M7 | Alta |
| M8 | Media |

La progresión buscada:

```text
fácil
→ curiosa
→ técnica
→ conectada
→ desafiante
→ satisfactoria
```

M7 es el pico.

---

# 21. Evidencia final mínima

Al terminar, cada equipo debe tener:

```text
1 request identificada
1 consulta directa a API
1 dato localizado en DB
1 modificación extremo a extremo
1 mapa de servicios
1 hipótesis descartada
1 diagnóstico con 2 evidencias
1 recuperación validada
1 diagrama final
```

Frases como:

```text
“ya funcionó”
“me salió 200”
“reinicié y volvió”
```

no son suficientes sin interpretación.

---

# 22. Criterio de éxito pedagógico

La sesión funciona si la mayoría puede explicar:

> “La aplicación no es una sola cosa. El navegador usa un frontend, el frontend pide datos, la API/backend procesa, la base persiste información y los servicios pueden fallar de forma independiente. Para diagnosticar seguimos evidencia.”

---

# 23. Decisiones cerradas en Bloque F

### DF-01
Todas las misiones tendrán P1, P2 y P3.

### DF-02
P4 será excepcional.

### DF-03
Pedir pistas no tendrá penalización.

### DF-04
Cada misión tendrá extensión opcional.

### DF-05
Toda misión producirá evidencia concreta.

### DF-06
Toda evidencia requerirá interpretación.

### DF-07
Se usará C0–C3 para observar comprensión.

### DF-08
M7 será el pico de dificultad.

### DF-09
Los equipos rápidos no adelantarán información crítica.

### DF-10
El Cuaderno de Misiones se derivará de este bloque.

### DF-11
El incidente exigirá predicción, descarte y validación.

### DF-12
Si falta tiempo, se recortarán extensiones antes que conceptos.

---

# 24. Entregables

```text
P08_Matriz_Dificultad
P08A_Sistema_de_Pistas
P08B_Extensiones
P09_Evidencias
P09A_Escala_Comprension
P09B_Hoja_Observacion_Instructor
P09C_Estructura_Cuaderno_Misiones
P09D_Reglas_Recorte
```

---

# 25. Criterios de aceptación

- [x] Sistema de pistas definido.
- [x] Timing de pistas definido.
- [x] Pistas M0–M8 consolidadas.
- [x] P4 definido.
- [x] Extensiones M0–M8 definidas.
- [x] Evidencias M0–M8 definidas.
- [x] Escala C0–C3 definida.
- [x] Predicción definida.
- [x] Descarte definido.
- [x] Hoja del instructor definida.
- [x] Evidencia a conservar definida.
- [x] Privacidad definida.
- [x] Reglas de recorte definidas.
- [x] Versión comprimida definida.
- [x] Equipos rápidos/lentos contemplados.

# BLOQUE F — COMPLETADO

---

# 26. Siguiente bloque

# BLOQUE G — Cronograma exacto de 120 minutos

Se definirá:

```text
inicio y fin de cada misión
bienvenida
formación de equipos
entrega de roles
rotación
punto de control
momento exacto del incidente
diagnóstico
reconstrucción
cierre
margen de contingencia
señales para acelerar o frenar
```

El objetivo será demostrar que todo lo diseñado cabe realmente en una sesión de dos horas.