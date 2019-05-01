import logging
import socketio
import pprint

from . import Controller, ControllerStatus, VolumeStatus

logger = logging.getLogger(__name__)


class VolumioController(Controller):
    min_vol = 0
    max_vol = 100

    def __init__(self, host: str, port: int = 3000):
        self._host = host
        self._port = port
        self._sio = socketio.AsyncClient()
        self._sio.on('pushState', self.handle_push_state)
        self._sio.on('connect', self.handle_connect)
        self._sio.on('disconnect', self.handle_disconnect)
        self.status = ControllerStatus(volume=VolumeStatus())

    async def connect(self):
        logger.debug('Attempting connection to %s:%s' % (self._host, self._port))
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
        logger.debug('Got state from %s: %s' % (self._host, pprint.pprint(state)))
        self.status.volume.value = state['volume']
        self.status.volume.mute = state['mute']

    def handle_connect(self):
        logger.info('Connected to %s' % self._host)

    def handle_disconnect(self):
        logger.info('Disconnected from %s' % self._host)

    async def get_volume(self) -> int:
        pass

    async def set_volume(self, value: int):
        if self.min_vol < value < self.max_vol:
            await self._sio.emit('volume', value)
        else:
            message = 'Got invalid volume %s. Should be between %s and %s.' % (value, self.min_vol, self.max_vol)
            logger.warning(message)
            raise ValueError(message)

    async def get_mute(self) -> bool:
        pass

    async def set_mute(self):
        pass

    async def set_unmute(self):
        pass
