import asyncio
import os

from controller import VolumioController

if __name__ == '__main__':
    VOLUMIO_HOST = os.getenv('VOLUMIO_HOST')

    volumio = VolumioController(VOLUMIO_HOST, 3000)

    loop = asyncio.get_event_loop()

    loop.run_until_complete(volumio.connect())

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    loop.run_until_complete(volumio.disconnect())
    loop.stop()
