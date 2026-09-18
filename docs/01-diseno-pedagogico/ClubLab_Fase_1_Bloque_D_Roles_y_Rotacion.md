# ClubLab — Fase 1 / Bloque D
## Roles + rotación de integrantes

**Proyecto:** ClubLab v1  
**Experiencia:** ClubLab #01 — *Desarmando una aplicación*  
**Fase:** 1 — Diseño pedagógico  
**Bloque:** D  
**Dependencias:** Bloques A, B y C  
**Estado:** CERRADO PARA DISEÑO v1  
**Entregable principal:** `P06_Roles_v1`

---

# 1. Propósito del Bloque D

Este bloque define cómo se reparten las responsabilidades dentro de cada equipo durante ClubLab #01.

El objetivo no es crear especialistas permanentes.

Los roles existen para:

- evitar que una sola persona monopolice la experiencia;
- asegurar que todos toquen una parte del sistema;
- distribuir herramientas y responsabilidades;
- hacer visible que una aplicación tiene varias capas;
- mejorar la comunicación durante el incidente;
- permitir rotación sin perder continuidad.

La regla central será:

> **Cada integrante investiga una parte, pero el equipo construye una sola explicación.**

---

# 2. Roles principales

ClubLab #01 utilizará cuatro roles base:

```text
R1 — Explorador de Interfaz
R2 — Investigador de API
R3 — Investigador de Datos
R4 — Operador de Sistemas
```

Para equipos de cinco personas podrá existir:

```text
R5 — Relator / Analista
```

El quinto rol es opcional.

---

# 3. Principios de los roles

Los roles deben cumplir estas reglas:

```text
1. Ningún rol trabaja aislado.
2. Ningún rol posee “la respuesta”.
3. Cada rol tiene herramientas propias.
4. Cada rol aporta evidencia al equipo.
5. Los roles rotan.
6. Nadie necesita privilegios del host.
7. Los roles describen tareas, no profesiones.
8. Un integrante puede descubrir que le interesa un área distinta a su rol inicial.
```

---

# 4. R1 — Explorador de Interfaz

## Propósito

Investigar lo que observa el usuario y utilizar el navegador como herramienta técnica.

## Pregunta principal

> **¿Qué está viendo el usuario y qué ocurre cuando interactúa con la aplicación?**

## Herramientas

```text
navegador
DevTools
Network
Fetch/XHR
Headers
Response
Console básica
```

## Responsabilidades

```text
navegar la aplicación;
reproducir comportamientos;
identificar errores visuales;
observar peticiones;
comparar pantallas;
registrar status HTTP;
informar al equipo qué sigue funcionando.
```

## Evidencia que aporta

```text
GET /api/ranking
status 200
status 500
respuesta JSON
captura del error
```

## Puede tocar

```text
frontend del equipo;
DevTools;
cuenta de laboratorio;
peticiones visibles;
datos de su propio equipo desde la UI.
```

## No puede tocar

```text
host Tulum;
Docker del host;
servicios productivos;
base de datos productiva;
configuración de red real;
credenciales administrativas.
```

## Riesgo frecuente

Convertirse en “la persona que solo hace clic”.

### Mitigación

Debe producir evidencia técnica mediante DevTools.

---

# 5. R2 — Investigador de API

## Propósito

Investigar la comunicación entre frontend y backend.

## Pregunta principal

> **¿Qué información está pidiendo la aplicación y qué responde el sistema?**

## Herramientas

```text
curl
HTTP
JSON
endpoint discovery
status codes
```

## Responsabilidades

```text
probar endpoints;
comparar respuestas;
identificar status;
leer JSON;
confirmar si un endpoint está vivo;
relacionar un endpoint con una pantalla.
```

## Evidencia que aporta

```text
URL consultada;
método;
status;
respuesta;
campo relevante;
comparación entre endpoint sano y fallido.
```

## Puede tocar

```text
API del entorno de su equipo;
terminal de laboratorio;
endpoints permitidos;
healthchecks.
```

## No puede tocar

```text
otros equipos;
servicios del host;
tokens productivos;
endpoints administrativos;
Docker socket.
```

## Comandos base

```bash
curl URL
curl -i URL
```

Opcional:

```bash
curl -s URL
```

No se espera memorizar flags.

## Riesgo frecuente

Convertir el rol en “copiar comandos”.

### Mitigación

Siempre debe responder:

```text
¿Qué demuestra esta respuesta?
```

---

# 6. R3 — Investigador de Datos

## Propósito

Investigar dónde persisten los datos y cómo cambian.

## Pregunta principal

> **¿Dónde vive la información que la aplicación muestra?**

## Herramientas

```text
psql
SQL básico
tablas
SELECT
UPDATE controlado
```

## Responsabilidades

```text
listar tablas;
identificar una tabla relevante;
buscar un registro;
relacionar datos con la API;
realizar modificaciones autorizadas;
comprobar persistencia.
```

## Evidencia que aporta

```text
tabla;
columna;
registro;
valor anterior;
valor nuevo;
consulta ejecutada.
```

## Puede tocar

```text
base de datos ClubLab de su equipo;
tablas de laboratorio;
registros autorizados;
datos propios del equipo.
```

## No puede tocar

```text
postgres-main;
whatsapp_db;
otros equipos;
roles administrativos;
schemas no asignados;
estructura productiva.
```

## Comandos base

```text
\dt
\d tabla
SELECT ...
UPDATE ...
\q
```

## Riesgo frecuente

Modificar datos sin entender el filtro.

### Mitigación

Antes de cualquier `UPDATE`:

```text
1. ejecutar SELECT;
2. verificar team_id;
3. mostrar al equipo;
4. ejecutar modificación.
```

---

# 7. R4 — Operador de Sistemas

## Propósito

Investigar cómo se ejecutan y cómo se comportan los servicios.

## Pregunta principal

> **¿Qué componentes están activos y cuál podría estar fallando?**

## Herramientas

La implementación deberá proporcionar una interfaz segura, por ejemplo:

```text
clublab status
clublab health
clublab logs
clublab recover
```

o equivalente.

También podrá utilizar:

```text
curl
ping limitado
getent
ss dentro de toolbox
```

## Responsabilidades

```text
consultar estado;
consultar healthchecks;
leer logs permitidos;
comparar servicios;
identificar dependencia fallida;
ejecutar recuperación controlada.
```

## Evidencia que aporta

```text
estado del servicio;
healthcheck;
fragmento de log;
servicio sospechoso;
acción de recuperación;
resultado.
```

## Puede tocar

```text
servicios ClubLab de su equipo;
herramientas de diagnóstico;
recuperación limitada;
logs del entorno propio.
```

## No puede tocar

```text
docker del host;
systemctl del host;
sudo;
Tulum;
Pelican;
WhatsApp;
PostgreSQL productivo;
redes productivas.
```

## Riesgo frecuente

Intentar “reiniciar todo”.

### Mitigación

No se habilitará un comando global destructivo para estudiantes.

La recuperación deberá ser específica.

---

# 8. R5 — Relator / Analista

## Estado

Opcional. Se utiliza cuando hay cinco integrantes.

## Propósito

Mantener la evidencia y conectar hallazgos entre roles.

## Pregunta principal

> **¿Qué sabemos realmente y qué estamos suponiendo?**

## Herramientas

```text
cuaderno de misiones;
diagrama;
tabla de hipótesis;
evidencias aportadas por el equipo.
```

## Responsabilidades

```text
registrar hallazgos;
distinguir evidencia de hipótesis;
actualizar diagrama;
controlar preguntas pendientes;
resumir el diagnóstico.
```

## Evidencia que aporta

```text
mapa actualizado;
hipótesis;
línea de tiempo;
resumen final.
```

## Riesgo frecuente

Convertirse en observador pasivo.

### Mitigación

Durante M6/M7 debe ser responsable de mantener:

```text
Síntoma
Hipótesis
Evidencia 1
Evidencia 2
Conclusión
```

---

# 9. Matriz de herramientas por rol

| Herramienta | Interfaz | API | Datos | Sistemas | Relator |
|---|---:|---:|---:|---:|---:|
| Navegador | Principal | Apoyo | — | Apoyo | Apoyo |
| DevTools | Principal | Apoyo | — | Apoyo | — |
| curl | — | Principal | Apoyo | Apoyo | — |
| psql | — | Apoyo | Principal | — | — |
| status/health | Apoyo | Apoyo | — | Principal | — |
| logs | Apoyo | Apoyo | — | Principal | Apoyo |
| diagrama | Apoyo | Apoyo | Apoyo | Apoyo | Principal |

---

# 10. Relación entre roles y misiones

| Misión | Rol principal | Roles de apoyo |
|---|---|---|
| M0 — Reconocimiento | Interfaz | Todos |
| M1 — Datos desde la UI | Interfaz | API |
| M2 — Habla con la API | API | Interfaz |
| M3 — Origen de datos | Datos | API |
| M4 — Cambia el sistema | Datos | API + Interfaz |
| M5 — Encuentra las piezas | Sistemas | Todos |
| M6 — Incidente | Interfaz | Todos |
| M7 — Diagnóstico | Sistemas | API + Datos + Interfaz |
| M8 — Reconstrucción | Todos | Relator si existe |

---

# 11. Regla de participación

En cada misión:

```text
1 persona opera;
1 persona observa;
1 persona verifica;
1 persona registra.
```

Aunque exista un rol principal, el resto del equipo debe participar.

Ejemplo en M3:

```text
Datos       → escribe consulta
API         → compara con JSON
Interfaz    → verifica la UI
Sistemas    → observa que el servicio siga sano
```

---

# 12. Rotación principal

La rotación ocurrirá después de M5 y antes de M6.

Motivo:

```text
M0–M5
→ descubrimiento guiado

M6–M7
→ incidente
```

La persona no debe investigar el incidente únicamente desde la herramienta que ya domina.

---

# 13. Esquema de rotación para cuatro integrantes

Antes:

```text
A → Interfaz
B → API
C → Datos
D → Sistemas
```

Después:

```text
A → Sistemas
B → Datos
C → API
D → Interfaz
```

Visualmente:

```text
Interfaz  ↔ Sistemas
API       ↔ Datos
```

---

# 14. Motivo de esta rotación

Permite que:

```text
quien observó síntomas
→ ahora investigue servicios;

quien consultó API
→ ahora investigue datos;

quien tocó BD
→ ahora vea peticiones;

quien operó servicios
→ ahora experimente el impacto desde usuario.
```

Esto fuerza a conectar capas.

---

# 15. Transferencia de rol

La rotación no debe ser solo “cambien de silla”.

Antes de cambiar, cada integrante tendrá 30–45 segundos para explicar al nuevo responsable:

```text
qué herramienta usó;
qué descubrió;
qué dato importante encontró;
qué error debe evitar.
```

Tiempo total máximo:

```text
2 minutos
```

---

# 16. Equipos de tres integrantes

Configuración recomendada:

```text
A → Interfaz
B → API + Datos
C → Sistemas
```

Durante M3/M4:

```text
B opera psql;
A verifica UI;
C registra/observa estado.
```

Rotación antes del incidente:

```text
A → Sistemas
B → Interfaz
C → API + Datos
```

---

# 17. Equipos de cinco integrantes

Configuración:

```text
A → Interfaz
B → API
C → Datos
D → Sistemas
E → Relator
```

Rotación:

```text
A ↔ D
B ↔ C
E permanece como Relator
```

Para evitar que E quede pasivo, durante M7 el Relator controla la matriz de diagnóstico.

---

# 18. Equipos de dos integrantes

No es la configuración objetivo, pero debe existir contingencia.

Distribución:

```text
Persona A
→ Interfaz + API

Persona B
→ Datos + Sistemas
```

Después intercambian.

La experiencia será más secuencial y puede requerir apoyo del instructor.

---

# 19. Equipo de una sola persona

No es la modalidad recomendada.

Si ocurre:

```text
la persona rota consigo misma entre herramientas;
el instructor actúa como interlocutor;
se omiten tareas administrativas de rol.
```

La experiencia sigue siendo posible, pero pierde parte del valor colaborativo.

---

# 20. Regla del teclado

Para evitar monopolio:

> **Quien tiene el rol principal de la misión controla el teclado.**

Los demás pueden:

```text
sugerir;
preguntar;
observar;
validar.
```

No deben arrebatar el teclado.

---

# 21. Excepción del teclado

El rol principal puede cederlo si:

```text
no entiende un comando;
necesita que otro demuestre una idea;
se encuentra en rotación;
el instructor lo solicita.
```

Pero debe seguir participando activamente.

---

# 22. Regla de explicación

La persona que ejecuta una acción debe decir brevemente:

```text
qué va a probar
y
qué espera que ocurra.
```

Ejemplo:

> “Voy a consultar `/api/ranking`. Si la API está bien, espero un 200.”

Esto convierte la acción en experimento.

---

# 23. Regla de evidencia

Ningún equipo debe avanzar con frases como:

```text
“creo que”
“seguro es”
“debe ser”
```

sin agregar:

```text
“porque observamos…”
```

Formato:

```text
HIPÓTESIS
+
EVIDENCIA
```

---

# 24. Límites de acción por rol

## Interfaz

Puede:

```text
navegar;
usar DevTools;
consultar UI.
```

No puede modificar infraestructura.

## API

Puede:

```text
consultar endpoints permitidos.
```

No puede usar rutas administrativas.

## Datos

Puede:

```text
consultar y modificar registros autorizados.
```

No puede cambiar esquema, usuarios, roles ni otras bases.

## Sistemas

Puede:

```text
consultar estado;
logs;
recuperar un servicio de su equipo.
```

No puede gestionar Docker del host ni reiniciar infraestructura global.

---

# 25. Tarjeta de rol — contenido futuro

Cada tarjeta de la Fase 6 deberá contener únicamente:

```text
nombre del rol;
objetivo;
qué observar;
herramientas;
3–6 comandos o accesos útiles;
qué evidencia aportar;
qué NO tocar;
preguntas guía.
```

No debe ser un manual largo.

---

# 26. Cheat sheet por rol

## Interfaz

```text
F12
Network
Fetch/XHR
Headers
Response
Reload
```

## API

```bash
curl URL
curl -i URL
```

## Datos

```text
\dt
\d tabla
SELECT ...
UPDATE ...
\q
```

## Sistemas

Ejemplos conceptuales:

```bash
clublab status
clublab health
clublab logs api
clublab recover api
```

Los nombres definitivos dependen de Fase 5.

---

# 27. Preguntas guía por rol

## Interfaz

```text
¿Qué ve el usuario?
¿Qué dejó de funcionar?
¿Qué request cambia?
¿Qué status aparece?
```

## API

```text
¿Responde el endpoint?
¿Qué status entrega?
¿Qué JSON devuelve?
¿Otros endpoints siguen funcionando?
```

## Datos

```text
¿Existe el dato?
¿Está correcto?
¿Puede consultarse?
¿Cambió después de la operación?
```

## Sistemas

```text
¿Qué servicios están vivos?
¿Qué healthcheck falla?
¿Qué dicen los logs?
¿Qué acción mínima recupera?
```

## Relator

```text
¿Qué sabemos?
¿Qué asumimos?
¿Qué evidencia falta?
¿Qué hipótesis es más fuerte?
```

---

# 28. Rotación y descubrimiento de intereses

Al final de la sesión se preguntará:

```text
¿Qué rol disfrutaste más?
¿Qué herramienta te dio más curiosidad?
¿En qué capa quisieras profundizar?
```

Esto servirá para futuros ClubLab.

No se utilizará para etiquetar al integrante permanentemente.

---

# 29. Antipatrones a evitar

## Antipatrón 1 — El avanzado toma todos los teclados

**Respuesta:** aplicar regla de rol principal.

## Antipatrón 2 — El principiante solo copia comandos

**Respuesta:** pedirle que prediga el resultado antes de ejecutar.

## Antipatrón 3 — Los roles no se comunican

**Respuesta:** antes de cambiar de misión, cada rol aporta una evidencia.

## Antipatrón 4 — Sistemas se convierte en “admin”

**Respuesta:** no entregar acceso al host ni comandos Docker reales.

## Antipatrón 5 — Datos se vuelve “persona SQL”

**Respuesta:** después de M4 rota hacia API.

---

# 30. Matriz de aportación en el incidente

Durante M7, cada rol debe aportar algo distinto:

| Rol | Evidencia mínima |
|---|---|
| Interfaz | síntoma + request fallida |
| API | status/respuesta del endpoint |
| Datos | estado o consulta de dato/BD |
| Sistemas | estado/log del servicio |
| Relator | hipótesis consolidada |

El diagnóstico solo se considera completo cuando se integran las evidencias.

---
# 31. Protocolo de diagnóstico por equipo

Sin imponer un orden rígido, el equipo debe responder:

```text
1. ¿Qué funciona?
2. ¿Qué no funciona?
3. ¿Dónde aparece la primera evidencia de fallo?
4. ¿Qué componente podemos descartar?
5. ¿Qué evidencia confirma la causa?
6. ¿Cuál es la acción mínima de recuperación?
```

---

# 32. Regla contra “reiniciar por reiniciar”

Antes de ejecutar una recuperación:

> **El equipo debe decir qué cree que falló y por qué.**

Solo entonces podrá usar la acción de recuperación.

Esto refuerza:

```text
diagnóstico
antes que
acción
```

---

# 33. Rol del instructor frente a los roles

El instructor no sustituye un rol.

Debe:

```text
observar;
preguntar;
pedir evidencia;
dar pistas;
mantener tiempo;
detectar monopolios;
forzar rotación si es necesario.
```

No debe convertirse en operador, DBA, programador o solucionador durante la actividad.

---

# 34. Escalado de ayuda por rol

## Si Interfaz se bloquea

```text
P1: ¿qué herramienta del navegador muestra actividad?
P2: abre DevTools
P3: Network → Fetch/XHR
```

## Si API se bloquea

```text
P1: ¿puedes repetir la petición sin el frontend?
P2: usa la URL encontrada
P3: curl -i <URL>
```

## Si Datos se bloquea

```text
P1: ¿qué tablas existen?
P2: usa \dt
P3: inspecciona la tabla indicada
```

## Si Sistemas se bloquea

```text
P1: ¿qué servicio sospechan?
P2: revisa su estado
P3: consulta logs del servicio
```

---

# 35. Evidencia de colaboración

Además de la evidencia técnica, cada equipo deberá ser capaz de decir:

```text
qué descubrió cada rol
```

Esto se preguntará durante M8.

Ejemplo:

```text
Interfaz descubrió la request.
API confirmó el 500.
Datos confirmó que la BD estaba viva.
Sistemas encontró el error de conexión.
```

---

# 36. Criterios para que un rol esté bien diseñado

Un rol es válido si:

```text
tiene una pregunta propia;
tiene herramientas propias;
produce evidencia;
no necesita privilegios peligrosos;
puede rotar;
puede explicarse en menos de 1 minuto;
no monopoliza la solución.
```

---

# 37. Decisiones cerradas en Bloque D

### DD-01
Se utilizarán cuatro roles base.

### DD-02
El quinto rol será Relator y solo se utilizará cuando convenga.

### DD-03
Los roles rotarán antes del incidente.

### DD-04
La rotación estándar será:

```text
Interfaz ↔ Sistemas
API ↔ Datos
```

### DD-05
El rol principal controla el teclado.

### DD-06
Antes de ejecutar, el operador debe expresar una predicción.

### DD-07
Cada rol debe aportar evidencia.

### DD-08
Los roles no proporcionarán acceso al host.

### DD-09
Las tarjetas futuras serán breves y orientadas a acción.

### DD-10
Los roles sirven también para descubrir intereses personales.

---

# 38. Entregables del Bloque D

Este bloque produce:

```text
P06_Roles_v1
P06A_Matriz_Roles_Misiones
P06B_Reglas_Rotacion
P06C_Limites_Por_Rol
P06D_CheatSheet_Base
P06E_Matriz_Incidente
```

---

# 39. Criterios de aceptación

- [x] R1 definido.
- [x] R2 definido.
- [x] R3 definido.
- [x] R4 definido.
- [x] R5 opcional definido.
- [x] Herramientas por rol definidas.
- [x] Límites por rol definidos.
- [x] Evidencia por rol definida.
- [x] Relación misión/rol definida.
- [x] Rotación definida.
- [x] Equipos de 3 definidos.
- [x] Equipos de 4 definidos.
- [x] Equipos de 5 definidos.
- [x] Contingencia para 2 personas definida.
- [x] Regla del teclado definida.
- [x] Regla de predicción definida.
- [x] Matriz del incidente definida.
- [x] Especificación de tarjetas futuras definida.

# BLOQUE D — COMPLETADO

---

# 40. Siguiente bloque

# BLOQUE E — Diseño del incidente principal

El siguiente bloque debe convertir el escenario conceptual de M6/M7 en un incidente pedagógico completo.

Se definirá:

```text
qué falla exactamente;
cómo se provoca;
qué ve el usuario;
qué muestra Network;
qué devuelve la API;
qué ocurre en PostgreSQL;
qué muestran los logs;
qué healthchecks siguen vivos;
qué hipótesis incorrectas son probables;
qué pistas existen;
qué acción mínima lo recupera;
cómo se resetea;
cuánto debe durar;
qué variante simplificada existe.
```

El Bloque E será el puente directo entre diseño pedagógico y el futuro Scenario Manager.