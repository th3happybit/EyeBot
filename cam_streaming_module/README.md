# Pi Video Streaming Project cs2


## Installation

Firstly make sure you've got a functioning Pi camera module (test it with
`raspistill` to be certain). Then make sure you've got the following packages
installed:

    $ sudo apt-get install ffmpeg git python3-picamera python3-ws4py
    $ sudo pip3 install picamera ws4py

Next, clone this repository:

    $ git clone repo


## Usage

Run the Python server script which should print out a load of stuff
to the console as it starts up:

    $ cd pistreaming
    $ python3 server.py
    Initializing websockets server on port 8084
    Initializing HTTP server on port 8082
    Initializing camera
    Initializing broadcast thread
    Spawning background conversion process
    Starting websockets thread
    Starting HTTP server thread
    Starting broadcast thread