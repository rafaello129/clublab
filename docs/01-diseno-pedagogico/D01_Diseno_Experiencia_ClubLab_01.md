# D01 — Diseño de Experiencia ClubLab #01
## Desarmando una aplicación

**Proyecto:** ClubLab v1  
**Fase:** 1 — Diseño pedagógico  
**Estado:** FINAL — FASE 1 COMPLETADA  
**Duración objetivo:** 120 minutos  
**Modalidad:** Presencial, práctica y colaborativa  
**Dependencia técnica:** `D00_Estado_Base_Servidor_ClubLab.md`

---

# 1. Propósito

ClubLab #01 es una experiencia práctica para que integrantes con niveles técnicos distintos descubran cómo está compuesta una aplicación moderna.

La sesión no busca enseñar sintaxis de React, NestJS, PostgreSQL, Docker o Linux.

Busca que el participante deje de pensar:

```text
“la aplicación”
```

como una sola caja y empiece a verla como un sistema de componentes relacionados:

```text
Usuario
  ↓
Navegador
  ↓
Frontend
  ↓
HTTP / API
  ↓
Backend
  ↓
Base de datos
```

ejecutados sobre infraestructura real.

La filosofía principal es:

```text
OBSERVAR
   ↓
PREGUNTAR
   ↓
PROBAR
   ↓
DESCUBRIR
   ↓
EXPLICAR
```

---

# 2. Resultado final esperado

Al terminar la sesión, un integrante debe poder explicar con sus propias palabras que:

> Una aplicación moderna está compuesta por varias partes. El navegador muestra una interfaz; el frontend realiza peticiones; una API/backend procesa esas peticiones; los datos pueden persistir en una base de datos; los componentes se ejecutan como servicios separados; y cuando algo falla se puede investigar siguiendo evidencia.

No se espera que el participante sea capaz de construir profesionalmente todas esas piezas después de dos horas.

El objetivo es **comprensión estructural y capacidad inicial de diagnóstico**.

---

# 3. Público objetivo

ClubLab #01 está diseñado para niveles mixtos:

```text
Principiante
→ conoce lógica o ha programado poco

Intermedio
→ ya ha creado proyectos pequeños

Avanzado
→ conoce alguna parte de web, backend,
   bases de datos o infraestructura
```

No se debe asumir conocimiento previo de:

```text
Docker
Linux
PostgreSQL
HTTP
REST
DevTools
redes
servidores
React
NestJS
```

Requisitos mínimos:

```text
usar un navegador
seguir instrucciones
trabajar en equipo
ejecutar comandos simples con apoyo
formular hipótesis
```

---

# 4. Organización de equipos

Configuración ideal:

```text
4 integrantes por equipo
```

Rango pedagógico previsto:

```text
2–6 equipos
8–24 participantes aproximadamente
```

Configuraciones soportadas:

```text
5 personas → agregar Relator / Analista
4 personas → configuración ideal
3 personas → combinar API + Datos
2 personas → combinar Interfaz+API / Datos+Sistemas
1 persona   → posible como contingencia, no recomendado
```

Requisito mínimo de dispositivo:

```text
1 laptop por equipo
```

Recomendado:

```text
1 laptop por integrante
```

La sesión debe evitar instalaciones durante la clase. El navegador será el único requisito local imprescindible.

---

# 5. Principios pedagógicos

## 5.1 Experimentar antes de explicar

Los conceptos aparecen después de observar evidencia.

```text
CONCEPTO OBSERVADO
       ↓
EVIDENCIA
       ↓
NOMBRE TÉCNICO
       ↓
EXPLICACIÓN BREVE
```

No:

```text
DEFINICIÓN
   ↓
TEORÍA
   ↓
SINTAXIS
   ↓
EJERCICIO
```

---

## 5.2 El participante debe tocar el sistema

Cada equipo debe poder:

```text
abrir
inspeccionar
consultar
modificar
romper
diagnosticar
recuperar
```

su propio entorno de laboratorio.

---

## 5.3 El error forma parte del aprendizaje

Los fallos deben ser:

```text
controlados
repetibles
diagnosticables
reversibles
aislados
```

---

## 5.4 Herramientas con propósito

No habrá bloques independientes como:

```text
“10 minutos de curl”
“15 minutos de SQL”
“20 minutos de Docker”
```

Las herramientas aparecerán porque ayudan a responder una pregunta real.

---

## 5.5 Evidencia antes que intuición

El lenguaje buscado es:

```text
“Creemos X porque observamos Y.”
```

No:

```text
“Seguro es la base.”
“Reinicia a ver si funciona.”
```

---

# 6. Objetivos de aprendizaje

Se establecen ocho objetivos obligatorios.

| ID | Objetivo | Evidencia principal |
|---|---|---|
| O1 | Diferenciar interfaz y datos | rastrear un dato visible |
| O2 | Reconocer una petición | observar método, URL y status |
| O3 | Comprender una API | consultar un endpoint sin frontend |
| O4 | Comprender el backend | relacionar request, lógica y respuesta |
| O5 | Comprender persistencia | localizar el dato en PostgreSQL |
| O6 | Relacionar BD → API → frontend | modificar y observar propagación |
| O7 | Entender componentes independientes | observar estados separados |
| O8 | Diagnosticar usando evidencia | incidente con múltiples fuentes |

Objetivo mínimo de comprensión:

```text
C2 — relaciona causa y efecto
```

Escala de observación:

```text
C0 — ejecuta sin entender
C1 — describe lo ocurrido
C2 — relaciona causa y efecto
C3 — puede predecir una variante
```

---

# 7. Narrativa de la experiencia

Nombre:

# ClubLab #01 — Desarmando una aplicación

Subtítulo:

> **¿Qué hay detrás de lo que ves en pantalla?**

Consigna inicial:

> **“La aplicación ya está funcionando. Su trabajo no es programarla: su trabajo es descubrir cómo funciona.”**

La sesión tiene cuatro actos:

```text
ACTO I   — DESCUBRIR
ACTO II  — CONECTAR
ACTO III — INCIDENTE
ACTO IV  — RECONSTRUIR
```

La primera pregunta detonadora será:

> **“Ese número que aparece en el ranking, ¿de dónde salió?”**

Si alguien responde:

> “De la base de datos.”

la respuesta del instructor será:

> **“¿Cómo lo sabes?”**

---

# 8. Arquitectura que debe descubrirse

Modelo inicial del alumno:

```text
┌─────────────────┐
│   APLICACIÓN    │
└─────────────────┘
```

Modelo mínimo final:

```text
USUARIO
   │
   ▼
NAVEGADOR
   │
   ▼
FRONTEND
   │
   │ HTTP
   ▼
API / BACKEND
   │
   ▼
POSTGRESQL
```

Posteriormente se añade infraestructura:

```text
                    SERVIDOR
                       │
                     Docker
                       │
        ┌──────────────┼──────────────┐
        │              │              │
    Frontend          API        PostgreSQL
```

No se exige precisión avanzada sobre redes, namespaces, layers, reverse proxies o internals de Docker.

---

# 9. Regla de revelación

Los términos técnicos se introducen después del descubrimiento.

Orden:

```text
UI visible
→ request
→ HTTP
→ JSON
→ API
→ backend
→ persistencia
→ PostgreSQL
→ servicios
→ contenedores/Docker
```

El código fuente aparece tarde, después de comprender el flujo.

Puede mostrarse posteriormente algo como:

```ts
@Get('ranking')
```

o:

```ts
const POINTS_PER_MISSION = 20;
```

pero comprender frameworks no será requisito para avanzar.

---

# 10. Roles

## R1 — Explorador de Interfaz

Pregunta:

> ¿Qué ve el usuario y qué ocurre al interactuar?

Herramientas:

```text
Navegador
DevTools
Network
Fetch/XHR
Headers
Response
```

Aporta:

```text
síntomas
requests
status
errores visibles
```

---

## R2 — Investigador de API

Pregunta:

> ¿Qué pide la aplicación y qué responde el sistema?

Herramientas:

```text
curl
HTTP
JSON
health endpoints
```

Aporta:

```text
endpoint
método
status
respuesta
comparaciones
```

---

## R3 — Investigador de Datos

Pregunta:

> ¿Dónde vive la información?

Herramientas:

```text
psql
SELECT
UPDATE controlado
```

Aporta:

```text
tabla
columna
registro
valor
cambio
```

---

## R4 — Operador de Sistemas

Pregunta:

> ¿Qué componentes están activos y cuál podría estar fallando?

Herramientas conceptuales:

```text
clublab status
clublab health
clublab logs
clublab recover
```

Aporta:

```text
estado
healthchecks
logs
acción de recuperación
```

---

## R5 — Relator / Analista

Opcional para equipos de cinco.

Pregunta:

> ¿Qué sabemos y qué estamos suponiendo?

Aporta:

```text
hipótesis
evidencias
diagrama
resumen
```

---

# 11. Reglas de participación

En cada misión:

```text
1 persona opera
1 observa
1 verifica
1 registra
```

Regla del teclado:

> **El rol principal de la misión controla el teclado.**

Antes de ejecutar una acción importante debe decir:

```text
qué va a probar
+
qué espera que ocurra
```

Esto convierte cada comando en experimento.

---

# 12. Rotación

Antes del incidente:

```text
Interfaz ↔ Sistemas
API      ↔ Datos
```

Ejemplo:

```text
A: Interfaz → Sistemas
B: API      → Datos
C: Datos    → API
D: Sistemas → Interfaz
```

Cada participante dispone de 30–45 segundos para transferir:

```text
herramienta
hallazgo
dato importante
error a evitar
```

La rotación completa no debe superar dos minutos.

---

# 13. Catálogo de misiones

```text
M0 — Reconocimiento
M1 — ¿De dónde vienen los datos?
M2 — Habla con la API
M3 — Encuentra dónde viven los datos
M4 — Cambia el sistema
M5 — ¿Dónde se está ejecutando?
M6 — Algo se rompió
M7 — Diagnostica y recupera
M8 — Reconstruye la arquitectura
```

---

# 14. M0 — Reconocimiento

**Pregunta:** ¿Qué hace la aplicación?

El equipo explora:

```text
perfil
equipo
ranking
misiones
actividad
```

Evidencia:

```text
puntos
posición
misión visible
dato a investigar
```

Descubrimiento:

> La aplicación contiene distintas vistas y datos relacionados.

Tiempo normal:

```text
6 min
```

---

# 15. M1 — ¿De dónde vienen los datos?

**Pregunta:** ¿De dónde salió el valor del ranking?

Herramientas:

```text
DevTools
Network
Fetch/XHR
```

Evidencia:

```text
método
endpoint
status
dato observado
```

Resultado esperado:

```text
GET /api/ranking
→ 200
```

Descubrimiento:

> El navegador realiza peticiones para obtener información.

Tiempo:

```text
9 min
```

---

# 16. M2 — Habla con la API

**Pregunta:** ¿Podemos obtener la información sin usar la interfaz?

Herramienta:

```bash
curl -i <endpoint>
```

Evidencia:

```text
status
JSON
dato coincidente con UI
```

Descubrimiento:

> La API puede consultarse directamente.

Tiempo:

```text
9 min
```

---

# 17. M3 — Encuentra dónde viven los datos

**Pregunta:** ¿Dónde persiste el dato?

Herramientas:

```text
psql
\dt
\d tabla
SELECT
```

Evidencia:

```text
tabla
columna
identificador
valor
```

Cadena que debe descubrirse:

```text
UI
→ JSON
→ registro SQL
```

Tiempo:

```text
11 min
```

---

# 18. M4 — Cambia el sistema

**Pregunta:** ¿Qué ocurre si cambiamos el dato desde su origen?

Proceso:

```text
SELECT
→ predicción
→ UPDATE autorizado
→ API
→ recargar UI
```

Evidencia:

```text
valor anterior
valor nuevo
respuesta API
valor final en UI
```

Descubrimiento:

```text
PostgreSQL
   ↓
Backend
   ↓
API
   ↓
Frontend
```

Tiempo:

```text
11 min
```

---

# 19. M5 — ¿Dónde se está ejecutando?

**Pregunta:** ¿Todo es un solo programa?

El alumno observa, mediante una interfaz segura:

```text
frontend   running
api        running
database   running
toolbox    running
```

No recibe acceso a Docker del host.

Evidencia:

```text
servicios
estado
healthcheck
```

Descubrimiento:

> Los componentes pueden ejecutarse y fallar por separado.

Tiempo:

```text
9 min
```

---

# 20. M6 — Algo se rompió

Mensaje:

> **INCIDENTE 01 — El ranking dejó de cargar. El resto de la aplicación parece funcionar. No reinicien cosas al azar. Encuentren evidencia.**

Durante M6 no se permite recuperar.

Se debe registrar:

```text
qué funciona
qué falla
request fallida
status
hipótesis inicial
```

Descubrimiento:

> Síntoma y causa no son lo mismo.

Tiempo:

```text
6 min
```

---

# 21. M7 — Diagnostica y recupera

Esta es la misión central.

El equipo debe responder:

```text
¿Qué componente falló?
¿Qué evidencia lo demuestra?
¿Qué hipótesis descartaron?
¿Qué acción mínima lo recupera?
```

Evidencia obligatoria:

```text
Síntoma
Hipótesis
Evidencia 1
Evidencia 2
Hipótesis descartada
Componente responsable
Causa
Acción
Resultado
```

No se permite:

```text
reiniciar todo
reset total como primera acción
borrar datos
```

Tiempo:

```text
23 min
```

---

# 22. M8 — Reconstruye la arquitectura

El equipo completa su diagrama y explica:

```text
qué pidió el navegador
quién respondió
de dónde salió el dato
qué falló
cómo lo demostraron
```

Evidencia:

```text
diagrama
+
explicación oral de 60–90 s
```

Tiempo:

```text
13 min
```

---

# 23. Incidente principal

## Síntoma

```text
Frontend = UP
API = UP
Database = UP
Ranking = ERROR
```

Comportamiento esperado:

```text
/api/health  → 200
/api/ranking → 500
```

El frontend muestra un mensaje genérico:

```text
“No se pudo cargar el ranking.”
```

---

# 24. Causa conceptual

La API no puede utilizar correctamente su dependencia de datos para construir el ranking.

Cadena:

```text
Browser
  ↓
Frontend
  ↓
API
  ↓
X  comunicación/dependencia de datos
  ↓
DB
```

La base continúa viva.

---

# 25. Implementación preferida del fallo

La propuesta inicial es introducir una configuración incorrecta de conexión a datos dentro del entorno del equipo.

Conceptualmente:

```text
host correcto:
database

host de escenario:
database-broken
```

Los logs pedagógicos podrían mostrar:

```text
API      GET /api/ranking
RANKING  loading scores
DATABASE connecting...
DATABASE host not found
API      /api/ranking → 500
```

---

# 26. Ajuste técnico obligatorio derivado de la consolidación

El objetivo pedagógico exige que el fallo sea **parcial**.
Si la arquitectura futura utiliza una única conexión global a PostgreSQL para todos los endpoints, cambiar globalmente `DB_HOST` provocaría que cualquier endpoint dependiente de DB falle, no solamente el ranking.

Por ello, en Fase 5 la inyección del incidente deberá cumplir una de estas estrategias:

```text
A. dependencia de datos específica de ranking;
B. configuración scoped al RankingService;
C. proxy/fault injection únicamente para consultas de ranking;
D. escenario equivalente que preserve:
   API health = 200
   otros endpoints clave = 200
   ranking = 500
```

La experiencia pedagógica es la restricción; la implementación exacta queda abierta.

---

# 27. Evidencia del incidente por capa

```text
UI
→ ranking no carga

Network
→ GET /api/ranking = 500

API health
→ 200

otro endpoint
→ 200

Database
→ healthy / consultable

Logs
→ error de dependencia/conexión del ranking
```

Camino esperado:

```text
síntoma
→ request
→ comparar endpoints
→ comprobar DB
→ logs
→ causa
→ recover
→ validar
```

---

# 28. Recuperación

La recuperación debe ser controlada y específica.

Interfaz conceptual:

```bash
clublab recover ranking-db
```

o equivalente.

No debe requerir:

```text
Docker Compose manual
sudo
systemctl del host
editar archivos de producción
```

La herramienta debe hacer visible lo que ocurre:

```text
restaurando configuración
recreando/reiniciando componente afectado
esperando healthcheck
healthy
```

Validación obligatoria:

```text
/api/health  → 200
/api/ranking → 200
UI ranking   → visible
```

---

# 29. Variante simplificada del incidente

Plan B:

```text
Frontend = UP
API = DOWN
DB = UP
```

Se utilizará si:

```text
el grupo es muy principiante
el tiempo se reduce
el escenario principal falla técnicamente
```

No será la variante por defecto.

---

# 30. Sistema de pistas

```text
P0 — sin ayuda
P1 — pregunta conceptual
P2 — dirección hacia herramienta/capa
P3 — instrucción concreta
P4 — desbloqueo excepcional
```

Timing orientativo:

```text
2–3 min → P1
2–3 min → P2
2 min   → P3
riesgo de romper cronograma → P4
```

Pedir pista no tiene penalización.

---

# 31. Pistas clave del incidente

```text
P1
“¿Qué partes siguen funcionando?”

P2
“¿La API está totalmente caída o solo una operación?”

P3
“La API está viva. Revisen qué reporta al obtener el ranking.”

P4
“El servicio intenta resolver una dependencia de base de datos incorrecta.”
```

P4 solo se utiliza para proteger el cronograma.

---

# 32. Extensiones avanzadas

Los equipos que terminen antes pueden:

```text
comparar dos requests
probar IDs válidos/inexistentes
encontrar relaciones entre tablas
relacionar puertos y healthchecks
crear matriz de hipótesis
mejorar el diagrama con HTTP/JSON/logs/red
```

No pueden:

```text
adelantar el incidente
afectar otros equipos
obtener permisos adicionales
explorar producción
```

---

# 33. Cronograma exacto

| Tiempo | Actividad |
|---|---|
| 00:00–00:05 | Bienvenida + reglas |
| 00:05–00:10 | Equipos + roles + acceso |
| 00:10–00:16 | M0 |
| 00:16–00:25 | M1 |
| 00:25–00:34 | M2 |
| 00:34–00:45 | M3 |
| 00:45–00:56 | M4 |
| 00:56–01:05 | M5 |
| 01:05–01:08 | Punto de control |
| 01:08–01:10 | Rotación |
| 01:10–01:16 | M6 |
| 01:16–01:39 | M7 |
| 01:39–01:41 | Buffer |
| 01:41–01:54 | M8 |
| 01:54–02:00 | Cierre |

Hitos del instructor:

```text
00:10 → iniciar M0
00:34 → iniciar M3
01:10 → activar incidente
01:41 → iniciar M8
01:54 → iniciar cierre
```

---

# 34. Barrera de sincronización

Los equipos pueden llevar ritmos ligeramente diferentes en M0–M5.

Sin embargo:

> **Ningún equipo entra al incidente antes del minuto 70.**

Entre M5 y M6:

```text
punto de control
+
rotación
+
sincronización
```

Los equipos rápidos trabajan extensiones mientras esperan.

---

# 35. Evidencia final mínima

Cada equipo debe terminar con:

```text
1 request identificada
1 consulta directa a API
1 dato localizado en DB
1 modificación extremo a extremo
1 mapa de servicios
1 hipótesis descartada
1 diagnóstico con dos evidencias
1 recuperación validada
1 diagrama final
```

La frase:

```text
“ya funcionó”
```

no cuenta como evidencia suficiente.

---

# 36. Cierre de cada misión

Cada misión termina respondiendo:

> **“¿Qué acabamos de descubrir?”**

Ejemplos:

```text
M1:
“El navegador realiza peticiones.”

M2:
“La API puede responder sin la interfaz.”

M3:
“Los datos persisten fuera del navegador.”

M5:
“La aplicación tiene servicios separados.”

M7:
“Diagnosticar es seguir evidencia y descartar hipótesis.”
```

---

# 37. Cierre de la sesión

Pregunta principal:

> **“Hace dos horas esto era una sola aplicación. ¿Cuántas piezas ven ahora?”**

Preguntas finales:

```text
¿Qué rol disfrutaste más?
¿Qué herramienta no conocías?
¿Qué parte te dio más curiosidad?
¿Qué área te gustaría explorar después?
```

Estas respuestas ayudan a elegir futuros ClubLab:

```text
frontend
backend
bases de datos
redes
DevOps
ciberseguridad
tiempo real
```

---

# 38. Contingencias

La experiencia debe sobrevivir a fallos parciales.

Principio:

```text
comprensión pedagógica
>
realismo técnico perfecto
```

Se contemplan:

```text
fallo de acceso
Internet caído
LAN/Tailscale con problemas
frontend accidentalmente caído
API accidentalmente caída
DB inaccesible
UPDATE fallido
Scenario Manager fallando
incidente no recuperable
falta de laptops
equipos incompletos
participantes tardíos
equipos demasiado rápidos/lentos
```

---

# 39. Kit mínimo de contingencia

El instructor debe disponer de:

```text
1 entorno de reserva
credenciales de respaldo
respuesta JSON preparada
snapshot de tablas
logs de incidente
capturas de UI
diagrama incompleto
diagrama final
versión 90 min
reset rápido
lista de Team IDs
```

La sesión debe poder ejecutarse sin depender de Internet público.

---

# 40. Modo demostración de emergencia

Solo ante fallo global grave.

Se utilizan:

```text
capturas
Network pregrabado
JSON
snapshot SQL
status
logs
diagrama
```

Los alumnos aún deben:

```text
formular hipótesis
interpretar evidencia
diagnosticar
reconstruir arquitectura
```

No es la modalidad normal.

---

# 41. Puntos frágiles

La simulación identifica cinco áreas que requieren especial atención técnica:

## PF-01 — M3 / PostgreSQL

`psql` puede intimidar.

Requisito:

```text
cheat sheet muy simple
esquema comprensible
```

## PF-02 — M4 / UPDATE

Debe ser imposible dañar otro equipo.

Requisito:

```text
permisos técnicos
aislamiento
filtro por equipo
```

## PF-03 — M5 / Docker

No convertir la sesión en teoría de contenedores.

## PF-04 — M7 / Logs

Deben ser:

```text
reales
legibles
filtrados
no reveladores
```

## PF-05 — Sincronización

El incidente debe activarse de forma coordinada.

---

# 42. Validación de la simulación

La corrida pedagógica completa confirma que la experiencia **cabe en 120 minutos**, bajo estas condiciones:

```text
accesos preconfigurados
sin instalaciones durante clase
entornos desplegados
pistas preparadas
M3/M4 simplificadas
reset rápido
incidente sincronizado
control de tiempos
```

Si estas condiciones no se cumplen, la duración puede crecer significativamente.

---

# 43. Versiones reducidas

Existirán:

```text
120 min → versión normal
105 min → contingencia logística
90 min  → contingencia seria
```

El orden de recorte será:

```text
extensiones
detalles secundarios
presentaciones largas
contenido avanzado
```

Se protege especialmente:

```text
M1
M2
M3
M4
M6
M7
cierre
```

---

# 44. Límites de seguridad pedagógica y técnica

Los integrantes nunca necesitarán:

```text
SSH a Tulum
usuario tulum
sudo
Docker socket
grupo docker
postgres-main
whatsapp_db
redes productivas
credenciales productivas
```

Los alumnos interactúan únicamente con recursos ClubLab.

---

# 45. Decisiones pedagógicas congeladas

Las siguientes decisiones quedan cerradas al terminar Fase 1:

```text
duración normal = 120 min
9 misiones
4 roles base
rotación antes del incidente
incidente en minuto 70
M7 como pico de dificultad
diagnóstico con ≥2 evidencias
1 hipótesis descartada
recuperación específica
diagrama final obligatorio
trabajo por equipos
niveles mixtos
sin acceso al host
```

Estas decisiones solo deberían cambiar después de evidencia obtenida en ensayo.

---

# 46. Aspectos todavía ajustables

Pueden cambiar sin rediseñar la experiencia:

```text
número exacto de participantes
número exacto de equipos
diseño visual de la aplicación
nombres finales de tablas
nombres finales de contenedores
forma de acceso LAN/Tailscale
topología de PostgreSQL ClubLab
implementación del Scenario Manager
nombre exacto de comandos clublab
formato impreso/digital de materiales
```

---

# 47. Requisitos derivados para Fase 2 — Arquitectura

La arquitectura técnica deberá soportar:

```text
2–6 entornos de equipo
frontend
API
database
toolbox
aislamiento por equipo
healthchecks
logs accesibles de forma segura
reset independiente
un entorno de reserva
mínimas instalaciones cliente
```

Deberá existir una forma sencilla de acceder desde el navegador y terminal de laboratorio.

No podrá depender de las redes o bases productivas identificadas en D00.

---

# 48. Requisitos derivados para Fase 3 — Seguridad

La capa de seguridad deberá garantizar:

```text
un equipo no puede tocar otro
un estudiante no puede tocar el host
sin Docker socket
sin sudo
sin credenciales productivas
DB limitada al equipo
DDL prohibido al alumno
UPDATE limitado
logs sanitizados
credenciales desechables
```

Para M4 se recomienda evaluar técnicamente:

```text
roles PostgreSQL por equipo
+
Row Level Security
o
base/contenedor independiente por equipo
```

La decisión final se toma en Fase 3.

---

# 49. Requisitos derivados para Fase 4 — Aplicación

La aplicación necesita al menos:

```text
Dashboard
Perfil
Equipo
Ranking
Misiones
Actividad
```

Debe existir un dato rastreable de extremo a extremo, preferiblemente:

```text
score / puntos
```

Endpoints pedagógicos mínimos:

```text
/api/health
/api/ranking
/api/me
/api/missions
```

La UI necesita:

```text
estado normal
estado de carga
estado de error del ranking
```

Los nombres exactos pueden ajustarse durante implementación.

---

# 50. Requisitos derivados para Fase 5 — Scenario Manager

Debe poder ejecutar por equipo:

```text
status
health
logs
scenario load
recover
reset
```

Propiedades obligatorias:

```text
aislado
idempotente
repetible
seguro
scope por team
sin comandos globales
sin prune
```

Escenarios mínimos:

```text
normal
ranking-db-failure
api-down como fallback
```

El incidente principal debe preservar el fallo parcial definido en D01.

---

# 51. Requisitos derivados para Fase 6 — Roles

Crear tarjetas físicas o digitales para:

```text
Interfaz
API
Datos
Sistemas
Relator opcional
```

Cada tarjeta tendrá solo:

```text
propósito
preguntas guía
herramientas
3–6 comandos/accesos
evidencia
qué no tocar
```

No manuales extensos.

---

# 52. Requisitos derivados para Fase 7 — Material del alumno

Se requerirán:

```text
D06 — Guía del alumno
D07 — Cheat Sheet
D08 — Cuaderno de Misiones
```

El Cuaderno deberá incorporar:

```text
pregunta
tarea
evidencia
P1
P2
P3
reto extra
¿Qué descubrimos?
```

El material debe funcionar también offline.

---

# 53. Requisitos derivados para Fase 8 — Instructor

El manual deberá incluir:

```text
cronograma minuto a minuto
hitos
pistas P1–P4
respuestas esperadas
errores frecuentes
matriz de observación
procedimiento de incidente
procedimiento de recuperación
planes B
versión 105 min
versión 90 min
```

---

# 54. Requisitos derivados para Fase 9 — Ensayo

Antes de la clase real se hará al menos una ejecución completa con:

```text
1 entorno
4 roles simulados
cronómetro
M0–M8
incidente
recover
reset
```

Registrar:

```text
tiempo real por misión
pista máxima utilizada
errores de UX
comandos confusos
calidad de logs
tiempo de reset
```

Criterio:

```text
la sesión completa debe caber realmente en ≤120 min
```

sin depender de intervención constante del instructor.

---

# 55. Criterios de éxito de ClubLab #01

La experiencia será considerada exitosa si la mayoría de los participantes puede explicar:

```text
qué pidió el navegador
qué respondió la API
de dónde salió el dato
qué papel tuvo la base de datos
qué componentes existían
qué parte falló
qué evidencia permitió descubrirlo
cómo se validó la recuperación
```

Además, la sesión debe producir curiosidad sobre áreas posteriores.

---

# 56. Criterios de cierre de Fase 1

```text
[x] Público definido
[x] Objetivos definidos
[x] Narrativa definida
[x] Arquitectura de descubrimiento definida
[x] M0–M8 diseñadas
[x] Roles definidos
[x] Rotación definida
[x] Incidente diseñado
[x] Pistas definidas
[x] Extensiones definidas
[x] Evidencias definidas
[x] Cronograma de 120 min definido
[x] Contingencias definidas
[x] Simulación pedagógica realizada
[x] Requisitos para fases posteriores derivados
```

# FASE 1 — COMPLETADA

---

# 57. Trazabilidad de diseño

Este documento consolida las decisiones de:

```text
Bloque A — Perfil + objetivos
Bloque B — Narrativa + arquitectura
Bloque C — Catálogo de misiones
Bloque D — Roles + rotación
Bloque E — Incidente
Bloque F — Pistas + extensiones + evidencias
Bloque G — Cronograma
Bloque H — Contingencias + simulación
Bloque I — Consolidación
```

Los documentos de bloque pueden conservarse como evidencia de diseño, pero **D01 es la referencia oficial de la Fase 1**.

---

# 58. Próximo paso oficial

Con la experiencia ya definida, el proyecto puede avanzar a:

# FASE 2 — Arquitectura técnica de ClubLab

La pregunta deja de ser:

> “¿Qué queremos que vivan los alumnos?”

y pasa a ser:

> **“¿Qué arquitectura debemos construir para que esa experiencia ocurra de forma segura, aislada, repetible y fácil de operar?”**