from flask import Flask, render_template, Response
import cv2
import numpy as np
from imutils import build_montages
from datetime import datetime
import imagezmq
import argparse
import imutils
import pandas as pd
from storage import RedisStorage, redis_client
import time 

app = Flask(__name__)

image_hub = imagezmq.ImageHub(open_port='tcp://0.0.0.0:5566')


store = RedisStorage()

whT = 320
confThreshold = 0.5
nmsThreshold= 0.3

classesFile = 'data/coco.names'
classNames = []

with open(classesFile, 'rt') as f:
    classNames = f.read().rstrip('\n').split('\n')

# modelConfiguration = 'models/yolov3-tiny.cfg'
# modelWeights = 'models/yolov3-tiny.weights'
modelConfiguration = 'models/yolov3.cfg'
modelWeights = 'models/yolov3.weights'

net = cv2.dnn.readNetFromDarknet(modelConfiguration, modelWeights)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

# initialize the dictionary which will contain  information regarding
# when a device was last active, then store the last time the check
# was made was now
lastActive = {}
lastActiveCheck = datetime.now()

# stores the estimated number of Pis, active checking period, and
# calculates the duration seconds to wait before making a check to
# see if a device was active
ESTIMATED_NUM_PIS = 1
ACTIVE_CHECK_PERIOD = 10
ACTIVE_CHECK_SECONDS = ESTIMATED_NUM_PIS * ACTIVE_CHECK_PERIOD

filePath = 'Objects.csv'
def markObjects(name):
    with open(filePath,'r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{dtString}')

def storeObjects(name):
    try:
        name = str(name)
        # current_time = time.time()
        # elements = redis_client.lrange("objects", 0, -1)
        if redis_client:
            redis_client.publish("objects-channel", name)
            # print("Object {} added to redis storage at time {} ".format(name, current_time))
        else:
            pass
    except Exception as e:
        print(e)

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
        name = classNames[classIds[i]].upper()
        cv2.rectangle(frame, (x,y), (x+w, y+h), (255,0,255),2)
        cv2.putText(frame,f'{classNames[classIds[i]].upper()} {int(confs[i]*100)}%', 
                    (x,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,0,255),2)
        storeObjects(name)
        markObjects(name)


def gen_frames():  
    while True:

        (rpiName, frame) = image_hub.recv_image()
        image_hub.send_reply(b'OK')
        
        if rpiName not in lastActive.keys():
            print("[INFO] receiving data from {}...".format(rpiName))
        
        # record the last active time for the device from which we just
        # received a frame
        lastActive[rpiName] = datetime.now()
        cv2.putText(frame, rpiName, (10, 25),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        #success, frame = camera.read()  # read the camera frame
        
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

@app.route('/data')
def parseCSV():
    with open('Objects.csv') as csv_file:
        # CVS Column Names
        col_names = ['Name','Time']
        # Use Pandas to parse the CSV file
        csvData = pd.read_csv(csv_file,names=col_names, header=None)
        # Loop through the Rows
    for i,row in csvData.iterrows():
        print(i,row['Name'],row['Time'])
   

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', use_reloader=False)


