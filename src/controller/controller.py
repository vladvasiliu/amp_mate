class ControllerStatus:
    """Holds last known status of the controller

    The controller is asynchronous,
    so it's not possible to return the exact status of the device at the time of the function call.
    """


class Controller:
    """This is an interface to control remote devices, such as Amp or Player. It uses asyncio.

    Numeric values are normalised: 0 is min, 100 is max.
    Implementation should handle conversion

    The controller is asynchronous,
    so it's not possible to return the exact status of the device at the time of the function call.
    The implementation should probably manage some sort of internal "cache" / last known good status.
    """

    async def __aenter__(self):
        raise NotImplementedError

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        raise NotImplementedError

    async def get_volume(self) -> int:
        raise NotImplementedError

    async def set_volume(self, value: int):
        raise NotImplementedError

    async def get_mute(self) -> bool:
        raise NotImplementedError

    async def set_mute(self):
        raise NotImplementedError

    async def set_unmute(self):
        raise NotImplementedError
