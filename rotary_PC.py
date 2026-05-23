# pip install paho-mqtt pyautogui

import json
import pyautogui
import paho.mqtt.client as mqtt

BROKER = "broker.emqx.io"
PORT = 1883
TOPIC = "JJ/mouse/pad/cmd"

pyautogui.FAILSAFE = True

def limit(v, min_v=-80, max_v=80):
    return max(min_v, min(max_v, int(v)))

def on_connect(client, userdata, flags, reason_code, properties=None):
    print("MQTT connected:", reason_code)
    client.subscribe(TOPIC)
    print("Subscribed:", TOPIC)

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode("utf-8"))
    except Exception:
        return

    if data.get("target") != "pc_mouse":
        return

    cmd_type = data.get("type")

    if cmd_type == "move":
        dx = limit(data.get("dx", 0))
        dy = limit(data.get("dy", 0))
        pyautogui.moveRel(dx, dy, duration=0)

    elif cmd_type == "click":
        button = data.get("button", "left")
        if button in ["left", "right", "middle"]:
            pyautogui.click(button=button)

    elif cmd_type == "scroll":
        dy = limit(data.get("dy", 0), -10, 10)
        pyautogui.scroll(dy)

    elif cmd_type == "stop":
        pass

client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2,
    client_id="JJ_PC_Mouse_Receiver"
)

client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT, 60)
client.loop_forever()