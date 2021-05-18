from piservo import Servo
import time

# Just testing module
cam_motor = Servo(12)

cam_motor.write(180)
time.sleep(3)
cam_motor.write(0)
time.sleep(3)
cam_motor.stop()