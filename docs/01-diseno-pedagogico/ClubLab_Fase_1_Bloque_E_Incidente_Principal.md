# ClubLab — Fase 1 / Bloque E
## Diseño del incidente principal

**Proyecto:** ClubLab v1  
**Experiencia:** ClubLab #01 — *Desarmando una aplicación*  
**Fase:** 1 — Diseño pedagógico  
**Bloque:** E  
**Dependencias:** Bloques A, B, C y D  
**Estado:** CERRADO PARA DISEÑO v1  
**Entregable principal:** `P07_Incidente_Principal`

---

# 1. Propósito del Bloque E

Este bloque define el incidente central de ClubLab #01.

El incidente debe obligar a los integrantes a utilizar lo aprendido durante las misiones anteriores:

```text
UI
Network
API
Base de datos
Servicios
Logs
```

El objetivo no es “arreglar algo roto” por ensayo y error.

El objetivo es:

> **diagnosticar una falla utilizando evidencia de varias capas.**

---

# 2. Incidente principal seleccionado

## Nombre

**INCIDENTE 01 — El ranking dejó de funcionar**

## Situación visible

La aplicación sigue abriendo correctamente.

El usuario puede:

```text
iniciar sesión;
ver su perfil;
ver sus misiones;
ver actividad;
navegar por la aplicación.
```

Pero:

```text
Ranking
→ error
```

o:

```text
Ranking
→ mensaje de “No se pudo cargar”
```

---

# 3. Causa técnica conceptual

La causa recomendada será:

> **La API está funcionando, pero perdió acceso correcto a la base de datos utilizada por el ranking.**

Estado conceptual:

```text
Frontend     = UP
API          = UP
Database     = UP
Conexión API → Database para ranking = FALLA
```

Resultado:

```text
/api/health
→ 200

/api/ranking
→ 500
```

---

# 4. Por qué este incidente

Este escenario se selecciona porque permite demostrar varias ideas importantes al mismo tiempo:

```text
un servicio puede estar “vivo” y aun así fallar;
un 500 no significa necesariamente que la API esté apagada;
una dependencia puede fallar;
no todo el sistema tiene que romperse;
los logs pueden revelar causas que la UI no muestra;
el diagnóstico requiere seguir la ruta del dato.
```

---

# 5. Qué NO debe fallar

Para que el incidente sea pedagógicamente útil:

```text
frontend debe cargar;
login debe seguir funcionando;
otras vistas deben funcionar;
healthcheck general debe responder;
la base de datos debe seguir viva;
el entorno del equipo debe seguir accesible.
```

El fallo debe ser parcial.

---

# 6. Síntoma desde el usuario

Pantalla del ranking:

```text
Ranking

No pudimos cargar el ranking.
Intenta nuevamente.

[Reintentar]
```

Evitar mostrar:

```text
“Database connection refused”
```

directamente al usuario.

La UI debe mostrar un error genérico.

---

# 7. Evidencia en DevTools

El rol de Interfaz debe poder encontrar:

```http
GET /api/ranking
```

con:

```text
Status:
500 Internal Server Error
```

Respuesta sugerida:

```json
{
  "statusCode": 500,
  "message": "Unable to load ranking",
  "error": "Internal Server Error"
}
```

No revelar detalles internos sensibles en la respuesta pública.

---

# 8. Evidencia en `/api/health`

El healthcheck general debe devolver:

```http
200 OK
```

Ejemplo:

```json
{
  "status": "ok",
  "service": "api"
}
```

Esto permite descartar:

```text
“la API está completamente caída”
```

---

# 9. Evidencia en otros endpoints

Al menos uno o dos endpoints adicionales deben continuar funcionando.

Ejemplo:

```http
GET /api/me
→ 200

GET /api/missions
→ 200
```

Así los integrantes pueden comparar:

```text
API general = responde
Ranking = falla
```

---

# 10. Estado de PostgreSQL

La base de datos debe seguir:

```text
running
healthy
```

Y el rol de Datos debe poder ejecutar:

```sql
SELECT 1;
```

o consultar una tabla autorizada.

Esto permite descubrir:

> **La base de datos está viva; el problema está en cómo la API intenta acceder a ella.**

---

# 11. Causa concreta recomendada para implementación futura

La implementación técnica preferida será una configuración rota únicamente para el servicio API del equipo.

Ejemplos válidos:

```text
host de DB incorrecto;
puerto interno incorrecto;
credencial de ClubLab incorrecta;
nombre de base incorrecto;
variable de entorno temporal incorrecta.
```

La opción recomendada para v1:

# **DB_HOST incorrecto para la API del equipo**

Ejemplo conceptual:

```text
Correcto:
DB_HOST=database

Escenario roto:
DB_HOST=database-broken
```

---

# 12. Por qué preferir DB_HOST incorrecto

Ventajas pedagógicas:

```text
la DB sigue viva;
los datos siguen intactos;
el fallo es reversible;
los logs son claros;
no requiere corrupción de datos;
no requiere borrar nada;
no requiere permisos destructivos;
es fácil de resetear;
se puede aplicar por equipo.
```

---

# 13. Lo que mostrarán los logs

El log de API debe ser comprensible.

Ejemplo:

```text
[API] GET /api/ranking
[RankingService] Fetching ranking...
[Database] Connection failed
[Database] Host: database-broken
[Database] Error: getaddrinfo ENOTFOUND database-broken
[API] GET /api/ranking -> 500
```

No debe ser un stack trace enorme como única evidencia.

Puede existir stack trace real internamente, pero la herramienta del alumno debería mostrar una versión legible.

---

# 14. Evidencia por capa

## Interfaz

```text
Ranking no carga.
```

## Network

```text
GET /api/ranking
500
```

## API

```text
/api/health
200
```

## Otros endpoints

```text
/api/missions
200
```

## Base de datos

```text
PostgreSQL
running / healthy
```

## Logs

```text
DB connection failed
ENOTFOUND database-broken
```

---

# 15. Camino lógico esperado

El camino ideal será:

```text
1. La página carga.
2. Ranking falla.
3. Network muestra 500.
4. /api/health responde 200.
5. Otros endpoints responden.
6. La base está viva.
7. Logs de API muestran fallo de conexión.
8. Se identifica configuración de conexión.
9. Se aplica recuperación.
10. Ranking vuelve a responder 200.
```

---

# 16. Hipótesis esperadas

Durante el diagnóstico pueden aparecer:

```text
H1 — El frontend está roto.
H2 — La API está caída.
H3 — La base está caída.
H4 — Los datos desaparecieron.
H5 — La API no puede llegar a la base.
```

La intención es que el equipo vaya descartando hipótesis.

---

# 17. Matriz de hipótesis

| Hipótesis | Evidencia que la debilita |
|---|---|
| Frontend caído | La aplicación carga |
| API caída | `/api/health` responde 200 |
| DB caída | PostgreSQL responde consultas |
| Datos borrados | El registro sigue existiendo |
| Comunicación API↔DB rota | Logs muestran fallo de conexión |

Conclusión esperada:

```text
H5
```

---

# 18. Mensaje del incidente para estudiantes

Texto sugerido:

> ## INCIDENTE 01
>
> El ranking dejó de cargar.
>
> El resto de la aplicación parece seguir funcionando.
>
> Su objetivo no es reiniciar todo.
>
> Encuentren:
>
> - qué funciona;
> - qué falla;
> - qué evidencia tienen;
> - qué componente es responsable;
> - cuál es la acción mínima para recuperarlo.

No revelar causa.

---

# 19. Inicio del incidente

El instructor debe activar el fallo sin anunciar qué componente cambió.

Secuencia:

```text
1. Confirmar que todos terminaron M5.
2. Confirmar sistema sano.
3. Rotar roles.
4. Activar escenario.
5. Esperar 10–20 segundos.
6. Mostrar mensaje INCIDENTE 01.
7. Iniciar M6.
```

---

# 20. Regla de “estado sano”

Antes del incidente debe quedar evidencia de que el sistema funcionaba.

Ejemplo:

```text
/api/ranking → 200
ranking visible
DB accesible
servicios running
```

Así pueden comparar:

```text
ANTES
vs
DESPUÉS
```

---

# 21. Fases del incidente

## Fase I — Observación

M6.

No se permite reparar.

Objetivo:

```text
capturar síntomas
```

---

## Fase II — Diagnóstico

Primera parte de M7.

Objetivo:

```text
aislar causa
```

---

## Fase III — Recuperación

Segunda parte de M7.

Objetivo:

```text
aplicar corrección mínima
```

---

## Fase IV — Verificación

Final de M7.

Objetivo:

```text
demostrar que volvió
```

---

# 22. Evidencia obligatoria antes de recuperar

El equipo debe presentar:

```text
Síntoma:
Ranking no carga.

Evidencia 1:
GET /api/ranking → 500

Evidencia 2:
/api/health → 200

Evidencia 3:
DB responde.

Hipótesis:
La API no puede conectarse correctamente a DB.
```

No es obligatorio usar exactamente tres evidencias, pero sí al menos dos.

---

# 23. Acción de recuperación

La recuperación para estudiantes no debe implicar editar Docker Compose ni variables del host.

Debe existir una acción controlada.

Ejemplo conceptual:

```bash
clublab recover ranking-db
```

o:

```bash
clublab scenario repair
```

La herramienta realizará internamente:

```text
restaurar configuración correcta;
reiniciar/recrear únicamente API del equipo;
esperar healthcheck;
confirmar recuperación.
```

---

# 24. Filosofía de recuperación

Los estudiantes deben entender qué se está corrigiendo.

No queremos:

```text
“ejecuten este botón mágico”
```

La interfaz de recuperación debería explicar:

```text
Restaurando configuración de conexión API → Database...
Reiniciando servicio API del equipo...
Esperando healthcheck...
API healthy.
```

---

# 25. Validación después de recuperar

El equipo debe comprobar tres cosas:

```text
1. /api/health → 200
2. /api/ranking → 200
3. Ranking visible en frontend
```

Opcional:

```text
4. logs sin nuevos errores de conexión
```

---

# 26. Condición de éxito

El incidente se considera resuelto solo si el equipo puede responder:

```text
¿Qué falló?
¿Por qué?
¿Qué evidencia lo demostró?
¿Qué acción realizaron?
¿Cómo comprobaron que funcionó?
```

---

# 27. Pistas del incidente

## Pista 0

No intervenir.

---

## Pista 1 — síntoma

> “¿Qué partes de la aplicación siguen funcionando?”

Objetivo:

```text
evitar asumir caída total
```

---

## Pista 2 — API

> “¿La API está completamente caída o solo falla una operación?”

Objetivo:

```text
comparar endpoints
```

---

## Pista 3 — dependencia

> “La API recibió la petición. ¿Qué necesita consultar para construir el ranking?”

Objetivo:

```text
pensar en DB
```

---

## Pista 4 — logs

> “Revisen qué reporta la API cuando intenta obtener el ranking.”

Objetivo:

```text
llegar a logs
```

---

## Pista 5 — causa casi explícita

> “El servicio está intentando encontrar un host de base de datos que no existe.”

Solo para desbloqueo.

---

# 28. Qué NO debe decir el instructor

Evitar:

```text
“la base está mal configurada”
“revisen DB_HOST”
“reinicien la API”
“miren este log exacto”
```

antes de agotar pistas previas.

---

# 29. Errores esperados

## Error 1 — “Frontend roto”

Porque la pantalla del ranking falla.

Respuesta:

> “¿El resto de la aplicación carga?”

---

## Error 2 — “API caída”

Porque hay status 500.

Respuesta:

> “¿Qué devuelve `/api/health`?”

---

## Error 3 — “DB caída”

Porque el ranking depende de datos.

Respuesta:

> “¿Pueden consultar la base directamente?”

---

## Error 4 — Reiniciar API inmediatamente

Respuesta:

> “¿Qué evidencia indica que reiniciarla resolvería la causa?”

---

## Error 5 — Reset total

No permitirlo como primera acción.

---

# 30. Qué aprende cada rol durante el incidente

## Interfaz

Descubre:

```text
síntoma visible ≠ causa
```

---

## API

Descubre:

```text
500 ≠ servicio apagado
```

---

## Datos

Descubre:

```text
DB viva ≠ aplicación capaz de conectarse
```

---

## Sistemas

Descubre:

```text
logs + health permiten aislar dependencias
```

---

## Relator

Descubre:

```text
una hipótesis necesita evidencia convergente
```

---

# 31. Variante simplificada

## Nombre

**INCIDENTE 01-B — API detenida**

Estado:

```text
Frontend = UP
API = DOWN
DB = UP
```

Síntomas:

```text
/api/health → error / conexión rechazada
/api/ranking → error / conexión rechazada
frontend carga estático
datos dinámicos fallan
```

Logs:

```text
servicio API stopped
```

Recuperación:

```text
start api
```

Uso:

```text
grupo muy principiante;
tiempo insuficiente;
problema técnico con escenario principal.
```

---

# 32. Variante avanzada

## Nombre

**INCIDENTE 01-C — Credenciales incorrectas**

Estado:

```text
API = UP
DB = UP
API → DB = auth failure
```

Log:

```text
password authentication failed for user "clublab_team01"
```

Ventajas:

```text
más realista;
introduce autenticación entre servicios.
```

Desventaja:

```text
puede abrir demasiados conceptos para ClubLab #01.
```

No usar en la primera edición salvo grupo avanzado.

---

# 33. Variante alternativa futura

Otros incidentes posibles para sesiones posteriores:

```text
dato inconsistente;
migración faltante;
endpoint roto;
cache desactualizada;
timeout;
DNS;
servicio lento;
auth expirada;
WebSocket caído;
permiso de DB incorrecto.
```

No mezclar con ClubLab #01.

---

# 34. Duración objetivo del incidente

```text
M6 observación      5–7 min
M7 diagnóstico     12–15 min
M7 recuperación     5 min
M7 validación       3 min
```

Total:

```text
25–30 minutos
```

Si supera 30 minutos:

```text
aumentar nivel de pista
o
activar variante simplificada
```

---

# 35. Estado inicial y final

## Antes

```text
frontend     healthy
api          healthy
database     healthy
ranking      200
```

## Durante

```text
frontend     healthy
api          healthy
database     healthy
ranking      500
api→db       broken
```

## Después

```text
frontend     healthy
api          healthy
database     healthy
ranking      200
```

---

# 36. Requisito de reproducibilidad

El escenario debe poder cargarse repetidamente sin acumular daño.

Ciclo:

```text
normal
  ↓
load incident
  ↓
diagnose
  ↓
recover
  ↓
normal```

Debe poder repetirse:

```text
N veces
```

sin recrear manualmente todo el laboratorio.

---

# 37. Requisito de aislamiento

Activar el incidente en:

```text
team01
```

no debe afectar:

```text
team02
team03
...
```

Cada equipo debe tener su propio estado de escenario.

---

# 38. Requisito de reset del instructor

El instructor debe poder ejecutar conceptualmente:

```bash
clublab reset team01
```

Resultado:

```text
configuración sana;
datos iniciales restaurados si aplica;
servicios healthy;
misiones utilizables.
```

Este comportamiento se implementará en Fase 5.

---

# 39. Requisito de observabilidad

El entorno deberá exponer a estudiantes solo logs relevantes de su equipo.

Ejemplo:

```bash
clublab logs api
```

No:

```bash
docker logs <host-container>
```

La herramienta debe filtrar:

```text
secrets;
tokens;
variables sensibles;
stack traces excesivos.
```

---

# 40. Requisito de healthcheck

Deben existir al menos:

```text
API health
Database health
Frontend reachability
```

Idealmente:

```text
clublab health
```

podrá resumirlos.

Pero durante M6 no debe revelar automáticamente la causa exacta.

---

# 41. Healthcheck pedagógico vs healthcheck técnico

## Técnico

Puede comprobar:

```text
proceso
TCP
DB
dependencias
```

## Pedagógico

Debe evitar mostrar:

```text
“ERROR: DB_HOST INCORRECTO”
```

directamente.

Queremos evidencia, no solución automática.

---

# 42. Diseño de logs pedagógicos

Formato ideal:

```text
timestamp
servicio
acción
resultado
detalle breve
```

Ejemplo:

```text
20:14:03 API      GET /api/ranking
20:14:03 RANKING  loading scores
20:14:03 DATABASE connecting to database-broken:5432
20:14:03 DATABASE connection failed: host not found
20:14:03 API      GET /api/ranking → 500
```

---

# 43. Qué no mostrar en logs del alumno

Excluir:

```text
contraseñas;
tokens;
JWT secrets;
connection strings completos con password;
datos productivos;
IPs del host real;
rutas sensibles;
variables de entorno completas.
```

---

# 44. Evidencia final del incidente

Cada equipo debe entregar:

```text
SÍNTOMA
¿Qué vio el usuario?

EVIDENCIA UI
¿Qué request falló?

EVIDENCIA API
¿Qué respondió?

EVIDENCIA DATOS
¿La DB estaba viva?

EVIDENCIA SISTEMAS
¿Qué dijeron los logs?

CAUSA
¿Qué falló?

RECUPERACIÓN
¿Qué acción mínima realizaron?

VALIDACIÓN
¿Cómo comprobaron que volvió?
```

---

# 45. Plantilla de diagnóstico

```text
INCIDENTE 01

Síntoma:
________________________________

¿Qué sigue funcionando?
________________________________

¿Qué falla?
________________________________

Hipótesis inicial:
________________________________

Evidencia 1:
________________________________

Evidencia 2:
________________________________

Componente responsable:
________________________________

Causa:
________________________________

Acción de recuperación:
________________________________

Validación:
________________________________
```

Esta plantilla se reutilizará en el Cuaderno de Misiones.

---

# 46. Métrica pedagógica del incidente

El incidente funciona correctamente si la mayoría de equipos:

```text
no descubre la causa instantáneamente;
puede avanzar con evidencia;
formula al menos una hipótesis incorrecta;
logra descartarla;
usa dos herramientas o más;
puede explicar la causa después.
```

---

# 47. Señales de que es demasiado fácil

```text
todos identifican la causa en menos de 3 minutos;
el mensaje de error revela DB_HOST;
health muestra directamente la solución;
solo se necesita un comando.
```

---

# 48. Señales de que es demasiado difícil

```text
nadie sabe qué revisar;
los logs son incomprensibles;
requiere conceptos no vistos;
todos necesitan pista 5;
dura más de 30 minutos;
se convierte en debugging de framework.
```

---

# 49. Criterio de ajuste después del ensayo

Después de la prueba piloto:

```text
< 10 min sin pistas
→ probablemente demasiado fácil

15–25 min con pistas 1–3
→ rango ideal

> 30 min
→ simplificar
```

---

# 50. Decisiones cerradas en Bloque E

### DE-01

El incidente principal será una falla parcial del ranking.

### DE-02

Frontend, API y DB permanecerán encendidos.

### DE-03

`/api/health` responderá correctamente.

### DE-04

`/api/ranking` devolverá 500.

### DE-05

La causa recomendada será configuración incorrecta de acceso API → DB.

### DE-06

La implementación preferida será un `DB_HOST` incorrecto controlado por escenario.

### DE-07

Los logs serán legibles y filtrados.

### DE-08

La recuperación será específica, no un reset global.

### DE-09

El diagnóstico requerirá al menos dos evidencias.

### DE-10

Existirá una variante simplificada con API detenida.

### DE-11

El incidente debe ser reproducible y aislado por equipo.

### DE-12

El Scenario Manager será responsable de cargar, recuperar y resetear el escenario en fases posteriores.

---

# 51. Entregables del Bloque E

Este bloque produce:

```text
P07_Incidente_Principal
P07A_Matriz_Sintomas
P07B_Matriz_Hipotesis
P07C_Pistas_Incidente
P07D_Plantilla_Diagnostico
P07E_Variante_Simplificada
P07F_Requisitos_Scenario_Manager
```

---

# 52. Criterios de aceptación

- [x] Causa conceptual definida.
- [x] Síntoma de UI definido.
- [x] Respuesta Network definida.
- [x] Respuesta API definida.
- [x] Healthcheck definido.
- [x] Estado de DB definido.
- [x] Logs esperados definidos.
- [x] Hipótesis incorrectas previstas.
- [x] Pistas escalonadas definidas.
- [x] Recuperación mínima definida.
- [x] Validación posterior definida.
- [x] Variante simplificada definida.
- [x] Reproducibilidad definida.
- [x] Aislamiento por equipo definido.
- [x] Plantilla de diagnóstico definida.
- [x] Requisitos del Scenario Manager derivados.

# BLOQUE E — COMPLETADO

---

# 53. Siguiente bloque

# BLOQUE F — Pistas + extensiones + evidencias

El siguiente bloque consolidará todo el sistema de ayudas y evidencias de ClubLab #01.

Se definirá:

```text
pista 1, 2 y 3 de cada misión;
regla de cuándo dar pistas;
extensiones para equipos rápidos;
evidencia mínima por misión;
formato del Cuaderno de Misiones;
qué debe observar el instructor;
qué evidencia debe conservarse;
qué actividades pueden omitirse si falta tiempo;
cómo diferenciar comprensión de simple ejecución.
```

El resultado servirá directamente para crear después:

```text
D07 Cheat Sheet
D08 Cuaderno de Misiones
D09 Manual del Instructor
```