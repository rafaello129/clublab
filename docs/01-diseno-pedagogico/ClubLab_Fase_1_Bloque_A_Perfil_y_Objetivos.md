# ClubLab — Fase 1 / Bloque A
## Perfil de participantes + objetivos de descubrimiento

**Proyecto:** ClubLab v1  
**Experiencia:** ClubLab #01 — *Desarmando una aplicación*  
**Fase:** 1 — Diseño pedagógico  
**Bloque:** A  
**Entregables cubiertos:** `P01_Perfil_Participantes` + `P02_Resultados_Aprendizaje`  
**Estado:** CERRADO PARA DISEÑO v1

---

# 1. Propósito del Bloque A

Este bloque fija para quién se diseña ClubLab #01 y qué debe conseguir la sesión.

No define todavía:

- arquitectura técnica;
- aplicación final;
- endpoints concretos;
- base de datos definitiva;
- contenedores;
- infraestructura de acceso.

Su función es evitar diseñar una experiencia demasiado fácil para algunos o demasiado compleja para quienes apenas comienzan.

---

# 2. Perfil objetivo de participantes

ClubLab #01 se diseña para un club de programación con niveles mixtos.

El participante típico puede estar en cualquiera de estos puntos:

```text
PRINCIPIANTE
Sabe lógica básica o ha programado poco.

INTERMEDIO
Ya ha creado proyectos pequeños.

AVANZADO
Conoce desarrollo web, backend, bases de datos
o alguna parte de infraestructura.
```

La clase debe funcionar para los tres perfiles al mismo tiempo.

---

# 3. Nivel mínimo requerido

Para participar no será necesario conocer previamente:

```text
Docker
Linux
PostgreSQL
HTTP
REST
DevTools
redes
servidores
NestJS
React
```

El mínimo esperado será:

```text
usar un navegador;
seguir instrucciones;
copiar y ejecutar comandos simples;
entender variables, datos y lógica básica;
trabajar en equipo;
formular hipótesis.
```

Incluso si una persona nunca ha usado terminal, debe poder completar la experiencia con apoyo del equipo y la guía.

---

# 4. Nivel que NO se debe asumir

No diseñar actividades suponiendo que todos saben:

```bash
cd
ls
curl
docker
psql
ssh
```

Tampoco asumir que conocen conceptos como:

```text
request
response
status code
JSON
API
backend
base de datos relacional
contenedor
puerto
```

Estos conceptos deben aparecer dentro de la experiencia.

---

# 5. Perfil de participantes avanzados

Los integrantes con experiencia no deben quedar esperando.

Cada misión tendrá una extensión opcional que les permita investigar más sin adelantar la solución principal.

Ejemplos:

```text
encontrar otro endpoint;
comparar dos respuestas;
medir tiempo de respuesta;
probar un ID inexistente;
interpretar otro status HTTP;
encontrar una relación adicional entre tablas;
seguir un log más profundo;
formular una hipótesis de arquitectura.
```

Estas extensiones no son necesarias para terminar la misión.

---

# 6. Tamaño de equipo

## Configuración ideal

```text
4 integrantes por equipo
```

porque coincide con los cuatro roles iniciales:

```text
1. Explorador de Interfaz
2. Investigador de API
3. Investigador de Datos
4. Operador de Sistemas
```

## Configuración válida

```text
3 integrantes
```

En ese caso:

```text
API + Datos
```

pueden combinarse.

## Si hay 5 integrantes

Agregar:

```text
Relator / Analista
```

Responsabilidades:

```text
registrar hipótesis;
anotar evidencia;
mantener actualizado el diagrama;
coordinar hallazgos del equipo.
```

---

# 7. Número de participantes soportado por el diseño pedagógico

La experiencia se diseñará para escalar aproximadamente entre:

```text
8 y 24 participantes
```

equivalente a:

```text
2–6 equipos
```

El número técnico máximo real se validará posteriormente en infraestructura.

Este rango no representa el límite físico del servidor; representa un rango pedagógico manejable para una sesión de dos horas con un instructor principal.

---

# 8. Organización del trabajo

La experiencia será:

```text
COLABORATIVA
```

No individual.

Cada integrante tendrá una responsabilidad principal, pero los resultados pertenecen al equipo.

La intención no es:

```text
“cada persona resuelve su parte”
```

sino:

```text
“cada persona descubre una parte
y el equipo reconstruye el sistema”.
```

---

# 9. Rotación

Los integrantes cambiarán parcialmente de rol antes del incidente.

Propuesta:

```text
Interfaz  ↔ Sistemas
API       ↔ Datos
```

Objetivo:

- evitar especialización temprana;
- permitir que todos toquen más de una capa;
- mejorar la comunicación durante el incidente.

La rotación debe tomar como máximo:

```text
2 minutos
```

---

# 10. Dispositivos

## Mínimo operativo

```text
1 laptop por equipo
```

## Recomendado

```text
1 laptop por integrante
```

Esto permitirá que varios roles trabajen en paralelo.

---

# 11. Software necesario del lado del alumno

La experiencia debe requerir la menor instalación posible.

Requisito base:

```text
navegador moderno
```

Preferiblemente:

```text
Chrome
Edge
Firefox
```

Las herramientas de terminal y base de datos deberían proporcionarse mediante el propio laboratorio cuando sea posible.

Objetivo:

> Evitar perder 30 minutos instalando software.

---

# 12. Terminal

La experiencia debe asumir que algunos integrantes nunca han utilizado una terminal.

Por ello, el acceso debe ser:

```text
simple;
aislado;
repetible;
sin acceso al host real.
```

Idealmente el integrante entra directamente a una terminal de laboratorio preparada con herramientas como:

```text
curl
psql
ping
getent
ss
```

La implementación pertenece a fases posteriores.

---

# 13. Condiciones de acceso

El participante nunca debe necesitar:

```text
SSH al servidor Tulum;
usuario tulum;
Docker del host;
sudo;
credenciales productivas;
acceso a redes de producción.
```

Desde el punto de vista pedagógico, el laboratorio debe sentirse real sin exponer infraestructura real.

---

# 14. Perfil de aprendizaje

La sesión está diseñada principalmente para personas que aprenden mejor al:

```text
ver algo;
tocarlo;
hacer una hipótesis;
probarla;
equivocarse;
observar el resultado.
```

Las explicaciones largas se reducen al mínimo.

---

# 15. Objetivo general de aprendizaje

Al finalizar ClubLab #01, un integrante debe poder explicar:

> **Una aplicación moderna está compuesta por varias partes que se comunican entre sí; el navegador muestra una interfaz, el frontend realiza peticiones, una API/backend procesa esas peticiones, los datos pueden persistir en una base de datos y todos esos componentes se ejecutan sobre infraestructura real.**

No es necesario que utilice exactamente esas palabras.

---

# 16. Objetivos principales

Se establecen ocho objetivos obligatorios.

---

## O1 — Diferenciar interfaz y datos

El integrante debe descubrir que:

```text
lo que aparece en pantalla
≠
el lugar donde necesariamente viven los datos
```

### Evidencia observable

Puede señalar un dato en la interfaz y explicar de dónde se obtiene.

---

## O2 — Reconocer una petición

Debe identificar que el navegador realiza solicitudes.

Debe reconocer visualmente:

```text
método
URL
status
respuesta
```

No necesita memorizar todos los métodos HTTP.

### Evidencia observable

Encuentra una petición real desde DevTools.

---

## O3 — Comprender qué es una API

Debe entender una API como un medio para pedir o enviar información a otra parte del sistema.

### Evidencia observable

Consulta un endpoint fuera de la interfaz gráfica y obtiene datos.

---

## O4 — Comprender el papel del backend

Debe identificar que existe una capa que:

```text
recibe peticiones;
ejecuta lógica;
consulta datos;
devuelve respuestas.
```

### Evidencia observable

Relaciona una petición observada con el servicio backend.

---

## O5 — Comprender persistencia

Debe descubrir que los datos pueden almacenarse en PostgreSQL.

### Evidencia observable

Encuentra un dato de la aplicación dentro de una tabla autorizada.

---

## O6 — Relacionar BD → API → frontend

Debe observar cómo una modificación controlada termina reflejándose en la interfaz.

### Evidencia observable

```text
modifica dato
→ consulta API
→ refresca interfaz
→ observa cambio
```

---

## O7 — Entender componentes independientes

Debe comprender que frontend, API y base de datos pueden funcionar o fallar de manera independiente.

### Evidencia observable

Durante el incidente puede decir qué partes siguen funcionando y cuál sospecha que falló.

---

## O8 — Diagnosticar usando evidencia

Debe utilizar al menos dos fuentes de evidencia.

Ejemplos:

```text
DevTools
status HTTP
respuesta JSON
logs
healthcheck
consulta SQL
estado de servicio
```

### Evidencia observable

Explica por qué llegó a una hipótesis de fallo.

---

# 17. Objetivos secundarios

Si el tiempo lo permite, los integrantes también deberían descubrir:

```text
qué es un puerto;
qué significa localhost;
qué es JSON;
qué es un contenedor;
por qué existen logs;
qué significa status 200 / 404 / 500;
qué diferencia hay entre dato y lógica.
```

Estos conceptos no deben consumir el tiempo principal de la sesión.

---

# 18. Objetivos actitudinales

ClubLab también debe fomentar:

```text
curiosidad técnica;
investigación;
trabajo en equipo;
formulación de hipótesis;
comunicación;
tolerancia al error;
uso de evidencia antes de adivinar.
```

Especialmente:

> **No tocar cosas al azar hasta que funcione.**

La cultura de diagnóstico debe ser:

```text
observar
→ formular hipótesis
→ probar
→ comparar resultado
```

---

# 19. Lo que NO se espera aprender

Al terminar la sesión no se espera que una persona pueda:

```text
crear una API completa;
crear una app React;
administrar PostgreSQL;
usar Docker profesionalmente;
administrar Linux;
diseñar redes;
desplegar producción;
escribir SQL avanzado.
```

ClubLab #01 busca comprensión, no dominio.

---

# 20. Matriz de descubrimiento

| Área | Antes de la sesión puede no conocer | Después debe reconocer |
|---|---|---|
| Frontend | Qué significa | Parte visible/interactiva |
| API | Concepto desconocido | Medio de comunicación |
| HTTP | Solo “internet” | Peticiones/respuestas |
| Backend | Palabra abstracta | Servicio que procesa |
| PostgreSQL | No lo ha usado | Lugar donde persisten datos |
| Docker | No lo conoce | Forma de ejecutar componentes aislados |
| Logs | No los usa | Evidencia para diagnóstico |
| Network DevTools | Nunca lo abrió | Herramienta para observar tráfico |
| Servidor | “Una computadora remota” | Host que ejecuta servicios |

---

# 21. Arquitectura mental esperada

## Antes

Un participante puede imaginar:

```text
APLICACIÓN
```

como una sola cosa.

## Después

Debe imaginar algo similar a:

```text
NAVEGADOR
   │
   ▼
FRONTEND
   │
   ▼
API / BACKEND
   │
   ▼
BASE DE DATOS
```

y ser capaz de añadir:

```text
Todo eso está ejecutándose
sobre infraestructura.
```

---

# 22. Criterio de comprensión

No se utilizará examen escrito.

Consideraremos que un equipo comprendió la sesión cuando pueda reconstruir y explicar:

```text
1. qué pidió el navegador;
2. quién respondió;
3. de dónde salió el dato;
4. qué se rompió;
5. qué evidencia lo demostró.
```

---

# 23. Evidencia mínima al final de la clase

Cada equipo debe haber producido al menos:

```text
1 petición identificada;
1 respuesta JSON observada;
1 consulta de datos;
1 modificación controlada;
1 diagnóstico;
1 recuperación;
1 diagrama final.
```

---

# 24. Escala de apoyo

El instructor no debe dar la respuesta inmediatamente.

## Nivel 0

No intervención.

## Nivel 1

Pregunta conceptual.

```text
“¿Qué parte sabes que todavía funciona?”
```

## Nivel 2

Orientación hacia una herramienta.

```text
“¿Hay algo en el navegador que permita ver las peticiones?”
```

## Nivel 3

Instrucción concreta.

```text
“Abre F12 → Network → Fetch/XHR.”
```

## Nivel 4

Desbloqueo del instructor.

Solo si el equipo no puede continuar.

---

# 25. Diferenciación por nivel

## Principiante

Debe poder completar:

```text
misión principal
+
evidencia mínima
```

## Intermedio

Puede completar:

```text
misión principal
+
una hipótesis adicional
```

## Avanzado

Puede recibir:

```text
reto opcional
+
explicar el porqué técnico
```

Todos comparten el mismo objetivo principal.

---

# 26. Ritmo pedagógico

Ningún bloque de explicación del instructor debería superar aproximadamente:

```text
5–7 minutos
```

sin que los participantes vuelvan a interactuar.

La mayor parte de la clase debe consistir en:

```text
actividad
discusión
investigación
```

---

# 27. Distribución objetivo de tiempo

Para la sesión completa:

```text
Instructor hablando          ≤ 30%
Integrantes investigando     ≥ 55%
Reconstrucción / discusión   ~15%
```

No es una métrica rígida, sino una guía de diseño.

---

# 28. Riesgos pedagógicos

## R1 — Los avanzados resuelven todo

Mitigación:

```text
roles;
rotación;
evidencia por rol;
retos opcionales.
```

---

## R2 — El principiante solo observa

Mitigación:

```text
misiones pequeñas;
responsabilidad propia;
comandos simples;
pistas escalonadas.
```

---

## R3 — Se convierte en clase de comandos

Mitigación:

```text
los comandos existen para resolver una pregunta;
no se explican comandos sin contexto.
```

---

## R4 — Demasiados conceptos

Mitigación:

```text
un concepto principal nuevo por misión.
```

---

## R5 — Se obsesionan con “ganar” la misión

Mitigación:

El cierre de cada misión incluye:

```text
“¿Qué acabamos de descubrir?”
```

---

# 29. Decisiones cerradas en Bloque A

A partir de este bloque quedan fijadas:

### DA-01

ClubLab #01 está diseñado para **niveles mixtos**.

### DA-02

El conocimiento previo de infraestructura **no es requisito**.

### DA-03

La unidad principal de trabajo será el **equipo**, no el individuo.

### DA-04

El tamaño objetivo es **3–4 integrantes por equipo**.

### DA-05

El diseño debe poder atender aproximadamente **2–6 equipos**.

### DA-06

No debe requerir software especializado instalado previamente en las laptops.

### DA-07

Los integrantes no tendrán acceso al host real.

### DA-08

El objetivo es **comprender relaciones entre componentes**, no aprender sintaxis.

### DA-09

La sesión debe permitir tanto a principiantes como avanzados mantenerse activos.

### DA-10

El resultado se evaluará mediante **evidencia y explicación**, no examen.

---

# 30. Datos que pueden ajustarse cuando se conozca la asistencia real

No bloquean el diseño:

```text
número exacto de asistentes;
número exacto de laptops;
cantidad final de equipos.
```

Cuando se conozcan, solo se recalculará:

```text
cantidad de entornos;
asignación de roles;
distribución física;
presupuesto técnico.
```

No será necesario rediseñar la experiencia.

---

# 31. Salida P01 — Perfil de participantes

```text
Perfil:
niveles mixtos

Requisitos mínimos:
navegador + lógica básica + trabajo en equipo

Tamaño:
3–4 integrantes por equipo

Escala pedagógica:
2–6 equipos

Dispositivo:
1 laptop/equipo mínimo
1 laptop/persona recomendado

Software local:
navegador

Infraestructura:
proporcionada por ClubLab

Acceso al host:
ninguno
```

---

# 32. Salida P02 — Resultados de aprendizaje

Resultados obligatorios:

```text
O1 diferenciar interfaz y datos
O2 identificar peticiones
O3 comprender API
O4 comprender backend
O5 comprender persistencia
O6 relacionar BD/API/frontend
O7 comprender componentes independientes
O8 diagnosticar con evidencia
```

Resultado final:

> El integrante deja de ver “la aplicación” como una sola caja y comienza a verla como un sistema de componentes conectados.

---

# 33. Criterios de aceptación del Bloque A

- [x] Perfil técnico mínimo definido.
- [x] Nivel avanzado contemplado.
- [x] Tamaño de equipos definido.
- [x] Escala pedagógica definida.
- [x] Requisitos de dispositivo definidos.
- [x] Requisitos de software definidos.
- [x] Objetivo general definido.
- [x] Objetivos observables definidos.
- [x] No-objetivos definidos.
- [x] Evidencias mínimas definidas.
- [x] Estrategia de diferenciación definida.
- [x] Riesgos pedagógicos identificados.
- [x] Decisiones cerradas documentadas.

# BLOQUE A — COMPLETADO

---

# 34. Siguiente bloque

# BLOQUE B — Narrativa + arquitectura a descubrir

El siguiente bloque debe definir:

```text
cómo comienza la experiencia;
qué sabe inicialmente el alumno;
qué información se oculta;
qué historia conecta las misiones;
cómo se presenta ClubLab;
qué arquitectura descubrirán progresivamente;
en qué orden aparecen frontend, API, backend, DB, Docker y servidor;
qué diagrama incompleto reciben;
qué diagrama deberían reconstruir al final.
```

El Bloque B debe convertir los objetivos definidos aquí en una experiencia concreta, pero todavía sin diseñar en detalle cada misión.