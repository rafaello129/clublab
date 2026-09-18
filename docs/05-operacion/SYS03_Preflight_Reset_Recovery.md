# SYS03 — Preflight, Reset, Recovery y Operación
## ClubLab v1

**Estado:** DISEÑO CERRADO + IMPLEMENTACIÓN BASE  
**Fase:** 5 / Bloques B–C

---

## Comandos operativos implementados

```bash
clublabctl preflight [team|all]
clublabctl status [team|all]
clublabctl resources [team|all]
clublabctl logs <team> <frontend|api|database|toolbox> --lines N

clublabctl scenario load <team|all> <scenario>
clublabctl scenario clear <team|all>
clublabctl scenario status [team|all]

clublabctl recover <team|all>
clublabctl reset <team|all> --yes

clublabctl spare status
clublabctl spare assign <team>
clublabctl spare release

clublabctl audit tail --lines N
```

---

## Reset

Reset es explícitamente destructivo.

```bash
clublabctl reset team01 --yes
```

Para todos los entornos:

```bash
clublabctl reset all --yes --confirm RESET-ALL
```

Nunca utiliza prune global.

---

## Recovery

```text
R1 scenario clear
R2 restart API
R3 reset explícito
```

R3 nunca se ejecuta automáticamente.

---

## Preflight

Checks críticos:

```text
Docker
Compose contract
bind IP
RAM
disk
runtime secrets
ports
IPAM
container security
```

Spare es un check no crítico.

---

## Status

Distingue:

```text
READY
SCENARIO
DEGRADED
ABSENT
```

y muestra cada capa del team.

---

## Auditoría

Runtime:

```text
audit/clublabctl.jsonl
```

No contiene secrets.

---

## Pendiente

```text
deploy
real compose
runtime env generation
gateway
full integration test on Tulum
```

Estos puntos se cierran en Bloque D y en la implementación de infraestructura.
