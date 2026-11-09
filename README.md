# ai-tools

Paquete [APM](https://github.com/microsoft/apm) con agentes de IA para trabajar con
[GitHub Spec Kit](https://github.com/github/spec-kit) (Spec-Driven Development) en Claude Code,
GitHub Copilot, OpenCode y Kiro.

## Agentes

| Agente | Rol | Comandos de Spec Kit |
|---|---|---|
| `speckit-product` | Product Owner: qué y por qué | `specify`, `clarify`, `checklist` |
| `speckit-architect` | Arquitecto: cómo técnico | `constitution`, `plan`, `tasks`, `analyze` |
| `speckit-developer` | Desarrollador | `implement` |
| `speckit-tester` | QA | `converge` |

Flujo: product → architect → developer → tester. Si `converge` encuentra brechas, vuelve a developer.

## Skill

`git-speckit`: política git para el flujo (rama por feature desde `main`, Conventional Commits, PR con squash merge).
Los agentes hacen ramas y commits locales; push, PR, merge y tags requieren confirmación del usuario.
Incluye una configuración recomendada para la extensión git de Spec Kit en `assets/git-config.yml`.

## Uso

Requisitos: [APM CLI](https://github.com/microsoft/apm) y, en el proyecto donde se usen los agentes,
Spec Kit inicializado (`specify init . --integration <claude|opencode|kiro-cli>`).

```bash
apm compile --validate   # valida las primitivas
python3 scripts/check-agents.py   # comprueba las convenciones de los agentes (también en la CI)
apm install              # despliega agentes, skill e instrucción en .claude/, .github/, .agents/, .opencode/ y .kiro/
```

Los agentes se editan en `.apm/agents/`. Las carpetas desplegadas son generadas y están en `.gitignore`.

### OpenCode

`apm install` despliega los agentes en `.opencode/agents/`, pero no la instrucción que coordina el flujo
(`speckit-flujo`): OpenCode lee sus instrucciones desde `AGENTS.md`, y ese archivo lo genera `apm compile`.
En el proyecto donde uses los agentes, ejecuta después de instalar:

```bash
apm compile
```

Si el proyecto ya tiene un `AGENTS.md` escrito a mano, APM no lo sobrescribe (avisa con `Protected AGENTS.md`).
En ese caso, copia en tu `AGENTS.md` el contenido de `.apm/instructions/speckit-flujo.instructions.md`.

Sin esa instrucción los agentes funcionan igual, pero el agente principal no sabrá que debe pedir aprobación
tras la spec y tras el plan, ni cortar tras 3 ciclos developer ↔ tester.

## Licencia

[MIT](LICENSE)
