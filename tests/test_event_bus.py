import asyncio
import gc

import pytest as pytest

from asyncio_event_bus import EventBus



class Listener:

    def __init__(self):
        self.events = []

    async def on_event(self, event: str) -> None:
        self.events.append(event)



@pytest.mark.asyncio
async def test_event_bus():
    event_bus = EventBus()
    listener = Listener()

    event_bus.add_listener("my_event", listener.on_event)
    for k in range(10):
        event_bus.post("my_event", f"Event {k}")
    # wait for all events to be processed
    coros = asyncio.all_tasks()
    # exclude the current coroutine
    coros.remove(asyncio.current_task())
    await asyncio.wait_for(asyncio.gather(*coros), 1.0)
    expected_res = [f"Event {k}" for k in range(10)]
    assert listener.events == expected_res

def temporary_function(event_bus: EventBus) -> list:
    listener = Listener()

    event_bus.add_listener("my_event", listener.on_event)
    for k in range(10):
        event_bus.post("my_event", f"Event {k}")
    gc.collect()
    refs = gc.get_referrers(listener.on_event)
    return refs


@pytest.mark.asyncio
async def test_automatic_listener_cleanup():
    event_bus = EventBus()
    refs = temporary_function(event_bus)
    print(refs)
    # wait for all events to be processed
    coros = asyncio.all_tasks()
    # exclude the current coroutine
    coros.remove(asyncio.current_task())
    await asyncio.wait_for(asyncio.gather(*coros), 1.0)
    assert len(event_bus._listeners["my_event"]) == 1
    assert event_bus._listeners["my_event"][0] is not None
    # as soon as another event is triggered event bus cleans up invalid references, so let's fire another one
    event_bus.post("my_event", f"Event Clean")
    assert len(event_bus._listeners["my_event"]) == 0
    assert len(refs) == 0
