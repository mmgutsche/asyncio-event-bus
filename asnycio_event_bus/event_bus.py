import asyncio
from typing import Coroutine, Any, Callable
import weakref

class EventBus:

    def __init__(self):
        self._listeners = {}

    def add_listener(self, event_type: str, listener: Callable[..., Coroutine]) -> None:
        if event_type not in self._listeners:
            self._listeners[event_type] = []
        listener_ref = weakref.WeakMethod(listener)
        self._listeners[event_type].append(listener_ref)

    def post(self, event_type: str, event: Any) -> None:
        for listener_ref in self._listeners.get(event_type, []):
            listener = listener_ref()
            if listener is not None:
                asyncio.create_task(listener(event))
            else:
                self._listeners[event_type].remove(listener_ref)