from typing import Any
from starlette import websockets as StarletteWebsockets
from starlite import Starlite, get, WebSocket, websocket


@get("/")
def hello_world() -> dict[str, Any]:
    return {"hello": "world"}


@websocket(path="/echo")
async def echo_websocket_handler(socket: WebSocket) -> None:
    await socket.accept()

    while True:
        try:
            data = await socket.receive_text()
        except StarletteWebsockets.WebSocketDisconnect:
            print(f"Websocket {socket.user} Disconnected")
            break
        await socket.send_text(data)

    await socket.close()


app = Starlite(route_handlers=[hello_world, echo_websocket_handler])
