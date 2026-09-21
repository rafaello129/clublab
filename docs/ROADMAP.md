# Roadmap

0. Auditoría del servidor — ✅ completada.
1. Diseño pedagógico — ✅ completada.
2. Arquitectura técnica — ✅ diseño completado.
3. Seguridad y aislamiento — ✅ diseño completado; validación empírica pendiente.
4. Aplicación ClubLab — ✅ diseño completado; implementación real pendiente.
5. Scenario Manager y operación — ✅ diseño y control plane completados; live validation pendiente.
6. Roles y dinámica de equipos — ✅ diseño completado; validación empírica pendiente en Fase 9.
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

## Fase 6 — cerrada

~~~text
Block A
contratos finales R1–R5
herramientas y límites reales por rol
evidencia mínima
configuraciones 2/3/4/5 integrantes

Block B
matriz M0–M8
OPERAR/OBSERVAR/VERIFICAR/REGISTRAR
POE
regla del teclado
rotación
handoff/readback

Block C
protocolo M6/M7
hipótesis
barrera de recovery
P0–P4
anti-monopolio
equipos rápidos/lentos
ausencias y contingencias

Block D
validación de diseño V2/V3/V4/V5
validación temporal
participación
seguridad
métricas y umbrales para ensayo
D05
~~~

Entregable oficial:

~~~text
D05_Roles_y_Dinamica_Equipos_ClubLab.md
~~~

La configuración recomendada permanece:

~~~text
4 integrantes por team
~~~

Dos integrantes se conserva como contingencia con riesgo de tiempo/carga cognitiva.

## Siguiente fase documental

~~~text
Fase 7 — Materiales del alumno
D06 Guía del alumno
D07 Cheat Sheet
D08 Cuaderno de Misiones
tarjetas de rol y hojas de evidencia
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

Las Fases 7–8 pueden documentarse en paralelo, pero Fase 9 no debe iniciarse hasta que la aplicación e infraestructura reales pasen preflight, smoke y security gates.
