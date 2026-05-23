# Mouse Pad UI

A touch-friendly browser control panel that publishes MQTT mouse commands, plus a small Python receiver that turns those commands into PC mouse movement, clicks, and scrolling.

## Files

- `mouse_pad_ui.html` - mobile/desktop touch UI for sending MQTT commands.
- `rotary_PC.py` - Python MQTT receiver for controlling the local mouse.
- `mouse_pad_config.js` - shared MQTT settings for both the UI and receiver.

## Run the Receiver

Create a local virtual environment and install dependencies:

```bash
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Start the receiver:

```bash
.\.venv\Scripts\python.exe rotary_PC.py
```

Then open `mouse_pad_ui.html` in a browser and use the touch controls.

## MQTT

Edit `mouse_pad_config.js` to make the browser UI and Python receiver use the same MQTT settings:

```js
window.MOUSE_PAD_CONFIG = {
  "mqtt": {
    "broker": "broker.emqx.io",
    "port": 1883,
    "websocketUrl": "wss://broker.emqx.io:8084/mqtt",
    "topic": "JJ/mouse/pad/cmd"
  }
};
```

The Python receiver reads `broker`, `port`, and `topic`. The browser UI reads `websocketUrl` and `topic`.

You can still temporarily override the browser values with URL parameters, for example `mouse_pad_ui.html?topic=your/topic`.
