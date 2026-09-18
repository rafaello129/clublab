# Infrastructure

Infraestructura de ClubLab por team:

```text
frontend
api
database
toolbox
```

Entrada compartida:

```text
clublab-gateway
```

## Redes

Cada team tendrá:

```text
clublab-teamXX-app
clublab-teamXX-data
```

El gateway solo participa en redes APP. PostgreSQL vive únicamente en DATA.

## Restricciones

- Sin Docker socket en contenedores de alumnos.
- Sin host network.
- Sin bind mounts productivos.
- Sin publicación directa de PostgreSQL o API.
- Recursos destructibles identificados por prefijo y labels.
