# Team Compose contract

El Scenario Manager de Fase 5 espera que la implementación de infraestructura cree:

```text
infrastructure/compose/team.compose.yml
```

## Servicios runtime

```text
frontend
api
database
toolbox
```

## Servicio one-shot

```text
bootstrap
```

`bootstrap` ejecutará migrations, roles/grants, objetos `lab`, seed y validación inicial.

## Labels obligatorias de containers

```text
com.clublab.project=clublab
com.clublab.team=<team>
com.clublab.role=<frontend|api|database|toolbox>
com.clublab.managed-by=clublab
com.clublab.disposable=true
```

## Volúmenes resetables

```text
db-data
lablogs
```

También deben incluir:

```text
com.clublab.project=clublab
com.clublab.team=<team>
com.clublab.managed-by=clublab
com.clublab.disposable=true
```

Hasta que este contrato no esté implementado, `clublabctl reset` falla de forma segura.
