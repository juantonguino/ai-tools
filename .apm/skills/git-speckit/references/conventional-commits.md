# Conventional Commits (resumen operativo)

Formato:
```
<tipo>(<scope opcional>)<! si rompe compatibilidad>: <descripción en imperativo, minúscula, sin punto>

<cuerpo opcional: qué y por qué, no cómo>

<pie opcional: Refs: T012 · BREAKING CHANGE: … · Co-authored-by: …>
```

## Tipos
| Tipo | Úsalo para | Versión |
|---|---|---|
| `feat` | funcionalidad nueva para el usuario | minor |
| `fix` | corrección de un defecto | patch |
| `docs` | documentación y artefactos de Spec Kit (spec, plan, tasks) | — |
| `test` | agregar o corregir pruebas | — |
| `refactor` | cambio de código sin cambiar comportamiento | — |
| `perf` | mejora de rendimiento | patch |
| `build` | sistema de build, dependencias | — |
| `ci` | pipelines de CI | — |
| `chore` | mantenimiento que no encaja arriba | — |
| `style` | formato, sin cambio de lógica | — |
| `revert` | revertir un commit anterior | — |

`!` después del tipo/scope o un pie `BREAKING CHANGE:` → versión major.

## Scopes sugeridos
- Artefactos Spec Kit: `spec`, `plan`, `tasks`, `constitution`.
- Código: el módulo o componente del plan (`auth`, `api`, `ui`…). Usa los nombres que define `plan.md`.

## Ejemplos
```
docs(spec): add login with Google user stories
docs(plan): choose OAuth provider and session model
feat(auth): add Google OAuth callback endpoint

Refs: T014
test(auth): cover expired token on callback
fix(auth)!: require PKCE on all OAuth flows

BREAKING CHANGE: clients must send code_verifier
```

## Reglas
- Una intención por commit. Si necesitas "y" en la descripción, probablemente son dos commits.
- Descripción ≤ 72 caracteres.
- El idioma de los mensajes: el que ya use el historial del repo (`git log --oneline -20`); si no hay historial, inglés.
- El título del PR también es un Conventional Commit: es el mensaje final del squash.
