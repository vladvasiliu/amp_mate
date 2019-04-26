import asyncio

from controller.volumio import VolumioController


if __name__ == '__main__':
    volumio = VolumioController('http://192.168.1.13', 3000)

    loop = asyncio.get_event_loop()

    loop.run_until_complete(volumio.connect())

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    loop.run_until_complete(volumio.disconnect())
    loop.stop()
