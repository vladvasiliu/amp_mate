import asyncio
from asyncio import StreamWriter, StreamReader


def get_input():
    msg = input('? ')
    return msg


async def read_from_amp(reader: StreamReader):
    while True:
        data = await reader.readuntil(b'$')
        print(f'Received: {data.decode()!r}')


async def write_to_amp(writer: StreamWriter):
    while True:
        loop = asyncio.get_running_loop()
        print("waiting for message...")
        msg = await loop.run_in_executor(None, get_input)
        # msg = await q.get()
        writer.write(msg.encode())
        # q.task_done()
        print("sent %s to amp" % msg)


async def tcp_echo_client():
    reader, writer = await asyncio.open_connection('rotel', 9590)

    writer.write('rs232_update_on!'.encode())
    writer.write('vol_up!'.encode())

    await asyncio.gather(
        read_from_amp(reader),
        write_to_amp(writer),
    )

    print('Close the connection')
    writer.close()
    await writer.wait_closed()


asyncio.run(tcp_echo_client())
