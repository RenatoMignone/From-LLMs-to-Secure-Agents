# Roadmap Policy

The stable ordered unit queue is root `ROADMAP.md`. Operational state belongs in `PROJECT_STATUS.md`; completed-change history belongs in `CHANGELOG.md`.

## Rules

- Keep units in strict prerequisite order.
- Maintain a concise main path and label optional deep-dive branches in their plans. A deep dive cannot become an undeclared prerequisite of the main path.
- The authoring queue includes deep dives for completeness; reader navigation collapses them by default.
- Give every unit a stable identifier, dependencies, and completion criteria.
- Complete all architecture units before detailed security units.
- Change the queue only when guide structure changes. Do not use it as a changelog.
- The validator resolves every unit identifier to exactly one planned chapter path and rejects title or filename drift.
- The next unit is the item immediately after `completed_through`, unless the current unit must be resumed.
- Use `scripts/project_state.py start` to record the resolved unit and path before research begins.
- Do not skip units. Record a blocker instead.
