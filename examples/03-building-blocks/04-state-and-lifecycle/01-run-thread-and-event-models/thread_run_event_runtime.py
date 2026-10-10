#!/usr/bin/env python3
"""Offline thread/run/event demonstration. All state is in memory."""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum, auto
import json

class RunStatus(Enum):
    QUEUED = auto()
    IN_PROGRESS = auto()
    REQUIRES_ACTION = auto()
    COMPLETED = auto()
    FAILED = auto()

class EventType(Enum):
    USER_MESSAGE = 'user.message'
    PLAN_RECORDED = 'plan.recorded'
    TOOL_CALL_REQUESTED = 'tool.call.requested'
    TOOL_EXECUTION_COMPLETED = 'tool.execution.completed'
    RUN_STATE_CHANGED = 'run.state.changed'
    AGENT_MESSAGE = 'agent.message'

@dataclass
class Event:
    event_id: str
    event_type: EventType
    timestamp: str
    thread_id: str
    run_id: str
    payload: dict

@dataclass
class ThreadState:
    thread_id: str
    variables: dict = field(default_factory=dict)
    messages: list = field(default_factory=list)
    event_history: list = field(default_factory=list)
    version: int = 0

    def apply_event(self, event):
        if event.thread_id != self.thread_id:
            raise ValueError('Event belongs to a different thread')
        self.event_history.append(event)
        self.version += 1
        if event.event_type in (EventType.USER_MESSAGE, EventType.AGENT_MESSAGE):
            role = 'user' if event.event_type == EventType.USER_MESSAGE else 'assistant'
            self.messages.append({'role': role, 'content': event.payload['content']})
        elif event.event_type == EventType.TOOL_EXECUTION_COMPLETED:
            self.variables[event.payload['store_as']] = event.payload['result']

class AgentRuntime:
    def __init__(self, tools):
        self.tools, self.threads, self.run_ids = tools, {}, set()
        self.counter = 0

    def get_or_create_thread(self, thread_id):
        return self.threads.setdefault(thread_id, ThreadState(thread_id))

    def emit(self, thread, run_id, kind, payload):
        self.counter += 1
        thread.apply_event(Event(f'evt_{self.counter:04d}', kind,
            datetime.now(timezone.utc).isoformat(), thread.thread_id, run_id, payload))

    def create_and_execute_run(self, thread_id, run_id, user_prompt):
        if run_id in self.run_ids:
            raise ValueError('Run ID already exists')
        self.run_ids.add(run_id)
        thread = self.get_or_create_thread(thread_id)
        def status(value):
            self.emit(thread, run_id, EventType.RUN_STATE_CHANGED, {'status': value.name})
        status(RunStatus.QUEUED)
        self.emit(thread, run_id, EventType.USER_MESSAGE, {'content': user_prompt})
        status(RunStatus.IN_PROGRESS)
        # An explicit mock plan, not hidden model reasoning.
        self.emit(thread, run_id, EventType.PLAN_RECORDED, {'plan': 'Read lamp stock'})
        status(RunStatus.REQUIRES_ACTION)
        self.emit(thread, run_id, EventType.TOOL_CALL_REQUESTED,
                  {'tool_name': 'lookup_stock', 'tool_args': {'sku': 'lamp'}})
        try:
            handler = self.tools['lookup_stock']
            result = handler({'sku': 'lamp'})
        except (KeyError, RuntimeError) as exc:
            self.emit(thread, run_id, EventType.AGENT_MESSAGE,
                      {'content': f'Stock could not be checked: {type(exc).__name__}'})
            status(RunStatus.FAILED)
            return RunStatus.FAILED
        self.emit(thread, run_id, EventType.TOOL_EXECUTION_COMPLETED,
                  {'result': result, 'store_as': 'stock_observation'})
        status(RunStatus.IN_PROGRESS)
        self.emit(thread, run_id, EventType.AGENT_MESSAGE,
                  {'content': f"Observed stock: {result['available']}. No reservation made."})
        status(RunStatus.COMPLETED)
        return RunStatus.COMPLETED

def main():
    runtime = AgentRuntime({'lookup_stock': lambda args: {'sku': args['sku'], 'available': 4}})
    for number in (1, 2):
        assert runtime.create_and_execute_run('lee-shop', f'run_{number}', 'Check lamp stock') == RunStatus.COMPLETED
    thread = runtime.threads['lee-shop']
    assert len(thread.messages) == 4
    assert thread.version == len(thread.event_history)
    assert len({e.event_id for e in thread.event_history}) == thread.version
    replay = ThreadState('lee-shop')
    for event in thread.event_history:
        replay.apply_event(event)  # Reducer only; no tool invocation during replay.
    assert replay.variables == thread.variables and replay.messages == thread.messages
    try:
        runtime.create_and_execute_run('lee-shop', 'run_1', 'Duplicate')
    except ValueError:
        pass
    else:
        raise AssertionError('Duplicate run accepted')
    missing = AgentRuntime({})
    assert missing.create_and_execute_run('lee-shop', 'failed_1', 'Check stock') == RunStatus.FAILED
    assert 'stock_observation' not in missing.threads['lee-shop'].variables
    print(json.dumps({'thread': thread.thread_id, 'runs': 2, 'events': thread.version,
                      'messages': thread.messages, 'missing_handler_status': 'FAILED'}, indent=2))

if __name__ == '__main__':
    main()
