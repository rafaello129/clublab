# Roadmap

0. Auditoría del servidor — ✅ completada.
1. Diseño pedagógico — ✅ completada.
2. Arquitectura técnica — ✅ diseño completado.
3. Seguridad y aislamiento — ✅ diseño completado; validación empírica pendiente.
4. Aplicación ClubLab — ✅ diseño completado; implementación real pendiente.
5. Scenario Manager y operación — ✅ diseño y control plane completados; live validation pendiente.
6. Roles y dinámica de equipos — 🟡 Bloque A completado; Bloques B–D pendientes.
7. Materiales del alumno — ⏳ pendiente.
8. Materiales del instructor — ⏳ pendiente.
9. Ensayo técnico y pedagógico — ⏳ pendiente.
10. Ejecución de clase — ⏳ pendiente.
11. Feedback y evolución — ⏳ pendiente.

## Fase 5 — cerrada

~~~text
Block A
inventory
student/instructor CLI contracts
runtime state model

Block B
scenario load/clear/status
ranking-db-failure
api-down
recovery R1/R2
guarded reset

Block C
preflight
status
resources
technical logs
spare
audit
security inspection

Block D
deploy orchestration
shared gateway contract
smoke tests
runtime templates
operational validation matrix
D04
~~~

## Fase 6

Completado:

~~~text
Block A
contratos finales R1–R5
herramientas y límites reales por rol
evidencia mínima por rol
configuraciones 2/3/4/5 integrantes
contingencia individual
reglas para avanzados/principiantes
~~~

Pendiente:

~~~text
Block B
matriz misión/rol
funciones operar/observar/verificar/registrar
rotación
handoff
regla del teclado
predicción/evidencia

Block C
incidente colaborativo
participación
avanzados/principiantes
contingencias

Block D
validación de mesa
validación de tiempos
consolidación D05
~~~

## Próxima necesidad técnica

Antes de un ensayo real hay que implementar los artefactos que el control plane ya espera:

~~~text
frontend
backend
database migrations/seeds/bootstrap
toolbox image
team.compose.yml
gateway.compose.yml
gateway config
runtime generation
pinned images
~~~

Las Fases 6–8 pueden documentarse en paralelo, pero Fase 9 no debe iniciarse hasta que la aplicación e infraestructura reales pasen preflight, smoke y security gates.
