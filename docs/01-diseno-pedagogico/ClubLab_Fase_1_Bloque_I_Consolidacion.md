# ClubLab — Fase 1 / Bloque I
## Consolidación del D01

**Estado:** COMPLETADO

El Bloque I consolida los Bloques A–H en el documento oficial:

`D01_Diseno_Experiencia_ClubLab_01.md`

Durante la consolidación se eliminaron redundancias y se derivaron requisitos explícitos para las Fases 2–9.

También se dejó documentado un ajuste técnico importante: el incidente debe preservar un fallo parcial del ranking. Si la implementación usa una única conexión global a PostgreSQL, no debe romperse globalmente `DB_HOST`; la Fase 5 deberá aplicar el fallo de manera scoped al ranking o mediante un mecanismo equivalente.

# FASE 1 — COMPLETADA