# Scenarios

Escenarios mínimos de ClubLab v1:

```text
normal
ranking-db-failure
api-down
```

## normal

Todos los servicios y endpoints funcionan.

## ranking-db-failure

El ranking devuelve HTTP 500 mientras health, perfil, equipo, misiones y actividad permanecen funcionales.

## api-down

Escenario de infraestructura. El contenedor API del team se detiene de forma controlada mientras frontend, DB y toolbox permanecen activos.
