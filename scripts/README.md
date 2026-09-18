# Scripts y operación

La operación se dividirá en:

```text
clublab     → alumno
clublabctl  → instructor
```

El alumno podrá observar y recuperar únicamente su escenario.

El instructor podrá realizar preflight, deploy, status, scenario, recover, reset, spare y audit.

Ningún script debe usar operaciones Docker globales destructivas como `docker system prune`.
