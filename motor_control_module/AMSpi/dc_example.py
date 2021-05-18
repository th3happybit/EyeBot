#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
   Servo Example - Example of usage ASMpi class

.. Licence MIT
.. codeauthor:: Jan Lipovský <janlipovsky@gmail.com>, janlipovsky.cz
"""

from AMSpi import AMSpi
import time

if __name__ == '__main__':
    # Calling AMSpi() we will use default pin numbering: BCM (use GPIO numbers)
    # if you want to use BOARD numbering do this: "with AMSpi(True) as amspi:"
    with AMSpi() as amspi:
        # Set PINs for controlling shift register (GPIO numbering)
        amspi.set_74HC595_pins(21, 20, 16)
        # Set PINs for controlling all 4 motors (GPIO numbering)
        amspi.set_L293D_pins(5, 6, 13, 19)
        print("GO: clockwise")
        amspi.run_dc_motors([amspi.DC_Motor_1, amspi.DC_Motor_2, amspi.DC_Motor_3, amspi.DC_Motor_4])
        time.sleep(2)

        print("Stop")
        amspi.stop_dc_motors([amspi.DC_Motor_1, amspi.DC_Motor_2, amspi.DC_Motor_3, amspi.DC_Motor_4])
        time.sleep(1)

        print("GO: counterclockwise")
        amspi.run_dc_motors([amspi.DC_Motor_1, amspi.DC_Motor_2, amspi.DC_Motor_3, amspi.DC_Motor_4], clockwise=False)
        time.sleep(2)

        print("Stop")
        amspi.stop_dc_motors([amspi.DC_Motor_1, amspi.DC_Motor_2, amspi.DC_Motor_3, amspi.DC_Motor_4])
        time.sleep(1)

        print("GO: clockwise with 50% of maximum speed")
        amspi.run_dc_motors([amspi.DC_Motor_1, amspi.DC_Motor_2, amspi.DC_Motor_3, amspi.DC_Motor_4], speed=50)
        time.sleep(2)

        print("Stop")
        amspi.stop_dc_motors([amspi.DC_Motor_1, amspi.DC_Motor_2, amspi.DC_Motor_3, amspi.DC_Motor_4])
        time.sleep(1)

        print("Turn right")
        amspi.run_dc_motors([amspi.DC_Motor_1, amspi.DC_Motor_3])
        amspi.run_dc_motors([amspi.DC_Motor_2, amspi.DC_Motor_4], clockwise=False)
        time.sleep(1)

        print("Stop")
        amspi.stop_dc_motors([amspi.DC_Motor_1, amspi.DC_Motor_2, amspi.DC_Motor_3, amspi.DC_Motor_4])
        time.sleep(1)

        print("Turn left")
        amspi.run_dc_motors([amspi.DC_Motor_1, amspi.DC_Motor_3], clockwise=False)
        amspi.run_dc_motors([amspi.DC_Motor_2, amspi.DC_Motor_4])
        time.sleep(1)

        print("Stop and Exit")
        amspi.stop_dc_motors([amspi.DC_Motor_1, amspi.DC_Motor_2, amspi.DC_Motor_3, amspi.DC_Motor_4])
