# ClubLab — Fase 2 / Bloque D
## Validación arquitectónica + cierre de D02

**Proyecto:** ClubLab v1  
**Fase:** 2 — Arquitectura técnica  
**Bloque:** D  
**Estado:** COMPLETADO  
**Dependencias:** D00 + D01 + Fase 2/Bloques A–C  

---

# 1. Propósito

Este bloque valida la arquitectura diseñada contra:

```text
estado real auditado del servidor;
objetivos pedagógicos;
aislamiento;
recursos;
puertos;
redes;
operación;
recuperación;
crecimiento inicial.
```

Además consolida el documento oficial:

```text
D02_Arquitectura_Tecnica_ClubLab.md
```

---

# 2. Resultado de validación

La arquitectura propuesta es:

# **VIABLE CON AJUSTES DE VALIDACIÓN**

Se mantienen las decisiones principales de A–C, pero se incorporan dos ajustes técnicos:

```text
AJ-01 — red dedicada clublab-ingress para el gateway;
AJ-02 — aliases únicos de gateway por team.
```

Estos ajustes evitan ambigüedades de red y mantienen las redes de equipo internas.

---

# 3. Ajuste AJ-01 — red `clublab-ingress`

El gateway necesita una interfaz clara de entrada y, al mismo tiempo, conectividad con todas las redes APP.

Se agrega:

```text
clublab-ingress
10.77.250.0/24
```

Conectado únicamente a:

```text
clublab-gateway
```

El gateway seguirá conectado también a:

```text
clublab-team01-app
...
clublab-team06-app
clublab-spare-app
```

Las redes APP/DATA de los teams permanecen:

```text
internal: true
```

`clublab-ingress` será la única red ClubLab no interna necesaria para el gateway.

---

# 4. Ajuste AJ-02 — aliases únicos desde gateway

Como `clublab-gateway` está conectado a múltiples redes, no se usarán nombres ambiguos como:

```text
frontend
api
toolbox
```

desde el gateway.

Cada servicio tendrá un alias único visible al gateway:

```text
team01-frontend
team01-api
team01-toolbox

team02-frontend
team02-api
team02-toolbox
```

Dentro del propio team podrán mantenerse aliases simples:

```text
frontend
api
database
toolbox
```

Esto evita resolución DNS ambigua dentro del gateway.

---

# 5. Validación contra D00

La arquitectura no utiliza:

```text
172.17.0.0/16
172.18.0.0/16
172.19.0.0/16
172.20.0.0/16
10.10.100.0/22 como red Docker
```

No toca:

```text
postgres-main
database-net
whatsapp_app-net
pelican_nw
Docker Root Dir
Pelican/Wings
Playit
Caddy actual
cloudflared-quick
Tailscale Serve existente
```

No modifica:

```text
Docker daemon default-address-pools
NetworkManager
eno1
rutas globales
```

Resultado:

```text
VALIDADO
```

---

# 6. Validación de puertos

Puertos ClubLab:

```text
8211–8216
8219
```

No colisionaban con los listeners identificados durante Fase 0.

Aun así, su disponibilidad no se considera permanente.

Preflight obligatorio:

```bash
ss -ltnup
```

antes de cada despliegue.

---

# 7. Validación de recursos

Presupuesto máximo inicial por team:

```text
RAM ≈ 1.5 GiB
CPU cap ≈ 2.0
```

Escenarios:

```text
4 teams              ≈ 6 GiB
6 teams              ≈ 9 GiB
6 teams + spare      ≈ 10.5 GiB
```

Más:

```text
gateway;
overhead de Docker;
logs efímeros.
```

El host auditado dispone de capacidad suficiente para un piloto, pero Pelican puede incrementar uso significativamente.

Por tanto:

```text
4 teams = objetivo operativo inicial
6 teams = capacidad a validar
spare healthy = condicionado a prueba de carga
```

---

# 8. Validación pedagógica

La arquitectura soporta:

```text
M1 → DevTools / Network
M2 → curl directo a API
M3 → psql desde toolbox
M4 → UPDATE DB → API → UI
M5 → status por servicio
M6 → request 500 con sistema parcialmente sano
M7 → logs + diagnóstico + recover
M8 → arquitectura observable
```

Resultado:

```text
D01 SATISFECHO
```

---

# 9. Validación del incidente

El escenario principal mantiene:

```text
frontend healthy
api healthy
database healthy

/api/health    200
/api/me        200
/api/missions  200
/api/ranking   500
```

Se utilizará:

```text
fault injection scoped al ranking
```

y no un cambio global de `DB_HOST`.

Resultado:

```text
VALIDADO
```

---

# 10. Validación de aislamiento

Cada team tiene:

```text
APP network propia
DATA network propia
DB propia
volumen DB propio
lablogs propios
credenciales propias
scenario state propio
```

No existe:

```text
red compartida entre teams;
DB compartida;
volumen compartido;
toolbox compartido.
```

La única pieza multihomed es:

```text
clublab-gateway
```

y funciona exclusivamente como reverse proxy.

---

# 11. Validación de acceso del alumno

El alumno necesita:

```text
navegador
```

y accede a:

```text
frontend
API
terminal web
```

por un único puerto del team.

No necesita:

```text
SSH;
Tailscale;
Docker;
psql local;
curl local;
sudo.
```

Resultado:

```text
VALIDADO
```

---

# 12. Validación operativa

Plano alumno:

```text
clublab
```

Plano instructor:

```text
clublabctl
```

Separación:

```text
alumno → observar/recover limitado
instructor → scenario/reset/deploy
```

No se introduce panel web administrativo en v1.

Resultado:

```text
VALIDADO
```

---

# 13. Mapa final de servicios

Por team:

```text
frontend
api
database
toolbox
```

Compartidos:

```text
clublab-gateway
clublabctl
Docker Engine
```

Para 4 teams:

```text
16 contenedores team
+ 1 gateway
= 17 contenedores ClubLab activos
```

Con 6 teams:

```text
24 + 1 = 25
```

Con spare activo:

```text
29
```

---

# 14. Mapa final de redes

```text
clublab-ingress        10.77.250.0/24

team01-app             10.77.1.0/24
team01-data            10.77.101.0/24

team02-app             10.77.2.0/24
team02-data            10.77.102.0/24

team03-app             10.77.3.0/24
team03-data            10.77.103.0/24

team04-app             10.77.4.0/24
team04-data            10.77.104.0/24

team05-app             10.77.5.0/24
team05-data            10.77.105.0/24

team06-app             10.77.6.0/24
team06-data            10.77.106.0/24

spare-app              10.77.9.0/24
spare-data             10.77.109.0/24
```

Todas las APP/DATA:

```text
internal: true
```

---

# 15. Mapa final de puertos

## Host

```text
8211 Team01
8212 Team02
8213 Team03
8214 Team04
8215 Team05
8216 Team06
8219 Spare
```

Solo:

```text
clublab-gateway
```

publica estos puertos.

## Internos

```text
frontend 80
api      3000
db       5432
toolbox  7681
```

Ninguno se publica directamente al host.

---

# 16. Mapa final de comunicación

```text
LAN
 │
 ▼
Gateway
 │
 ├── frontend
 ├── api
 └── toolbox
      │
      ├── api
      └── database

API
 └── database
```

Prohibido:

```text
gateway → database
frontend → database
team01 → team02
LAN → database
LAN → API:3000 directo
LAN → toolbox:7681 directo
```

---

# 17. Mapa final de persistencia

Por team:

```text
db-data      → persistencia funcional
lablogs      → persistencia operativa efímera
```

No se montan rutas productivas.

---

# 18. Estado final de la Fase 2

```text
[A] Arquitectura base             ✅
[B] Redes + acceso + aislamiento  ✅
[C] Observabilidad + operación    ✅
[D] Validación + D02              ✅
```

# FASE 2 — COMPLETADA

---

# 19. Próximo paso

La Fase 3 deberá convertir estas fronteras arquitectónicas en controles concretos:

```text
usuarios;
credenciales;
permisos PostgreSQL;
RLS o equivalente;
capabilities;
read-only;
seccomp/no-new-privileges;
auth de terminal;
tokens de recover;
protección del gateway;
firewall;
secrets;
validaciones de aislamiento.
```

La pregunta de la siguiente fase será:

> **¿Cómo hacemos cumplir técnicamente todo lo que esta arquitectura promete?**