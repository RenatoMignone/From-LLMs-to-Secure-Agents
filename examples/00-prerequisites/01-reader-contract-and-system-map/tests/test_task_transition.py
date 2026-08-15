import importlib.util
import sys
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).parents[1] / "task_transition.py"
SPEC = importlib.util.spec_from_file_location("task_transition", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)
create_task = MODULE.create_task


class TaskTransitionTest(unittest.TestCase):
    def setUp(self):
        self.request = {"action": "create_task", "task": {"title": "Send the brief"}}

    def test_authorized_request_changes_state_and_emits_event(self):
        result = create_task(self.request, {"tasks:create"})
        self.assertEqual(result.state["task-1"]["status"], "open")
        self.assertEqual(result.events, [{"type": "task.created", "task_id": "task-1"}])
        self.assertEqual(
            result.side_effect_requests,
            [{"type": "notification.requested", "task_id": "task-1"}],
        )

    def test_missing_permission_does_not_change_state(self):
        with self.assertRaises(PermissionError):
            create_task(self.request, set())


if __name__ == "__main__":
    unittest.main()
