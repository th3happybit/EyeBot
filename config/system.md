# install system
`sudo dd if=/home/sam/dev/robot/2021-03-04-raspios-buster-armhf-lite.img of=/dev/sda bs=1M status=progress`

# setup
1. mount boot partition
2. create empty file ssh
3. configure wifi connection:
    copy wpa_supplicant.conf on boot

4. unmount boot partition

# start raspberry pi
wait until it's connect to wifi
and then ssh into it
`ssh pi@raspberrypi`
password: raspberry

# update
`sudo apt update`
`sudo apt full-upgrade`

# install deps
`sudo apt install python3 python3-pip`
`sudo apt install mosquitto`
`sudo systemctl enable mosquitto.service`
`curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add -`
`echo "deb https://dl.yarnpkg.com/debian/ stable main" | sudo tee /etc/apt/sources.list.d/yarn.list`
`sudo apt update`
`sudo apt install -y yarn`
`sudo yarn global add serve`
`sudo apt-get install python3-opencv`
`sudo apt-get install pigpio`
`sudo apt-get install python-pigpio python3-pigpio`
`sudo systemctl enable pigpiod`
`sudo systemctl start pigpiod`
`sudo apt-get install python-picamera python3-picamera`

# config camera
`sudo raspi-config`

Use the cursor keys to select and open Interfacing Options, and then select Camera and follow the prompt to enable the camera.

Upon exiting raspi-config, it will ask to reboot, reboot

# copy project into raspberry pi
`scp -r project pi@raspberrypi:/home/pi`

# setup project

Install deps for every module

# run services
sudo cp services/*.service /etc/systemd/system/
sudo systemctl daemon-reload
bash services/start.sh