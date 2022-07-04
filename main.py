from typing import Any
from starlite import Starlite, WebSocket, get, websocket
from starlette import websockets as starlette_websockets


@get("/")
def hello_world() -> dict[str, Any]:
    return {"hello": "world"}


@websocket(path="/echo")
async def echo_websocket_handler(socket: WebSocket) -> None:
    await socket.accept()

    while True:
        try:
            data = await socket.receive_text()
        except starlette_websockets.WebSocketDisconnect:
            print("Websocket Disconnected")
            return
        await socket.send_text(data)


app = Starlite(route_handlers=[hello_world, echo_websocket_handler])
