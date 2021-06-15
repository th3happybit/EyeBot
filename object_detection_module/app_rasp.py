from flask import Flask, render_template, Response
import cv2
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
from threading import Thread
from imutils.video.pivideostream import PiVideoStream
import time

# class PiVideoStream:
# 	def __init__(self, resolution=(640, 480), framerate=32, **kwargs):
# 		# initialize the camera
# 		self.camera = PiCamera()

# 		# set camera parameters
# 		self.camera.resolution = resolution
# 		self.camera.framerate = framerate

# 		# set optional camera parameters (refer to PiCamera docs)
# 		for (arg, value) in kwargs.items():
# 			setattr(self.camera, arg, value)

# 		# initialize the stream
# 		self.rawCapture = PiRGBArray(self.camera, size=resolution)
# 		self.stream = self.camera.capture_continuous(self.rawCapture,
# 			format="bgr", use_video_port=True)

# 		# initialize the frame and the variable used to indicate
# 		# if the thread should be stopped
# 		self.frame = None
# 		self.stopped = False

# 	def start(self):
# 		# start the thread to read frames from the video stream
# 		t = Thread(target=self.update, args=())
# 		t.daemon = True
# 		t.start()
# 		return self

# 	def update(self):
# 		# keep looping infinitely until the thread is stopped
# 		for f in self.stream:
# 			# grab the frame from the stream and clear the stream in
# 			# preparation for the next frame
# 			self.frame = f.array
# 			self.rawCapture.truncate(0)

# 			# if the thread indicator variable is set, stop the thread
# 			# and resource camera resources
# 			if self.stopped:
# 				self.stream.close()
# 				self.rawCapture.close()
# 				self.camera.close()
# 				return

# 	def read(self):
# 		# return the frame most recently read
# 		return self.frame

# 	def stop(self):
# 		# indicate that the thread should be stopped
# 		self.stopped = True

app = Flask(__name__)

# camera = cv2.VideoCapture('/dev/video0')
whT = 320
confThreshold = 0.5
nmsThreshold= 0.3

classesFile = '/home/pi/project/object_detection_module/data/coco.names'
classNames = []

with open(classesFile, 'rt') as f:
    classNames = f.read().rstrip('\n').split('\n')

modelConfiguration = '/home/pi/project/object_detection_module/models/yolov3-tiny.cfg'
modelWeights = '/home/pi/project/object_detection_module/models/yolov3-tiny.weights'

# modelConfiguration = 'models/yolov3.cfg'
# modelWeights = 'models/yolov3.weights'

net = cv2.dnn.readNetFromDarknet(modelConfiguration, modelWeights)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

def findObjects(outputs,frame):
    hT, wT, cT = frame.shape
    bbox = [] # it will contains values of x, y, width, height
    classIds = []
    confs = [] # contains confidence values 

    for output in outputs:
        for detection in output:
            scores = detection[5:]  # remove the first five elements 
            classId = np.argmax(scores) # find the index of max values
            confidence = scores[classId]
            if confidence > confThreshold:
                w,h = int(detection[2]*wT), int(detection[3]*hT)
                x,y = int((detection[0]*wT)-w/2), int((detection[1]*hT)-h/2)
                bbox.append([x,y,w,h])
                classIds.append(classId)
                confs.append(float(confidence))
    # print(len(bbox))
    indices = cv2.dnn.NMSBoxes(bbox,confs,confThreshold,nmsThreshold)

    for i in indices:
        i = i[0]
        box = bbox[i]
        x,y,w,h = box[0], box[1], box[2], box[3]
        cv2.rectangle(frame, (x,y), (x+w, y+h), (255,0,255),2)
        cv2.putText(frame,f'{classNames[classIds[i]].upper()} {int(confs[i]*100)}%', 
                    (x,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,0,255),2)

def gen_frames():
    videostream = PiVideoStream().start()
    time.sleep(1)
    try:
        while True:
            frame = videostream.read()
            blob = cv2.dnn.blobFromImage(frame, 1/255, (whT, whT), [0,0,0], 1, crop=False)
            net.setInput(blob)
            layerNames = net.getLayerNames()
            outputNames = [layerNames[i[0]-1] for i in net.getUnconnectedOutLayers()]
            outputs = net.forward(outputNames)
            findObjects(outputs, frame)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    except Exception:
        videostream.stop()
    # camera = PiCamera()
    # camera.resolution = (640, 480)
    # camera.framerate = 32
    # rawCapture = PiRGBArray(camera, size=(640, 480))
    # for fframe in camera.capture_continuous(rawCapture, burst=True, format="bgr", use_video_port=False):
    #     frame = fframe.array
    #     blob = cv2.dnn.blobFromImage(frame, 1/255, (whT, whT), [0,0,0], 1, crop=False)
    #     net.setInput(blob)
    #     layerNames = net.getLayerNames()
    #     outputNames = [layerNames[i[0]-1] for i in net.getUnconnectedOutLayers()]
    #     outputs = net.forward(outputNames)
    #     findObjects(outputs, frame)
    #     ret, buffer = cv2.imencode('.jpg', frame)
    #     frame = buffer.tobytes()
    #     rawCapture.truncate(0)
    #     yield (b'--frame\r\n'
    #             b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    # while True:
    #     success, frame = camera.read()  # read the camera frame
    #     if not success:
    #         break
    #     else:
    #         blob = cv2.dnn.blobFromImage(frame, 1/255, (whT, whT), [0,0,0], 1, crop=False)
    #         net.setInput(blob)
    #         layerNames = net.getLayerNames()
    #         outputNames = [layerNames[i[0]-1] for i in net.getUnconnectedOutLayers()]
    #         outputs = net.forward(outputNames)
    #         findObjects(outputs, frame)
    #         ret, buffer = cv2.imencode('.jpg', frame)
    #         frame = buffer.tobytes()
    #         yield (b'--frame\r\n'
    #                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8082)
