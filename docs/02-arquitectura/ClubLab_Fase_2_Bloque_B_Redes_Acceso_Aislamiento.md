# ClubLab — Fase 2 / Bloque B
## Redes, acceso y aislamiento

**Proyecto:** ClubLab v1  
**Fase:** 2 — Arquitectura técnica  
**Bloque:** B  
**Estado:** CERRADO PARA DISEÑO v1  
**Dependencias:** Fase 0 + D01 + Fase 2/Bloque A

---

# 1. Propósito

Este bloque define cómo se conectará cada entorno ClubLab sin exponer el servidor real ni mezclar equipos.

Debe responder:

```text
¿Qué redes existen?
¿Qué puede comunicarse con qué?
¿Cómo entra el alumno?
¿Cómo entra a la terminal?
¿Qué puertos se publican?
¿Dónde queda PostgreSQL?
¿Cómo evitamos conexiones entre equipos?
¿Qué papel tienen LAN y Tailscale?
```

La prioridad es:

```text
aislamiento
+
simplicidad para el alumno
+
operación predecible
```

---

# 2. Decisión de conectividad

La primera versión utilizará:

> **LAN como acceso principal de los alumnos y Tailscale como canal administrativo/alternativo, no como requisito del estudiante.**

Esto permite que ClubLab funcione incluso sin Internet público.

No se utilizará Cloudflare Quick Tunnel como dependencia de la sesión.

---

# 3. Vista global

```text
                        ALUMNOS
                           │
                           │ LAN
                           ▼
                  ┌─────────────────┐
                  │ clublab-gateway │
                  │     Caddy       │
                  └───────┬─────────┘
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
        ▼                 ▼                 ▼
     TEAM 01           TEAM 02           TEAM XX
        │                 │                 │
   app + data        app + data        app + data
   networks          networks          networks
```

El único componente ClubLab publicado hacia los alumnos será:

```text
clublab-gateway
```

Los contenedores de los equipos no publicarán puertos directamente al host.

---

# 4. Gateway

## Tecnología elegida

```text
Caddy
```

pero como:

> **contenedor independiente de ClubLab**

No se modificará el Caddy existente que actualmente sirve Pelican.

Nombre:

```text
clublab-gateway
```

Imagen:

```text
caddy:<versión fijada>
```

La versión exacta se fijará durante implementación.

---

# 5. Por qué un gateway separado

Ventajas:

```text
no tocar Caddy productivo;
un solo punto de entrada;
rutas predecibles;
frontend y API bajo el mismo origen;
soporte WebSocket para terminal;
sin publicar DB;
sin publicar API individualmente;
sin publicar toolbox individualmente.
```

---

# 6. Acceso por equipo

Para ClubLab v1 se evitará depender de DNS local.

Cada equipo tendrá un puerto propio en el gateway.

Reservas:

```text
Team 01 → 8211
Team 02 → 8212
Team 03 → 8213
Team 04 → 8214
Team 05 → 8215
Team 06 → 8216

Spare   → 8219
```

Ejemplo, si la IP LAN de la sesión es:

```text
10.10.100.41
```

entonces:

```text
Team 01
http://10.10.100.41:8211

Team 02
http://10.10.100.41:8212
```

La IP no debe quedar hardcodeada en los materiales permanentes.

Se genera al preparar la sesión.

---

# 7. Por qué utilizar puertos por equipo en v1

Esta decisión evita añadir dependencias como:

```text
DNS local;
mDNS;
edición de hosts;
wildcard DNS;
certificados;
configuración del router.
```

Y aun así conserva:

```text
un solo gateway;
cero puertos directos de API/DB/toolbox;
una URL clara por equipo.
```

Más adelante podría migrarse a:

```text
team01.clublab.local
```

sin cambiar la arquitectura interna.

---

# 8. IP de publicación

La interfaz `eno1` utiliza DHCP.

Por tanto, no se fijará permanentemente:

```text
10.10.100.41
```

en Compose.

Se utilizará una variable:

```text
CLUBLAB_BIND_IP
```

Ejemplo en una sesión:

```text
CLUBLAB_BIND_IP=10.10.100.41
```

Antes del despliegue se comprobará que esa IP:

```text
pertenece a eno1;
está activa;
corresponde a la LAN esperada.
```

---

# 9. Regla de binding

Los puertos de alumnos se enlazarán explícitamente a:

```text
CLUBLAB_BIND_IP
```

No a:

```text
0.0.0.0
```

como configuración normal.

Objetivo:

```text
evitar publicación accidental
en interfaces no previstas.
```

---

# 10. Tailscale

Tailscale seguirá disponible para:

```text
administración;
soporte;
acceso del instructor;
contingencia.
```

No será requisito para alumnos.

La sesión normal no exigirá:

```text
instalar Tailscale;
crear cuenta;
entrar al tailnet.
```

Esto reduce preparación y dependencia externa.

---

# 11. Cloudflare

ClubLab v1 no dependerá de:

```text
trycloudflare.com
```

ni del `cloudflared-quick` existente.

Razones:

```text
URL temporal;
dependencia de Internet;
servicio actual pertenece a otra aplicación;
no es necesario para una clase dentro de LAN.
```

---

# 12. HTTP vs HTTPS

En la primera versión, dentro de la LAN controlada:

```text
HTTP
```

será suficiente.

Motivos:

```text
sin datos reales;
credenciales desechables;
sin dominio;
sin certificados;
menos fricción en clase.
```

Si en el futuro se habilita acceso remoto:

```text
Tailscale HTTPS
o
dominio/certificado dedicado
```

podrán añadirse.

---

# 13. Rutas públicas de cada equipo

En el puerto de cada equipo:

```text
/
```

→ frontend

```text
/api/*
```

→ API del equipo

```text
/terminal/*
```

→ terminal web del toolbox

Así el alumno utiliza una única dirección base.

Ejemplo:

```text
http://10.10.100.41:8211/
http://10.10.100.41:8211/api/ranking
http://10.10.100.41:8211/terminal/
```

---

# 14. API bajo mismo origen

La API quedará detrás del gateway.

Ventajas:

```text
sin CORS complejo;
DevTools muestra rutas claras;
una URL por equipo;
el navegador no necesita conocer puertos internos.
```

El frontend consumirá:

```text
/api/...
```

de forma relativa.

---

# 15. Terminal del alumno

Se selecciona como diseño base:

> **Terminal web dentro del toolbox.**

Tecnología preferida:

```text
ttyd
```

o equivalente ligero compatible con WebSocket.

Ruta:

```text
/terminal/
```

El gateway realizará reverse proxy hacia:

```text
toolbox:<puerto-terminal>
```

---

# 16. Motivo de terminal web

Evita:

```text
SSH al host;
usuarios Linux;
instalaciones locales;
PowerShell/WSL diferente por alumno;
problemas de PATH;
configuración de clientes.
```

Requisito del alumno:

```text
navegador
```

---

# 17. Usuario del toolbox

El shell del alumno se ejecutará como:

```text
usuario no-root
```

No tendrá:

```text
sudo;
CAP_SYS_ADMIN;
CAP_NET_ADMIN;
Docker socket;
host PID;
host network;
mounts del host.
```

La shell solo existe dentro del contenedor del equipo.

---

# 18. Autenticación de terminal

Cada toolbox tendrá credenciales:

```text
exclusivas de su equipo;
desechables;
distintas de DB;
distintas de producción.
```

La terminal web deberá requerir autenticación.

Fase 3 cerrará el mecanismo definitivo:

```text
Basic Auth temporal;
token;
o integración equivalente.
```

No se permitirá una shell anónima accesible desde toda la LAN.

---

# 19. Redes por equipo

Se refina la arquitectura del Bloque A.

Cada equipo tendrá **dos redes**, no una sola:

```text
app network
data network
```

Ejemplo Team 01:

```text
clublab-team01-app
clublab-team01-data
```

La separación aumenta seguridad sin cambiar la experiencia pedagógica.

---

# 20. Red APP

Conectados:

```text
gateway
frontend
api
toolbox
```

No conectado:

```text
database
```

Funciones:

```text
reverse proxy;
API;
terminal;
diagnóstico de aplicación.
```

---

# 21. Red DATA

Conectados:

```text
api
database
toolbox
```

No conectados:

```text
frontend
gateway
```

Funciones:

```text
acceso PostgreSQL;
M3;
M4;
diagnóstico de DB;
futuro fault injection.
```

---

# 22. Resultado de segmentación

```text
                         GATEWAY
                            │
                     teamXX-app
                            │
              ┌─────────────┼─────────────┐
              │             │             │
          FRONTEND         API         TOOLBOX
                            │             │
                            └─────┬───────┘
                                  │
                           teamXX-data
                                  │
                              DATABASE
```

El gateway no tiene ruta directa a PostgreSQL.

El frontend tampoco.

---

# 23. Redes internas

Las redes:

```text
clublab-teamXX-app
clublab-teamXX-data
```

se configurarán como redes Docker internas cuando la implementación lo permita:

```text
internal: true
```

Los servicios del equipo no necesitan salir a Internet durante la clase.

---

# 24. Beneficio de redes internas

Impide que un alumno desde toolbox use el entorno como salto hacia:

```text
Internet;
LAN;
servicios del host;
producción.
```

La experiencia sigue permitiendo:

```text
curl a API;
psql a DB;
DNS interno;
ping entre servicios autorizados.
```

---

# 25. Comunicación permitida

Matriz:

| Origen | Frontend | API | DB | Toolbox | Otro team |
|---|---:|---:|---:|---:|---:|
| Gateway | Sí | Sí | **No** | Sí | Solo vía su propia red conectada |
| Frontend | — | No directa | **No** | **No** | **No** |
| API | No necesaria | — | Sí | No necesaria | **No** |
| Toolbox | Sí/diagnóstico | Sí | Sí | — | **No** |
| DB | **No** | responde | — | responde | **No** |

El tráfico del navegador hacia API pasa por gateway.

---

# 26. El frontend no necesita hablar directamente con API

Esto es intencional.

El código React se ejecuta en:

```text
navegador del alumno
```

y hace:

```text
GET /api/ranking
```

hacia el gateway.

El contenedor Nginx del frontend únicamente sirve archivos estáticos.

---

# 27. DNS interno de Docker

Dentro de cada red se utilizarán aliases sencillos:

```text
frontend
api
database
toolbox
```

Ejemplos desde toolbox:

```bash
curl http://api:3000/api/health
```

y:

```bash
psql -h database ...
```

Esto permite aprender nombres de servicio sin mostrar IPs internas.

---

# 28. IPAM reservado para ClubLab

Se reserva conceptualmente:

```text
10.77.0.0/16
```

para redes Docker de ClubLab.

No se superpone con lo observado en Fase 0:

```text
LAN              10.10.100.0/22
Docker actual     172.17.0.0/16
                  172.18.0.0/16
                  172.19.0.0/16
                  172.20.0.0/16
Tailscale         100.64.0.0/10
```

---

# 29. Subredes por equipo

Asignación inicial:

| Equipo | APP | DATA |
|---|---|---|
| team01 | 10.77.1.0/24 | 10.77.101.0/24 |
| team02 | 10.77.2.0/24 | 10.77.102.0/24 |
| team03 | 10.77.3.0/24 | 10.77.103.0/24 |
| team04 | 10.77.4.0/24 | 10.77.104.0/24 |
| team05 | 10.77.5.0/24 | 10.77.105.0/24 |
| team06 | 10.77.6.0/24 | 10.77.106.0/24 |
| spare | 10.77.9.0/24 | 10.77.109.0/24 |

Rangos reservados para crecimiento:

```text
10.77.7.0/24
10.77.8.0/24
10.77.10.0/24 – 10.77.99.0/24
10.77.107.0/24 – 10.77.199.0/24
```

---

# 30. Validación obligatoria antes de crear redes

Aunque `10.77.0.0/16` queda elegido para diseño, antes del despliegue se debe ejecutar un preflight.

Comprobar:

```text
ip route;
docker network inspect;
tailscale routes;
redes VPN presentes.
```

Si en ese momento existe un conflicto real:

```text
NO crear las redes;
recalcular el rango;
actualizar D02.
```

El diseño no justifica ignorar una colisión descubierta después.

---

# 31. No modificar `default-address-pools`

No se cambiará globalmente:

```text
Docker daemon default-address-pools
```

en esta fase.

Razón:

```text
es configuración del daemon del host;
Docker ya sostiene producción;
no necesitamos alterar comportamiento global.
```

ClubLab utilizará IPAM explícito únicamente en sus propias redes.

---

# 32. Puertos internos

Valores iniciales:

```text
frontend → 80
api      → 3000
db       → 5432
toolbox terminal → 7681
```

Solo son visibles dentro de las redes Docker.

No se publican al host.

---

# 33. Puertos del host reservados para ClubLab

Publicados únicamente por `clublab-gateway`:

```text
8211
8212
8213
8214
8215
8216
8219
```

Antes del despliegue:

```text
ss -ltnup
```

debe confirmar que siguen disponibles.

---

# 34. No reutilizar puertos existentes

No se utilizarán:

```text
22
443
631
2022
3500
5432
8080
8081
8090
8443
8444
9090
2019
25567
25568
```

ni otros detectados como ocupados durante el preflight.

---

# 35. Firewall

No se abrirán puertos de:

```text
DB;
API;
toolbox;
frontend individual.
```

Solo los puertos del gateway necesarios para la clase.

La implementación deberá restringirlos a la interfaz/red esperada.

Como Docker puede interactuar con reglas de firewall de forma distinta a servicios host normales, no se confiará únicamente en una zona de firewalld como frontera de aislamiento.

Las fronteras principales serán:

```text
binding específico;
redes Docker separadas;
servicios sin published ports;
autenticación;
permisos de aplicación.
```

---

# 36. Aislamiento entre equipos

Un equipo no comparte ninguna red Docker con otro equipo.

Ejemplo:

```text
team01-api
```

solo participa en:

```text
clublab-team01-app
clublab-team01-data
```

Nunca:

```text
clublab-team02-*
```

---

# 37. Excepción: gateway

`clublab-gateway` será el único contenedor conectado a varias redes APP.

Ejemplo:

```text
team01-app
team02-app
...
team06-app
spare-app
```

No se conecta a redes DATA.

---

# 38. Endurecimiento del gateway

Como el gateway toca varias redes de equipos:

```text
no privileged;
sin Docker socket;
sin host network;
filesystem read-only donde sea viable;
capabilities mínimas;
sin NET_ADMIN;
sin mounts productivos;
```

Además, no se utilizará como router L3.

La implementación deberá desactivar/evitar forwarding innecesario dentro del contenedor.

---

# 39. Regla de no tránsito lateral

El gateway solo debe realizar:

```text
reverse proxy HTTP/WebSocket
```

No:

```text
routing IP entre redes;
shell;
NAT entre equipos;
proxy genérico;
SOCKS;
forward arbitrario.
```

Así:

```text
team01
≠
team02
```

aunque el gateway conozca ambas redes.

---

# 40. Rutas del gateway por puerto

Ejemplo Team 01:

```text
:8211
```

reglas:

```text
/api/*       → team01 API/terminal/*  → team01 toolbox
/*           → team01 frontend
```

Team 02:

```text
:8212
```

mismo patrón contra servicios de Team 02.

---

# 41. Orden de rutas

El gateway debe evaluar primero:

```text
/terminal/*
```

y:

```text
/api/*
```

antes del fallback:

```text
/*
```

para evitar que React/Nginx capture rutas técnicas.

---

# 42. WebSocket

La ruta de terminal debe soportar:

```text
WebSocket
```

Caddy puede realizar esta función mediante reverse proxy.

Se validará técnicamente durante implementación.

---

# 43. Credenciales del alumno

Cada equipo tendrá al menos:

```text
credencial de aplicación
credencial de terminal
credencial DB
```

No necesariamente serán iguales.

Preferencia:

```text
separadas
```

para limitar impacto.

---

# 44. Acceso a PostgreSQL

PostgreSQL:

```text
NO published port;
NO LAN;
NO Tailscale;
NO host port.
```

Solo:

```text
API
+
Toolbox del mismo team
```

pueden llegar a:

```text
database:5432
```

---

# 45. Acceso instructor a DB

El instructor no necesita publicar 5432.

Podrá utilizar herramientas administrativas futuras a través de:

```text
control plane;
docker exec administrado;
toolbox instructor;
scripts internos.
```

sin abrir DB a red externa.

---

# 46. Experiencia M1

El alumno abre:

```text
http://<LAN_IP>:8211
```

y DevTools observa:

```text
GET /api/ranking
```

No ve:

```text
3000;
5432;
IPs Docker.
```

Esto mantiene el descubrimiento limpio.

---

# 47. Experiencia M2

Desde terminal:

```bash
curl http://api:3000/api/ranking
```

Aquí descubre que existe un servicio API independiente.

La diferencia entre:

```text
ruta pública /api/ranking
```

y:

```text
servicio interno api:3000
```

puede explicarse brevemente.

---

# 48. Experiencia M3/M4

Desde toolbox:

```text
database
```

será el hostname de PostgreSQL.

Ejemplo conceptual:

```bash
psql -h database -U <usuario> -d <base>
```

No necesita conocer IP interna.

---

# 49. Experiencia M5

La herramienta `clublab status` o equivalente podrá mostrar:

```text
frontend
api
database
toolbox
```

sin revelar:

```text
otras redes;
contenedores de producción;
host Docker.
```

---

# 50. Experiencia M7

La topología permite que:

```text
gateway    healthy
frontend   healthy
api        healthy
database   healthy
```

mientras:

```text
ranking dependency
```

falla dentro del stack del equipo.

El fallo permanece limitado a ese team.

---

# 51. Acceso remoto futuro

La arquitectura deja abierta una segunda entrada futura por:

```text
Tailscale
```

sin modificar las redes de los equipos.

Opciones posteriores:

```text
Tailscale Serve al gateway;
binding secundario a tailscale0;
proxy administrativo dedicado.
```

No se implementará como dependencia inicial.

---

# 52. Material entregado al alumno

La tarjeta inicial del equipo necesita únicamente:

```text
Team ID
URL
usuario/password de app
usuario/password de terminal
```

Las credenciales DB se entregarán cuando llegue M3, no al inicio.

Esto mantiene la revelación progresiva definida en D01.

---

# 53. QR opcional

La URL de cada equipo podrá imprimirse como:

```text
texto
+
QR
```

generado el día de la sesión con la IP LAN actual.

No es requisito técnico, pero reduce errores al copiar direcciones.

---

# 54. Preflight de red antes de cada sesión

El instructor deberá verificar:

```text
[ ] eno1 tiene IP
[ ] CLUBLAB_BIND_IP coincide con eno1
[ ] gateway ports están libres
[ ] 10.77.0.0/16 no colisiona
[ ] redes teamXX existen o pueden crearse
[ ] gateway alcanza frontend/API/toolbox
[ ] gateway NO alcanza DB directamente
[ ] team01 no alcanza team02
[ ] DB no tiene published port
[ ] terminal exige autenticación
```

---

# 55. Pruebas de aislamiento obligatorias

Antes del ensayo real:

## Test 1

Desde `team01-toolbox`:

```text
api team01 → accesible
db team01  → accesible
```

## Test 2

Desde `team01-toolbox`:

```text
team02 API → no accesible
team02 DB  → no accesible
```

## Test 3

Desde LAN:

```text
gateway team01 → accesible
DB team01      → no accesible
API:3000       → no accesible directamente
```

## Test 4

Desde gateway:

```text
frontend team01 → sí
api team01      → sí
toolbox team01  → sí
db team01       → no
```

---

# 56. Riesgos del diseño

## RB-01 — IP LAN cambia

Mitigación:

```text
CLUBLAB_BIND_IP dinámico por despliegue;
tarjetas/QR generados en preflight.
```

## RB-02 — Puerto reservado ocupado

Mitigación:

```text
preflight;
no iniciar si existe colisión;
usar mapa alternativo documentado si fuese necesario.
```

## RB-03 — Gateway se vuelve puente lateral

Mitigación:

```text
solo reverse proxy;
sin NET_ADMIN;
sin forwarding;
sin shell de alumno;
sin data networks.
```

## RB-04 — Terminal web expuesta

Mitigación:

```text
autenticación por team;
usuario no-root;
red interna;
sin host mounts.
```

## RB-05 — DNS/IPAM cambia en servidor

Mitigación:

```text
validación previa;
IPAM explícito;
no modificar Docker daemon global.
```

---

# 57. Decisiones cerradas del Bloque B

### DB2-01
LAN será el acceso principal de alumnos.

### DB2-02
Tailscale será administrativo/alternativo.

### DB2-03
Cloudflare Quick Tunnel no será dependencia de ClubLab.

### DB2-04
Se utilizará `clublab-gateway` separado del Caddy existente.

### DB2-05
El gateway será Caddy.

### DB2-06
ClubLab v1 utilizará puertos por equipo:

```text
8211–8216
8219 spare
```

### DB2-07
El bind se hará a `CLUBLAB_BIND_IP`, no normalmente a `0.0.0.0`.

### DB2-08
No se requerirá DNS local en v1.

### DB2-09
La terminal será web, dentro del toolbox.

### DB2-10
La terminal requerirá autenticación.

### DB2-11
Cada equipo tendrá dos redes:

```text
app
data
```

### DB2-12
Las redes serán internas cuando sea técnicamente viable.

### DB2-13
El rango reservado de diseño será:

```text
10.77.0.0/16
```

con IPAM explícito.

### DB2-14
Cada team tendrá /24 APP y /24 DATA.

### DB2-15
PostgreSQL no publicará ningún puerto.

### DB2-16
Frontend/API/toolbox tampoco publicarán puertos al host.

### DB2-17
El único punto de entrada de alumnos será el gateway.

### DB2-18
El gateway nunca se conectará a las redes DATA.

### DB2-19
No habrá comunicación lateral entre teams.

### DB2-20
No se modificará `default-address-pools` del Docker daemon.

### DB2-21
La sesión podrá funcionar sin Internet público.

---

# 58. Arquitectura de red congelada

```text
                       LAN
                        │
                        ▼
              ┌─────────────────┐
              │ clublab-gateway │
              │      Caddy      │
              └────────┬────────┘
                       │
                teamXX-app
                       │
      ┌────────────────┼────────────────┐
      │                │                │
  FRONTEND            API           TOOLBOX
                       │                │
                       └──────┬─────────┘
                              │
                        teamXX-data
                              │
                          POSTGRESQL
```

Por cada equipo se repite la caja, sin redes compartidas entre ellos.

---

# 59. Lo que pasa al Bloque C

El siguiente bloque cerrará:

```text
healthchecks;
logs;
status;
observabilidad;
fault injection;
control plane;
reset;
recover;
entorno spare;
operación del instructor;
requisitos concretos del Scenario Manager.
```

La conectividad base ya no necesita reabrirse salvo que una prueba técnica demuestre una incompatibilidad real.

---

# 60. Criterios de aceptación

```text
[x] acceso principal decidido
[x] Tailscale definido
[x] Cloudflare descartado como dependencia
[x] gateway definido
[x] puertos definidos
[x] bind definido
[x] rutas gateway definidas
[x] terminal web definida
[x] redes APP/DATA definidas
[x] IPAM definido
[x] subredes team01–team06 definidas
[x] spare definido
[x] comunicación permitida definida
[x] comunicación prohibida definida
[x] PostgreSQL sin publicación
[x] servicios internos sin publicación
[x] preflight definido
[x] pruebas de aislamiento definidas
[x] riesgos documentados
```

# BLOQUE B — COMPLETADO