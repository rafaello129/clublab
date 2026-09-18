# ClubLab

Laboratorio práctico de arquitectura de software para el Club de Programación.

ClubLab está diseñado para una clase de aproximadamente 120 minutos en la que los alumnos descubren cómo se compone una aplicación moderna investigando un sistema real: navegador, frontend, API, backend, PostgreSQL, contenedores, redes, logs y fallos controlados.

## Objetivo

La experiencia sigue la secuencia:

```text
observar
→ formular una hipótesis
→ probar
→ reunir evidencia
→ explicar
```

El alumno no construye la aplicación desde cero. Primero la desarma mentalmente y descubre cómo se conectan sus componentes.

## Arquitectura prevista

```text
Alumno
  │
  ▼
Browser
  │
  ▼
clublab-gateway
  │
  ├── Frontend
  ├── API
  └── Toolbox
        │
        ├── API
        └── PostgreSQL
```

Cada equipo tendrá un entorno aislado con:

- frontend React + TypeScript;
- API NestJS + TypeScript;
- PostgreSQL;
- toolbox web para `curl`, `psql` y utilidades de diagnóstico.

## Estado del proyecto

| Fase | Estado |
| --- | --- |
| 0 — Auditoría del servidor | ✅ Completada |
| 1 — Diseño pedagógico | ✅ Completada |
| 2 — Arquitectura técnica | ✅ Diseño completado |
| 3 — Seguridad y aislamiento | ✅ Diseño completado |
| 4 — Aplicación ClubLab | ✅ Diseño completado |
| 5 — Scenario Manager y operación | 🟡 En diseño |
| 6 — Roles y dinámica | ⏳ Pendiente |
| 7 — Materiales del alumno | ⏳ Pendiente |
| 8 — Materiales del instructor | ⏳ Pendiente |
| 9 — Ensayo completo | ⏳ Pendiente |
| 10 — Ejecución de clase | ⏳ Pendiente |
| 11 — Feedback y evolución | ⏳ Pendiente |

## Estructura del repositorio

```text
clublab/
├── app/
│   ├── frontend/
│   └── backend/
├── database/
│   ├── migrations/
│   ├── seeds/
│   └── tests/
├── infrastructure/
│   ├── compose/
│   ├── gateway/
│   ├── toolbox/
│   └── teams/
├── scenarios/
├── scripts/
├── tests/
└── docs/
```

La documentación técnica y pedagógica vive en `docs/`. El código y la infraestructura se irán implementando después de cerrar los contratos de diseño.

## Principios

- No usar servicios productivos para el laboratorio.
- Cada team tiene su propia red y base de datos.
- El alumno nunca recibe acceso al Docker del host.
- Los fallos son deliberados, controlados y reproducibles.
- `recover` corrige el incidente sin borrar el trabajo del alumno.
- `reset` devuelve un team al seed inicial.
- Los datos del laboratorio son ficticios y desechables.

## Licencia

Pendiente de definir.
