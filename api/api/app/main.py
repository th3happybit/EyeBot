from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.websockets import WebSocket
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi_mqtt import FastMQTT, MQTTConfig
import json
import hashlib
import aioredis
import asyncio
# BACKEND_CORS_ORIGINS = [
#     "http://raspberrypi:3000"
#     "http://raspberrypi"
#     "http://localhost:8000",
#     "https://localhost:8000",
#     "http://localhost",
#     "https://localhost",
#     "http://localhost:3000",
#     "https://localhost:3000",
#     "http://0.0.0.0:3000",
#     "http://172.10.20.6"
# ]

KEY = "1a46f2b7-b2e5-4bfd-a806-5c35c9368aa3"


def get_application():
    _app = FastAPI(title="raspApi")

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return _app


WHITELIST_ROUTES = ["/auth/", "/docs", "/openapi.json"]

app = get_application()

@app.middleware("http")
async def auth(request: Request, call_next):
    response = await call_next(request)
    path = request.scope.get("path")
    # Verify if the route is whitelisted from middelware
    if path in WHITELIST_ROUTES:
        return response
    # get authorization header    
    request_key = request.headers.get("Authorization", None)
    if request_key:
        request_key = request_key.split(" ")[1]
        hashed_key = hashlib.sha256(KEY.encode()).hexdigest()
        # Verify key
        if hashed_key == request_key:
            return response
    return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                        content={"details": "Authentication creds non provided"})


mqtt_config = MQTTConfig()
# print mqtt config
print(mqtt_config)
mqtt = FastMQTT(
    config=mqtt_config
)
mqtt.init_app(app)


@app.post("/auth/")
async def authenticate(request: Request):
    # Parse request body
    body = await request.json()
    key = body.get("key", None)
    if key:
        # Preparing key stored on server
        hashed_key = hashlib.sha256(KEY.encode()).hexdigest()
        if hashed_key == key:
            # compare keys
            status_code = status.HTTP_200_OK
            content = {"key": hashed_key}
        else:
            status_code = status.HTTP_400_BAD_REQUEST
            content = {"detail": "Creds provided are incorrects"}
    else:
        status_code = status.HTTP_400_BAD_REQUEST
        content = {"detail": "Malformed Request"}
    return JSONResponse(status_code=status_code, content=content)


@app.get("/publish")
async def func():
    mqtt.publish("/mqtt", "Hello from Fastapi")  # publishing mqtt topic
    return {"result": True, "message": "Published"}


@app.websocket("/joystick_ws")
async def joystick_websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_json()
        mqtt.publish("control/base/motor", str(data.get("x", 0)) +
                     ":"+str(data.get("y", 0)))


@app.websocket("/camera_ws")
async def camera_websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        print(data)
        mqtt.publish("control/cam/motor", str(data))


@mqtt.on_connect()
def connect(client, flags, rc, properties):
    mqtt.client.subscribe("control/base/motor")  # subscribing mqtt topic
    mqtt.client.subscribe("control/cam/motor")  # subscribing mqtt topic
    print("Connected: ", client, flags, rc, properties)


@mqtt.on_message()
async def message(client, topic, payload, qos, properties):
    print("Received message: ", topic, payload.decode(), qos, properties)


@mqtt.on_disconnect()
def disconnect(client, packet, exc=None):
    print("Disconnected")


@mqtt.on_subscribe()
def subscribe(client, mid, qos, properties):
    print("subscribed", client, mid, qos, properties)

async def redis_connector(
    websocket: WebSocket, redis_uri: str = "redis://192.168.43.10:6379"
):
    async def producer_handler(r, ws: WebSocket):
        (channel,) = await r.subscribe("objects-channel")
        assert isinstance(channel, aioredis.Channel)
        try:
            while True:
                message = await channel.get()
                print("Received: ",message)
                if message:
                    await ws.send_json({ "name": message.decode("utf-8") })
        except Exception as exc:
            print(exc)

    redis = await aioredis.create_redis_pool(redis_uri)
    producer_task = producer_handler(redis, websocket)
    done, pending = await asyncio.wait(
        [producer_task], return_when=asyncio.FIRST_COMPLETED,
    )

    for task in pending:
        task.cancel()
    redis.close()
    await redis.wait_closed()
    

@app.websocket("/objects_ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await redis_connector(websocket)
