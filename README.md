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

## Uso

Requisitos: [APM CLI](https://github.com/microsoft/apm) y, en el proyecto donde se usen los agentes,
Spec Kit inicializado (`specify init . --integration <claude|opencode|kiro-cli>`).

```bash
apm compile --validate   # valida las primitivas
apm install              # despliega los agentes en .claude/, .github/, .opencode/ y .kiro/
```

Los agentes se editan en `.apm/agents/`. Las carpetas desplegadas son generadas y están en `.gitignore`.

## Licencia

[MIT](LICENSE)
