"""
Minimal Starlite websockets implementation.
"""

from starlette import websockets as starlette_websockets
from starlite import Starlite, WebSocket, get, websocket
from starlite.enums import MediaType


@get("/", media_type=MediaType.HTML)
def web_socket_testing() -> str:
    """
    Minimal functional example.
    """
    return """<html>
  <head>
    <title>Web Socket Testing</title>
  </head>
  <body>
    <p>Hello.</p>
    <label for="echo-input">Type something and press enter:</label>
    <input id="echo-input">
    <br>
    <label for="echo-response">Echo response:</label>
    <input id="echo-response">
  </body>
  <script>
// Create WebSocket connection.
const socket = new WebSocket('ws://localhost:8000/echo');

// Send a message
function sendMessage(message) {
    socket.send(message)
}

document.getElementById("echo-input").addEventListener("keyup", event => {
    if(event.key !== "Enter") return;
    sendMessage(event.target.value);
    event.preventDefault();
});

// Listen for messages
socket.addEventListener('message', function (event) {
    document.getElementById("echo-response").value = event.data;
});
  </script>
</html>
"""


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


app = Starlite(route_handlers=[web_socket_testing, echo_websocket_handler])
