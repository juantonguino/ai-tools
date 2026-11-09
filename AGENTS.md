# AGENTS.md

Contexto para agentes de IA (Claude Code, GitHub Copilot, OpenCode, Kiro, etc.) que trabajan en este repositorio.

## Qué es este repo

`ai-tools` es un proyecto **APM (Agent Package Manager)** que empaqueta primitivas de IA reutilizables
(agentes, instrucciones, prompts, skills y hooks) para distribuirlas a varias herramientas.
No contiene código de aplicación: el "código" son archivos Markdown con frontmatter YAML.

- Manifiesto: `apm.yml` (nombre `ai-tools`, v0.1.0, licencia MIT, autor `juantonguino`).
- Targets configurados: `copilot`, `claude`, `opencode` y `kiro` (`apm install` despliega en `.github/agents/`,
  `.claude/agents/`, `.opencode/agents/` y `.kiro/agents/`).
- Sin dependencias (`dependencies.apm` y `dependencies.mcp` vacíos), `includes: auto`, sin `scripts`.

## Estructura

```
apm.yml                 Manifiesto del paquete APM
scripts/check-agents.py Comprueba las convenciones de los agentes
.apm/
  agents/               Definiciones de agentes (*.agent.md)
  instructions/         Instrucciones (speckit-flujo.instructions.md)
  prompts/              Prompts reutilizables (vacío, con .gitkeep)
  skills/git-speckit/   Skill de git (SKILL.md, references/, assets/)
  hooks/                Hooks (vacío, con .gitkeep)
```

## Agentes incluidos: flujo Spec Kit

Los cuatro agentes en `.apm/agents/` implementan un flujo de **Spec-Driven Development** con
[GitHub Spec Kit](https://github.com/github/spec-kit). Son subagentes (`mode: subagent`), escritos en español,
y cada uno tiene un rol acotado:

| Agente | Rol | Comandos Spec Kit | Puede modificar |
|---|---|---|---|
| `speckit-product` | Product Owner: QUÉ y POR QUÉ | `specify`, `clarify`, `checklist` | Solo la spec |
| `speckit-architect` | Arquitecto: CÓMO técnico | `constitution`, `plan`, `tasks`, `analyze` | Plan, tareas, constitución |
| `speckit-developer` | Desarrollador | `implement` (y tareas nuevas tras `converge`) | Código de producción |
| `speckit-tester` | QA | `converge` | Solo pruebas y fixtures |

Flujo: `product → architect → developer → tester`. Si `converge` detecta brechas, vuelve a `developer`;
si reporta `Converged` y las pruebas pasan, la feature está lista.

La coordinación del flujo para el agente principal está en `.apm/instructions/speckit-flujo.instructions.md`
(puntos de control con el usuario tras la spec y tras el plan, máximo 3 ciclos developer↔tester).
`apm install` la despliega en `.claude/rules/`, `.github/instructions/` y `.kiro/steering/`. OpenCode no la recibe
por `install`: la lee desde un `AGENTS.md` generado por `apm compile`.

Convenciones compartidas por todos los agentes (mantenerlas al editar o agregar agentes):
- Sección **"Antes de empezar"**: verificar `.specify/`, leer `.specify/feature.json` (o `SPECIFY_FEATURE_DIRECTORY`), la constitución y los artefactos previos; detenerse si falta algo.
- Tabla **"Cómo ejecutar los comandos de Spec Kit"** que resuelve la ubicación del comando según la herramienta
  (Claude Code: `.claude/skills/speckit-<cmd>/SKILL.md`; OpenCode: `.opencode/commands/`; Kiro: `.kiro/prompts/`).
- Sección **"Preguntas al usuario"**: como subagentes no responden decisiones del usuario; las devuelven numeradas con opciones y recomendación.
- Sección **"Formato de respuesta final"** numerada, terminando con el siguiente paso/agente.
- Sección **"Límites de seguridad"**: nunca `git push`, `git reset --hard`, borrado de ramas ni comandos destructivos sin petición explícita.
- Sección **"Restricciones de herramientas"** (al final): si puede usar la web y qué archivos puede modificar. Solo `speckit-architect` usa la web, y solo para documentación oficial.

La tabla de comandos, "Preguntas al usuario" y "Límites de seguridad" se repiten **a propósito** en los 4 agentes, porque
cada subagente arranca sin contexto. Deben mantenerse idénticos: si cambias uno, cambia los cuatro.

## Skill `git-speckit`

`.apm/skills/git-speckit/` define la política git para proyectos con Spec Kit: GitHub Flow (una rama por feature,
con el nombre de su carpeta), Conventional Commits y squash merge a `main` con `gh`. Las ramas y los commits locales
se hacen sin confirmación; push, PR, merge, tags y reescritura de historial, solo con confirmación del usuario.
Los 4 agentes la citan en "Límites de seguridad" y la instrucción del flujo la usa para arrancar desde `main` y para
integrar (paso 8).

- Se llama `git-speckit` y no `speckit-git` para no compartir prefijo con los skills `speckit-git-*` que instala la
  extensión git de Spec Kit en `.claude/skills/` (chocarían si Spec Kit agrega un comando `git`).
- `references/`: Conventional Commits y plantilla de PR (se cargan bajo demanda).
- `assets/git-config.yml`: configuración para la extensión git de Spec Kit (`specify extension add git`). Usa
  `commit_style: fixed`, porque con `conventional` la extensión ignora los mensajes configurados.
- `apm install` la despliega en `.claude/skills/`, `.agents/skills/` (Copilot y OpenCode) y `.kiro/skills/`.

## Cómo trabajar en este repo

- **Agregar un agente**: crear `.apm/agents/<nombre>.agent.md` con frontmatter `name`, `description` (cuándo usarlo) y
  `mode: subagent` (lo usa OpenCode). Seguir la estructura de secciones de los agentes existentes.
- **No usar `tools:` en el frontmatter.** APM lo copia sin traducir y cada target exige un formato distinto: Claude/Copilot una lista,
  OpenCode un mapa (`{read: true}`) y Kiro sus propias etiquetas (`read, write, shell, web…`). Con la lista de Claude, Kiro
  rechaza el agente y `apm install` falla. Las restricciones de herramientas se expresan en el texto del agente.
  - **Decisión (2026-11-08):** esperar a que APM adapte el frontmatter por target (en APM 0.35.0 figura como
    "Phase 2 (per-target frontmatter transformer)" en `apm_cli/integration/agent_integrator.py`). Se descartaron
    un script `lifecycle: post-install` (APM no ejecuta los scripts de las dependencias, solo los del proyecto que
    instala) y paquetes generados por herramienta (demasiada complejidad para quien instala, a cambio de solo
    bloquear web y MCP).
  - Cuando APM lo soporte: agregar `tools:` según la sección "Restricciones de herramientas" de cada agente
    y comprobar con `apm install` que se despliega en los 4 targets sin avisos.
- Después de cambiar un agente, verificar con `apm install` que se despliega en los 4 targets sin avisos.
- **Agregar otras primitivas**: usar la carpeta correspondiente en `.apm/` (`instructions/`, `prompts/`, `skills/`, `hooks/`).
- **Compilar / distribuir** (CLI `apm` v0.35.0 instalado):
  - `apm compile --validate` — valida las primitivas sin compilar.
  - `apm compile --dry-run` — muestra qué archivos generaría.
  - `apm compile` — genera los archivos de contexto para los targets de `apm.yml`.
  - `apm install` — instala dependencias APM/MCP.
- Escribir el contenido de los agentes en español, manteniendo el tono imperativo y las reglas explícitas actuales.
- No hay build, suite de pruebas ni CI (GitHub Actions está desactivado). Antes de hacer commit, ejecutar a mano:
  `apm compile --validate`, `python3 scripts/check-agents.py` (bloques comunes idénticos y sin `tools:`),
  `apm install` sin avisos y `git status` limpio (todo lo generado está en `.gitignore`).
- Si cambias un bloque común, cámbialo en los 4 agentes: `scripts/check-agents.py` falla si difieren.

## Notas

- Este `AGENTS.md` y `CLAUDE.md` están escritos a mano. `apm compile` los detecta como protegidos y no los sobrescribe
  (avisa con `Protected AGENTS.md`), así que en este repo `apm compile` no genera nada; es lo esperado.
- `CLAUDE.md` solo importa este archivo para que Claude Code cargue el mismo contexto.
