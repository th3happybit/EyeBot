from flask import Flask, render_template, Response
import cv2
import numpy as np

app = Flask(__name__)

# camera = cv2.VideoCapture('/dev/video0')
whT = 320
confThreshold = 0.5
nmsThreshold= 0.3

classesFile = 'data/coco.names'
classNames = []

with open(classesFile, 'rt') as f:
    classNames = f.read().rstrip('\n').split('\n')

modelConfiguration = 'models/yolov3-tiny.cfg'
modelWeights = 'models/yolov3-tiny.weights'

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
    camera = cv2.VideoCapture('/dev/video0')
    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            blob = cv2.dnn.blobFromImage(frame, 1/255, (whT, whT), [0,0,0], 1, crop=False)
            net.setInput(blob)
            layerNames = net.getLayerNames()
            outputNames = [layerNames[i[0]-1] for i in net.getUnconnectedOutLayers()]
            outputs = net.forward(outputNames)
            findObjects(outputs, frame)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8082)
