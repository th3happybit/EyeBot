mkdir /home/pi/project/frontend/log/
touch /home/pi/project/frontend/log/logfile
mkdir /home/pi/project/api/log/
touch /home/pi/project/api/log/logfile
mkdir /home/pi/project/motor_control_module/log/
touch /home/pi/project/motor_control_module/log/logfile
mkdir /home/pi/project/cam_motor_module/log/
touch /home/pi/project/cam_motor_module/log/logfile
mkdir /home/pi/project/object_detection_module/log/
touch /home/pi/project/object_detection_module/log/logfile
mkdir /home/pi/project/cam_streaming_module/log/
touch /home/pi/project/cam_streaming_module/log/logfile

sudo systemctl start api.service 
sudo systemctl status api.service 
sudo systemctl start frontend.service
sudo systemctl status frontend.service
sudo systemctl start motor_control.service 
sudo systemctl status motor_control.service 
sudo systemctl start cam_motor.service 
sudo systemctl status cam_motor.service 
sudo systemctl start streaming.service 
sudo systemctl status streaming.service
sudo systemctl start streaming_only.service 
sudo systemctl status streaming_only.service