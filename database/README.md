# Database

Cada team tendrá una instancia PostgreSQL independiente.

## Schemas

```text
app
lab
```

## Dominio

```text
Team
User
Mission
Submission
Score
ActivityLog
```

## Superficie pedagógica

```text
lab.environment_context
lab.my_team_score
```

El usuario estudiante podrá consultar datos pedagógicos y actualizar únicamente el score de su propio entorno mediante `lab.my_team_score`.

No se usará `synchronize: true`; el schema se mantendrá mediante migrations versionadas.
