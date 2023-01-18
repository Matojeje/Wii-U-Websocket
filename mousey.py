import win32api
import asyncio
import websockets
import json
import ctypes
import mouse
import time


# https://stackoverflow.com/questions/1181464/controlling-mouse-with-python

async def main():
    uri = "ws://localhost:8080"
    last = (-1, -1)
    lastPress = time.time()
    async with websockets.connect(uri) as websocket:
        while True:
            message = await websocket.recv()
            data = json.loads(message)["wiiUGamePad"]
            # print(f"Received message: {data}")
            # print(data["touched"])
            if data["touched"] == 0:
                if data["drag"] == 1:
                    mouse.release()
                    touchLength = time.time() - lastPress
                    if touchLength < 0.1:
                        mouse.click()
            else:
                if data["valid"] == 0:
                    current = (
                        round(data["x"] / 854 * 1920),
                        round(data["y"] / 480 * 1080)
                    )
                    if current != last:
                        # win32api.SetCursorPos(current)
                        mouse.move(current[0], current[1], duration=(0.005 if data["smooth"] == 1 else 0))
                        last = current

                    if data["drag"] == 1:
                        if not mouse.is_pressed():
                            mouse.press()
                            lastPress = time.time()
                    elif mouse.is_pressed():
                        mouse.release()

asyncio.run(main())
