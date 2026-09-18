# D00 — Estado Base del Servidor para ClubLab

**Proyecto:** ClubLab v1  
**Fase:** 0 — Auditoría y congelación del estado actual  
**Estado del documento:** FINAL — FASE 0 COMPLETADA  
**Bloque completado:** A — Host + CPU + RAM + almacenamiento  
**Servidor:** Tulum  
**Fecha de auditoría:** 2026-09-16

---

# 1. Resumen ejecutivo parcial

El Bloque A confirma que el servidor Tulum continúa siendo un **Dell PowerEdge R440** con **CentOS Stream 10**, arquitectura **x86-64**, **32 CPU lógicos** y **77 GiB de RAM**.

El equipo presenta actualmente una carga muy baja:

- Load average: `0.10 / 0.22 / 0.24`
- RAM disponible: `66 GiB`
- Swap utilizada: `0 B`
- `/home`: aproximadamente `1.3 TB` disponibles
- `/`: `54 GB` disponibles

A nivel de capacidad, no se observa presión inmediata que impida continuar evaluando ClubLab.

Se detectaron algunos cambios respecto al manual de agosto de 2026:

1. El kernel pasó de la serie `6.12.0-170` a `6.12.0-264`.
2. El uso de `/` aumentó aproximadamente de 20% a 24%.
3. El uso de `/home` aumentó aproximadamente de 2% a 5%.
4. Los nombres de dispositivo `sda` y `sdb` aparecen intercambiados respecto a la fotografía documentada en el manual.
5. El hostname estático continúa sin configurarse.

---

# 2. Identidad del servidor

| Campo | Estado actual |
|---|---|
| Fabricante | Dell Inc. |
| Modelo | PowerEdge R440 |
| Hostname estático | No configurado |
| Hostname transitorio | `localhost` |
| Sistema operativo | CentOS Stream 10 (Coughlan) |
| Kernel | `6.12.0-264.el10.x86_64` |
| Arquitectura | x86-64 |
| Firmware | 2.4.8 |
| Fecha firmware | 2019-11-27 |
| Uptime observado | 4 días, 23 h 57 min |

## Estado

**CONFIRMADO CON CAMBIOS MENORES**

El hardware y sistema operativo siguen coincidiendo con el manual. El cambio principal es el kernel.

---

# 3. CPU

| Campo | Estado actual |
|---|---|
| Modelo | Intel Xeon Silver 4208 @ 2.10 GHz |
| Sockets | 2 |
| Núcleos por socket | 8 |
| Hilos por núcleo | 2 |
| CPU lógicos | 32 |
| Frecuencia máxima reportada | 3.2 GHz |
| Virtualización | Intel VT-x |
| NUMA visible | 1 nodo |

## Carga observada

```text
0.10 / 0.22 / 0.24
```

Para 32 CPU lógicos, esta carga es muy baja.

## Estado

**CONFIRMADO**

No se observan cambios relevantes en CPU respecto al manual.

---

# 4. Memoria

```text
Total:       77 GiB
Usada:       10 GiB
Libre:       64 GiB
Disponible:  66 GiB
Swap total:  31 GiB
Swap usada:   0 B
```

## Interpretación

El servidor tiene aproximadamente **66 GiB disponibles** en el momento de la auditoría.

Esto deja un margen amplio para evaluar múltiples entornos ClubLab, aunque el presupuesto definitivo por equipo se calculará después de medir también los contenedores y servicios actualmente activos.

## Estado

**CONFIRMADO**

---

# 5. Almacenamiento

## Filesystems

| Montaje | Tipo | Tamaño | Usado | Disponible | Uso |
|---|---|---:|---:|---:|---:|
| `/` | XFS | 70 GB | 17 GB | 54 GB | 24% |
| `/home` | XFS | 1.3 TB | 54 GB | 1.3 TB | 5% |
| `/boot` | XFS | 960 MB | 534 MB | 427 MB | 56% |
| `/boot/efi` | VFAT | 599 MB | 8.9 MB | 590 MB | 2% |

## LVM

```text
cs-root   70 GB
cs-swap   32 GB
cs-home   1.3 TB
```

`cs-home` se extiende sobre los dos discos físicos.

## Discos físicos observados

```text
sda  TOSHIBA HDWD110   931.5 GB
sdb  ST3500630NS       465.8 GB
```

### Distribución observada

```text
sda
├── sda1  EFI
├── sda2  /boot
└── sda3  LVM
    └── cs-home

sdb
└── sdb1  LVM
    ├── cs-root
    └── cs-home
```

---

# 6. Diferencias respecto al manual

| Componente | Manual agosto 2026 | Estado actual | Clasificación |
|---|---|---|---|
| Hardware | Dell PowerEdge R440 | Dell PowerEdge R440 | CONFIRMADO |
| SO | CentOS Stream 10 | CentOS Stream 10 | CONFIRMADO |
| Kernel | `6.12.0-170.el10.x86_64` | `6.12.0-264.el10.x86_64` | CAMBIÓ |
| CPU | 32 CPU lógicos | 32 CPU lógicos | CONFIRMADO |
| RAM | 77 GiB | 77 GiB | CONFIRMADO |
| Swap | ~31 GiB disponible | 31 GiB, 0 usada | CONFIRMADO |
| Hostname estático | No definido | No definido | CONFIRMADO |
| `/` | ~20% usado | 24% usado | CAMBIÓ |
| `/home` | ~2% usado | 5% usado | CAMBIÓ |
| `/home` capacidad | ~1.3 TB | ~1.3 TB | CONFIRMADO |
| Firmware | 2.4.8 | 2.4.8 | CONFIRMADO |
| Disco 931.5 GB | documentado con otro nombre de dispositivo | `sda` | REQUIERE NOTA |
| Disco 465.8 GB | documentado con otro nombre de dispositivo | `sdb` | REQUIERE NOTA |

---

# 7. Hallazgo importante — nombres `sda` / `sdb`

El manual anterior asociaba las particiones de arranque a otro nombre de dispositivo. En la auditoría actual:

```text
TOSHIBA 931.5 GB  → sda
Seagate 465.8 GB  → sdb
```

Los nombres `/dev/sda` y `/dev/sdb` pueden depender del orden de enumeración del hardware al arrancar.

## Decisión documental preliminar

Para ClubLab y para futuros procedimientos:

> **No se debe identificar un disco crítico únicamente como `/dev/sda` o `/dev/sdb`.**

Cuando sea necesario referirse a almacenamiento físico, conviene usar también:

- modelo;
- UUID;
- LVM PV/VG/LV;
- punto de montaje.

Esto evita asumir que la letra del dispositivo será estable después de un reinicio.

---

# 8. Capacidad preliminar para ClubLab

## Estado actual

```text
CPU lógicos:      32
Load average:     0.10 / 0.22 / 0.24
RAM disponible:   66 GiB
/home disponible: ~1.3 TB
Swap usada:       0 B
```

## Evaluación provisional

**Capacidad física: VERDE**

El hardware tiene margen suficiente para continuar con el diseño de múltiples entornos ClubLab.

Aún NO se determina cuántos equipos simultáneos soportará el laboratorio porque faltan:

- consumo real de Docker;
- contenedores actuales;
- redes;
- bases de datos;
- servicios;
- carga durante operación normal.

---

# 9. Clasificación preliminar

## ROJO — no tocar

```text
cs-root
cs-home
cs-swap
particiones de arranque
firmware
configuración de almacenamiento físico
```

## AMARILLO — compartible con planificación

```text
CPU
RAM
/home
host físico
```

## VERDE — capacidad disponible

```text
CPU ociosa
RAM libre
espacio en /home
```

La categoría VERDE significa capacidad disponible, no autorización para modificar todavía.

---

# 10. Conclusión del Bloque A

El Bloque A se considera **APROBADO**.

No se detecta ninguna limitación de hardware o almacenamiento que impida continuar con ClubLab.

Los principales puntos a conservar son:

1. recursos ampliamente holgados;
2. kernel actualizado respecto al manual;
3. crecimiento moderado del uso de disco;
4. hostname estático todavía pendiente;
5. no depender de las letras `sda`/`sdb` en documentación futura;
6. no reservar todavía recursos definitivos hasta auditar Docker y servicios.

---

# 11. Bloque B — Red, rutas, puertos y firewall

## Estado

**COMPLETADO**

La red principal documentada continúa operativa y se confirmaron varios componentes nuevos que no formaban parte de la fotografía de agosto de 2026.

---

# 12. Interfaces actuales

| Interfaz | Estado | Dirección / red | Función preliminar |
|---|---|---|---|
| `lo` | UP | `127.0.0.1/8`, `::1/128` | Loopback |
| `eno1` | UP | `10.10.100.41/22` | Interfaz LAN principal |
| `eno2` | DOWN / NO-CARRIER | Sin IP | Segunda NIC física no conectada |
| `tailscale0` | UP | `100.115.55.35/32` | Red privada Tailscale |
| `pelican0` | UP | `172.20.0.1/16` | Bridge adicional asociado a la infraestructura Pelican/Wings |
| `docker0` | DOWN | `172.17.0.1/16` | Bridge Docker por defecto, sin enlaces activos |
| `br-baa4f0d2260f` | UP | `172.18.0.1/16` | Bridge Docker |
| `br-a9af8457cee6` | UP | `172.19.0.1/16` | Bridge Docker |

También existen múltiples interfaces `veth`, correspondientes a conexiones de contenedores con los bridges Docker.

## Hallazgo

`eno2` existe físicamente, pero aparece:

```text
DOWN
NO-CARRIER
sin dirección IP
```

Por tanto, no participa actualmente en la conectividad del servidor.

---

# 13. Dirección LAN y rutas

## LAN

```text
IP:       10.10.100.41/22
Gateway:  10.10.100.1
DNS 1:    8.8.8.8
DNS 2:    1.1.1.1
Origen:   DHCP
```

La configuración coincide con la fotografía anterior.

## Rutas principales

```text
default           → 10.10.100.1 por eno1
10.10.100.0/22    → eno1
172.17.0.0/16     → docker0 (linkdown)
172.18.0.0/16     → br-baa4f0d2260f
172.19.0.0/16     → br-a9af8457cee6
172.20.0.0/16     → pelican0
```

Tailscale añade reglas de routing policy, incluyendo la tabla `52`.

## Estado

**LAN: CONFIRMADA**

**RUTAS DOCKER: CAMBIARON / CRECIERON**

---

# 14. NetworkManager

La conexión principal sigue siendo:

```text
eno1
```

Interfaces externas administradas por otros componentes aparecen como `connected (externally)`:

```text
tailscale0
pelican0
br-a9af8457cee6
br-baa4f0d2260f
docker0
```

Esto es consistente con interfaces creadas por Tailscale y motores de contenedores.

No se debe intentar administrar estas interfaces como conexiones Ethernet normales de NetworkManager.

---

# 15. Mapa de listeners actuales

## Exposición relevante

| Dirección | Puerto | Proceso | Lectura preliminar |
|---|---:|---|---|
| `0.0.0.0` / `[::]` | 22/TCP | `sshd` | SSH en interfaces del host |
| `*` | 9090/TCP | `systemd` / Cockpit socket | Cockpit expuesto en todas las interfaces |
| `0.0.0.0` / `[::]` | 41641/UDP | `tailscaled` | Transporte Tailscale |
| `100.115.55.35` | 443/TCP | `tailscaled` | Tailscale Serve / servicio privado |
| `100.115.55.35` | 8443/TCP | `tailscaled` | Servicio Tailscale adicional |
| `100.115.55.35` | 8444/TCP | `tailscaled` | Servicio Tailscale adicional |
| `100.115.55.35` | 2022/TCP | `wings` | Servicio Wings restringido a Tailscale |
| `127.0.0.1` | 8081/TCP | `wings` | Wings local |
| `127.0.0.1` | 8080/TCP | `docker-proxy` | Servicio web existente |
| `127.0.0.1` | 3500/TCP | `docker-proxy` | Backend existente |
| `127.0.0.1` | 8090/TCP | `caddy` | Caddy activo |
| `127.0.0.1` | 2019/TCP | `caddy` | API administrativa local de Caddy |
| `127.0.0.1` | 20241/TCP | `cloudflared` | Endpoint local cloudflared |
| `172.20.0.1` | 25567/TCP+UDP | `docker-proxy` | Servicio asociado a bridge `pelican0` |
| `172.20.0.1` | 25568/TCP+UDP | `docker-proxy` | Servicio asociado a bridge `pelican0` |
| varias | UDP dinámicos | `playitd` | Agente Playit activo |
| `0.0.0.0` / `[::]` | 5353/UDP | `avahi-daemon` | mDNS |
| loopback | 631/TCP | `cupsd` | CUPS local |

## Interpretación

Los puertos `8080`, `3500`, `8090`, `2019`, `8081`, `2022`, `25567`, `25568`, `443`, `8443`, `8444` y los listeners gestionados por `playitd` deben considerarse **ocupados o reservados** hasta completar el mapa de servicios.

No reservar ningún puerto para ClubLab todavía.

---

# 16. Cambios relevantes frente al manual

## Caddy

El manual anterior indicaba:

```text
caddy = disabled / inactive
```

Ahora existe:

```text
127.0.0.1:8090  → caddy
127.0.0.1:2019  → caddy
```

Por tanto:

**CADDY: CAMBIÓ — ahora está activo.**

Su función exacta se determinará en el Bloque G.

---

## Pelican / Wings

Ahora aparecen elementos no documentados originalmente:

```text
pelican0
wings
puerto 2022 sobre Tailscale
puerto 8081 sobre loopback
25567 / 25568 sobre pelican0
```

Clasificación:

**NUEVO / REQUIERE MAPEO**

No se utilizarán para ClubLab hasta conocer su función y dependencias.

---

## Playit

Existe un proceso:

```text
playitd
```

con varios sockets UDP.

Clasificación:

**NUEVO / REQUIERE MAPEO**

Es probable que forme parte de la publicación de servicios de juego u otra infraestructura reciente, pero la función exacta se documentará al revisar servicios.

---

## Tailscale

La IP sigue siendo:

```text
100.115.55.35
```

pero ahora existen listeners adicionales:

```text
443
8443
8444
```

y un servicio `wings` sobre:

```text
100.115.55.35:2022
```

La topología privada ha crecido respecto al manual.

---

# 17. Firewall

## Estado

```text
firewalld: running
```

## Zona `public`

Interfaz:

```text
eno1
```

Servicios permitidos:

```text
cockpit
dhcpv6-client
ssh
```

No existen puertos adicionales declarados explícitamente.

`forward` está habilitado.

## Zona `docker`

Interfaces:

```text
pelican0
br-a9af8457cee6
br-baa4f0d2260f
docker0
```

Configuración destacada:

```text
target: ACCEPT
forward: yes
```

## Implicación para ClubLab

No debemos asumir que `firewalld` aislará por sí solo los entornos de alumnos entre bridges Docker.

La arquitectura de ClubLab deberá basar su aislamiento principalmente en:

```text
redes Docker dedicadas
ausencia de publicación innecesaria de puertos
sin conexión a redes de producción
sin Docker socket
sin mounts del host
reglas adicionales solo si Fase 2 demuestra que son necesarias
```

---

# 18. Clasificación de interfaces y redes

## ROJO — no utilizar para ClubLab directamente

```text
eno1
tailscale0
pelican0
br-a9af8457cee6
br-baa4f0d2260f
docker0
```

La clasificación ROJO en esta fase significa:

> infraestructura existente; no reutilizar ni modificar hasta terminar el mapeo.

No significa que todos los componentes sean peligrosos.

## AMARILLO — posible dependencia compartida

```text
Tailscale
Caddy
Cloudflare
host Docker
```

Su reutilización se decidirá después.

## VERDE — aún no asignado

Todavía no existe una red ClubLab.

La Fase 2 deberá crear un namespace/rango de red propio que no colisione con:

```text
172.17.0.0/16
172.18.0.0/16
172.19.0.0/16
172.20.0.0/16
10.10.100.0/22
```

---

# 19. Restricción nueva para el diseño de ClubLab

La arquitectura debe evitar seleccionar automáticamente rangos Docker consecutivos sin comprobar disponibilidad.

Rangos ya observados:

```text
172.17.0.0/16
172.18.0.0/16
172.19.0.0/16
172.20.0.0/16
```

Durante Fase 2 se elegirá explícitamente una subred para ClubLab para evitar colisiones actuales y futuras.

---

# 20. Posible modelo de acceso — todavía no decidido

La auditoría demuestra que existen al menos cuatro mecanismos potenciales:

```text
LAN
Tailscale
Cloudflare
Caddy
```

Además existe infraestructura `Playit`.

Todavía NO se decide cuál usarán los integrantes.

Criterios que se evaluarán:

```text
facilidad de acceso
aislamiento
número de alumnos
necesidad de instalar cliente
exposición pública
estabilidad de URL
control de permisos
dependencia de Internet
```

---

# 21. Conclusión del Bloque B

El Bloque B se considera **APROBADO CON CAMBIOS IMPORTANTES**.

La red base del manual sigue vigente:

```text
eno1 → 10.10.100.41/22
gateway → 10.10.100.1
Tailscale → 100.115.55.35
```

pero la infraestructura del servidor ha evolucionado.

Se detectaron:

```text
Caddy activo
Pelican/Wings
bridge pelican0
Playit
nuevos bridges Docker
nuevos servicios sobre Tailscale
puertos adicionales
```

Por tanto, la arquitectura de ClubLab no debe diseñarse usando únicamente la fotografía de agosto.

---

# 22. Estado de la Fase 0

```text
[A] Host + CPU + RAM + almacenamiento   ✅
[B] Red + rutas + puertos + firewall    ✅
[C] Servicios systemd                   ← SIGUIENTE
[D] Docker + contenedores
[E] Redes + volúmenes Docker
[F] PostgreSQL
[G] Tailscale + Cloudflare + Caddy
[H] Directorios + backups + monitor
```

---

# 23. Bloque C — Servicios systemd

## Estado

**COMPLETADO**

Se confirmó que los servicios principales del servidor están habilitados y activos, y se identificaron formalmente tres componentes que no formaban parte del estado base original de agosto: **Pelican Queue, Pelican Wings y Playit**.

---

# 24. Servicios principales

| Servicio | Enabled | Active | Función |
|---|---|---|---|
| `docker.service` | Sí | Sí | Motor de contenedores |
| `tailscaled.service` | Sí | Sí | Red privada Tailscale |
| `cloudflared-quick.service` | Sí | Sí | Quick Tunnel actual |
| `caddy.service` | Sí | Sí | Reverse proxy / servidor web |
| `cockpit.socket` | Sí | Sí | Administración web |
| `crond.service` | Sí | Sí | Tareas programadas |
| `sshd.service` | Sí | Sí | Acceso SSH |
| `pelican-queue.service` | Sí | Sí | Cola de trabajos de Pelican |
| `playit.service` | Sí | Sí | Agente Playit |
| `wings.service` | Sí | Sí | Pelican Wings Daemon |

## Diferencia respecto al manual anterior

El cambio más claro es:

```text
Caddy
ANTES: disabled / inactive
AHORA: enabled / active
```

Además ahora existen:

```text
pelican-queue.service
playit.service
wings.service
```

Por tanto, el servidor ya no debe tratarse únicamente como host de WhatsApp + PostgreSQL; actualmente también aloja infraestructura de administración/ejecución de servidores de juego.

---

# 25. Pelican Wings

Servicio detectado:

```text
wings.service
Descripción: Pelican Wings Daemon
Binario: /usr/local/bin/wings
Estado: active (running)
Inicio observado: 2026-09-11
```

Consumo observado:

```text
RAM actual: ~100 MiB
RAM pico:   ~104 MiB
CPU acumulada: ~17 min 52 s
```

Wings está gestionando contenedores Docker y realizando:

```text
resource polling
power actions
server limit modifications
cron interno
actualización de estados hacia Panel
```

También confirma los listeners detectados en el Bloque B:

```text
Webserver interno:
127.0.0.1:8081

SFTP:
100.115.55.35:2022
```

## Implicación

Wings debe considerarse **infraestructura productiva existente**.

ClubLab no debe:

```text
reutilizar sus redes
reutilizar sus puertos
interferir con sus contenedores
modificar su configuración
usar su SFTP
depender de sus IDs de servidor
```

---

# 26. Playit

Servicio detectado:

```text
playit.service
Descripción: Playit Agent
Binario: /usr/local/bin/playitd
Estado: active (running)
Inicio observado: 2026-09-11
```

Consumo observado:

```text
RAM actual: ~21 MiB
RAM pico:   ~24 MiB
CPU acumulada: ~7 min 11 s
```

El agente utiliza:

```text
/etc/playit/playit.toml
/run/playit/playitd.sock
/var/log/playit/playit.log
```

## Precaución

`/etc/playit/playit.toml` puede contener secretos o datos sensibles.

No leer ni copiar su contenido dentro de la auditoría salvo que exista una necesidad específica y se haga una revisión segura.

## Implicación

Playit es infraestructura existente y no se utilizará para ClubLab durante el diseño inicial.

Podrá evaluarse posteriormente como mecanismo de exposición solo si existe una razón clara, pero no se tomará como dependencia por defecto.

---

# 27. Pelican Queue

Servicio confirmado:

```text
pelican-queue.service
Estado: active (running)
Enabled: sí
```

No se inspeccionó todavía su configuración ni consumo individual.

## Clasificación

```text
PRODUCCIÓN / INFRAESTRUCTURA EXISTENTE
```

Se mantendrá fuera de ClubLab.

---

# 28. Arquitectura actual revisada

Con los Bloques A–C, el servidor debe entenderse aproximadamente así:

```text
                       TULUM HOST
                           │
      ┌────────────────────┼────────────────────┐
      │                    │                    │
   Servicios            Docker              Acceso
   del host             Engine              remoto
      │                    │                    │
      │                    │                    ├── Tailscale
      │                    │                    └── Cloudflare
      │                    │
      ├── Caddy            ├── Apps existentes
      ├── Cockpit          ├── PostgreSQL
      ├── SSH              └── Servidores gestionados
      ├── Cron                  por Wings/Pelican
      ├── Wings
      ├── Pelican Queue
      └── Playit
```

Esto confirma que ClubLab deberá agregarse como una **zona nueva y aislada**, no como extensión improvisada de los servicios actuales.

---

# 29. Clasificación actualizada de servicios

## ROJO — no tocar

```text
docker.service
wings.service
pelican-queue.service
playit.service
cloudflared-quick.service
tailscaled.service
sshd.service
crond.service
cockpit.socket
servicios productivos existentes
```

`docker.service` aparece en ROJO porque reiniciarlo afectaría a todos los contenedores del host.

## AMARILLO — potencialmente reutilizable con diseño explícito

```text
caddy.service
Tailscale
Cloudflare
```

No se reutilizarán todavía.

## VERDE

Todavía no existe ningún servicio ClubLab.

---

# 30. Riesgo operativo identificado

La presencia de Wings significa que Docker ya no está siendo utilizado únicamente por los proyectos desplegados manualmente.

Ahora existe un sistema externo de orquestación/control que también:

```text
crea o administra contenedores
aplica límites
consulta recursos
ejecuta acciones de energía
mantiene estados
```

Por ello, en fases posteriores:

> **No se deben asumir como "huérfanos" contenedores, redes o volúmenes desconocidos.**

Antes de eliminar cualquier recurso Docker habrá que comprobar si pertenece a:

```text
WhatsApp
PostgreSQL
Pelican/Wings
ClubLab
otro servicio
```

---

# 31. Conclusión del Bloque C

El Bloque C se considera **APROBADO CON CAMBIOS IMPORTANTES**.

Se confirma:

```text
Docker       activo
Tailscale    activo
Cloudflare   activo
Caddy        activo
Cockpit      activo
Cron         activo
SSH          activo
Wings        activo
Pelican      activo
Playit       activo
```

La principal consecuencia para ClubLab es que el host ya tiene una capa adicional de administración de servidores mediante Pelican/Wings.

La futura arquitectura de ClubLab deberá coexistir con ella sin compartir nombres, redes, volúmenes, puertos ni ciclos de vida.

---

# 32. Estado de la Fase 0

```text
[A] Host + CPU + RAM + almacenamiento   ✅
[B] Red + rutas + puertos + firewall    ✅
[C] Servicios systemd                   ✅
[D] Docker + contenedores               ← SIGUIENTE
[E] Redes + volúmenes Docker
[F] PostgreSQL
[G] Tailscale + Cloudflare + Caddy[H] Directorios + backups + monitor
```

---

# 33. Bloque D — Docker y contenedores

## Estado

**COMPLETADO**

Se confirmó que Docker mantiene la misma versión documentada (`29.7.2`) y continúa utilizando:

```text
Storage driver: overlayfs
Logging driver: json-file
Docker Root Dir: /home/docker-data
```

Actualmente existen:

```text
6 contenedores totales
5 en ejecución
1 detenido
13 imágenes
1 volumen local
```

---

# 34. Inventario actual de contenedores

| Contenedor | Imagen | Estado | Puertos | Clasificación preliminar |
|---|---|---|---|---|
| `c73774b2-bb45-412b-997f-2f2080abade8` | `ghcr.io/pelican-eggs/yolks:java_8` | Up | `172.20.0.1:25567` TCP/UDP | Pelican / servidor de juego |
| `2286e7b1-ca54-4540-99ae-21f7ee8193d8` | `ghcr.io/pelican-eggs/yolks:java_21` | Up | `172.20.0.1:25568` TCP/UDP | Pelican / servidor de juego |
| `87d9a146-3fdd-4491-9595-a0c404d9f800` | `ghcr.io/pelican-eggs/yolks:java_25` | Exited | Ninguno visible | Pelican / servidor detenido |
| `whatsapp-backend` | `whatsapp-backend` | Up | `127.0.0.1:3500→3500` | Aplicación existente |
| `postgres-main` | `postgres:18-bookworm` | Up / healthy | `5432/tcp` solo Docker | PostgreSQL central |
| `whatsapp-frontend` | `whatsapp-frontend` | Up | `127.0.0.1:8080→80` | Aplicación existente |

---

# 35. Consumo actual de contenedores

| Contenedor | CPU | RAM | Límite visible | Observación |
|---|---:|---:|---:|---|
| Java 8 / Pelican | 0.17% | 3.957 GiB | 18.9 GiB | Servidor de juego activo |
| Java 21 / Pelican | 6.95% | 1.573 GiB | 21 GiB | Servidor de juego activo |
| WhatsApp backend | 1.30% | 2.8 GiB | 77.51 GiB | Sin límite de memoria específico aparente |
| PostgreSQL | 0.00% | 75.11 MiB | 77.51 GiB | Consumo bajo |
| WhatsApp frontend | 0.00% | 32.41 MiB | 77.51 GiB | Consumo bajo |

## Consumo total observado aproximado

Solo sumando memoria reportada por `docker stats`:

```text
Pelican Java 8     ~3.96 GiB
Pelican Java 21    ~1.57 GiB
WhatsApp backend   ~2.80 GiB
PostgreSQL         ~0.07 GiB
Frontend           ~0.03 GiB
--------------------------------
Total              ~8.43 GiB
```

Esto es consistente con la memoria global observada en el Bloque A (~10 GiB usados).

---

# 36. Hallazgo — límites de recursos

Los contenedores administrados por Pelican muestran límites explícitos:

```text
Java 8  → 18.9 GiB
Java 21 → 21 GiB
```

Los contenedores de WhatsApp y PostgreSQL muestran como límite la RAM total del host (`77.51 GiB`), lo que indica que no parecen tener un límite de memoria específico definido a nivel de Docker.

## Implicación para ClubLab

ClubLab sí deberá definir límites explícitos por servicio y por equipo.

Ejemplo conceptual futuro:

```text
frontend  → límite pequeño
api       → límite pequeño
database  → límite moderado
toolbox   → límite pequeño
```

Los valores exactos se decidirán en Fase 2.

---

# 37. Imágenes Docker

Imágenes relevantes observadas:

```text
Pelican yolks:
  java_8
  java_21
  java_25

Pelican installers:
  debian
  java_8
  alpine

Aplicaciones:
  whatsapp-frontend
  whatsapp-backend

Infraestructura:
  postgres:18-bookworm
  nginx:alpine
  node:22-bookworm-slim
  alpine:3.22
```

También existe:

```text
hello-world:latest
```

No se eliminará ninguna imagen durante Fase 0.

---

# 38. Uso de almacenamiento Docker

```text
Images:
  5.31 GB
  730.5 MB reclaimable

Containers:
  ~1.37 MB writable layer

Local Volumes:
  66.38 MB
  1 volumen activo

Build Cache:
  5.33 GB
  3.438 GB reclaimable
```

## Comparación con el manual

El build cache coincide prácticamente con el estado documentado anteriormente:

```text
Manual:
~5.33 GB total
~3.44 GB recuperable

Actual:
5.33 GB total
3.438 GB recuperable
```

No existe presión de almacenamiento que justifique realizar limpieza durante la auditoría.

---

# 39. Hallazgo — contenedor Pelican detenido

Existe:

```text
87d9a146-3fdd-4491-9595-a0c404d9f800
ghcr.io/pelican-eggs/yolks:java_25
Exited (0)
```

Este contenedor NO se considerará basura.

Dado que Wings/Pelican administra servidores y sus ciclos de vida, un contenedor detenido puede representar simplemente un servidor apagado desde el panel.

## Regla

> **Nunca utilizar `docker container prune` ni eliminar contenedores UUID desconocidos sin verificar primero su pertenencia a Pelican/Wings.**

---

# 40. Hallazgo — PostgreSQL central

`postgres-main` continúa:

```text
Up
healthy
5432/tcp sin publicación al host
```

Esto coincide con el diseño anterior.

ClubLab continuará planificándose con una base de datos aislada propia; no se conectará a `postgres-main` salvo que una decisión posterior cambie explícitamente esta regla.

---

# 41. Capacidad preliminar actualizada

Del Bloque A:

```text
RAM total:       77 GiB
RAM disponible:  66 GiB
```

Del Bloque D:

```text
RAM Docker observada: ~8.43 GiB
```

Los servicios del host completan el resto del uso.

## Evaluación

Sigue existiendo margen amplio para ClubLab.

Sin embargo, hay dos servidores Pelican con límites potenciales altos:

```text
18.9 GiB
21 GiB
```

Aunque actualmente no estén consumiendo esos máximos, podrían crecer.

Por tanto, el presupuesto de ClubLab deberá considerar:

> **memoria actualmente libre ≠ memoria garantizada permanentemente.**

La arquitectura deberá reservar una cuota conservadora y limitar cada entorno.

---

# 42. Clasificación de contenedores

## ROJO — producción / infraestructura existente

```text
whatsapp-backend
whatsapp-frontend
postgres-main
c73774b2-bb45-412b-997f-2f2080abade8
2286e7b1-ca54-4540-99ae-21f7ee8193d8
87d9a146-3fdd-4491-9595-a0c404d9f800
```

Ninguno debe reutilizarse ni modificarse para ClubLab.

## VERDE

Todavía no existe ningún contenedor ClubLab.

---

# 43. Convención de nombres recomendada para ClubLab

Para evitar confusiones con Pelican y servicios existentes, todos los recursos propios deberán usar un prefijo consistente.

Ejemplo:

```text
clublab-gateway
clublab-team01-frontend
clublab-team01-api
clublab-team01-db
clublab-team01-toolbox
```

Redes:

```text
clublab-core
clublab-team01
clublab-team02
```

Volúmenes:

```text
clublab-team01-db-data
```

Esto facilita reconocer qué puede administrar el Scenario Manager y qué no debe tocar jamás.

---

# 44. Conclusión del Bloque D

El Bloque D se considera **APROBADO**.

Docker está estable y tiene capacidad suficiente, pero actualmente sirve a tres dominios distintos:

```text
1. aplicación WhatsApp
2. PostgreSQL central
3. Pelican/Wings y servidores de juego
```

ClubLab constituirá un cuarto dominio claramente aislado.

La presencia de contenedores administrados por Pelican refuerza la necesidad de que las futuras herramientas de ClubLab operen únicamente sobre recursos identificados con su propio prefijo o labels.

---

# 45. Estado de la Fase 0

```text
[A] Host + CPU + RAM + almacenamiento   ✅
[B] Red + rutas + puertos + firewall    ✅
[C] Servicios systemd                   ✅
[D] Docker + contenedores               ✅
[E] Redes + volúmenes Docker            ← SIGUIENTE
[F] PostgreSQL
[G] Tailscale + Cloudflare + Caddy
[H] Directorios + backups + monitor
```

---

# 46. Bloque E — Redes y volúmenes Docker

## Estado

**COMPLETADO**

El mapa de redes Docker quedó identificado de forma completa y consistente con los bridges observados en el host.

---

# 47. Inventario de redes Docker

| Red Docker | Driver | Subred | Gateway | IPv6 | Contenedores |
|---|---|---|---|---|---|
| `bridge` | bridge | `172.17.0.0/16` | `172.17.0.1` | No | Ninguno |
| `database-net` | bridge | `172.18.0.0/16` | `172.18.0.1` | No | `whatsapp-backend`, `postgres-main` |
| `whatsapp_app-net` | bridge | `172.19.0.0/16` | `172.19.0.1` | No | `whatsapp-backend`, `whatsapp-frontend` |
| `pelican_nw` | bridge | `172.20.0.0/16` | `172.20.0.1` | Sí | Servidores administrados por Pelican |
| `host` | host | — | — | No | Ninguno |
| `none` | null | — | — | No | Ninguno |

---

# 48. Correspondencia entre bridges del host y redes Docker

El Bloque B mostraba:

```text
docker0          → 172.17.0.1/16
br-baa4f0d2260f → 172.18.0.1/16
br-a9af8457cee6 → 172.19.0.1/16
pelican0         → 172.20.0.1/16
```

Ahora se confirma la correspondencia:

```text
docker0
   ↓
bridge
172.17.0.0/16

br-baa4f0d2260f
   ↓
database-net
172.18.0.0/16

br-a9af8457cee6
   ↓
whatsapp_app-net
172.19.0.0/16

pelican0
   ↓
pelican_nw
172.20.0.0/16
```

---

# 49. Topología Docker actual

```text
                         Docker Engine
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
 database-net          whatsapp_app-net        pelican_nw
 172.18.0.0/16          172.19.0.0/16        172.20.0.0/16
        │                     │                     │
   ┌────┴─────┐          ┌────┴─────┐          ┌────┴─────┐
   │          │          │          │          │          │
postgres   whatsapp   whatsapp   whatsapp    Java 8     Java 21
-main      backend    backend    frontend

                                              Java 25
                                             (detenido)
```

El backend de WhatsApp es el único contenedor que actualmente conecta dos dominios Docker:

```text
database-net
+
whatsapp_app-net
```

Esto le permite comunicarse tanto con PostgreSQL como con el frontend/app network.

---

# 50. Pelican y contenedores detenidos

`pelican_nw` muestra como miembros activos en `docker network inspect`:

```text
2286e7b1-ca54-4540-99ae-21f7ee8193d8
c73774b2-bb45-412b-997f-2f2080abade8
```

El contenedor Java 25 detenido:

```text
87d9a146-3fdd-4491-9595-a0c404d9f800
```

sigue conservando `pelican_nw` en su configuración de `NetworkSettings`.

Esto refuerza que un contenedor detenido de Pelican mantiene metadatos de red aunque no aparezca como endpoint activo del bridge.

---

# 51. Propiedades relevantes de las redes

Todas las redes bridge observadas tienen:

```text
Internal=false
Attachable=false
Scope=local
```

Esto significa que no son redes Docker marcadas como `internal`.

`pelican_nw` es además la única red observada con IPv6 habilitado:

```text
IPv4: 172.20.0.0/16
IPv6: fdba:17c8:6c94::/64
```

---

# 52. Restricciones definitivas de direccionamiento para ClubLab

ClubLab NO debe utilizar ni superponer:

```text
172.17.0.0/16
172.18.0.0/16
172.19.0.0/16
172.20.0.0/16
```

Tampoco debe utilizar:

```text
10.10.100.0/22
```

como red Docker interna, ya que corresponde a la LAN física.

La subred definitiva de ClubLab se seleccionará explícitamente en Fase 2.

## Regla

> No permitir que el diseño de ClubLab dependa de una asignación automática de subred sin comprobar previamente colisiones.

---

# 53. Volúmenes Docker

Actualmente existe un único volumen Docker administrado formalmente por el motor:

```text
postgres_postgres_data
```

Propiedades:

```text
Driver: local
Scope: local
Mountpoint:
/home/docker-data/volumes/postgres_postgres_data/_data
```

## Clasificación

**ROJO — PERSISTENCIA DE PRODUCCIÓN**

No debe:

```text
eliminarse
renombrarse
montarse en ClubLab
inspeccionarse manualmente
reutilizarse
```

---

# 54. Persistencia de Pelican

No aparecen volúmenes Docker adicionales asociados a los servidores Pelican en `docker volume ls`.

Esto significa que su persistencia puede estar implementada mediante:

```text
bind mounts
rutas administradas por Wings
otro mecanismo externo a Docker volumes
```

La Fase 0 no necesita inspeccionar todavía esos datos para ClubLab.

Lo importante es no asumir que:

> "si no aparece en docker volume ls, el contenedor no tiene datos persistentes".

---

# 55. Persistencia de WhatsApp

Tampoco existe un Docker volume específico visible para la aplicación WhatsApp, aparte del volumen de PostgreSQL.

Según la arquitectura histórica del servidor, parte de la persistencia de WhatsApp reside en rutas del proyecto bajo `/home/tulum/apps`.

Esto se comprobará únicamente a nivel de estructura en el Bloque H, sin leer contenido sensible.

---

# 56. Diseño preliminar de redes ClubLab

El resultado de esta auditoría permite establecer una regla de diseño:

Cada equipo deberá tener una red con nombre identificable, por ejemplo:

```text
clublab-team01
clublab-team02
clublab-team03
```

y, si existe infraestructura compartida:

```text
clublab-core
```

El rango IP todavía queda **PENDIENTE DE FASE 2**.

Antes de elegirlo se deberá comprobar también la configuración global de Docker y cualquier `default-address-pools` existente.

---

# 57. Diseño preliminar de volúmenes ClubLab

Los recursos persistentes propios deberán tener nombres inequívocos:

```text
clublab-team01-db-data
clublab-team02-db-data
```

El Scenario Manager solo podrá operar sobre:

```text
clublab-*
```

y nunca sobre recursos que no cumplan esa convención.

Una protección adicional recomendable en Fase 2 será aplicar labels, por ejemplo conceptualmente:

```text
project=clublab
team=team01
managed-by=clublab
```

De esta forma, un reset podría exigir:

```text
prefijo correcto
+
label correcto
```

antes de eliminar o recrear un recurso.

---

# 58. Clasificación de redes

## ROJO — infraestructura existente

```text
bridge
database-net
whatsapp_app-net
pelican_nw
host
none
```

No deben modificarse para ClubLab.

## VERDE — espacio lógico futuro

```text
clublab-core
clublab-teamXX
```

Todavía no existen físicamente.

---

# 59. Mapa de aislamiento resultante

```text
PRODUCCIÓN ACTUAL

database-net
    │
    ├── postgres-main
    └── whatsapp-backend


whatsapp_app-net
    │
    ├── whatsapp-backend
    └── whatsapp-frontend


pelican_nw
    │
    ├── game-server-java8
    ├── game-server-java21
    └── game-server-java25 (apagado)


CLUBLAB FUTURO

clublab-core
    │
    └── servicios compartidos, si se requieren

clublab-team01
    │
    ├── frontend
    ├── api
    ├── db
    └── toolbox

clublab-team02
    │
    ├── frontend
    ├── api
    ├── db
    └── toolbox
```

No habrá conexión entre redes ClubLab y:

```text
database-net
whatsapp_app-net
pelican_nw
```

salvo una decisión explícita posterior, que actualmente no se prevé necesaria.

---

# 60. Conclusión del Bloque E

El Bloque E se considera **APROBADO**.

Ya existe un mapa claro de la infraestructura Docker:

```text
172.17 → bridge por defecto
172.18 → database-net
172.19 → whatsapp_app-net
172.20 → pelican_nw
```

El único volumen Docker formal existente es:

```text
postgres_postgres_data
```

y debe considerarse crítico.

Este bloque permite afirmar que ClubLab puede construirse como un dominio Docker completamente separado sin necesidad de tocar las redes existentes.

---

# 61. Estado de la Fase 0

```text
[A] Host + CPU + RAM + almacenamiento   ✅
[B] Red + rutas + puertos + firewall    ✅
[C] Servicios systemd                   ✅
[D] Docker + contenedores               ✅
[E] Redes + volúmenes Docker            ✅
[F] PostgreSQL                          ← SIGUIENTE
[G] Tailscale + Cloudflare + Caddy
[H] Directorios + backups + monitor
```

---

# 62. Bloque F — PostgreSQL

## Estado

**COMPLETADO**

Se confirmó que `postgres-main` conserva la arquitectura documentada y continúa operando como PostgreSQL central para la aplicación existente.

---

# 63. Estado del contenedor PostgreSQL

```text
Contenedor:      postgres-main
Imagen:          postgres:18-bookworm
Estado:          Up / healthy
Puerto:          5432/tcp solo dentro de Docker
Restart policy:  unless-stopped
Red:             database-net
Volumen:         postgres_postgres_data
Destino volumen: /var/lib/postgresql
```

## Evaluación

La arquitectura coincide con el diseño esperado:

```text
whatsapp-backend
      │
      ▼
 database-net
      │
      ▼
 postgres-main
      │
      ▼
postgres_postgres_data
```

No existe publicación del puerto `5432` al host.

---

# 64. Versión real de PostgreSQL

La imagen utilizada continúa siendo:

```text
postgres:18-bookworm
```

La versión exacta observada dentro del contenedor es:

```text
PostgreSQL 18.6
Debian package: 18.6-1.pgdg12+2
Arquitectura: x86_64
64-bit
```

## Clasificación

**CONFIRMADO / ACTUALIZADO A NIVEL DE PATCH**

El manual identificaba PostgreSQL 18 mediante la imagen, mientras que la auditoría actual permite registrar específicamente la versión `18.6`.

---

# 65. Bases de datos existentes

Se observaron únicamente bases no-template:

| Base | Tamaño aproximado | Clasificación |
|---|---:|---|
| `whatsapp_db` | 8678 kB | Aplicación existente |
| `postgres` | 7662 kB | Base administrativa |

No se consultaron tablas ni datos funcionales.

## Evaluación

El servidor PostgreSQL central tiene actualmente una huella de datos pequeña, pero esto no cambia su clasificación como infraestructura crítica.

---

# 66. Roles PostgreSQL

Roles funcionales relevantes observados:

```text
postgres_admin
whatsapp_user
```

## `postgres_admin`

```text
Superuser:       sí
Create DB:       sí
Create role:     sí
Login:           sí
```

Clasificación:

**ADMINISTRACIÓN — CRÍTICO**

---

## `whatsapp_user`

```text
Superuser:       no
Create DB:       no
Create role:     no
Login:           sí
```

Clasificación:

**ROL DE APLICACIÓN**

El resto de roles listados corresponden a roles internos/predefinidos de PostgreSQL.

---

# 67. Conexión administrativa observada

La consulta devolvió:

```text
current_database = postgres
current_user     = postgres_admin
inet_server_addr = NULL
inet_server_port = NULL
```

## Interpretación

Los campos `inet_server_addr` e `inet_server_port` aparecen vacíos porque `docker exec psql ...` establece la conexión local mediante **socket Unix**, no mediante TCP/IP.

Esto no indica un fallo.

La conectividad TCP utilizada por las aplicaciones sigue ocurriendo a través de `database-net`.

---

# 68. Healthcheck y persistencia

El contenedor reporta:

```text
HealthStatus=healthy
```

y utiliza:

```text
postgres_postgres_data
    ↓
/var/lib/postgresql
```

Esto confirma que la persistencia del PostgreSQL central está correctamente desacoplada del ciclo de vida del contenedor.

---

# 69. Decisión arquitectónica para ClubLab

A partir de la Fase 0 queda establecida como **decisión base recomendada**:

> **ClubLab no utilizará `postgres-main`, `whatsapp_db`, `postgres_admin` ni `whatsapp_user`.**

ClubLab tendrá PostgreSQL propio.

La forma exacta se decidirá en Fase 2 entre opciones como:

```text
A. Un PostgreSQL compartido exclusivo de ClubLab
B. Una base por equipo dentro de un PostgreSQL ClubLab
C. Un PostgreSQL aislado por equipo
```

Para la experiencia educativa inicial, la opción C puede aportar mayor aislamiento y facilitar escenarios de fallo, pero todavía no se adopta como decisión definitiva.

---

# 70. Razones para no compartir PostgreSQL de producción

Compartir `postgres-main` introduciría riesgos innecesarios:

```text
errores de permisos
borrados accidentales
migraciones incorrectas
carga inesperada
confusión entre bases
acceso de estudiantes a infraestructura real
dependencia de credenciales productivas
dificultad para resetear escenarios
```

Además, uno de los objetivos de ClubLab es permitir:

```text
romper
reiniciar
resetear
recrear
corromper escenarios deliberadamente
```

Eso es incompatible con una base productiva compartida.

---

# 71. Clasificación PostgreSQL

## ROJO — no tocar desde ClubLab

```text
postgres-main
postgres_postgres_data
database-net
postgres_admin
whatsapp_user
whatsapp_db
postgres
```

## VERDE — futuro

```text
clublab-db
clublab-teamXX-db
clublab-teamXX-db-data
```

Todavía no existen.

---

# 72. Implicación para el Scenario Manager

El futuro sistema de escenarios deberá ser capaz de hacer operaciones destructivas únicamente sobre recursos ClubLab.

Ejemplos válidos futuros:

```text
vaciar base ClubLab
recrear base ClubLab
restaurar seed
romper credenciales ClubLab
detener PostgreSQL ClubLab
```

Ejemplos prohibidos:
```text
tocar postgres-main
tocar postgres_postgres_data
usar postgres_admin
usar whatsapp_db
```

---

# 73. Conclusión del Bloque F

El Bloque F se considera **APROBADO**.

Se confirmó:

```text
PostgreSQL 18.6
postgres-main healthy
database-net
restart unless-stopped
persistencia en volumen dedicado
whatsapp_db activa
postgres_admin como superusuario
whatsapp_user como rol de aplicación
```

No se detectó ninguna necesidad de modificar la infraestructura actual.

ClubLab deberá usar su propia capa de base de datos para mantener aislamiento total y permitir escenarios destructivos seguros.

---

# 74. Estado de la Fase 0

```text
[A] Host + CPU + RAM + almacenamiento   ✅
[B] Red + rutas + puertos + firewall    ✅
[C] Servicios systemd                   ✅
[D] Docker + contenedores               ✅
[E] Redes + volúmenes Docker            ✅
[F] PostgreSQL                          ✅
[G] Tailscale + Cloudflare + Caddy      ← SIGUIENTE
[H] Directorios + backups + monitor
```

---

# 75. Bloque G — Tailscale, Cloudflare y Caddy

## Estado

**COMPLETADO CON UNA EVIDENCIA PENDIENTE MENOR**

Se confirmó la topología real de publicación privada y pública del servidor.

La única evidencia que no se recuperó en este bloque fue la URL `trycloudflare.com` actual, porque no apareció dentro de las últimas 100 líneas consultadas del journal. Esto no impide confirmar que el Quick Tunnel está activo y apunta al frontend de WhatsApp.

---

# 76. Tailscale

## Estado actual

```text
Nodo Tulum:
100.115.55.35
fd7a:115c:a1e0::6d01:37d9

Nombre:
localhost-0
```

También se observó un cliente Windows conectado al mismo tailnet.

## Advertencia conocida

Tailscale continúa reportando:

```text
System DNS config not ideal.
/etc/resolv.conf overwritten.
```

Este warning ya estaba documentado previamente y no impide actualmente el funcionamiento observado.

No se realizará ninguna modificación DNS durante Fase 0.

---

# 77. Tailscale Serve

Actualmente existen tres publicaciones privadas diferentes:

```text
https://localhost-0.tail4666b9.ts.net
        │
        └── http://127.0.0.1:8080
            └── WhatsApp frontend


https://localhost-0.tail4666b9.ts.net:8443
        │
        └── http://127.0.0.1:8090
            └── Caddy
                └── Pelican Panel


https://localhost-0.tail4666b9.ts.net:8444
        │
        └── http://127.0.0.1:8081
            └── Pelican Wings API
```

Estas publicaciones son:

```text
tailnet only
```

por lo que no constituyen exposición pública convencional a Internet.

---

# 78. Mapa privado actual

```text
                         TAILNET
                            │
              localhost-0.tail4666b9.ts.net
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
      :443                :8443               :8444
        │                   │                   │
        ▼                   ▼                   ▼
127.0.0.1:8080      127.0.0.1:8090      127.0.0.1:8081
        │                   │                   │
 WhatsApp Frontend        Caddy              Wings
                            │
                            ▼
                      Pelican Panel
```

Adicionalmente:

```text
100.115.55.35:2022
        │
        ▼
Pelican Wings SFTP
```

---

# 79. Cloudflare Quick Tunnel

Servicio:

```text
cloudflared-quick.service
```

Estado:

```text
enabled
active (running)
```

Comando ejecutado por systemd:

```text
/usr/local/bin/cloudflared tunnel
  --no-autoupdate
  --url http://127.0.0.1:8080
```

Por tanto, la publicación pública existente sigue apuntando a:

```text
127.0.0.1:8080
```

que corresponde al frontend de WhatsApp.

---

# 80. URL pública de Cloudflare

El comando utilizado:

```text
journalctl -u cloudflared-quick -n 100
| grep trycloudflare.com
```

no devolvió una URL.

## Interpretación

Esto no significa que el túnel esté inactivo.

El servicio está:

```text
active (running)
```

y los logs muestran conexiones registradas correctamente después de reintentos.

La URL probablemente fue emitida durante el arranque inicial y ya no se encuentra dentro de la ventana de 100 líneas consultada.

## Estado

```text
Quick Tunnel: CONFIRMADO
Destino: CONFIRMADO
URL actual: PENDIENTE DE RECUPERAR
```

---

# 81. Eventos recientes de cloudflared

Se observaron eventos temporales:

```text
failed to run datagram handler
failed to accept incoming stream
failed to serve tunnel connection
retrying connection
registered tunnel connection
```

La secuencia indica que cloudflared experimentó una interrupción/transición y posteriormente volvió a registrar la conexión.

No se observó evidencia de que el servicio permanezca caído.

## Clasificación

```text
INCIDENCIA TRANSITORIA
NO ACCIÓN DURANTE FASE 0
```

---

# 82. Versión de cloudflared

Los logs indican:

```text
Versión instalada: 2026.8.2
Versión más reciente reportada: 2026.9.1
```

## Estado

**ACTUALIZACIÓN DISPONIBLE**

No se actualizará durante esta auditoría.

Cualquier actualización futura deberá realizarse bajo una ventana controlada y con posibilidad de verificar/restaurar el túnel.

---

# 83. Caddy

Servicio:

```text
caddy.service
```

Estado:

```text
enabled
active (running)
```

Consumo observado:

```text
RAM actual: ~77 MiB
RAM pico:   ~82 MiB
```

Listeners:

```text
127.0.0.1:8090
127.0.0.1:2019
```

El puerto `2019` corresponde a la API administrativa local de Caddy.

---

# 84. Configuración actual de Caddy

El Caddyfile define un único sitio:

```text
:8090
```

con bind exclusivo:

```text
127.0.0.1
```

Por tanto, Caddy no escucha directamente sobre la LAN.

Root:

```text
/var/www/pelican/public
```

Procesamiento PHP:

```text
unix//run/php-fpm/pelican.sock
```

El sitio corresponde claramente al **Panel Pelican**.

También se observaron:

```text
zstd/gzip
file_server
límite de body 100 MB
headers de seguridad
timeouts PHP elevados
```

La configuración fue validada mediante:

```text
caddy validate --config /etc/caddy/Caddyfile
```

Resultado:

```text
Valid configuration
```

---

# 85. Arquitectura Pelican actual

La infraestructura Pelican puede representarse así:

```text
Usuario autorizado por Tailscale
            │
            ▼
https://localhost-0...:8443
            │
      Tailscale Serve
            │
            ▼
     127.0.0.1:8090
            │
          Caddy
            │
            ▼
    /var/www/pelican/public
            │
          PHP-FPM
            │
       Pelican Panel
            │
            ▼
         Wings
            │
      Docker Engine
            │
       Game Servers
```

Wings además expone:

```text
API:
Tailscale :8444
→ 127.0.0.1:8081

SFTP:
100.115.55.35:2022
```

---

# 86. Arquitectura WhatsApp actual

```text
                    WhatsApp Frontend
                    127.0.0.1:8080
                         ▲      ▲
                         │      │
                         │      │
                 Tailscale     Cloudflare
                    Serve       Quick Tunnel
                     :443           │
                         \           /
                          \         /
                           usuarios
```

El frontend dispone por tanto de dos vías:

```text
privada → Tailscale
pública → Cloudflare Quick Tunnel
```

El backend continúa separado en:

```text
127.0.0.1:3500
```

y no se publica directamente mediante estos mecanismos.

---

# 87. Clasificación de componentes de publicación

## ROJO — no modificar desde ClubLab

```text
Tailscale Serve :443
Tailscale Serve :8443
Tailscale Serve :8444
Wings SFTP :2022
Cloudflare Quick Tunnel actual
Caddy :8090 / Pelican
```

Son rutas productivas o de infraestructura existentes.

---

## AMARILLO — tecnología potencialmente reutilizable

```text
Tailscale Serve
Caddy
Cloudflare
```

La tecnología puede reutilizarse conceptualmente, pero no las rutas/configuraciones existentes.

La Fase 2 decidirá si ClubLab necesita:

```text
su propio path
su propio puerto
su propio hostname
su propio servicio Serve
su propio reverse proxy
o publicación únicamente dentro de LAN
```

---

# 88. Implicación para ClubLab

Ya no es necesario imaginar la publicación desde cero: Tulum dispone de mecanismos probados para exposición privada y pública.

Sin embargo, la primera versión de ClubLab deberá priorizar:

```text
aislamiento
simplicidad
estabilidad
mínima exposición
```

Una hipótesis para Fase 2 será estudiar:

```text
ClubLab → Caddy/servicio local dedicado → Tailscale Serve
```

o acceso LAN directo durante la clase.

Cloudflare no será asumido como requisito para la primera sesión.

---

# 89. Puertos confirmados de publicación

```text
Tailscale:
443
8443
8444

Wings:
2022

Locales:
8080   WhatsApp frontend
8081   Wings
8090   Caddy / Pelican
2019   Caddy admin API
20241  cloudflared local
```

Estos puertos quedan reservados para infraestructura actual.

---

# 90. Conclusión del Bloque G

El Bloque G se considera **APROBADO**.

La topología actual queda claramente separada:

```text
WhatsApp
├── Tailscale Serve :443
└── Cloudflare Quick Tunnel

Pelican Panel
└── Tailscale Serve :8443
    └── Caddy :8090

Pelican Wings
├── Tailscale Serve :8444
│   └── Wings :8081
└── SFTP :2022
```

Caddy está activo, su configuración es válida y sirve exclusivamente el Panel Pelican en la configuración observada.

Queda únicamente como evidencia menor pendiente recuperar la URL pública actual del Quick Tunnel.

---

# 91. Estado de la Fase 0

```text
[A] Host + CPU + RAM + almacenamiento   ✅
[B] Red + rutas + puertos + firewall    ✅
[C] Servicios systemd                   ✅
[D] Docker + contenedores               ✅
[E] Redes + volúmenes Docker            ✅
[F] PostgreSQL                          ✅
[G] Tailscale + Cloudflare + Caddy      ✅
[H] Directorios + backups + monitor     ← ÚLTIMO BLOQUE
```

---

# 92. Bloque H — Directorios, respaldos, cron y monitorización

## Estado

**COMPLETADO**

Con este bloque se cierra la auditoría técnica de Fase 0.

---

# 93. Organización real bajo `/home/tulum`

Directorios principales confirmados:

```text
/home/tulum
├── apps
├── infra
├── scripts
└── backups
```

Permisos observados:

```text
/home/tulum            700
/home/tulum/apps       755
/home/tulum/infra      755
/home/tulum/scripts    755
/home/tulum/backups    700
```

Esto mantiene una separación razonable entre proyectos, infraestructura, scripts y respaldos.

---

# 94. Aplicaciones existentes

Actualmente existen:

```text
/home/tulum/apps/
├── minecraft
│   └── wings
└── whatsapp
    ├── backend
    └── frontend
```

## Clasificación

```text
/home/tulum/apps/whatsapp   → PRODUCCIÓN
/home/tulum/apps/minecraft  → INFRAESTRUCTURA EXISTENTE
```

No deben reutilizarse para ClubLab.

---

# 95. Infraestructura existente

Actualmente:

```text
/home/tulum/infra/
├── minecraft
│   ├── docs
│   ├── networking
│   ├── panel
│   ├── playit
│   └── wings
└── postgres
```

Esto confirma que la infraestructura de Minecraft/Pelican fue incorporada después de la fotografía original del servidor.

## Implicación

La estructura futura de ClubLab puede seguir la misma convención:

```text
/home/tulum/apps/clublab
/home/tulum/infra/clublab
```

pero todavía no se crearán durante Fase 0.

---

# 96. Scripts administrativos

Se observaron:

```text
backup-whatsapp-db.sh
backup-whatsapp-session.sh
monitor-whatsapp.sh
```

Todos están orientados actualmente a WhatsApp.

ClubLab deberá tener scripts propios y no reutilizar estos archivos.

Una estructura futura coherente sería:

```text
/home/tulum/scripts/clublab/
```

o mantener los scripts dentro del repositorio de ClubLab y exponer únicamente wrappers administrativos necesarios.

La decisión final se tomará durante la arquitectura técnica.

---

# 97. Estructura de respaldos

Actualmente existen:

```text
/home/tulum/backups/
├── minecraft
│   ├── configs
│   ├── panel
│   └── servers
├── postgres
├── system-baselines
│   └── 20260902-123305-pre-minecraft
└── whatsapp-session
```

Esto confirma que ya existe una política de conservar:

```text
respaldos de aplicaciones
respaldos de configuración
baselines del sistema
```

## Implicación para ClubLab

Si ClubLab almacena estado persistente relevante deberá utilizar un namespace propio:

```text
/home/tulum/backups/clublab
```

Sin embargo, para los entornos de estudiantes puede ser preferible que el estado sea **desechable y reproducible desde seeds**, reduciendo la necesidad de backups por equipo.

---

# 98. Respaldos PostgreSQL

Los respaldos observados de `whatsapp_db` tienen:

```text
Tamaño aproximado: 31 KiB
Hora:              03:15
Frecuencia:        diaria según cron
```

Se observan archivos fechados:

```text
04 sep
05 sep
06 sep
07 sep
11 sep
12 sep
13 sep
14 sep
15 sep
16 sep
```

## Observación

No aparecen respaldos fechados `08`, `09` o `10` de septiembre dentro de los diez archivos más recientes.

La causa no se determinó en esta auditoría.

Puede corresponder, por ejemplo, a una indisponibilidad previa del servidor o a otra intervención, pero no debe inferirse una causa sin evidencia.

## Estado

```text
BACKUP ACTUAL: FUNCIONANDO
HUECO HISTÓRICO 08–10 SEP: DOCUMENTADO / NO INVESTIGADO
```

---

# 99. Respaldos de sesión WhatsApp

Los respaldos observados siguen el horario:

```text
03:30 diario
```

Tamaños recientes:

```text
04 sep   71 MiB
05 sep   77 MiB
06 sep   83 MiB
07 sep   89 MiB
11 sep   74 MiB
12 sep   84 MiB
13 sep   90 MiB
14 sep   97 MiB
15 sep  103 MiB
16 sep  110 MiB
```

También se observa el mismo hueco de fechas:

```text
08–10 septiembre
```

## Tendencia

Los backups de sesión están creciendo.

Entre el 11 y el 16 de septiembre:

```text
74 MiB → 110 MiB
```

No representa presión inmediata de almacenamiento, pero conviene vigilar su crecimiento y política de retención a futuro.

---

# 100. Cron actual

Crontab del usuario `tulum`:

```cron
15 3 * * * /home/tulum/scripts/backup-whatsapp-db.sh >> /home/tulum/backups/postgres/backup.log 2>&1

30 3 * * * /home/tulum/scripts/backup-whatsapp-session.sh >> /home/tulum/backups/whatsapp-session/backup.log 2>&1

*/5 * * * * /home/tulum/scripts/monitor-whatsapp.sh
```

## Mapa

```text
03:15
  └── Backup PostgreSQL WhatsApp

03:30
  └── Backup sesión WhatsApp

Cada 5 minutos
  └── Monitor WhatsApp
```

No se detectaron timers systemd relevantes para backups o monitorización en el filtro ejecutado.

---

# 101. Monitorización WhatsApp

Durante la ventana observada, el monitor registra repetidamente:

```text
WARN: WhatsApp status = qr_required
OK: servicios principales funcionando
```

La comprobación ocurre cada cinco minutos.

## Interpretación

Los servicios técnicos principales están operativos, pero el estado funcional de WhatsApp requiere autenticación mediante QR.

Esto es una incidencia existente de WhatsApp y no un problema de ClubLab.

## Estado

```text
SERVICIOS: OK
WHATSAPP SESSION: qr_required
```

No se realizará ninguna corrección dentro de Fase 0.

---

# 102. Almacenamiento de Pelican

Se confirmó:

```text
/var/www/pelican → 234 MiB
```

No se obtuvo una medida para:

```text
/var/lib/pelican
```

por lo que no se afirmará que esa ruta exista o no exista.

La carpeta web de Pelican queda clasificada como infraestructura existente.

---

# 103. Uso de directorios principales

```text
/home/tulum/apps      27 GiB
/home/tulum/infra     80 KiB
/home/tulum/scripts   12 KiB
/home/tulum/backups   2.0 GiB
```

## Interpretación

La mayor parte del uso bajo `/home/tulum` se concentra actualmente en:

```text
apps
```

Con `/home` alrededor de 1.3 TiB disponible, todavía existe margen amplio para ClubLab.

---

# 104. Cloudflare Quick Tunnel — URL recuperada

Se recuperó la URL pública actual:

```text
https://queens-congressional-architects-economic.trycloudflare.com
```

## Clasificación

**TEMPORAL**

Es una URL de Quick Tunnel y no debe considerarse una dirección estable o contractual.

Su presencia completa la evidencia pendiente del Bloque G.

---

# 105. Bloque H — conclusión

El Bloque H se considera **APROBADO**.

Se confirmó:

```text
estructura de aplicaciones
estructura de infraestructura
scripts administrativos
respaldos
cron
monitorización
rutas Minecraft/Pelican
uso de almacenamiento
URL Quick Tunnel actual
```

Con esto se completa toda la Fase 0.

---

# 106. Matriz final de cambios respecto al manual base

| Componente | Estado base anterior | Estado auditado | Resultado |
|---|---|---|---|
| Servidor | Dell PowerEdge R440 | Dell PowerEdge R440 | CONFIRMADO |
| SO | CentOS Stream 10 | CentOS Stream 10 | CONFIRMADO |
| Kernel | `6.12.0-170` | `6.12.0-264` | CAMBIÓ |
| CPU | 32 lógicos | 32 lógicos | CONFIRMADO |
| RAM | 77 GiB | 77 GiB | CONFIRMADO |
| `/` | ~20% usado | 24% usado | CAMBIÓ |
| `/home` | ~2% usado | 5% usado | CAMBIÓ |
| Hostname | sin estático | sin estático | CONFIRMADO |
| LAN | `10.10.100.41/22` | `10.10.100.41/22` | CONFIRMADO |
| Gateway | `10.10.100.1` | `10.10.100.1` | CONFIRMADO |
| Tailscale | `100.115.55.35` | `100.115.55.35` | CONFIRMADO |
| Docker | 29.7.2 | 29.7.2 | CONFIRMADO |
| Docker root | `/home/docker-data` | `/home/docker-data` | CONFIRMADO |
| PostgreSQL | 18 / central | 18.6 / central | CONFIRMADO |
| `database-net` | existente | `172.18.0.0/16` | CONFIRMADO |
| `whatsapp_app-net` | existente | `172.19.0.0/16` | CONFIRMADO |
| Pelican/Wings | no presente en foto base | activo | NUEVO |
| `pelican_nw` | no presente | `172.20.0.0/16` | NUEVO |
| Playit | no presente | activo | NUEVO |
| Caddy | inactivo | activo | CAMBIÓ |
| Caddy destino | — | Pelican Panel | NUEVO |
| Tailscale :443 | WhatsApp | WhatsApp | CONFIRMADO |
| Tailscale :8443 | — | Pelican Panel | NUEVO |
| Tailscale :8444 | — | Wings API | NUEVO |
| Wings SFTP :2022 | — | activo | NUEVO |
| Cloudflare Quick Tunnel | WhatsApp | WhatsApp | CONFIRMADO |
| Backups Minecraft | no presentes | presentes | NUEVO |
| Baseline pre-Minecraft | no presente | presente | NUEVO |
| Monitor WhatsApp | cada 5 min | cada 5 min | CONFIRMADO |

---

# 107. Mapa final del servidor

```text
                              INTERNET
                                 │
                         Cloudflare Quick
                                 │
                                 ▼
                         127.0.0.1:8080
                                 │
                         WhatsApp Frontend
                                 │
                                 │
─────────────────────────────────┼──────────────────────────────────

                              TAILNET
                                 │
          ┌──────────────────────┼───────────────────────┐
          │                      │                       │
        :443                   :8443                   :8444
          │                      │                       │
          ▼                      ▼                       ▼
      WhatsApp                 Caddy                   Wings
      Frontend                   │                       │
                                 ▼                       │
                            Pelican Panel                │
                                                         │
                                   SFTP :2022 ◄──────────┘
─────────────────────────────────┼──────────────────────────────────

                           DOCKER ENGINE
                                 │
          ┌──────────────────────┼───────────────────────┐
          │                      │                       │
   database-net           whatsapp_app-net          pelican_nw
   172.18/16              172.19/16                172.20/16
          │                      │                       │
   postgres-main          frontend/backend          game servers
          │
 postgres_postgres_data

─────────────────────────────────┼──────────────────────────────────

                           HOST STORAGE
                                 │
                     /home/docker-data
                                 │
                      gestionado por Docker

                          /home/tulum
                    ┌────────┼────────┐
                   apps     infra    backups
                    │         │         │
              WhatsApp    Postgres   WhatsApp
              Minecraft   Minecraft  Minecraft
```

---

# 108. Clasificación final ROJO / AMARILLO / VERDE

## ROJO — no tocar desde ClubLab

```text
SERVICIOS
docker.service
wings.service
pelican-queue.service
playit.service
cloudflared-quick.service
sshd.service
crond.service
cockpit.socket

DOCKER
postgres-main
whatsapp-backend
whatsapp-frontend
contenedores UUID de Pelican
database-net
whatsapp_app-net
pelican_nw
postgres_postgres_data

POSTGRESQL
postgres_admin
whatsapp_user
whatsapp_db
base postgres productiva

RED
eno1
NetworkManager
rutas actuales
firewall productivo
Tailscale Serve actual
puertos 443 / 8443 / 8444 / 2022

ARCHIVOS
/home/docker-data
/home/tulum/apps/whatsapp
/home/tulum/apps/minecraft
/home/tulum/infra/postgres
/home/tulum/infra/minecraft
/home/tulum/backups existentes
/var/www/pelican
```

---

## AMARILLO — tecnología o recurso compartible con diseño explícito

```text
CPU del host
RAM del host
/home
Docker Engine como plataforma
Tailscale como tecnología
Caddy como tecnología
Cloudflare como tecnología
LAN del laboratorio
/home/tulum/apps como directorio padre
/home/tulum/infra como directorio padre
/home/tulum/backups como directorio padre
```

Compartible no significa modificar la infraestructura existente.

---

## VERDE — namespace futuro de ClubLab

Todavía no existe físicamente, pero queda reservado conceptualmente:

```text
/home/tulum/apps/clublab
/home/tulum/infra/clublab
/home/tulum/backups/clublab

clublab-*
clublab-team01-*
clublab-team02-*
...

redes clublab-*
volúmenes clublab-*
credenciales exclusivas ClubLab
PostgreSQL exclusivo ClubLab
```

---

# 109. Recursos disponibles para ClubLab

Estado observado:

```text
CPU:               32 CPU lógicos
Load:              muy bajo durante auditoría
RAM total:         77 GiB
RAM disponible:    ~66 GiB
/home disponible:  ~1.3 TiB
Swap usada:        0
```

## Reserva conservadora

No toda la RAM libre puede considerarse garantizada porque Pelican tiene actualmente dos servidores con límites combinados cercanos a:

```text
~40 GiB
```

aunque su uso real sea mucho menor.

Por ello, para el piloto de ClubLab se recomienda diseñar inicialmente para un presupuesto total aproximado de:

```text
8–12 GiB RAM
```

con límites estrictos.

Esto permitiría estudiar cómodamente un piloto de aproximadamente:

```text
4–6 equipos
```

con entornos ligeros.

Esta cifra es una **capacidad de diseño preliminar**, no un benchmark final.

Antes de una clase real deberá hacerse un ensayo de carga.

---

# 110. Presupuesto preliminar por equipo

Hipótesis inicial para Fase 2:

| Componente | RAM objetivo preliminar |
|---|---:|
| Frontend | 64–128 MiB |
| API | 256–512 MiB |
| PostgreSQL | 384–512 MiB |
| Toolbox | 128–256 MiB |
| Margen | 128–256 MiB |
| **Total por equipo** | **~1–1.6 GiB** |

Por ejemplo:

```text
4 equipos → ~4–6.5 GiB
6 equipos → ~6–10 GiB
```

La arquitectura deberá imponer límites explícitos de CPU y RAM.

---

# 111. Restricciones obligatorias para la arquitectura ClubLab

La Fase 2 deberá respetar:

1. No utilizar `postgres-main`.
2. No utilizar redes Docker existentes.
3. No utilizar volúmenes existentes.
4. No entregar Docker socket del host a estudiantes.
5. No añadir estudiantes al grupo Docker.
6. No dar acceso SSH al usuario `tulum`.
7. No publicar PostgreSQL al host o Internet.
8. No montar `/home/tulum`, `/home/docker-data` ni otras rutas productivas dentro de entornos de estudiantes.
9. No reutilizar los puertos productivos identificados.
10. Todo recurso destructible debe llevar prefijo y labels ClubLab.
11. Un equipo debe poder romper su entorno sin afectar otro equipo.
12. Debe existir un reset reproducible.
13. El instructor debe poder recuperar cualquier equipo rápidamente.
14. Las credenciales del laboratorio deben ser exclusivas y desechables.
15. Los escenarios de fallo nunca deben actuar sobre recursos ajenos a ClubLab.

---

# 112. Decisiones pendientes para Fase 2

Quedan deliberadamente abiertas:

## Acceso de integrantes

Evaluar:

```text
LAN
Tailscale
gateway propio
combinación
```

La primera versión debe priorizar simplicidad y mínima exposición.

---

## Base de datos

Elegir entre:

```text
PostgreSQL ClubLab compartido
base independiente por equipo
contenedor PostgreSQL por equipo
```

---

## Subred Docker

No utilizar:

```text
172.17.0.0/16
172.18.0.0/16
172.19.0.0/16
172.20.0.0/16
10.10.100.0/22
```

La subred de ClubLab deberá seleccionarse explícitamente.

---

## Reverse proxy

Definir si:

```text
ClubLab usa gateway propio
ClubLab reutiliza Caddy con configuración separada
ClubLab usa acceso LAN directo
```

No modificar el sitio Pelican existente.

---

## Persistencia

Determinar qué datos:

```text
son permanentes
se generan desde seeds
se resetean por misión
requieren backup
```

---

# 113. Riesgos identificados

## R1 — Error humano sobre Docker productivo

Mitigación:

```text
prefijo clublab-*
labels obligatorios
scripts restrictivos
sin prune global
```

---

## R2 — Uso excesivo de RAM por servidores Pelican

Mitigación:

```text
límites ClubLab
ensayo antes de clase
presupuesto conservador
```

---

## R3 — Confusión de redes

Mitigación:

```text
subred explícita ClubLab
documentación de IPAM
sin conexión a redes productivas
```

---

## R4 — Exposición innecesaria de estudiantes

Mitigación:

```text
no SSH al host
no Docker socket
toolbox aislado
puertos mínimos
```

---

## R5 — Dependencia de URL temporal Cloudflare

Mitigación:

```text
no hacer del Quick Tunnel un requisito del laboratorio
```

---

## R6 — Recuperación lenta durante clase

Mitigación:

```text
seeds
reset automático
scenario manager
entornos independientes
```

---

# 114. Observaciones operativas fuera de ClubLab

La auditoría encontró dos aspectos de producción que quedan documentados pero fuera del alcance de este proyecto:

```text
WhatsApp reporta qr_required de forma continua.
Existen huecos de backup entre el 08 y 10 de septiembre.
```

También:

```text
cloudflared reporta una versión más reciente disponible.
Tailscale reporta advertencia sobre configuración DNS.
```

Ninguno bloquea el diseño de ClubLab.

---

# 115. Conclusión de viabilidad

## Resultado

**CLUBLAB ES VIABLE EN TULUM.**

La infraestructura actual dispone de:

```text
capacidad de CPU
capacidad de RAM
almacenamiento
Docker
red privada
mecanismos de publicación
estructura administrativa estable
```

y permite añadir ClubLab sin modificar las aplicaciones existentes.

La condición fundamental es construirlo como un dominio nuevo y aislado.

---

# 116. Arquitectura conceptual permitida después de Fase 0

```text
                         TULUM
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
   PRODUCCIÓN          PELICAN            CLUBLAB
        │                  │                  │
   NO TOCAR            NO TOCAR          AISLADO
                                             │
                           ┌─────────────────┼─────────────────┐
                           │                 │                 │
                       team01            team02            teamXX
                           │                 │                 │
                      Front/API/DB       Front/API/DB       ...
                       /Toolbox           /Toolbox
```

ClubLab no requiere compartir base de datos, red o ciclo de vida con ninguno de los dominios existentes.

---

# 117. Resultado final de Fase 0

```text
[A] Host + CPU + RAM + almacenamiento   ✅
[B] Red + rutas + puertos + firewall    ✅
[C] Servicios systemd                   ✅
[D] Docker + contenedores               ✅
[E] Redes + volúmenes Docker            ✅
[F] PostgreSQL                          ✅
[G] Tailscale + Cloudflare + Caddy      ✅
[H] Directorios + backups + monitor     ✅
```

# FASE 0 — COMPLETADA

---

# 118. Entregables cerrados

Principal:

```text
D00_Estado_Base_Servidor_ClubLab.md
```

El documento contiene:

```text
estado real
diferencias respecto al manual
mapa de infraestructura
mapa Docker
mapa de redes
mapa de publicación
recursos disponibles
clasificación ROJO/AMARILLO/VERDE
riesgos
restricciones de arquitectura
decisiones pendientes
conclusión de viabilidad
```

---

# 119. Próximo paso oficial

Con la infraestructura ya congelada documentalmente, el siguiente trabajo es:

# FASE 1 — Diseño pedagógico de ClubLab #01

En esa fase se definirá con precisión:

```text
qué experimentarán los integrantes
qué descubrirán
qué misiones harán
qué herramientas tocarán
qué fallos investigarán
qué pistas recibirán
qué evidencia debe producir cada misión
cómo se distribuyen las dos horas
```

La arquitectura técnica definitiva se desarrollará después, utilizando las restricciones obtenidas en esta auditoría.