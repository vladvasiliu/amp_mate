import asyncio
import socketio


class VolumioConnector:
    def __init__(self, host: str, port: str = 3000):
        self._host = host
        self._port = port
        self.sio = socketio.AsyncClient()
        self.sio.on("pushState", self.handle_push_state)
        self.sio.on("connect", self.handle_connect)
        self.sio.on("disconnect", self.handle_disconnect)

    async def connect(self):
        await self.sio.connect("%s:%s" % (self._host, self._port))
        await self.get_state()

    async def disconnect(self):
        await self.sio.disconnect()

    async def get_state(self):
        await self.sio.emit("getState")

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.disconnect()

    def handle_push_state(self, state: dict):
        print("got state from %s:" % self._host)
        print(state)

    def handle_connect(self):
        print("Connected to %s" % self._host)

    def handle_disconnect(self):
        print("Disconnected from %s" % self._host)


async def work():
    async with VolumioConnector("http://192.168.1.13") as vc:
        await vc.sio.wait()


if __name__ == "__main__":
    asyncio.run(work())
