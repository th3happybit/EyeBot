# Objects detection module


## Installation

Firstly make sure you've got a functioning Pi camera module (test it with
`raspistill` to be certain). 
Then make sure you've got the following packages installed:

    $ sudo pip3 install -r requirements.txt


## Setup && Usage

Run the Python server script which should print out a load of stuff
to the console as it starts up:

    $ copy yolov3.cfg and yolov3.weights in models dir

Run server.py on your server machine:

    $ python server.py

Set the configuration for the client.py (Set ip of the server there):

    `sender = imagezmq.ImageSender(connect_to="tcp://192.168.43.10:5566")`
     
Run the client.py inside the raspberry pi:

    $ python client.py