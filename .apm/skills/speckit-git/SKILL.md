---
name: speckit-git
description: Use when you need to do any git operation in a project that uses GitHub Spec Kit — create or switch the feature branch, commit after a Spec Kit phase or a task, sync with main, open or merge a pull request, tag a release, or resolve conflicts. Applies GitHub Flow, Conventional Commits and squash merge, and says which operations need the user's confirmation.
---

# Git para proyectos con Spec Kit

Política del proyecto (no la cambies sin que el usuario lo pida):

| Tema | Regla |
|---|---|
| Modelo de ramas | **GitHub Flow**: `main` siempre estable; una rama por feature de Spec Kit |
| Nombre de rama | El de la carpeta de la feature (`001-nombre-corto`), igual al que crea la extensión git de Spec Kit |
| Commits | **Conventional Commits** (LOAD `references/conventional-commits.md`) |
| Integración | **Pull request + squash merge** a `main` con `gh` |
| Autonomía | Ramas y commits locales: sí. Push, PR, merge, tags y reescritura de historial: **solo con confirmación** |

## Niveles de autonomía

| Sin confirmación | Con confirmación del usuario | Nunca |
|---|---|---|
| `git status`, `diff`, `log`, `fetch` | `git push` (incluida la primera) | Commit directo en `main` |
| Crear/cambiar a la rama de la feature | Crear, editar o fusionar un PR | `git push --force` (sin `--with-lease`) |
| `git add` + `git commit` en la rama de la feature | `git rebase` de una rama ya publicada | `--no-verify` para saltar hooks |
| `git merge origin/main` en la rama de la feature (sin conflictos) | `git push --force-with-lease` sobre la rama propia | Reescribir commits que ya están en `main` |
| `git stash` temporal | Crear o borrar tags; borrar ramas remotas | Commitear secretos (`.env`, llaves, tokens) |
| | `git reset --hard`, `git clean`, descartar cambios | |

**Pedir confirmación**: si corres como subagente y no puedes preguntar al usuario, NO ejecutes la operación. Termina y devuelve el comando exacto que propones y por qué, para que el agente principal lo confirme con el usuario.

## Paso 0 — Diagnóstico (siempre)
```bash
git status --short --branch
git remote -v
git log --oneline -5
```
- Lee `.specify/feature.json` para saber la feature activa.
- Revisa si la extensión git de Spec Kit está instalada (existe `.specify/extensions/git/`). Si está, ella crea la rama en `specify` y puede hacer auto-commit: no lo dupliques.
- Si hay cambios sin commitear que no son de esta tarea, DETENTE y repórtalo.

## Flujo por fase de Spec Kit

| Fase | Rama | Commit (tipo y scope) |
|---|---|---|
| constitution | `main` solo si es el commit inicial del proyecto; si no, rama `chore/constitution` + PR | `docs(constitution): …` |
| specify | crear rama de la feature (ver abajo) | `docs(spec): …` |
| clarify / checklist | rama de la feature | `docs(spec): …` |
| plan | rama de la feature | `docs(plan): …` |
| tasks / analyze | rama de la feature | `docs(tasks): …` |
| implement | rama de la feature | un commit por tarea o grupo pequeño: `feat`, `fix`, `refactor`… con `Refs: T0XX` |
| pruebas (tester) | rama de la feature | `test(<scope>): …` |
| converge | rama de la feature | commits de las tareas nuevas, igual que implement |

Si la extensión git tiene auto-commit activo para una fase, no hagas un segundo commit de lo mismo.

### Crear la rama de la feature
Antes de ejecutar `specify`, haya o no extensión git, parte de `main` actualizado. La extensión crea la rama
desde donde estés (`git checkout -b`): si estás en otra feature, la nueva saldría de esa rama.
```bash
git fetch origin
git switch main && git pull --ff-only origin main
```
Si la extensión git NO crea la rama, créala tú después:
```bash
git switch -c <nombre-carpeta-feature>     # ej. 001-login-google
```
Si la rama ya existe: `git switch <rama>`. Nunca trabajes la feature en `main`.

### Hacer un commit
1. `git diff --staged` y `git status`: agrega solo archivos de la tarea (`git add <rutas>`, no `git add -A` a ciegas).
2. Revisa que no entren secretos ni archivos generados (`.env`, `*.pem`, `node_modules/`, `dist/`). Si los ves, sácalos del stage y avisa.
3. Mensaje en Conventional Commits; en implement incluye el ID de la tarea en el pie (`Refs: T012`).
4. Si un hook de pre-commit falla, corrige la causa; no lo saltes.

### Sincronizar con main
```bash
git fetch origin
git merge origin/main        # preferido: no reescribe historial; el squash final deja main limpio
```
Usa `git rebase origin/main` solo si la rama nunca se ha publicado, o con confirmación (luego requiere `--force-with-lease`).

### Conflictos
1. `git status` para listar archivos en conflicto.
2. Código: resuelve conservando la intención de ambos lados; corre build y pruebas después.
3. Artefactos de Spec Kit (`spec.md`, `plan.md`, `tasks.md`, constitución): NO los resuelvas tú; DETENTE y reporta el conflicto al agente dueño (producto, arquitecto).
4. Si no estás seguro: `git merge --abort` y reporta.

## Pull request (con confirmación)
Requisitos antes de proponerlo: `converge` reporta `Converged`, las pruebas pasan, la rama está sincronizada con `main`.
```bash
git push -u origin <rama>
gh pr create --base main --head <rama> --title "<tipo>(<scope>): <resumen>" --body-file <archivo>
```
Arma el cuerpo con LOAD `references/pr-template.md`. El título del PR será el mensaje del squash, así que debe ser un Conventional Commit válido.

## Merge (con confirmación)
```bash
gh pr checks <número>                 # todo en verde
gh pr merge <número> --squash --delete-branch
gh pr view <número> --json state      # debe ser MERGED antes de seguir
git switch main && git pull --ff-only origin main
git branch -D <rama>                  # solo si aún existe localmente y el PR está MERGED
```
Con squash merge los commits de la rama no quedan en `main`, así que `git branch -d` falla con
"not fully merged". Usa `-D`, pero solo después de confirmar que el PR está `MERGED`.

## Release (opcional, con confirmación)
Tags semver anotados sobre `main`: `git tag -a vX.Y.Z -m "vX.Y.Z"` y `git push origin vX.Y.Z`. La versión sale de los commits desde el último tag: `feat` → minor, `fix` → patch, `!`/`BREAKING CHANGE` → major.

## Quién hace qué
- `speckit-product`, `speckit-architect`: commits de sus artefactos en la rama de la feature.
- `speckit-developer`: crea/usa la rama de la feature y hace los commits de código.
- `speckit-tester`: commits solo de pruebas.
- Push, PR, merge y tags: el agente principal, después de confirmar con el usuario.

## Configuración recomendada de la extensión git
Si el proyecto usa `specify extension add git`, copia `assets/git-config.yml` a `.specify/extensions/git/git-config.yml` (con confirmación si ya existe uno).
