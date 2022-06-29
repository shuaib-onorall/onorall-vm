import asyncio
import websockets


async def handler(websocket):
    while True:
        message = await websocket.recv()
        print(message , '.......................................')


async def main():
    url = "ws://localhost:8000/ws/new/"
    async with websockets.connect(url) as ws:
        print(';;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;')
        await handler(ws)
        await asyncio.Future()  # run forever
    async with websockets.disconnect(url) as ws:
      print('88888888888888888888888888888')


if __name__ == "__main__":
    print(';;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;===================================')
    asyncio.run(main())