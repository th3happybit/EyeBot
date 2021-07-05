# EyeBot

Web Controlled Moving Car with Vision.


## Project structure

- Cam Motor Module (cam_motor_module):

to control the cam motor and turn it in any direction (180 degree).

- Cam Streaming Module (cam_streaming_module):

to stream camera video to your web application without object detection.

- Motor Control Module (motor_control_module):

to drive the car and control the motors using the L293D Arduino shield.

- API (api):

web application API, to maintain communication with the control modules and frontend.

- Frontend (frontend):

web application UI. an interface to control the car and see the video stream, and the detected objects.

- Object Detection Module (object_detection_module):

a module to capture pi camera frames and send it to the server to perform an object detection processing on it
and stream to the frontend module.


## Team

- Benahmed Djawed
- Madani Yousfi Abdelwahed
- Messabih Oussama
- Reggam Moncef
- Touhami Wided Ahlem

## Supervisors

- Pr. Rahmoun Abdellatif
- Dr. Hamdan Bensnane