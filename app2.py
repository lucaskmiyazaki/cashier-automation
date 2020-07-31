from flask import Flask
from flask import request, jsonify
import cv2
import numpy as np
import json

# Elastic Beanstalk looks for an 'application' that is callable by default
app = Flask(__name__)

# Health Check 
@app.route('/healthcheck')
def hello_world():
    return 'Your Server is working!'

# REST API
@app.route('/api/add_message/<uuid>', methods=['GET', 'POST'])
def add_message(uuid):
    content = request.json
    frame = json.loads(content)
    n = len(frame)
    hashtable = {"size": n, "data": frame}
    content = json.dumps(hashtable)
    return content

@app.route('/api/prediction', methods=['POST'])
def prediction():
    content = request.json
    frame = json.loads(content)
    frame = cv2.UMat(np.array(frame, dtype=np.uint8))

    # Load Yolo
    net = cv2.dnn.readNet("yolov3_pao2.weights", "yolov3_pao2.cfg")

    # Name custom object
    classes = ["pao frances"]

    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    colors = np.random.uniform(0, 255, size=(len(classes), 3))

    # Loading image
    img = frame 
    #img = cv2.resize(img, None, fx=0.4, fy=0.4)
    height, width, channels = img.get().shape

    # Detecting objects
    blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    # Showing informations on the screen
    class_ids = []
    confidences = []
    boxes = []
    qtd = np.zeros(len(classes))
    for out in outs:
        for detection in out: # detection = [w, h, x, y, c1, c2, ...]
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.3:
                # Object detected
                qtd[class_id] += 1
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                # Rectangle coordinates
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    font = cv2.FONT_HERSHEY_PLAIN
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            color = colors[class_ids[i]]
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
            cv2.putText(img, label, (x, y + 30), font, 3, color, 2)

    img = cv2.UMat.get(img).tolist()
    qtd = qtd.tolist()
    hashtable = {"qtd": qtd, "data": img}
    content = json.dumps(hashtable)
    return content



# Run the application
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production application.
    app.debug = True
    app.run(host="0.0.0.0")
