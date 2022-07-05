"""
Minimal Starlite websockets implementation.
"""
import logging

from pydantic import BaseModel
from starlite import Starlite, get
from starlite.enums import MediaType
from starlite.handlers import ws_message

logger = logging.getLogger("uvicorn.error")


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
    sendMessage(JSON.stringify({data: event.target.value}));
    event.preventDefault();
});

// Listen for messages
socket.addEventListener('message', function (event) {
    console.log(event);
    document.getElementById("echo-response").value = JSON.parse(event.data).data;
});
  </script>
</html>
"""


class Data(BaseModel):
    """Model for websocket in/out"""

    data: str


@ws_message(path="/echo")
async def echo_websocket_handler(data: Data) -> Data:
    """
    Echo the payload.
    """
    return data


app = Starlite(route_handlers=[web_socket_testing, echo_websocket_handler])
