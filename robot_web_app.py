import network
import socket
from time import sleep

from robot_motor_controller import backward, forward, stop, turn_left, turn_right


AP_SSID = "PatchBot"
AP_IP = "192.168.4.1"


COMMANDS = {
    "/forward": ("Forward", forward),
    "/reverse": ("Reverse", backward),
    "/left": ("Left", turn_left),
    "/right": ("Right", turn_right),
    "/stop": ("Stop", stop),
}


HTML = """<!doctype html>
<html>
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>PatchBot</title>
  <style>
    body {
      margin: 0;
      min-height: 100vh;
      display: grid;
      place-items: center;
      font-family: Arial, sans-serif;
      background: #f4f7fb;
      color: #172033;
    }
    main {
      width: min(92vw, 420px);
    }
    h1 {
      margin: 0 0 18px;
      font-size: 32px;
      text-align: center;
    }
    .controls {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 12px;
    }
    button {
      min-height: 76px;
      border: 0;
      border-radius: 8px;
      background: #1f6feb;
      color: white;
      font-size: 18px;
      font-weight: 700;
      box-shadow: 0 4px 14px rgba(31, 111, 235, 0.24);
    }
    button:active {
      transform: translateY(1px);
    }
    .forward {
      grid-column: 2;
    }
    .left {
      grid-column: 1;
    }
    .stop {
      grid-column: 2;
      background: #d1242f;
      box-shadow: 0 4px 14px rgba(209, 36, 47, 0.24);
    }
    .right {
      grid-column: 3;
    }
    .reverse {
      grid-column: 2;
    }
    .status {
      margin-top: 18px;
      min-height: 24px;
      text-align: center;
      font-size: 16px;
    }
  </style>
</head>
<body>
  <main>
    <h1>PatchBot</h1>
    <section class="controls">
      <button class="forward" onclick="sendCommand('forward')">Forward</button>
      <button class="left" onclick="sendCommand('left')">Left</button>
      <button class="stop" onclick="sendCommand('stop')">Stop</button>
      <button class="right" onclick="sendCommand('right')">Right</button>
      <button class="reverse" onclick="sendCommand('reverse')">Reverse</button>
    </section>
    <div class="status" id="status">Ready</div>
  </main>
  <script>
    async function sendCommand(command) {
      const status = document.getElementById('status');
      status.textContent = 'Sending ' + command + '...';
      try {
        const response = await fetch('/' + command);
        status.textContent = await response.text();
      } catch (error) {
        status.textContent = 'Connection lost';
      }
    }
  </script>
</body>
</html>
"""


def start_access_point():
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid=AP_SSID)
    ap.ifconfig((AP_IP, "255.255.255.0", AP_IP, AP_IP))

    while not ap.active():
        sleep(0.1)

    print("Wi-Fi access point:", AP_SSID)
    print("Open http://{}/".format(ap.ifconfig()[0]))
    return ap


def response(client, status, content_type, body):
    if isinstance(body, str):
        body = body.encode()

    client.send("HTTP/1.1 {}\r\n".format(status))
    client.send("Content-Type: {}\r\n".format(content_type))
    client.send("Connection: close\r\n\r\n")
    client.send(body)


def handle_request(path):
    command = COMMANDS.get(path)
    if command:
        label, action = command
        action()
        return "200 OK", "text/plain", label

    if path == "/" or path == "/index.html":
        return "200 OK", "text/html", HTML

    return "404 Not Found", "text/plain", "Not found"


def run_server():
    stop()
    start_access_point()

    server = socket.socket()
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("0.0.0.0", 80))
    server.listen(2)
    print("Web server ready at http://{}/".format(AP_IP))

    while True:
        client, _address = server.accept()
        try:
            request = client.recv(1024).decode()
            request_line = request.split("\r\n", 1)[0]
            parts = request_line.split()
            path = parts[1] if len(parts) > 1 else "/"
            status, content_type, body = handle_request(path)
            response(client, status, content_type, body)
        except Exception as error:
            response(client, "500 Internal Server Error", "text/plain", str(error))
        finally:
            client.close()
