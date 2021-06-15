import io
import picamera
import logging
import socketserver
from threading import Condition
from http import server
import cv2
import numpy as np

whT = 320
confThreshold = 0.5
nmsThreshold= 0.3

classesFile = 'data/coco.names'
classNames = []

with open(classesFile, 'rt') as f:
    classNames = f.read().rstrip('\n').split('\n')

modelConfiguration = 'models/yolov3.cfg'
modelWeights = 'models/yolov3.weights'

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


PAGE="""\
<html>
<head>
<title>picamera MJPEG streaming demo</title>
</head>
<body>
<h1>PiCamera MJPEG Streaming Demo</h1>
<img src="stream.mjpg" width="640" height="480" />
</body>
</html>
"""
def raw_resolution(resolution, splitter=False):
    """
    Round a (width, height) tuple up to the nearest multiple of 32 horizontally
    and 16 vertically (as this is what the Pi's camera module does for
    unencoded output).
    """
    width, height = resolution
    if splitter:
        fwidth = (width + 15) & ~15
    else:
        fwidth = (width + 31) & ~31
    fheight = (height + 15) & ~15
    return fwidth, fheight
    
def bytes_to_rgb(data, resolution):
    """
    Converts a bytes objects containing RGB/BGR data to a `numpy`_ array.
    """
    width, height = resolution
    fwidth, fheight = raw_resolution(resolution)
    # Workaround: output from the video splitter is rounded to 16x16 instead
    # of 32x16 (but only for RGB, and only when a resizer is not used)
    if len(data) != (fwidth * fheight * 3):
        fwidth, fheight = raw_resolution(resolution, splitter=True)
        if len(data) != (fwidth * fheight * 3):
            print('Incorrect buffer length for resolution')

    # Crop to the actual resolution
    return np.frombuffer(data, dtype=np.uint8).\
            reshape((fheight, fwidth, 3))[:height, :width, :]

class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # New frame, copy the existing buffer's content and notify all
            # clients it's available
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)

class StreamingHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            content = PAGE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    with output.condition:
                        output.condition.wait()
                        frame = output.frame
                        data = np.fromstring(frame, dtype=np.uint8)
                        image = cv2.imdecode(data, 1)
                        blob = cv2.dnn.blobFromImage(image, 1/255, (whT, whT), [0,0,0], 1, crop=False)
                        net.setInput(blob)
                        layerNames = net.getLayerNames()
                        outputNames = [layerNames[i[0]-1] for i in net.getUnconnectedOutLayers()]
                        outputs = net.forward(outputNames)
                        findObjects(outputs, image)
                        ret, buffer = cv2.imencode('.jpg', image)
                        frame = buffer.tobytes()
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
        else:
            self.send_error(404)
            self.end_headers()

class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True
                
with picamera.PiCamera(resolution='640x480', framerate=24) as camera:
    output = StreamingOutput()
    camera.start_recording(output, format='mjpeg')
    try:
        address = ('0.0.0.0', 8000)
        server = StreamingServer(address, StreamingHandler)
        server.serve_forever()
    finally:
        camera.stop_recording()