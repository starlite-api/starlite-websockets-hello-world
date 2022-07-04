"""
Minimal Starlite websockets implementation.
"""

from starlette import websockets as starlette_websockets
from starlite import Starlite, WebSocket, websocket


@websocket(path="/echo")
async def echo_websocket_handler(socket: WebSocket) -> None:
    """
    Receive and return text messages via `socket`.
    """
    await socket.accept()

    while True:
        try:
            data = await socket.receive_text()
        except starlette_websockets.WebSocketDisconnect:
            return
        await socket.send_text(data)


app = Starlite(route_handlers=[echo_websocket_handler])
