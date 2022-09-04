import asyncio

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

