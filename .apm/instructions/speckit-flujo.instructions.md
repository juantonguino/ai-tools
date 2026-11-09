---
description: "Cómo coordinar los subagentes de Spec Kit (product → architect → developer → tester)"
applyTo: "**"
---

# Flujo Spec Kit con subagentes

Este proyecto usa GitHub Spec Kit con cuatro subagentes. Como agente principal, tú coordinas el flujo y
hablas con el usuario. No hagas tú el trabajo de un subagente: invócalo.

## Orden

1. **`speckit-product`**: cuando el usuario describa una funcionalidad nueva o pida cambiar requisitos.
   Para una funcionalidad nueva, la rama debe salir de `main` actualizado (skill `speckit-git`).
2. **Punto de control**: muestra al usuario el resumen de la spec y pide su aprobación antes de seguir.
3. **`speckit-architect`**: con la spec aprobada, genera plan y tareas.
4. **Punto de control**: muestra las decisiones de arquitectura y pide aprobación antes de implementar.
5. **`speckit-developer`**: implementa `tasks.md`.
6. **`speckit-tester`**: verifica y ejecuta `converge`.
7. Si `converge` agrega tareas, vuelve al paso 5 con esas tareas. Tras 3 ciclos sin converger,
   detente y consulta al usuario en vez de seguir iterando.
8. **Integración**: con `Converged` y pruebas en verde, propón al usuario push y pull request siguiendo
   la skill `speckit-git` (squash merge a `main`). Ejecuta push, PR y merge solo cuando el usuario lo confirme.

## Al invocar un subagente

- Cada subagente arranca sin contexto: pásale la petición del usuario, la feature activa y lo que
  devolvió el agente anterior.
- Si un subagente devuelve preguntas o decisiones pendientes, házselas al usuario tal cual (con las
  opciones y la recomendación que trae) y vuelve a invocarlo con las respuestas. No las respondas tú.
- Si un subagente devuelve un comando git que necesita confirmación (push, PR, merge, tags, rebase),
  confírmalo con el usuario y ejecútalo tú; no se lo devuelvas al subagente.
- Si un subagente se detiene y señala a otro (por ejemplo, "falta la spec → speckit-product"),
  sigue esa indicación en lugar de saltarte el paso.
- Antes de dar la feature por terminada, comprueba que el tester reportó `Converged` y pruebas en verde,
  con la salida real de los comandos.
