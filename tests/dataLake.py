import cv2
import json
import numpy as np
import requests
import sys
from zipfile import ZipFile
import io
import os

cap=cv2.VideoCapture(0)
flag = True
while(True):
    if cv2.waitKey(1) & 0xFF == ord(' '):
        flag = not(flag)
        print(flag)
        # Capture frame-by-frame
    if flag == True:
        ret, frame = cap.read()
        if frame is None:
            break
        # Display the resulting frame
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        continue
ret,frame=cap.read()
cap.release()
cv2.destroyAllWindows()
hashtable = {"time_stamp": "12-12-12", "frame_type": "ref", "number": "12", "frame": frame.tolist()}
data = json.dumps(hashtable)
res = requests.post('http://localhost:5000/api/datalake/cocacola', json = data)
print(res)
res = requests.get('http://localhost:5000/api/datalake')
print(res)
if res.ok:
    hashtable = res.json()
    print(hashtable)
res = requests.get('http://localhost:5000/api/datalake/cocacola', json = data)
print(res)
if res.ok:
    hashtable = res.json()
    frame = hashtable["frame"]
    frame = cv2.UMat(np.array(frame, dtype=np.uint8))
    cv2.imshow("oi", frame)
    cv2.waitKey(0)
