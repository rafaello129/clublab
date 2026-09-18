# Tests

ClubLab tendrá cuatro niveles de validación:

```text
database
API
frontend
end-to-end
```

Además se mantendrá una suite de seguridad para comprobar:

- ausencia de root y Docker socket en toolbox;
- aislamiento entre teams;
- DB no publicada;
- permisos PostgreSQL del alumno;
- recovery scoped;
- guard rails de reset;
- ausencia de secrets en logs;
- gateway no utilizado como proxy abierto.

Un piloto no debe ejecutarse con pruebas críticas en FAIL.
