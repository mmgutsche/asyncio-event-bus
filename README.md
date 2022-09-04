# Asyncio Event Bus

Asyncio Event Bus provides a simple event system which can be used with async functions.

Python provides a great asyncio library, but it lacks an event system for your application. This library aims to provide a simple event system which can be used with async functions.
The code has no dependencies and is written in pure python and is fully type hinted.
It uses weakrefs internally to avoid memory leaks, and you do not have to worry about unsubscribing from events.

## Usage



```python
import asyncio

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




if __name__ == "__main__":
    event_bus = EventBus()
    event_generator = SomeEventGenerator(event_bus)
    listener: SomeListener = SomeListener()
    event_bus.add_listener("my_event", listener.on_event)
    asyncio.run(event_generator.generate())

```

