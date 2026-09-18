# SYS01 — CLI `clublab`
## Herramienta del alumno

**Estado:** contrato cerrado; scaffold funcional

### Comandos

```text
clublab whoami
clublab status
clublab health
clublab logs api [--lines N]
clublab recover ranking-db
```

### Fuentes de configuración

```text
CLUBLAB_TEAM_ID
CLUBLAB_TEAM_NAME
CLUBLAB_API_URL
CLUBLAB_FRONTEND_URL
CLUBLAB_DB_HOST
CLUBLAB_DB_PORT
CLUBLAB_DB_NAME
CLUBLAB_DB_USER
CLUBLAB_LABLOG_PATH
CLUBLAB_RECOVERY_TOKEN_FILE
```

Defaults internos solo describen DNS/puertos del laboratorio; no existen defaults para passwords o tokens.

### Seguridad

La herramienta:

- no invoca Docker;
- no usa sudo;
- no acepta paths libres;
- no acepta team IDs;
- no contiene control token;
- solo puede recuperar `ranking-db`;
- lee únicamente el lablog pedagógico.

### Estado

El script inicial ya implementa whoami, status, health, logs y recover sobre los contratos definidos en APP02/APP04.
