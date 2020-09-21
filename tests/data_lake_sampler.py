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

def seg(product, class_number, used_dates, zf, sample_number):
    datatype = "ref"
    res = requests.get('http://localhost:5000/api/datalake')
    mean = None
    std = None
    sample_folder = None
    subfolder = None
    hashtable = {}

    if res.ok:
        print("requesting informations")
        hashtable = res.json()
        for key in hashtable:
            if re.search(product, key) and re.search(datatype, key):
                folder = key
            if re.search(product, key) and re.search("sample", key):
                sample_folder = key
        most_recent = parse("0")
        for key in hashtable[folder]:
            date = parse(key)
            if date > most_recent and date not in used_dates:
                most_recent = date
                subfolder = key
        date = most_recent
        for number in range(len(hashtable[folder][subfolder])):
            hashtable2 = {}
            hashtable2["frame_type"] = datatype
            hashtable2["time_stamp"] = subfolder
            hashtable2["number"] = number
            data = json.dumps(hashtable2)
            res = requests.get('http://localhost:5000/api/datalake/%s'%product, json = data)
            print("requested")

    if res.ok:
        print("calibrating")
        hashtable2 = res.json()
        frame = hashtable2["frame"]
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
    folder = sample_folder
    res = requests.get('http://localhost:5000/api/datalake')
    if res.ok and mean and std:
        print(folder)
        print(subfolder)
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
                cv2.imwrite("%s%d-%d.jpg" %(path+class_name, sample_number, number), frame)
                box = (class_number, res['x'], res['y'], res['w'], res['h'])
                f = open("%s%d-%d.txt" %(path+class_name, sample_number, number), 'w')
                f.write("%d %f %f %f %f" %box)
                print("%d %f %f %f %f" %box)
                f.close()
                zf.write("%s%d-%d.jpg" %(path+class_name, sample_number, number))
                zf.write("%s%d-%d.txt" %(path+class_name, sample_number, number))
                os.remove("%s%d-%d.jpg" %(path+class_name, sample_number, number))
                os.remove("%s%d-%d.txt" %(path+class_name, sample_number, number))
    return date

classes = "coke\nbread\napple\nbanana\npepsi\ncoxinha\neclair\ncheese_bread\nchoux_cream\nmate"
class_name = "choux_cream"
class_number = 8
path = "../temp/"
used_dates = []
n_folders = 2
with ZipFile('%s%s.zip'%(path, class_name), mode="w") as zf:
    f = open("classes.txt", 'w')
    f.write(classes)
    f.close()
    zf.write("classes.txt")
    os.remove("classes.txt")
    for i in range(n_folders):
        date = seg(class_name, class_number, used_dates, zf, i)
        used_dates.append(date)
