from piservo import Servo
import time
import paho.mqtt.client as mqtt


cam_motor = Servo(12)
step = 0
step_length = 20

current = 0

def move_left():
    global step
    newstep = step + step_length
    if step >= 0 and step <= 180 and (newstep <= 180):
        step += step_length
        print('Step: ', step)
        cam_motor.write(step)
        time.sleep(2)

def move_right():
    global step
    newstep = step - step_length
    if step >= 0 and step <= 180 and (newstep >= 0):
        step -= step_length
        print('Step: ', step)
        cam_motor.write(step)
        time.sleep(2)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("control/cam/motor")

def on_message(client, userdata, msg):
    global current
    print(msg.topic+" "+str(msg.payload))
    if msg.topic == 'control/cam/motor':
        # if msg.payload and msg.payload == b'right':
        #     move_right()
        # elif msg.payload and msg.payload == b'left':
        #     move_left()
        cam_motor.write(int(msg.payload))
        time.sleep(1)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)
client.loop_forever()
