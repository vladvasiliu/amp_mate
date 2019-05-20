import asyncio
import logging
import os
import threading
from typing import Iterable

from controller import Controller, VolumioController

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class Master:
    """This ties the different controllers together.

    The controllers are asynchronous. The Master runs its own event loop and runs the controllers inside it.
    """

    def __init__(self, controllers: Iterable[Controller]):
        self._controllers = controllers
        self.loop = asyncio.get_event_loop()
        self._async_runner = None

    def __enter__(self):
        self.run()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    async def _connect(self):
        logger.debug("Starting master.")
        for c in self._controllers:
            await c.connect()

    async def _disconnect(self):
        logger.info("Stopping master")
        for c in self._controllers:
            await c.disconnect()

    def run(self):
        self.loop.run_until_complete(self._connect())
        self.loop.run_forever()

    def stop(self):
        logger.info("Stopping master (got ^C).")
        self.loop.run_until_complete(self._disconnect())
        self.loop.stop()


if __name__ == "__main__":
    VOLUMIO_HOST = os.getenv("VOLUMIO_HOST")
    volumio = VolumioController(VOLUMIO_HOST, 3000)

    master = Master([volumio])
    try:
        master.run()
    except KeyboardInterrupt:
        master.stop()
