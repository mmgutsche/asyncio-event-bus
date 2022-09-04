import asyncio
import sys
import time
import weakref
from typing import Any

from asnycio_event_bus.event_bus import EventBus


class SomeListener:

    async def on_event(self, event: str) -> None:
        print(event)


class SomeEventGenerator:

    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus

    async def generate(self):
        for i in range(10):
            self.event_bus.post("my_event", f"Event {i}")


def count_refs(obj: Any):
    print("Hard count:", sys.getrefcount(obj))
    print("Weak count:", weakref.getweakrefcount(obj))


def intermediate(event_bus: EventBus):
    listener: SomeListener = SomeListener()

    event_bus.add_listener("my_event", listener.on_event)
    print(len(event_bus._listeners["my_event"]))
    count_refs(listener.on_event)
    event_generator = SomeEventGenerator(event_bus)
    asyncio.run(event_generator.generate())
    print(len(event_bus._listeners["my_event"]))



if __name__ == "__main__":
    event_bus = EventBus()
    intermediate(event_bus)
    event_generator = SomeEventGenerator(event_bus)
    asyncio.run(event_generator.generate())

    print(len(event_bus._listeners["my_event"]))


    # count_refs(listener.on_event)
    # event_bus.remove_listener("my_event", listener.on_event)