#!/usr/bin/env python3
"""Comprueba las convenciones de los agentes en .apm/agents/.

- Los bloques que se repiten a propósito deben ser idénticos en todos los agentes.
- Ningún agente declara `tools:` en el frontmatter (ver AGENTS.md: cada target exige otro formato).

Uso: python3 scripts/check-agents.py  (sale con código 1 si algo falla). Ejecutar antes de cada commit.
"""

import re
import sys
from pathlib import Path

AGENTS_DIR = Path(__file__).resolve().parent.parent / ".apm" / "agents"

# Secciones que deben ser idénticas en todos los agentes.
SHARED_SECTIONS = ["Preguntas al usuario", "Límites de seguridad"]
# En esta sección solo se compara la parte común (tabla y viñetas), no los comandos de cada rol.
COMMANDS_SECTION = "Cómo ejecutar los comandos de Spec Kit"
COMMANDS_SPLIT = re.compile(r"\nComandos? que te corresponde")

SECTION_RE = re.compile(r"^## ([^\n]+)\n(.*?)(?=^## |\Z)", re.S | re.M)
FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.S)


def sections(text: str) -> dict[str, str]:
    return {m.group(1).strip(): m.group(2).strip() for m in SECTION_RE.finditer(text)}


def main() -> int:
    files = sorted(AGENTS_DIR.glob("*.agent.md"))
    if not files:
        print(f"ERROR: no hay agentes en {AGENTS_DIR}")
        return 1

    errors: list[str] = []
    parsed: dict[str, dict[str, str]] = {}
    for f in files:
        text = f.read_text(encoding="utf-8")
        fm = FRONTMATTER_RE.match(text)
        if fm and re.search(r"^tools\s*:", fm.group(1), re.M):
            errors.append(f"{f.name}: declara `tools:` en el frontmatter (no usarlo, ver AGENTS.md)")
        parsed[f.name] = sections(text)

    checks = [(name, lambda body: body) for name in SHARED_SECTIONS]
    checks.append((COMMANDS_SECTION, lambda body: COMMANDS_SPLIT.split(body)[0].strip()))

    for name, normalize in checks:
        versions: dict[str, list[str]] = {}
        for agent, secs in parsed.items():
            if name not in secs:
                errors.append(f"{agent}: falta la sección '## {name}'")
                continue
            versions.setdefault(normalize(secs[name]), []).append(agent)
        if len(versions) > 1:
            groups = " | ".join(", ".join(agents) for agents in versions.values())
            errors.append(f"'## {name}' no es idéntica en todos los agentes: {groups}")

    if errors:
        print("Convenciones de agentes: FALLÓ")
        for e in errors:
            print(f"  - {e}")
        return 1
    print(f"Convenciones de agentes: OK ({len(files)} agentes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
