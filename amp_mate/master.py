from typing import Iterable

from controller import Controller


class Master:
    """This ties the different controllers together.

    The controllers are asynchronous. The Master runs its own event loop and runs the controllers inside it.
    """
    def __init__(self, controllers: Iterable[Controller]):
        self._controllers = controllers

    async def __aenter__(self):
        self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    def connect(self):
        for c in self._controllers:
            c.connect()

    def disconnect(self):
        for c in self._controllers:
            c.disconnect()
