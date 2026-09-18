# ClubLab — Fase 1 / Bloque H
## Contingencias + simulación pedagógica completa

**Proyecto:** ClubLab v1  
**Experiencia:** ClubLab #01 — *Desarmando una aplicación*  
**Fase:** 1 — Diseño pedagógico  
**Bloque:** H  
**Dependencias:** Bloques A–G  
**Estado:** CERRADO PARA DISEÑO v1  
**Entregables principales:** `P10_Contingencias` + `P11_Revision_Pedagogica`

---

# 1. Propósito del Bloque H

Este bloque somete ClubLab #01 a una revisión de resistencia.

Hasta ahora diseñamos la sesión suponiendo que:

```text
los accesos funcionan;
los equipos avanzan;
los servicios responden;
el incidente se activa;
el instructor mantiene el ritmo.
```

En una sesión real, algunas de esas condiciones pueden fallar.

Por ello, este bloque tiene dos objetivos:

```text
1. definir planes de contingencia;
2. simular la sesión completa antes de implementarla.
```

La meta es que la experiencia siga siendo útil incluso si una parte de la infraestructura o del ritmo pedagógico no sale como se esperaba.

---

# 2. Principio de contingencia

Las contingencias deben preservar primero:

```text
COMPRENSIÓN
```

y después:

```text
REALISMO TÉCNICO
```

Si una herramienta falla, se puede reemplazar temporalmente.

Si se pierde la oportunidad de comprender el concepto, la sesión deja de cumplir su objetivo.

---

# 3. Prioridades de recuperación

Ante cualquier problema:

```text
P1 — mantener a los participantes activos;
P2 — conservar la pregunta pedagógica;
P3 — recuperar el flujo principal;
P4 — mantener evidencia;
P5 — volver al entorno real si es posible.
```

No detener toda la sesión por un solo equipo salvo que el problema sea global.

---

# 4. Tipos de contingencia

Se clasifican en:

```text
C1 — acceso
C2 — red
C3 — servicio
C4 — datos
C5 — escenario
C6 — dispositivos
C7 — participantes
C8 — ritmo
C9 — instructor
C10 — tiempo
```

---

# 5. C1 — Un equipo no puede acceder

## Síntoma

```text
login falla;
URL no abre;
credenciales no funcionan.
```

## Acción inmediata

```text
1. verificar Team ID;
2. verificar URL;
3. usar credencial de respaldo;
4. mover temporalmente al equipo a entorno reserva.
```

## Tiempo máximo de resolución

```text
3 minutos
```

Si supera ese tiempo:

```text
activar entorno backup.
```

## Plan B pedagógico

El equipo puede empezar M0 usando:

```text
captura funcional;
demo del instructor;
entorno compartido solo lectura.
```

hasta recuperar acceso.

---

# 6. C2 — Falla de Internet

## Impacto esperado

Si ClubLab depende únicamente de servicios internos:

```text
debería ser bajo.
```

## Diseño deseado

La sesión debe poder funcionar:

```text
sin Internet público.
```

No depender de:

```text
CDN externos;
Google;
GitHub;
Cloudflare Quick Tunnel;
documentación online;
APIs externas.
```

## Plan B

```text
LAN local
o
Tailscale previamente disponible
```

según arquitectura final.

---

# 7. C3 — Falla de LAN / Tailscale

## Si solo falla un alumno

```text
usar laptop de otro integrante;
trabajar por equipo;
no detener la sesión.
```

## Si falla un equipo completo

```text
mover a red alternativa;
usar equipo del instructor;
activar entorno local de emergencia.
```

## Si falla globalmente

Prioridad:

```text
preservar M1–M8 con entorno local o demo guiada.
```

La implementación técnica debe contemplar al menos una ruta alternativa.

---

# 8. C4 — Frontend real falla antes del incidente

## Problema

El alumno no puede diferenciar:

```text
fallo planeado
vs
fallo accidental.
```

## Acción

No iniciar la sesión con estado degradado.

Antes de abrir ClubLab:

```text
frontend healthy;
API healthy;
DB healthy;
ranking 200.
```

Si no puede recuperarse en menos de 5 minutos:

```text
usar build estático/backup;
o posponer incidente técnico y usar simulación controlada.
```

---

# 9. C5 — API falla accidentalmente durante M1–M5

## Acción

```text
instructor confirma;
resetea solo el equipo;
repite healthcheck;
restaura seed si aplica.
```

## Si afecta varios equipos

Pausar brevemente y anunciar:

> “Tenemos una falla real de laboratorio. No forma parte de la misión.”

Esto evita mezclarla con la narrativa.

---

# 10. C6 — DB no disponible durante M3/M4

## Plan A

Reset del entorno del equipo.

## Plan B

Proporcionar snapshot SQL de lectura:

```text
tabla;
columnas;
filas;
registro del equipo.
```

## Plan C

Utilizar una terminal simulada con salida pregrabada.

El concepto que debe preservarse:

```text
UI → API → dato persistente
```

---

# 11. C7 — UPDATE falla en M4

## Causas posibles

```text
permiso;
filtro;
dato inválido;
transacción;
conexión.
```

## Acción

Primero verificar:

```text
SELECT correcto.
```

Después:

```text
reintentar UPDATE autorizado.
```

## Plan B

El instructor puede realizar el cambio en backend administrativo, pero el equipo debe:

```text
predecir el resultado;
consultar API;
verificar UI.
```

---

# 12. C8 — El Scenario Manager no activa el incidente

## Acción

Intentos permitidos:

```text
1. scenario load;
2. verificar estado;
3. reintentar una vez.
```

Si no funciona:

```text
activar variante simplificada
API DOWN
```

Si tampoco:

```text
usar incidente simulado con logs/respuestas preparadas.
```

Nunca perder 15 minutos intentando arreglar el sistema frente al grupo.

---

# 13. C9 — El incidente no se recupera

## Acción

Tiempo máximo:

```text
3 minutos después del recover.
```

Si continúa roto:

```text
reset teamXX
```

Si reset falla:

```text
mover a entorno reserva.
```

Pedagógicamente, el equipo ya obtuvo:

```text
diagnóstico;
evidencia;
causa.
```

La recuperación real es deseable, pero no vale sacrificar M8 y cierre.

---

# 14. C10 — El incidente resulta demasiado fácil

## Señal

La mayoría descubre la causa en:

```text
< 5 minutos
```

sin pistas.

## Ajuste futuro

```text
hacer logs menos explícitos;
reducir pistas automáticas;
usar un síntoma más indirecto;
```

No aumentar dificultad durante la sesión en vivo.

---

# 15. C11 — El incidente resulta demasiado difícil

## Señal

```text
todos piden P4;
nadie conecta API y DB;
M7 supera 30 minutos.
```

## Acción durante clase

```text
subir pistas;
reducir investigación;
forzar recuperación;
proteger M8.
```

## Acción posterior

Simplificar escenario.

---

# 16. C12 — Falta una laptop

## Estrategia

ClubLab ya está diseñado para funcionar con:

```text
1 laptop por equipo
```

Por lo tanto:

```text
no bloquea la sesión.
```

Los roles se ejecutan de forma secuencial sobre el mismo dispositivo.

---

# 17. C13 — Hay demasiadas laptops pero pocos participantes

No es problema.

Prioridad:

```text
trabajo colaborativo
>
1 dispositivo por persona
```

Puede usarse:

```text
1 equipo principal
+
1 dispositivo secundario para documentación/API.
```

---

# 18. C14 — Faltan integrantes en un equipo

## 3 personas

```text
API + Datos combinados.
```

## 2 personas

```text
Interfaz + API
Datos + Sistemas
```

## 1 persona

```text
rotación individual;
instructor como interlocutor.
```

La sesión no se cancela.

---

# 19. C15 — Llegan participantes tarde

Hasta minuto:

```text
20
```

pueden integrarse a un equipo existente.

Después:

```text
no crear equipo nuevo.
```

Se asignan como:

```text
Relator
o
rol de apoyo
```

hasta la rotación.

---

# 20. C16 — Equipo muy avanzado se adelanta

No permitir que avance a M6 antes del minuto 70.

Actividades permitidas:

```text
extensiones;
diagrama parcial;
comparar endpoints;
mejorar evidencia;
explicar hallazgos.
```

---

# 21. C17 — Equipo muy lento

## Regla

No permitir que una misión individual destruya el resto de la experiencia.

Acciones:

```text
subir pista;
dar comando;
reducir evidencia secundaria;
eliminar extensión;
hacer desbloqueo.
```

Preservar:

```text
la pregunta;
la interpretación;
la conexión con la siguiente misión.
```

---

# 22. C18 — Una persona monopoliza el equipo

## Señales

```text
escribe todos los comandos;
responde por todos;
toma el teclado;
no permite hipótesis.
```

## Intervención

El instructor dice:

> “En esta misión el teclado pertenece al rol principal.”

Si persiste:

```text
forzar cambio de operador.
```

---

# 23. C19 — Nadie quiere usar terminal

## Acción

No obligar mediante explicación larga.

Dar una tarea mínima:

```bash
curl -i <URL>
```

y preguntar:

> “¿Qué cambió respecto a usar la pantalla?”

Después introducir terminal como herramienta, no como objetivo.

---

# 24. C20 — Nadie entiende SQL

## Acción

Entregar consulta parcial:

```sql
SELECT * FROM ...
```

o una plantilla:

```sql
SELECT <columnas>
FROM <tabla>
WHERE <condición>;
```

La misión sigue siendo:

```text
encontrar el dato;
relacionarlo;
interpretarlo.
```

---

# 25. C21 — Confusión entre backend y servidor

## Acción

Usar una aclaración breve:

```text
Backend = servicio de la aplicación.
Servidor = infraestructura donde puede ejecutarse.
```

No abrir una explicación larga sobre cliente-servidor.

---

# 26. C22 — Confusión entre API y backend

Aclaración:

```text
Backend = sistema que procesa.
API = interfaz que expone operaciones/datos.
```

Para ClubLab #01 pueden aparecer juntos en el diagrama:

```text
API / Backend
```

sin exigir precisión arquitectónica avanzada.

---

# 27. C23 — El grupo empieza a preguntar por seguridad

Es una señal positiva.

Responder brevemente y registrar como puente:

```text
“Eso merece un ClubLab propio.”
```

No desviar 20 minutos hacia:

```text
JWT;
SQL injection;
XSS;
auth;
TLS.
```

---

# 28. C24 — El grupo quiere ver código antes de tiempo

Respuesta:

> “Primero demuestren qué hace el sistema. Después veremos cómo está implementado.”

El código puede mostrarse:

```text
después de M5
o
en el cierre
```

si hay tiempo.

---

# 29. C25 — El instructor pierde tiempo explicando

Regla:

```text
ninguna explicación continua > 7 minutos.
```

Si ocurre:

```text
detener explicación;
hacer pregunta;
devolver control al grupo.
```

---

# 30. Kit mínimo de contingencia del instructor

Antes de la sesión debe existir:

```text
1 entorno de reserva;
1 credencial de respaldo;
1 copia de respuestas JSON;
1 snapshot de tablas;
1 log de incidente preparado;
1 diagrama incompleto impreso;
1 diagrama final del instructor;
1 versión 90 min;
1 forma de reset rápido;
1 lista de Team IDs.
```

---

# 31. Material offline

Preparar localmente:

```text
cuaderno de misiones;
tarjetas de rol;
cheat sheet;
capturas de UI;
JSON de ejemplo;
salida psql;
logs del incidente;
diagrama.
```

Así la sesión puede continuar incluso con una falla mayor.

---

# 32. Simulación pedagógica — objetivo

Ahora se realiza una corrida completa “en papel”.

La simulación busca detectar:

```text
dependencias ocultas;
tiempos muertos;
momentos de confusión;
conceptos prematuros;
puntos frágiles;
sobreexplicación.
```

---

# 33. Simulación — minuto 0 a 10

## Estado

Los alumnos llegan con niveles mixtos.

## Acción

```text
bienvenida;
equipos;
roles;
acceso.
```

## Riesgo

Perder 15 minutos en credenciales.

## Mitigación

```text
credenciales precreadas;
Team ID visible;
entornos prevalidos.
```

## Resultado esperado

A minuto 10:

```text
todos dentro.
```

---

# 34. Simulación — minuto 10 a 16 / M0

Los equipos exploran.

Posibles comportamientos:

```text
avanzado abre F12;
principiante navega;
alguien pregunta stack.
```

Intervención:

```text
“Primero entiendan qué hace.”
```

Resultado:

```text
datos visibles identificados.
```

Sin bloqueo importante.

---

# 35. Simulación — minuto 16 a 25 / M1

Pregunta detonadora:

> “¿De dónde salieron esos puntos?”

Probable respuesta:

```text
“de la base”
```

Instructor:

> “¿Cómo lo sabes?”

Esto empuja a evidencia.

Posible bloqueo:

```text
no conocen Network.
```

P1/P2 suficiente para la mayoría.

Resultado:

```text
GET /api/ranking
200
JSON
```

---

# 36. Simulación — minuto 25 a 34 / M2

El alumno de API usa curl.

Posible problema:

```text
copiar URL equivocada.
```

Pista:

```text
“Usa exactamente la request encontrada.”
```

Resultado:

```text
API independiente de UI.
```

Transición conceptual correcta.

---

# 37. Simulación — minuto 34 a 45 / M3

Primera interacción con PostgreSQL.

Este es el primer salto de dificultad técnico.

Riesgos:

```text
psql intimida;
no saben tablas;
confunden ranking con tabla.
```

Mitigación:

```text
cheat sheet;
\dt;
tabla con nombres comprensibles.
```

Resultado:

```text
mismo dato encontrado en DB.
```

---

# 38. Simulación — minuto 45 a 56 / M4

El equipo cambia un dato.

Riesgo principal:

```text
UPDATE inseguro.
```

Mitigación:

```text
SELECT previo;
team_id;
permisos limitados;
WHERE obligatorio.
```

Momento pedagógico fuerte:

```text
dato cambia en DB
→ cambia API
→ cambia UI.
```

Debe protegerse.

---

# 39. Simulación — minuto 56 a 65 / M5

Se introduce estado de servicios.

Riesgo:

```text
Docker distrae.
```
Mitigación:

No explicar Docker internals.

Solo:

```text
“Estas piezas están ejecutándose por separado.”
```

Resultado:

```text
frontend / api / db como componentes.
```

---

# 40. Simulación — minuto 65 a 70

Punto de control + rotación.

Riesgo:

```text
rotación caótica.
```

Mitigación:

```text
tarjetas claras;
transferencia de 30–45 s;
temporizador.
```

Resultado:

```text
todos sincronizados.
```

---

# 41. Simulación — minuto 70 a 76 / M6

Se activa incidente.

Los alumnos ven:

```text
ranking error.
```

Probables hipótesis:

```text
frontend;
API caída;
DB caída.
```

Esto es deseable.

Regla:

```text
no reparar.
```

Resultado:

```text
500 identificado;
health 200.
```

---

# 42. Simulación — minuto 76 a 99 / M7

Este es el punto crítico.

Flujo esperado:

```text
API viva
↓
DB consultable
↓
logs
↓
error de host
↓
causa
↓
recover
↓
200
```

Riesgo:

```text
logs demasiado claros.
```

Mitigación:

Mostrar evidencia suficiente, no solución textual.

Riesgo:

```text
logs demasiado complejos.
```

Mitigación:

vista pedagógica filtrada.

Resultado:

```text
diagnóstico con dos evidencias;
una hipótesis descartada;
recuperación validada.
```

---

# 43. Simulación — minuto 99 a 101

Buffer.

Si todo salió bien:

```text
respirar;
ordenar evidencia;
preparar M8.
```

Si no:

```text
reset final;
mover equipo;
usar P4.
```

---

# 44. Simulación — minuto 101 a 114 / M8

Los equipos completan arquitectura.

Riesgo:

```text
dibujar Docker entre servicios.
```

Intervención:

> “¿Docker transporta el mensaje o ejecuta las piezas?”

Resultado:

```text
modelo mental explícito.
```

---

# 45. Simulación — minuto 114 a 120

Cierre.

Pregunta central:

> “Hace dos horas esto era una sola aplicación. ¿Cuántas piezas ven ahora?”

Después:

```text
rol favorito;
herramienta nueva;
área de interés;
próximo tema.
```

Resultado:

```text
experiencia cerrada;
intereses capturados.
```

---

# 46. Dependencias detectadas por la simulación

La simulación confirma que ClubLab #01 depende de que existan antes de la clase:

```text
app funcional;
ranking con datos;
API observable;
terminal accesible;
DB con esquema comprensible;
permisos limitados;
status seguro;
logs filtrados;
scenario manager;
reset;
entorno reserva.
```

Estas dependencias alimentan Fases 2–5.

---

# 47. Puntos frágiles detectados

## PF-01 — M3

`psql` puede ser el primer momento intimidante.

Acción futura:

```text
hacer interfaz/cheat sheet muy simple.
```

## PF-02 — M4

`UPDATE` requiere seguridad técnica real.

Acción:

```text
permisos + datos aislados.
```

## PF-03 — M5

Docker puede convertirse en teoría.

Acción:

```text
mantenerlo observable, no profundo.
```

## PF-04 — M7

Logs pueden ser demasiado fáciles o difíciles.

Acción:

```text
diseñar salida pedagógica.
```

## PF-05 — Sincronización

El incidente depende de que todos lleguen al minuto 70.

Acción:

```text
checkpoint obligatorio.
```

---

# 48. Tiempos muertos detectados

No se detecta ningún tiempo muerto estructural importante.

Posibles esperas:

```text
equipos rápidos antes del incidente;
reset de un equipo;
transición tras M7.
```

Ya existen extensiones y buffer para absorberlos.

---

# 49. Sobrecarga conceptual revisada

Conceptos principales por orden:

```text
M0 UI
M1 request
M2 API
M3 DB
M4 flujo
M5 servicios
M6 síntoma
M7 diagnóstico
M8 arquitectura
```

No se observan saltos conceptuales excesivos si las herramientas están simplificadas.

---

# 50. ¿Cabe realmente en 120 minutos?

Resultado de la simulación:

# **SÍ, CON CONDICIONES**

Condiciones:

```text
accesos preconfigurados;
sin instalaciones;
entornos ya desplegados;
pistas activas;
M3 y M4 bien guiadas;
incidente sincronizado;
reset rápido;
instructor controla tiempos.
```

Sin estas condiciones:

```text
la sesión probablemente se extiende.
```

---

# 51. Revisión de objetivos O1–O8

| Objetivo | Dónde se cubre | Estado |
|---|---|---|
| O1 — interfaz vs datos | M1–M3 | Cubierto |
| O2 — reconocer petición | M1 | Cubierto |
| O3 — comprender API | M2 | Cubierto |
| O4 — comprender backend | M2/M5 | Cubierto |
| O5 — persistencia | M3 | Cubierto |
| O6 — BD→API→frontend | M4 | Cubierto |
| O7 — componentes independientes | M5–M7 | Cubierto |
| O8 — diagnóstico con evidencia | M6–M7 | Cubierto |

No quedan objetivos sin actividad asociada.

---

# 52. Revisión de roles

Todos los roles tienen momento útil:

```text
Interfaz → M0/M1/M6
API      → M2/M7
Datos    → M3/M4/M7
Sistemas → M5/M7
Relator  → evidencia/M7/M8
```

No existe un rol claramente decorativo si se aplica correctamente.

---

# 53. Revisión de dificultad

Curva final:

```text
M0  ●
M1  ●●
M2  ●●
M3  ●●●
M4  ●●●
M5  ●●
M6  ●●●
M7  ●●●●
M8  ●●
```

La curva es razonable.

M7 sigue siendo el pico.

---

# 54. Revisión de evidencia

Cada misión produce algo observable.

No existen misiones que terminen únicamente con:

```text
“ya entendí”.
```

Esto facilita evaluación de la experiencia.

---

# 55. Revisión de seguridad pedagógica

La sesión no necesita exponer:

```text
Tulum real;
Docker socket;
sudo;
postgres-main;
credenciales productivas;
redes productivas.
```

Todo puede ocurrir dentro de ClubLab.

---

# 56. Revisión de dependencia del instructor

Riesgo:

```text
demasiadas pistas dependen oralmente del instructor.
```

Mitigación futura:

```text
tarjetas;
cuaderno;
pistas numeradas;
cheat sheet.
```

Esto será importante en Fase 7 y 8.

---

# 57. Criterios de ensayo técnico posterior

Antes de dar la clase real se deberá hacer una ejecución piloto con:

```text
1 equipo simulado;
4 roles;
cronómetro;
todas las misiones;
incidente;
reset;
```

Registrar:

```text
tiempo real;
pistas;
errores;
comandos;
problemas de UX;
logs;
reset.
```

Esto pertenece formalmente a Fase 9.

---

# 58. Contingencia máxima — modo demostración

Solo si ocurre una falla global grave.

El instructor conserva:

```text
capturas de UI;
Network pregrabado;
JSON;
snapshot SQL;
status;
logs del incidente;
diagrama.
```

Puede ejecutar una versión demostrativa interactiva.

No es ideal, pero preserva:

```text
preguntas;
hipótesis;
diagnóstico;
arquitectura.
```

---

# 59. Regla para decidir cancelar

La sesión solo debería cancelarse si no es posible proporcionar:

```text
ninguna interacción;
ninguna evidencia;
ningún entorno;
ninguna simulación.
```

Una falla parcial no justifica cancelar.

---

# 60. Decisiones cerradas en Bloque H

### DH-01
ClubLab tendrá planes B técnicos y pedagógicos.

### DH-02
La sesión debe poder funcionar sin Internet público.

### DH-03
Existirá al menos un entorno de reserva.

### DH-04
Scenario Manager tendrá variante simplificada.

### DH-05
M3, M4 y M7 son los puntos más frágiles.

### DH-06
La simulación confirma que la experiencia cabe en 120 min bajo condiciones controladas.

### DH-07
Los objetivos O1–O8 están cubiertos.

### DH-08
No existen roles sin función real.

### DH-09
Las contingencias deben proteger comprensión antes que realismo técnico.

### DH-10
Debe existir material offline.

### DH-11
La ejecución piloto cronometrada será obligatoria antes de la clase real.

### DH-12
El modo demostración será último recurso, no modalidad normal.

---

# 61. Entregables

Este bloque produce:

```text
P10_Contingencias
P10A_Matriz_Fallos
P10B_Kit_Offline
P10C_Entorno_Reserva
P10D_Reglas_Recuperacion
P11_Revision_Pedagogica
P11A_Simulacion_120min
P11B_Puntos_Fragiles
P11C_Validacion_Objetivos
P11D_Condiciones_Exito
```

---

# 62. Criterios de aceptación

- [x] Fallos de acceso contemplados.
- [x] Fallos de red contemplados.
- [x] Fallos de frontend contemplados.
- [x] Fallos de API contemplados.
- [x] Fallos de DB contemplados.
- [x] Fallos de Scenario Manager contemplados.
- [x] Fallos de recuperación contemplados.
- [x] Equipos rápidos contemplados.
- [x] Equipos lentos contemplados.
- [x] Falta de dispositivos contemplada.
- [x] Falta de integrantes contemplada.
- [x] Llegadas tardías contempladas.
- [x] Material offline definido.
- [x] Simulación completa realizada.
- [x] Puntos frágiles identificados.
- [x] Objetivos O1–O8 validados.
- [x] Roles validados.
- [x] Duración validada conceptualmente.
- [x] Condiciones para 120 min establecidas.

# BLOQUE H — COMPLETADO

---

# 63. Estado de la Fase 1

```text
[A] Perfil + objetivos                    ✅
[B] Narrativa + arquitectura              ✅
[C] Catálogo de misiones                  ✅
[D] Roles + rotación                      ✅
[E] Incidente principal                   ✅
[F] Pistas + extensiones + evidencias     ✅
[G] Cronograma de 120 min                 ✅
[H] Contingencias + simulación            ✅
[I] Consolidación D01                     ← SIGUIENTE
```

---

# 64. Siguiente bloque

# BLOQUE I — Consolidación del D01

El siguiente bloque no diseñará conceptos nuevos.

Su objetivo será reunir todo lo anterior en un único documento coherente:

```text
D01_Diseno_Experiencia_ClubLab_01.md
```

Debe eliminar redundancias entre bloques y dejar una versión lista para guiar las siguientes fases.

La estructura final será aproximadamente:

```text
1. Propósito
2. Público
3. Resultados
4. Principios
5. Narrativa
6. Arquitectura a descubrir
7. Misiones
8. Roles
9. Incidente
10. Pistas y evidencias
11. Cronograma
12. Contingencias
13. Criterios de éxito
14. Requisitos derivados para Fases 2–9
```

Con el Bloque I quedará formalmente cerrada la Fase 1.