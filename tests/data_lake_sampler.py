import cv2
import json
import numpy as np
import requests
import sys
from zipfile import ZipFile
import io
import os
import re
from dateparser import parse

product = "maçã"
datatype = "ref"
res = requests.get('http://localhost:5000/api/datalake')
mean = None
std = None
if res.ok:
    print("requesting informations")
    hashtable = res.json()
    for key in hashtable:
        if re.search(product, key) and re.search(datatype, key):
            folder = key
            break
    most_recent = parse("0")
    for key in hashtable[folder]:
        date = parse(key)
        if date > most_recent:
            most_recent = date
            subfolder = key
    for number in range(len(hashtable[folder][subfolder])):
        hashtable = {}
        hashtable["frame_type"] = datatype
        hashtable["time_stamp"] = subfolder
        hashtable["number"] = number
        data = json.dumps(hashtable)
        res = requests.get('http://localhost:5000/api/datalake/%s'%product, json = data)

if res.ok:
    print("calibrating")
    hashtable = res.json()
    frame = hashtable["frame"]
    #frame = cv2.UMat(np.array(frame, dtype=np.uint8))
    #frame = cv2.resize(frame, None, fx=0.4, fy=0.4)
    #list_frame = frame.tolist()
    list_frame = frame
    data = json.dumps(list_frame)
    res = requests.post('http://localhost:5000/api/get_ref', json = data)

if res.ok:
    #print("res ok")
    res = res.json()
    mean = res["mean"]
    std = res["std"]
    print("mean: ")
    print(mean)
    print("std: ")
    print(std)

datatype = "sample"
res = requests.get('http://localhost:5000/api/datalake')
if res.ok and mean and std:
    print("processing frames")
    hashtable = res.json()
    for key in hashtable:
        if re.search(product, key) and re.search(datatype, key):
            folder = key
            break
    most_recent = parse("0")
    for key in hashtable[folder]:
        date = parse(key)
        if date > most_recent:
            most_recent = date
            subfolder = key

    max_frame = 10
    class_number = 0
    class_name = product
    path = "../temp/"
    with ZipFile(path+'sample.zip', mode="w") as zf:
        f = open("classes.txt", 'w')
        f.write(class_name)
        f.close()
        zf.write("classes.txt")
        os.remove("classes.txt")
        total = len(hashtable[folder][subfolder])
        for number in range(total):
            hashtable = {}
            hashtable["frame_type"] = datatype
            hashtable["time_stamp"] = subfolder
            hashtable["number"] = number
            data = json.dumps(hashtable)
            res = requests.get('http://localhost:5000/api/datalake/%s'%product, json = data)
            if res.ok:
                hashtable = res.json()
                frame = hashtable["frame"]
                #frame = cv2.UMat(np.array(frame, dtype=np.uint8))
                #frame = cv2.resize(frame, None, fx=0.4, fy=0.4)
                #img = frame.tolist()
                img = frame
                hashtable = {"img": img, "mean": mean, "std": std}
                data = json.dumps(hashtable)
                res = requests.post('http://localhost:5000/api/segmentation', json = data)
                if res.ok and res.status_code != 204:
                    print("%d of %d"%(number, total))
                    res = res.json()
                    frame = cv2.UMat(np.array(frame, dtype=np.uint8))
                    cv2.imwrite("%s%d.jpg" %(path+class_name, number), frame)
                    box = (class_number, res['x'], res['y'], res['w'], res['h'])
                    f = open("%s%d.txt" %(path+class_name, number), 'w')
                    f.write("%d %f %f %f %f" %box)
                    print("%d %f %f %f %f" %box)
                    f.close()
                    zf.write("%s%d.jpg" %(path+class_name, number))
                    zf.write("%s%d.txt" %(path+class_name, number))
                    os.remove("%s%d.jpg" %(path+class_name, number))
                    os.remove("%s%d.txt" %(path+class_name, number))

