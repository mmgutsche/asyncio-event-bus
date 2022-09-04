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

