# SYS02 — CLI `clublabctl`
## Herramienta del instructor

**Estado:** contrato cerrado; scaffold de Block A implementado

### Lenguaje

Python 3.11+ con librería estándar.

### Comandos reservados

```text
inventory list|show|validate
preflight
deploy
status
resources
logs
scenario load|clear|status
recover
reset
spare status|assign
audit tail
version
```

### Block A funcional

```text
version
inventory list
inventory show
inventory validate
```

Las operaciones sobre Docker/scenarios quedan intencionalmente sin implementar hasta los Bloques B/C.

### Guard rails

- target debe existir en `teams.json`;
- `all` se habilita solo por comando;
- scenario debe estar en allowlist;
- role debe estar en allowlist;
- ninguna operación futura puede construirse con shell interpolation;
- recursos destructivos deberán requerir prefijo + labels.

### Exit codes

```text
0 OK
2 USAGE
3 CONFIG
4 CHECK_FAILED
5 OPERATION_FAILED
6 STATE_CONFLICT
7 PARTIAL_SUCCESS
8 DEPENDENCY_UNAVAILABLE
9 SECURITY_GUARD
10 NOT_IMPLEMENTED
```
