import network
import socket
import wifi_manager
import time
from machine import Pin, SoftI2C
from neopixel import NeoPixel
import dht
from ssd1306 import SSD1306_I2C

pin = Pin(48, Pin.OUT)
neo = NeoPixel(pin, 1)

dht_pin = Pin(4)
sensor = dht.DHT11(dht_pin)

i2c = SoftI2C(scl=Pin(9), sda=Pin(8))
oled = SSD1306_I2C(128, 64, i2c)

def display_message_on_oled(msg):
    oled.fill(0)
    max_chars_per_line = 16
    max_chars_total = 64
    msg = msg[:max_chars_total]
    words = msg.split(" ")
    lines = []
    current_line = ""
    for word in words:
        if len(current_line) + len(word) + 1 <= max_chars_per_line:
            current_line += (" " if current_line else "") + word
        else:
            lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    y = 0
    for line in lines[:4]:
        oled.text(line, 5, y)
        y += 16
    oled.show()

display_message_on_oled("I AM SHEERAZ")
print("I AM SHEERAZ")

r = g = b = 0
try:
    sensor.measure()
    temp = str(sensor.temperature())
    humidity = str(sensor.humidity())
    print("Temperature:", temp, "°C")
    print("Humidity:", humidity, "%")
except Exception as e:
    print("Sensor Error:", e)
    temp = "N/A"
    humidity = "N/A"

#SSID = "Heart Snatcher"
#PASS = "iaminvincible07"
SSID = "Link"
PASS = "Pa$$word"

wifi_manager.connect_to_wifi(SSID,PASS)

wifi_manager.start_access_point("sherry-esp","connected")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("0.0.0.0", 80))
s.listen(5)

def web_page(r=0, g=0, b=0, temp="N/A", humidity="N/A"):
    hex_color = '#{:02x}{:02x}{:02x}'.format(r, g, b)
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>ESP32 RGB & OLED Dashboard</title>
    <style>
        body {{
            font-family: 'Segoe UI', sans-serif;
            text-align: center;
            background: {hex_color};
            transition: background 0.3s ease;
            margin: 0; padding: 0;
        }}
        .container {{
            width: 90%;
            max-width: 500px;
            margin: 5vh auto;
            padding: 5vw;
            background: rgba(255,255,255,0.9);
            border-radius: 12px;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
        }}
        h1 {{ color: #333; margin-bottom: 10px; font-size: 1.8em; }}
        p {{ font-size: 1.1em; color: #555; }}
        label {{ font-weight: bold; display: block; margin-top: 10px; }}
        .slider {{
            width: 100%;
            max-width: 300px;
        }}
        .color-preview {{
            width: 60px; height: 60px;
            margin: 10px auto;
            background-color: {hex_color};
            border-radius: 50%;
            border: 2px solid #888;
            transition: background-color 0.3s ease;
        }}
        input[type="number"] {{
            width: 60px;
            margin-left: 10px;
        }}
        input[type="text"] {{
            padding: 10px;
            width: 90%;
            max-width: 300px;
            margin-top: 15px;
            font-size: 1em;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🌈 ESP32 RGB Controller <br> Temperature and Humidity Monitor</h1>
        <p id="sensorData">🌡️ Temperature: {temp}°C &nbsp;&nbsp; 💧 Humidity: {humidity}%</p>
        <div class="color-preview" id="colorCircle"></div>

        <label>🔴 Red:</label>
        <input class="slider" type="range" id="red" min="0" max="255" value="{r}" oninput="updateRGB('red')">
        <input type="number" id="redValue" min="0" max="255" value="{r}" oninput="syncRGB('red')">

        <label>🟢 Green:</label>
        <input class="slider" type="range" id="green" min="0" max="255" value="{g}" oninput="updateRGB('green')">
        <input type="number" id="greenValue" min="0" max="255" value="{g}" oninput="syncRGB('green')">

        <label>🔵 Blue:</label>
        <input class="slider" type="range" id="blue" min="0" max="255" value="{b}" oninput="updateRGB('blue')">
        <input type="number" id="blueValue" min="0" max="255" value="{b}" oninput="syncRGB('blue')">

        <h2>📺 OLED Display</h2>
        <input type="text" id="msg" placeholder="Enter message (Max 64 chars)" maxlength="64" oninput="sendMessage()">
    </div>

    <script>
        function updateRGB(color) {{
            let value = document.getElementById(color).value;
            document.getElementById(color + "Value").value = value;
            syncAll();
        }}
        function syncRGB(color) {{
            let value = parseInt(document.getElementById(color + "Value").value);
            value = Math.min(255, Math.max(0, value));
            document.getElementById(color).value = value;
            syncAll();
        }}
        function syncAll() {{
            let r = document.getElementById("red").value;
            let g = document.getElementById("green").value;
            let b = document.getElementById("blue").value;
            fetch("/?r=" + r + "&g=" + g + "&b=" + b);
            let colorHex = "#" + [r,g,b].map(x => ("0" + parseInt(x).toString(16)).slice(-2)).join('');
            document.getElementById("colorCircle").style.backgroundColor = colorHex;
            document.body.style.backgroundColor = colorHex;
        }}
        function sendMessage() {{
            let msg = document.getElementById("msg").value;
            fetch("/?msg=" + encodeURIComponent(msg));
        }}

        setInterval(() => {{
            fetch("/sensor").then(resp => resp.json()).then(data => {{
                document.getElementById("sensorData").innerHTML =
                    `🌡️ Temperature: ${{data.temp}}°C &nbsp;&nbsp; 💧 Humidity: ${{data.humidity}}%`;
            }}).catch(err => console.log("Sensor fetch error:", err));
        }}, 2000);
    </script>
</body>
</html>"""
    return html

while True:
    conn, addr = s.accept()
    print("Connection from:", addr)
    request = conn.recv(1024).decode()
    print("Request:", request)

    if "/?r=" in request and "&g=" in request and "&b=" in request:
        try:
            parts = request.split("/?")[1].split(" ")[0]
            params = {kv.split("=")[0]: kv.split("=")[1] for kv in parts.split("&")}
            r = min(255, max(0, int(params["r"])))
            g = min(255, max(0, int(params["g"])))
            b = min(255, max(0, int(params["b"])))
            neo[0] = (r, g, b)
            neo.write()
        except Exception as e:
            print("RGB Error:", e)

    elif "/?msg=" in request:
        try:
            msg = request.split("/?msg=")[1].split(" ")[0]
            msg = msg.replace("%20", " ")
            display_message_on_oled(msg)
        except Exception as e:
            print("OLED Msg Error:", e)

    elif "GET /sensor" in request:
        try:
            sensor.measure()
            temp = str(sensor.temperature())
            humidity = str(sensor.humidity())
        except:
            temp = "N/A"
            humidity = "N/A"
        json_data = '{{"temp": "{0}", "humidity": "{1}"}}'.format(temp, humidity)
        conn.send("HTTP/1.1 200 OK\nContent-Type: application/json\n\n" + json_data)
        conn.close()
        continue

    try:
        sensor.measure()
        temp = str(sensor.temperature())
        humidity = str(sensor.humidity())
        print("Updated Temp:", temp, "Humidity:", humidity)
    except Exception as e:
        print("Sensor Read Error:", e)
        temp = "N/A"
        humidity = "N/A"

    response = web_page(r, g, b, temp, humidity)
    conn.send("HTTP/1.1 200 OK\nContent-Type: text/html\n\n" + response)
    conn.close()

