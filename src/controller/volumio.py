import socketio

from . import Controller


class VolumioController(Controller):
    def __init__(self, host: str, port: int = 3000):
        self._host = host
        self._port = port
        self._sio = socketio.AsyncClient()
        self._sio.on('pushState', self.handle_push_state)
        self._sio.on('connect', self.handle_connect)
        self._sio.on('disconnect', self.handle_disconnect)

    async def connect(self):
        await self._sio.connect('%s:%s' % (self._host, self._port))
        await self._get_state()

    async def disconnect(self):
        await self._sio.disconnect()

    async def _get_state(self):
        await self._sio.emit('getState')

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.disconnect()

    def handle_push_state(self, state: dict):
        print("got state from %s:" % self._host)
        print(state)

    def handle_connect(self):
        print('Connected to %s' % self._host)

    def handle_disconnect(self):
        print('Disconnected from %s' % self._host)

    async def get_volume(self) -> int:
        pass

    async def set_volume(self, value: int):
        pass

    async def get_mute(self) -> bool:
        pass

    async def set_mute(self):
        pass

    async def set_unmute(self):
        pass
