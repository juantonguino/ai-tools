# Plantilla de cuerpo de PR

Rellena con datos reales; no dejes secciones con texto de relleno. Borra una sección solo si de verdad no aplica.

```markdown
## Qué
<1–3 líneas: qué entrega esta feature para el usuario, tomado de spec.md>

## Artefactos de Spec Kit
- Spec: `<ruta>/spec.md`
- Plan: `<ruta>/plan.md`
- Tareas: `<ruta>/tasks.md` (<completadas>/<total>)

## Criterios de aceptación
| Criterio | Prueba | Resultado |
|---|---|---|
| <criterio de spec.md> | <archivo::test> | ✅ / ❌ |

## Verificación
- Comando de pruebas: `<comando>` → <resultado real>
- `converge`: Converged
- Build / lint: <resultado real>

## Decisiones y riesgos
<decisiones del plan que el revisor debe conocer; deuda o riesgos abiertos>

## Fuera de alcance
<lo que la spec dejó explícitamente fuera>
```
