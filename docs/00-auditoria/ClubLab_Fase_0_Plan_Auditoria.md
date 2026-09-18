# ClubLab — Plan de Fase 0
## Auditoría y congelación del estado actual del servidor Tulum

**Proyecto:** ClubLab v1  
**Fase:** 0  
**Nombre:** Auditoría y congelación del estado actual  
**Objetivo:** conocer el estado real del servidor antes de diseñar o desplegar ClubLab  
**Tipo de trabajo:** inspección y documentación  
**Cambios permitidos:** ninguno  
**Resultado principal:** `D00_Estado_Base_Servidor_ClubLab.md`

---

# 1. Propósito de la Fase 0

La infraestructura documentada del servidor Tulum corresponde a un estado conocido de agosto de 2026. Antes de diseñar redes, puertos, contenedores, publicación, bases de datos o accesos para ClubLab, se debe comprobar el estado real.

Esta fase responde cuatro preguntas:

1. **¿Qué existe actualmente en Tulum?**
2. **¿Qué recursos podemos utilizar sin interferir con producción?**
3. **¿Qué componentes no debemos tocar?**
4. **¿Qué restricciones reales debe respetar la arquitectura de ClubLab?**

La Fase 0 no instala, elimina, reinicia ni reconfigura ningún servicio.

---

# 2. Principio de operación

Durante esta fase se trabaja bajo la regla:

> **Observar, registrar y comparar. No corregir todavía.**

Si se descubre una configuración incorrecta, desactualizada o insegura:

```text
DESCUBRIR
   ↓
DOCUMENTAR
   ↓
CLASIFICAR
   ↓
NO MODIFICAR
```

La corrección se planificará posteriormente y solo si es necesaria para ClubLab o para la administración del servidor.

---

# 3. Referencia base

El manual del servidor documenta, entre otros componentes:

```text
Servidor físico Dell PowerEdge R440
CentOS Stream 10
Docker Engine
PostgreSQL central
Tailscale
Cloudflare Tunnel
SSH
firewalld
Cockpit
respaldos
monitorización
```

También documenta la separación general:

```text
Acceso externo
      │
      ▼
Servidor Tulum
      │
  Docker Engine
   /    |     \
Frontend Backend PostgreSQL
```

ClubLab deberá integrarse sin asumir que esa fotografía sigue siendo idéntica.

---

# 4. Reglas de seguridad de la auditoría

## 4.1 Permitido

Solo operaciones de consulta:

```text
consultar estado
listar recursos
consultar puertos
consultar rutas
consultar redes Docker
consultar volúmenes
consultar uso de CPU/RAM/disco
consultar servicios
consultar healthchecks
consultar metadatos de PostgreSQL
```

---

## 4.2 Prohibido durante Fase 0

No ejecutar:

```bash
docker stop
docker start
docker restart
docker rm
docker rmi
docker compose down
docker compose down -v
docker volume rm
docker network rm
docker system prune
docker builder prune

sudo systemctl restart ...
sudo systemctl stop ...
sudo systemctl disable ...
sudo systemctl enable ...

sudo firewall-cmd --add-...
sudo firewall-cmd --remove-...
sudo firewall-cmd --reload

nmcli connection modify ...
sudo systemctl restart NetworkManager

tailscale down
tailscale up
tailscale serve reset

dnf update
dnf upgrade
```

Tampoco:

```text
editar archivos
cambiar permisos
modificar cron
crear usuarios
crear bases de datos
crear redes Docker
crear volúmenes
publicar puertos
instalar paquetes
```

---

# 5. Precauciones sobre secretos

Durante la auditoría no deben copiarse a documentación o chat:

```text
contraseñas
tokens
JWT secrets
API keys
contenido de llaves SSH
cookies de sesión
variables de entorno sensibles
credenciales de PostgreSQL
credenciales de Cloudflare
credenciales de Tailscale
```

Evitar comandos como:

```bash
docker inspect <contenedor>
docker exec <contenedor> env
printenv
cat .env
cat ~/.ssh/*
```

cuando puedan exponer secretos.

Si se necesita inspeccionar un contenedor, se utilizarán formatos concretos que extraigan solo metadatos necesarios.

---

# 6. Evidencia de la auditoría

Cada bloque debe registrar:

```text
Fecha:
Hora:
Comando:
Resultado:
Estado:
Observación:
Diferencia respecto al manual:
Impacto potencial en ClubLab:
```

Estados permitidos:

```text
CONFIRMADO
CAMBIÓ
NO ENCONTRADO
NUEVO
REQUIERE REVISIÓN
```

---

# 7. Subfase 0.1 — Identidad del host y sistema operativo

## Objetivo

Confirmar qué equipo estamos auditando y su software base.

## Comandos

```bash
echo "===== HOST ====="
hostnamectl

echo
echo "===== KERNEL ====="
uname -a

echo
echo "===== RELEASE ====="
cat /etc/os-release

echo
echo "===== UPTIME ====="
uptime
```

## Registrar

```text
hostname
sistema operativo
versión
kernel
arquitectura
tiempo encendido
```

## Preguntas

- ¿Sigue siendo CentOS Stream 10?
- ¿Existe ya un hostname estático?
- ¿Cambió el kernel?
- ¿Ha habido una actualización significativa desde el manual?

---

# 8. Subfase 0.2 — CPU, memoria y presión actual

## Objetivo

Determinar capacidad real disponible para ejecutar laboratorios simultáneos.

## Comandos

```bash
echo "===== CPU ====="
lscpu

echo
echo "===== MEMORIA ====="
free -h

echo
echo "===== CARGA ====="
uptime

echo
echo "===== TOP PROCESOS CPU ====="
ps -eo pid,user,comm,%cpu,%mem --sort=-%cpu | head -15

echo
echo "===== TOP PROCESOS RAM ====="
ps -eo pid,user,comm,%cpu,%mem --sort=-%mem | head -15
```

## Registrar

```text
CPU lógicos
modelo CPU
RAM total
RAM usada
RAM disponible
swap
load average
procesos principales
```

## Objetivo de diseño posterior

Calcular cuánto puede recibir cada entorno:

```text
team01
team02
team03
...
```

sin comprometer servicios existentes.

---

# 9. Subfase 0.3 — Almacenamiento

## Objetivo

Confirmar distribución y espacio disponible.

## Comandos

```bash
echo "===== FILESYSTEMS ====="
df -hT

echo
echo "===== BLOQUES ====="
lsblk -o NAME,MODEL,SIZE,TYPE,FSTYPE,MOUNTPOINTS

echo
echo "===== USO PRINCIPAL ====="
sudo du -sh \
  /home/tulum/apps \
  /home/tulum/infra \
  /home/tulum/backups \
  /home/docker-data \
  2>/dev/null
```

## Registrar

```text
/
 /home
swap
discos físicos
LVM
uso de /home
uso de Docker
uso de aplicaciones
uso de respaldos
```

## No hacer

No entrar a modificar:

```text
/home/docker-data
```

El directorio se trata como almacenamiento interno administrado por Docker.

---

# 10. Subfase 0.4 — Interfaces y direccionamiento

## Objetivo

Comprender la red actual antes de decidir cómo accederán los integrantes.

## Comandos

```bash
echo "===== INTERFACES ====="
ip -br addr

echo
echo "===== ENO1 ====="
ip -4 addr show eno1

echo
echo "===== RUTAS ====="
ip route

echo
echo "===== NETWORKMANAGER ====="
nmcli device status

echo
echo "===== CONFIG ENO1 ====="
nmcli device show eno1 | grep -E \
'GENERAL.CONNECTION|IP4.ADDRESS|IP4.GATEWAY|IP4.DNS'
```

## Registrar

```text
interfaces
estado de eno1
IP LAN
prefijo
gateway
DNS
interfaces adicionales
bridges Docker
interfaces Tailscale
```

## Preguntas

- ¿La IP sigue entregándose mediante DHCP?
- ¿La IP documentada sigue siendo válida?
- ¿Hay una segunda interfaz activa?
- ¿Hay bridges nuevos?
- ¿Existe una red que pueda aprovechar ClubLab?

---

# 11. Subfase 0.5 — Puertos y superficie de exposición

## Objetivo

Saber qué puertos ya están ocupados y qué servicios están expuestos.

## Comandos

```bash
echo "===== SOCKETS TCP/UDP ====="
sudo ss -lntup

echo
echo "===== FIREWALL ====="
sudo firewall-cmd --state

echo
echo "===== ZONAS ====="
sudo firewall-cmd --get-active-zones

echo
echo "===== PUBLIC ====="
sudo firewall-cmd --zone=public --list-all

echo
echo "===== DOCKER ZONE ====="
sudo firewall-cmd --zone=docker --list-all
```

Si la zona `docker` no existe, solo registrar el resultado; no crearla.

## Registrar

Tabla:

| Puerto | Protocolo | Dirección | Servicio | Alcance | ¿Relacionado con ClubLab? |
|---|---|---|---|---|---|

## Verificar especialmente

```text
22
80
443
3500
5432
8080
8090
9090
41641
```

No asumir que estos son los únicos puertos.

---

# 12. Subfase 0.6 — Servicios systemd

## Objetivo

Conocer qué servicios relevantes están activos.

## Comandos

```bash
echo "===== DOCKER ====="
systemctl is-enabled docker
systemctl is-active docker

echo
echo "===== TAILSCALE ====="
systemctl is-enabled tailscaled
systemctl is-active tailscaled

echo
echo "===== CLOUDFLARED ====="
systemctl is-enabled cloudflared-quick 2>/dev/null
systemctl is-active cloudflared-quick 2>/dev/null

echo
echo "===== CADDY ====="
systemctl is-enabled caddy 2>/dev/null
systemctl is-active caddy 2>/dev/null

echo
echo "===== COCKPIT ====="
systemctl is-enabled cockpit.socket 2>/dev/null
systemctl is-active cockpit.socket 2>/dev/null

echo
echo "===== CRON ====="
systemctl is-enabled crond
systemctl is-active crond

echo
echo "===== SSH ====="
systemctl is-enabled sshd
systemctl is-active sshd
```

## Registrar

| Servicio | Enabled | Active | Manual | Actual | Observación |
|---|---|---|---|---|---|

---

# 13. Subfase 0.7 — Docker Engine

## Objetivo

Crear un mapa real del entorno Docker sin alterar nada.

## Comandos

```bash
echo "===== DOCKER VERSION ====="
docker version

echo
echo "===== DOCKER INFO RESUMIDO ====="
docker info --format \
'Server={{.ServerVersion}}
Driver={{.Driver}}
DockerRoot={{.DockerRootDir}}
Containers={{.Containers}}
Running={{.ContainersRunning}}
Images={{.Images}}'

echo
echo "===== CONTENEDORES ====="
docker ps --format \
'table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}'

echo
echo "===== TODOS LOS CONTENEDORES ====="
docker ps -a --format \
'table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}'

echo
echo "===== REDES ====="
docker network ls

echo
echo "===== VOLUMENES ====="
docker volume ls

echo
echo "===== USO ====="
docker system df

echo
echo "===== RECURSOS EN TIEMPO REAL ====="
docker stats --no-stream
```

## Registrar

```text
versión Docker
Docker Root Dir
contenedores activos
contenedores detenidos
imágenes
redes
volúmenes
uso de disco
consumo CPU/RAM por contenedor
```

---

# 14. Subfase 0.8 — Mapa de contenedores

## Objetivo

Entender relaciones entre contenedores sin revelar variables de entorno.

Para cada contenedor relevante:

```bash
docker inspect \
  --format 'Name={{.Name}}
Image={{.Config.Image}}
Networks={{range $k,$v := .NetworkSettings.Networks}}{{$k}} {{end}}
Ports={{json .NetworkSettings.Ports}}
Restart={{.HostConfig.RestartPolicy.Name}}' \
  NOMBRE_CONTENEDOR
```

## Registrar

```text
nombre
imagen
redes
puertos
restart policy
```

No registrar `Env`.

---

# 15. Subfase 0.9 — Redes Docker

## Objetivo

Determinar qué redes ya existen y cuáles son de producción.

## Comandos

Primero:

```bash
docker network ls
```

Después, únicamente sobre redes identificadas como relevantes:

```bash
docker network inspect NOMBRE_RED \
  --format 'Name={{.Name}}
Driver={{.Driver}}
Internal={{.Internal}}
Attachable={{.Attachable}}
Subnet={{range .IPAM.Config}}{{.Subnet}}{{end}}
Containers={{range $id,$c := .Containers}}{{$c.Name}} {{end}}'
```

## Registrar

```text
nombre
driver
subnet
internal
attachable
contenedores conectados
función
```

## Clasificación

Cada red se marcará como:

```text
PRODUCCIÓN
INFRAESTRUCTURA
SISTEMA
DESCONOCIDA
CANDIDATA CLUBLAB
```

No se conectará ClubLab todavía.

---

# 16. Subfase 0.10 — Volúmenes Docker

## Objetivo

Identificar persistencia existente para evitar cualquier colisión.

## Comando

```bash
docker volume ls
```

Para volúmenes relevantes:

```bash
docker volume inspect NOMBRE_VOLUMEN \
  --format 'Name={{.Name}}
Driver={{.Driver}}
Mountpoint={{.Mountpoint}}
Scope={{.Scope}}'
```

## Registrar

```text
nombre
propósito conocido
contenedor asociado
criticidad
```

No inspeccionar manualmente archivos del mountpoint.

---

# 17. Subfase 0.11 — PostgreSQL existente

## Objetivo

Confirmar que PostgreSQL de producción existe y conocer únicamente sus metadatos básicos.

Primero:

```bash
docker ps --filter name=postgres
```

Después, si el contenedor y el acceso administrativo siguen coincidiendo con el manual:

```bash
docker exec -it postgres-main \
  psql -U postgres_admin -d postgres
```

Dentro de `psql`:

```text
\conninfo
\l
\du
\q
```

Opcionalmente:

```text
SELECT datname,
       pg_size_pretty(pg_database_size(datname))
FROM pg_database
ORDER BY pg_database_size(datname) DESC;
```

## No hacer

```text
no consultar tablas de aplicaciones
no modificar registros
no crear bases
no crear roles
no cambiar passwords
no ejecutar migraciones
```

## Resultado esperado

Determinar:

```text
PostgreSQL producción = NO TOCAR
```

y confirmar si ClubLab deberá tener PostgreSQL propio.

---

# 18. Subfase 0.12 — Tailscale

## Objetivo

Comprobar el canal privado existente y valorar si puede utilizarse para administración o acceso de ClubLab.

## Comandos

```bash
echo "===== TAILSCALE STATUS ====="
tailscale status

echo
echo "===== TAILSCALE IP ====="
tailscale ip -4

echo
echo "===== TAILSCALE SERVE ====="
tailscale serve status
```

## Registrar

```text
estado
IP
nombre del nodo
servicios publicados
Serve activo
destinos de Serve
```

## Preguntas

- ¿Tailscale será solo administrativo?
- ¿Los integrantes pertenecerán al tailnet?
- ¿Conviene publicar ClubLab por otro mecanismo?
- ¿Existe actualmente una ruta que no se debe reemplazar?

No cambiar configuración todavía.

---

# 19. Subfase 0.13 — Cloudflare

## Objetivo

Determinar si el Quick Tunnel sigue activo y qué publica.

## Comandos

```bash
systemctl status cloudflared-quick --no-pager

journalctl \
  -u cloudflared-quick \
  -n 50 \
  --no-pager
```

Si es necesario identificar únicamente una URL pública:

```bash
journalctl \
  -u cloudflared-quick \
  --no-pager \
  -n 100 \
| grep -o 'https://[^ ]*trycloudflare.com' \
| tail -1
```

## Registrar

```text
activo/inactivo
destino local
URL actual
tipo de túnel
dependencias
```

No copiar tokens si aparecieran en logs.

---

# 20. Subfase 0.14 — Caddy / reverse proxy actual

## Objetivo

Resolver si Caddy sigue inactivo o ya forma parte de la infraestructura.

## Comandos

```bash
systemctl status caddy --no-pager

sudo ss -lntup | grep -i caddy || true
```

Si Caddy está activo, obtener únicamente el archivo de configuración principal:

```bash
sudo cat /etc/caddy/Caddyfile
```

### Precaución

Antes de guardar el contenido en documentación, revisar que no contenga:

```text
tokens
credenciales
API keys
secrets
```

## Registrar

```text
activo/inactivo
puertos
sitios
reverse proxies
relación con Tailscale/Cloudflare
```

---

# 21. Subfase 0.15 — Organización de directorios

## Objetivo

Confirmar las rutas disponibles para una futura instalación de ClubLab.

## Comandos

```bash
echo "===== HOME TULUM ====="
ls -la /home/tulum

echo
echo "===== APPS ====="
find /home/tulum/apps \
  -maxdepth 2 \
  -mindepth 1 \
  -type d \
  -printf '%p\n' 2>/dev/null

echo
echo "===== INFRA ====="
find /home/tulum/infra \
  -maxdepth 2 \
  -mindepth 1 \
  -type d \
  -printf '%p\n' 2>/dev/null

echo
echo "===== SCRIPTS ====="
ls -la /home/tulum/scripts 2>/dev/null

echo
echo "===== BACKUPS ====="
ls -la /home/tulum/backups 2>/dev/null
```

## No hacer

No mostrar:

```text
.ssh
.env
archivos de credenciales
contenido de respaldos
```

## Pregunta

¿Sigue teniendo sentido reservar:

```text
/home/tulum/apps/clublab
```

como futura ruta?

---

# 22. Subfase 0.16 — Respaldos y monitorización

## Objetivo

Conocer qué mecanismos existentes podrían verse afectados por ClubLab.

## Comandos

```bash
echo "===== CRONTAB ====="
crontab -l

echo
echo "===== BACKUPS POSTGRES ====="
ls -lh /home/tulum/backups/postgres 2>/dev/null | tail -10

echo
echo "===== MONITOR ====="
journalctl \
  -t whatsapp-monitor \
  --since "24 hours ago" \
  --no-pager \
  | tail -50
```

## Registrar

```text
cron jobs
horarios
rutas
monitorizaciónconsumo aproximado
dependencias
```

No ejecutar ningún script de backup manualmente en esta fase.

---

# 23. Subfase 0.17 — Diagnóstico de capacidad para ClubLab

Con la información recopilada se calculará una primera reserva de recursos.

## Inventario

```text
CPU total:
CPU actualmente utilizada:
RAM total:
RAM normalmente disponible:
Disco disponible:
Puertos libres:
Redes existentes:
```

## Presupuesto preliminar por equipo

No fijar aún valores definitivos.

Crear escenarios como:

| Recurso | Team | 4 equipos | 6 equipos | 8 equipos |
|---|---:|---:|---:|---:|
| API | TBD | TBD | TBD | TBD |
| Frontend | TBD | TBD | TBD | TBD |
| PostgreSQL | TBD | TBD | TBD | TBD |
| Toolbox | TBD | TBD | TBD | TBD |
| RAM total | TBD | TBD | TBD | TBD |
| CPU total | TBD | TBD | TBD | TBD |

---

# 24. Subfase 0.18 — Clasificación de infraestructura

Cada componente descubierto se clasificará:

## ROJO — No tocar

Ejemplos probables:

```text
postgres-main
volúmenes productivos
/home/docker-data
SSH
eno1
NetworkManager
redes productivas
respaldos productivos
```

## AMARILLO — Compartible con precaución

Ejemplos posibles:

```text
Tailscale
Cloudflare
Caddy
host Docker
almacenamiento /home
```

## VERDE — Disponible para ClubLab

Solo después de la auditoría:

```text
puertos libres
rango de nombres
rango de subredes
directorio nuevo
recursos CPU/RAM
```

---

# 25. Subfase 0.19 — Comparación contra el manual

Crear una matriz de diferencias:

| Componente | Manual agosto 2026 | Estado actual | Cambio | Impacto ClubLab |
|---|---|---|---|---|
| Hostname | TBD | TBD | TBD | TBD |
| IP LAN | TBD | TBD | TBD | TBD |
| Docker | TBD | TBD | TBD | TBD |
| PostgreSQL | TBD | TBD | TBD | TBD |
| Tailscale | TBD | TBD | TBD | TBD |
| Cloudflare | TBD | TBD | TBD | TBD |
| Caddy | TBD | TBD | TBD | TBD |
| Cockpit | TBD | TBD | TBD | TBD |
| Puertos | TBD | TBD | TBD | TBD |
| Redes Docker | TBD | TBD | TBD | TBD |
| Volúmenes | TBD | TBD | TBD | TBD |
| Disco | TBD | TBD | TBD | TBD |
| RAM | TBD | TBD | TBD | TBD |

---

# 26. Subfase 0.20 — Decisiones que deben salir de la Fase 0

La fase NO diseña todavía toda la arquitectura.

Pero sí debe permitir cerrar estas decisiones:

### D0.1 Ruta del proyecto

Ejemplo:

```text
/home/tulum/apps/clublab
```

### D0.2 Aislamiento

```text
ClubLab NO usará redes productivas.
```

### D0.3 Base de datos

Definir si:

```text
A) una BD ClubLab compartida
B) una BD por equipo
C) un PostgreSQL por equipo
```

La decisión final pertenece a Fase 2, pero Fase 0 debe identificar qué es viable.

### D0.4 Publicación

Opciones a evaluar:

```text
LAN
Tailscale
Caddy
Cloudflare
combinación
```

### D0.5 Recursos máximos

Definir un presupuesto seguro para:

```text
CPU
RAM
disco
número de equipos
```

### D0.6 Rango de puertos

Reservar conceptualmente un rango libre para ClubLab.

No abrirlo todavía.

### D0.7 Dependencias productivas

Determinar qué componentes compartirá ClubLab, si alguno.

---

# 27. Documento de salida D00

El entregable oficial será:

`D00_Estado_Base_Servidor_ClubLab.md`

## Estructura

```text
1. Resumen ejecutivo
2. Fecha y alcance
3. Identidad del servidor
4. Hardware y recursos
5. Almacenamiento
6. Red
7. Firewall
8. Puertos
9. Servicios
10. Docker
11. Contenedores
12. Redes Docker
13. Volúmenes
14. PostgreSQL
15. Tailscale
16. Cloudflare
17. Caddy
18. Directorios
19. Backups y monitorización
20. Diferencias respecto al manual
21. Mapa de componentes críticos
22. Recursos disponibles para ClubLab
23. Restricciones de diseño
24. Riesgos
25. Decisiones pendientes para Fase 2
26. Conclusión de viabilidad
```

---

# 28. Evidencias complementarias

Guardar, si son necesarias:

```text
E00_hostname.txt
E01_resources.txt
E02_storage.txt
E03_network.txt
E04_ports_firewall.txt
E05_services.txt
E06_docker.txt
E07_docker_networks.txt
E08_docker_volumes.txt
E09_postgres_metadata.txt
E10_tailscale.txt
E11_cloudflare.txt
E12_caddy.txt
E13_directories.txt
E14_monitoring.txt
```

Nunca guardar secretos.

---

# 29. Criterios de aceptación de la Fase 0

La fase se considera terminada cuando podemos responder con evidencia:

- [ ] ¿Qué SO y kernel ejecuta Tulum?
- [ ] ¿Cuánta CPU y RAM tiene disponibles?
- [ ] ¿Cuánto almacenamiento real queda?
- [ ] ¿Qué interfaces de red existen?
- [ ] ¿Cuál es la IP LAN actual?
- [ ] ¿Cuál es la IP Tailscale actual?
- [ ] ¿Qué puertos están ocupados?
- [ ] ¿Qué servicios están expuestos?
- [ ] ¿Qué contenedores existen?
- [ ] ¿Qué redes Docker existen?
- [ ] ¿Qué volúmenes existen?
- [ ] ¿Qué componentes son de producción?
- [ ] ¿PostgreSQL sigue siendo central?
- [ ] ¿Tailscale Serve está activo?
- [ ] ¿Cloudflare sigue activo?
- [ ] ¿Caddy está activo o inactivo?
- [ ] ¿Qué directorio puede usar ClubLab?
- [ ] ¿Qué recursos podemos reservar?
- [ ] ¿Qué infraestructura no debe tocar ClubLab?
- [ ] ¿Qué cambió respecto al manual?
- [ ] ¿Es viable ejecutar múltiples entornos ClubLab?

---

# 30. Condición de salida

No comenzar Fase 1/2 técnica hasta disponer de:

```text
D00 completo
+
matriz de diferencias
+
mapa de puertos
+
mapa Docker
+
clasificación rojo/amarillo/verde
+
presupuesto preliminar de recursos
```

Una vez cerrada Fase 0:

```text
ESTADO REAL
   ↓
RESTRICCIONES
   ↓
CAPACIDAD
   ↓
DECISIONES DE ARQUITECTURA
   ↓
FASE 1 / FASE 2
```

---

# 31. Orden recomendado de ejecución real

Para no generar una salida gigantesca ni perder contexto, ejecutar la auditoría en bloques:

```text
BLOQUE A
Host + CPU + RAM + almacenamiento

BLOQUE B
Red + rutas + puertos + firewall

BLOQUE C
Servicios systemd

BLOQUE D
Docker + contenedores

BLOQUE E
Redes + volúmenes Docker

BLOQUE F
PostgreSQL

BLOQUE G
Tailscale + Cloudflare + Caddy

BLOQUE H
Directorios + backups + monitorización
```

Después de cada bloque:

```text
1. guardar la salida
2. analizarla
3. compararla con el manual
4. registrar diferencias
5. continuar al siguiente bloque
```

Esto evita ejecutar decenas de comandos sin analizar lo que aparece.

---

# 32. Primer bloque a ejecutar

La ejecución de la Fase 0 debe comenzar únicamente con:

```bash
echo "===== HOST ====="
hostnamectl

echo
echo "===== KERNEL ====="
uname -a

echo
echo "===== RELEASE ====="
cat /etc/os-release

echo
echo "===== UPTIME ====="
uptime

echo
echo "===== CPU ====="
lscpu

echo
echo "===== MEMORIA ====="
free -h

echo
echo "===== DISCOS ====="
df -hT

echo
echo "===== BLOQUES ====="
lsblk -o NAME,MODEL,SIZE,TYPE,FSTYPE,MOUNTPOINTS
```

Con la salida de este bloque se inicia formalmente `D00`.

No ejecutar todavía los bloques siguientes hasta analizar este resultado.