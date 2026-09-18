# P06 — Roles v1
## Contrato final de roles para ClubLab #01

**Estado:** FINAL PARA FASE 6 / BLOQUE A

---

# R1 — Explorador de Interfaz

**Pregunta:** ¿Qué ve el usuario y qué ocurre cuando interactúa?

**Objetivo:** conectar el comportamiento visible con requests reales.

**Herramientas:**

~~~text
Browser
DevTools
Network
Fetch/XHR
Headers
Response
~~~

**Puede:**

~~~text
navegar
recargar
inspeccionar requests
leer headers/responses
comparar estado normal y fallo
~~~

**No puede:**

~~~text
usar /internal/*
usar clublabctl
modificar infraestructura
entrar a otro team
~~~

**Evidencia mínima:**

~~~text
pantalla
request
método
status
dato/error
~~~

**Lidera:** M0, M1 y observación inicial de M6.

**Preguntas guía:**

~~~text
¿Qué cambió?
¿Qué request corresponde?
¿Qué status aparece?
¿Qué sigue funcionando?
~~~

---

# R2 — Investigador de API

**Pregunta:** ¿Qué pide la aplicación y qué responde el backend?

**Objetivo:** consultar y comparar endpoints sin depender de la UI.

**Herramientas:**

~~~text
curl
HTTP
JSON
/api/health
/api/me
/api/team
/api/ranking
/api/missions
/api/activity
~~~

**Puede:**

~~~text
consultar endpoints públicos
leer status
leer JSON
comparar endpoint sano/fallido
~~~

**No puede:**

~~~text
usar /internal/*
usar control token
explorar otros teams
hacer fuzzing
~~~

**Evidencia mínima:**

~~~text
URL
método
status
campo JSON
comparación
~~~

**Lidera:** M2 y comparación de endpoints en M7.

**Pregunta obligatoria tras cada curl:**

> ¿Qué demuestra esta respuesta?

---

# R3 — Investigador de Datos

**Pregunta:** ¿Dónde vive la información?

**Objetivo:** conectar UI/API con persistencia en PostgreSQL.

**Herramientas:**

~~~text
psql
\dt
\d
SELECT
lab.my_team_score
UPDATE controlado
~~~

**Puede:**

~~~text
consultar objetos autorizados
leer el score local
actualizar score mediante lab.my_team_score
comprobar el cambio
~~~

**No puede:**

~~~text
usar roles administrativos
crear/borrar tablas
cambiar grants
consultar otras bases
modificar fuera de la superficie autorizada
~~~

**Evidencia mínima:**

~~~text
objeto
registro
valor anterior
consulta
valor nuevo
~~~

**Lidera:** M3 y M4.

**Secuencia obligatoria:**

~~~text
SELECT
→ verificar
→ predecir
→ UPDATE
→ comprobar
~~~

---

# R4 — Operador de Sistemas

**Pregunta:** ¿Qué componentes funcionan y dónde aparece el fallo?

**Objetivo:** observar estado/logs y ejecutar la recuperación mínima cuando exista evidencia.

**Herramientas:**

~~~bash
clublab whoami
clublab status
clublab health
clublab logs api
clublab recover ranking-db
~~~

**Puede:**

~~~text
consultar estado
consultar health
leer lablogs sanitizados
ejecutar recover ranking-db
~~~

**No puede:**

~~~text
usar clublabctl
usar docker
usar sudo
usar systemctl del host
hacer reset
~~~

**Evidencia mínima:**

~~~text
estado
health
ranking status
lablog
resultado del recover
~~~

**Lidera:** M5 y M7.

**Regla:** recover ocurre después del diagnóstico, no antes.

---

# R5 — Relator / Analista

**Pregunta:** ¿Qué sabemos y qué estamos suponiendo?

**Objetivo:** conectar evidencia de varias capas y mantener la explicación del equipo.

**Herramientas:**

~~~text
hoja de evidencia
matriz hipótesis/evidencia
diagrama
línea de tiempo
~~~

**Puede:**

~~~text
registrar hallazgos
pedir evidencia
actualizar diagrama
resumir hipótesis
coordinar M8
~~~

**No puede:**

~~~text
quedar como observador pasivo
decidir solo el diagnóstico
monopolizar el teclado
~~~

**Evidencia mínima en M7:**

~~~text
Síntoma
Hipótesis
Evidencia 1
Evidencia 2
Hipótesis descartada
Causa
Acción
Resultado
~~~

**Uso:** principalmente equipos de cinco.

---

# Reglas comunes

~~~text
el rol no concede permisos
el rol principal controla el teclado cuando lidera
cada afirmación importante necesita evidencia
un integrante avanzado no sustituye al rol principal
un principiante puede usar cualquier rol con apoyo
~~~

Las tarjetas visuales se producirán en Fase 7.
