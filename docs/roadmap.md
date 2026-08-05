# Roadmap Policy

The stable ordered unit queue is root `ROADMAP.md`. Operational state belongs in `PROJECT_STATUS.md`; completed-change history belongs in `CHANGELOG.md`.

## Rules

- Keep units in strict prerequisite order.
- Give every unit a stable identifier, dependencies, and completion criteria.
- Complete all architecture units before detailed security units.
- Change the queue only when curriculum structure changes. Do not use it as a changelog.
- The next unit is the first incomplete unit whose dependencies are complete and which has no recorded blocker.
- Resolve a unit to its chapter path by matching its numbered position and title to the nearest `chapter-plan.md` entry.
- Record the resolved path in `PROJECT_STATUS.md` before research begins.
