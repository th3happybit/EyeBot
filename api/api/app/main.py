from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.websockets import WebSocket
from fastapi.responses import HTMLResponse
from fastapi_mqtt import FastMQTT, MQTTConfig
import json

from app.core.config import settings


def get_application():
    _app = FastAPI(title=settings.PROJECT_NAME)

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return _app


app = get_application()
mqtt_config = MQTTConfig()
# print mqtt config
print(mqtt_config)
mqtt = FastMQTT(
    config=mqtt_config
)
mqtt.init_app(app)

@app.get("/publish")
async def func():
    mqtt.publish("/mqtt", "Hello from Fastapi") #publishing mqtt topic
    return {"result": True,"message":"Published" }

@app.websocket("/joystick_ws")
async def joystick_websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_json()
        print(data)
        mqtt.publish("/mqtt", str(data.get("x", 0))+":"+str(data.get("y", 0)))


@app.websocket("/camera_ws")
async def camera_websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        print(data)
        mqtt.publish("/mqtt", str(data))

@mqtt.on_connect()
def connect(client, flags, rc, properties):
    mqtt.client.subscribe("/mqtt") #subscribing mqtt topic
    print("Connected: ", client, flags, rc, properties)

@mqtt.on_message()
async def message(client, topic, payload, qos, properties):
    print("Received message: ",topic, payload.decode(), qos, properties)

@mqtt.on_disconnect()
def disconnect(client, packet, exc=None):
    print("Disconnected")

@mqtt.on_subscribe()
def subscribe(client, mid, qos, properties):
    print("subscribed", client, mid, qos, properties)