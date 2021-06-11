from AMSpi.AMSpi import AMSpi
import time
import paho.mqtt.client as mqtt
from math import sqrt
import RPi.GPIO as GPIO

motor_controller = AMSpi()
motor_controller.set_74HC595_pins(21, 20, 16)
motor_controller.set_L293D_pins(5, 6, 13, 19)
deadZone = 10

def calSpeed(xspeed, yspeed):
    abs = sqrt(xspeed*xspeed + yspeed*yspeed)
    return abs

def move(yspeed, xspeed, motorSpeed):
    print("Y Speed", yspeed)
    print("X Speed", xspeed)
    print("Speed", motorSpeed)
    # forward right
    if yspeed > deadZone and xspeed > deadZone:
        print('forward right')
        motor_controller.run_dc_motor(motor_controller.DC_Motor_1, clockwise=True, speed=(motorSpeed-xspeed))
        motor_controller.run_dc_motor(motor_controller.DC_Motor_4, clockwise=True, speed=motorSpeed)
    # forward left
    elif yspeed > deadZone and xspeed < -deadZone:
        print('forward left')
        motor_controller.run_dc_motor(motor_controller.DC_Motor_1, clockwise=True, speed=motorSpeed)
        motor_controller.run_dc_motor(motor_controller.DC_Motor_4, clockwise=True, speed=(motorSpeed- (-xspeed)))
    # forward
    elif yspeed > 0 and xspeed < deadZone and xspeed > -deadZone:
        print('forward')
        motor_controller.run_dc_motor(motor_controller.DC_Motor_1, clockwise=True, speed=motorSpeed)
        motor_controller.run_dc_motor(motor_controller.DC_Motor_4, clockwise=True, speed=motorSpeed)
    # back right
    elif yspeed < -deadZone and xspeed > deadZone:
        print('back right')
        motor_controller.run_dc_motor(motor_controller.DC_Motor_1, clockwise=False, speed=(motorSpeed- xspeed))
        motor_controller.run_dc_motor(motor_controller.DC_Motor_4, clockwise=False, speed=motorSpeed)
    # back left
    elif yspeed < -deadZone and xspeed < -deadZone:
        print('back left')
        motor_controller.run_dc_motor(motor_controller.DC_Motor_1, clockwise=False, speed=motorSpeed)
        motor_controller.run_dc_motor(motor_controller.DC_Motor_4, clockwise=False, speed=motorSpeed- (-xspeed))
    # back
    elif yspeed < -deadZone and xspeed > -deadZone and xspeed < deadZone:
        print('back')
        motor_controller.run_dc_motor(motor_controller.DC_Motor_1, clockwise=False, speed=motorSpeed)
        motor_controller.run_dc_motor(motor_controller.DC_Motor_4, clockwise=False, speed=motorSpeed)
    else:
        print('stop')
        motor_controller.stop_dc_motor(motor_controller.DC_Motor_1)
        motor_controller.stop_dc_motor(motor_controller.DC_Motor_4)
    
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("control/base/motor")

def on_message(client, userdata, msg):
    global motor_controller
    print(msg.topic+" "+str(msg.payload))
    if len(msg.payload.decode().split(':')) == 2:
        xspeed, yspeed = msg.payload.decode().split(':')
        if xspeed != None and yspeed != None:
            xspeed = int(xspeed)
            yspeed = int(yspeed)
            mspeed = calSpeed(int(), yspeed)
            move(yspeed,xspeed, int(mspeed))
    if msg.payload == b'test':
        print('m1')
        motor_controller.run_dc_motor(motor_controller.DC_Motor_1, clockwise=True, speed=100)
        time.sleep(3)
        motor_controller.stop_dc_motor(motor_controller.DC_Motor_1)
        print('m2')
        motor_controller.run_dc_motor(motor_controller.DC_Motor_2, clockwise=True, speed=100)
        time.sleep(3)
        motor_controller.stop_dc_motor(motor_controller.DC_Motor_2)
        print('m3')
        motor_controller.run_dc_motor(motor_controller.DC_Motor_3, clockwise=True, speed=100)
        time.sleep(3)
        motor_controller.stop_dc_motor(motor_controller.DC_Motor_3)
        print('m4')
        motor_controller.run_dc_motor(motor_controller.DC_Motor_4, clockwise=True, speed=100)
        time.sleep(3)
        motor_controller.stop_dc_motor(motor_controller.DC_Motor_4)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)
client.loop_forever()
