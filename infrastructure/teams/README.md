# Team inventory

`teams.json` es el inventario versionado y **no contiene secrets**.

Cada target define su puerto de entrada, subnets APP/DATA y nombre de proyecto Compose.

La configuración runtime sensible debe generarse fuera de Git, bajo el árbol `runtime/` del servidor.

Validación:

```bash
python3 scripts/clublabctl/clublabctl.py inventory validate
```
