from PIL import Image
from PIL import ImageTk
import tkinter as tki
import cv2
import datetime
import os
import time
import json
import sys
import requests
import numpy as np

def create_home_screen(obj):
    obj.lab_home = tki.Label(text="Bem Vindo")
    obj.btn_go_client = tki.Button(obj.root, text="Comprar",
            command=lambda: obj.event_manager("go_client"))
    obj.btn_go_admin = tki.Button(obj.root, text="admin",
            command=lambda: obj.event_manager("go_admin"))

def pack_home_screen(obj):
    obj.lab_home.pack(side="bottom", fill="both", expand="yes", padx=10,
                        pady=10)
    obj.btn_go_client.pack(side="bottom", fill="both", expand="yes", padx=10,
                        pady=10)
    obj.btn_go_admin.pack(side="bottom", fill="both", expand="yes", padx=10,
                        pady=10)

def hide_home_screen(obj):
    obj.lab_home.pack_forget()
    obj.btn_go_client.pack_forget()
    obj.btn_go_admin.pack_forget()

def create_client_main(obj):
    obj.panel = tki.Label(image=None)
    obj.panel.image = None
    obj.btn_snapshot = tki.Button(obj.root, text="Snapshot!",
            command=lambda: obj.event_manager("snapshot"))
    obj.btn_go_home = tki.Button(obj.root, text="go home",
            command=lambda: obj.event_manager("go_home"))

def pack_client_main(obj):
    obj.panel.pack(side="left", padx=10, pady=10)
    obj.btn_snapshot.pack(side="bottom", fill="both", expand="yes", padx=10,
                        pady=10)
    obj.btn_go_home.pack(side="bottom", fill="both", expand="yes", padx=10,
                        pady=10)


def hide_client_main(obj):
    obj.btn_snapshot.pack_forget()
    obj.btn_go_home.pack_forget()
    obj.panel.pack_forget()

def create_client_show(obj):
    obj.lab_checkout = tki.Label(text="Confirme seu pedido jndfnanlsnaka = 1000 reais")
    obj.btn_checkout = tki.Button(obj.root, text="checkout",
            command=lambda: obj.event_manager("checkout"))
    obj.btn_repeat = tki.Button(obj.root, text="repeat",
            command=lambda: obj.event_manager("repeat"))

def pack_client_show(obj):
    obj.panel.pack(side="left", padx=10, pady=10)
    obj.lab_checkout.pack(side="bottom", fill="both", expand="yes", padx=10,
                        pady=10)
    obj.btn_checkout.pack(side="bottom", fill="both", expand="yes", padx=10,
                        pady=10)
    obj.btn_repeat.pack(side="bottom", fill="both", expand="yes", padx=10,
                        pady=10)
    obj.btn_go_home.pack(side="bottom", fill="both", expand="yes", padx=10,
                        pady=10)

def hide_client_show(obj):
    obj.lab_checkout.pack_forget()
    obj.btn_checkout.pack_forget()
    obj.btn_repeat.pack_forget()
    obj.btn_go_home.pack_forget()
    obj.panel.pack_forget()

def create_client_pay(obj):
    obj.btn_pay = tki.Button(obj.root, text="pagar",
            command=lambda: obj.event_manager("pay"))
    obj.btn_cancel = tki.Button(obj.root, text="cancel",
            command=lambda: obj.event_manager("cancel"))

def pack_client_pay(obj):
    obj.lab_checkout.pack(side="bottom", fill="both", expand="yes", padx=10,
                        pady=10)
    obj.btn_pay.pack(side="bottom", fill="both", expand="yes", padx=10,
                        pady=10)
    obj.btn_cancel.pack(side="bottom", fill="both", expand="yes", padx=10,
                        pady=10)

def hide_client_pay(obj):
    obj.lab_checkout.pack_forget()
    obj.btn_pay.pack_forget()
    obj.btn_cancel.pack_forget()

def create_thanks(obj):
    obj.lab_thanks = tki.Label(text="Compra Efetivada!! Volte Sempre")

def pack_thanks(obj):
    obj.lab_thanks.pack(side="bottom", fill="both", expand="yes", padx=10,
                        pady=10)

def hide_thanks(obj):
    obj.lab_thanks.pack_forget()

def create_admin_login(obj):
    obj.btn_go_home = tki.Button(obj.root, text="go home",
            command=lambda: obj.event_manager("go_home"))
    obj.btn_login = tki.Button(obj.root, text="login",
            command=lambda: obj.event_manager("login"))

def pack_admin_login(obj):
    obj.btn_go_home.pack(side="bottom", fill="both", expand="yes", padx=10,
                        pady=10)
    obj.btn_login.pack(side="bottom", fill="both", expand="yes", padx=10,
                        pady=10)

def hide_admin_login(obj):
    obj.btn_go_home.pack_forget()
    obj.btn_login.pack_forget()

def create_admin_index(obj):
    obj.btn_go_home = tki.Button(obj.root, text="go home",
            command=lambda: obj.event_manager("go_home"))
    #res = requests.get('http://localhost:5000/api/index_products')
    res = requests.get('http://localhost:5000/api/database')
    #msg = ''
    obj.btns_product = []
    if res.ok:
        res = res.json()
        for product in res["productList"]:
            obj.btns_product.append(tki.Button(obj.root, text=product["name"], command=lambda name=product["name"]: obj.event_manager(name)))
    else:
        print("fail")

def pack_admin_index(obj):
    obj.btn_go_home.pack(side="bottom", fill="both", expand="yes", padx=10,
                        pady=10)
    #obj.lab_index.pack(side="bottom", fill="both", expand="yes", padx=10,
    #                    pady=10)
    for btn in obj.btns_product:
        btn.pack(side="bottom", fill="both", expand="yes", padx=10,
                        pady=10)

def hide_admin_index(obj):
    obj.btn_go_home.pack_forget()
    #obj.lab_index.pack_forget()
    for btn in obj.btns_product:
        btn.pack_forget()

def create_show(obj, product):
    #res = requests.get('http://localhost:5000/api/show_product/%s'%product)
    res = requests.get('http://localhost:5000/api/database/%s'%product)
    if res.ok:
        res = res.json()
        price = res["price"]
        obj.lab_prod = tki.Label(text="%s: $%.2f"%(product, price))
        obj.ent_price = tki.Entry(obj.root)
        obj.ent_price.delete(0)
        obj.ent_price.insert(0, "%.2f"%price)
    else:
        print("fail")

    obj.btn_record = tki.Button(obj.root, text="record", command=lambda name=product: obj.event_manager(name))
    obj.btn_go_home = tki.Button(obj.root, text="go_home",
            command=lambda: obj.event_manager("go_home"))
    obj.panel = tki.Label(image=None)

def pack_show(obj):
    obj.ent_price.pack(side="bottom", fill="both", expand="yes", padx=10,
                        pady=10)
    obj.lab_prod.pack(side="bottom", fill="both", expand="yes", padx=10,
                        pady=10)
    obj.btn_record.pack(side="bottom", fill="both", expand="yes", padx=10,
                        pady=10)
    obj.btn_go_home.pack(side="bottom", fill="both", expand="yes", padx=10,
                        pady=10)
    obj.panel.pack(side="left", padx=10, pady=10)

def hide_show(obj):
    obj.ent_price.pack_forget()
    obj.lab_prod.pack_forget()
    obj.btn_record.pack_forget()
    obj.btn_go_home.pack_forget()
    obj.panel.pack_forget()

def create_calibrated(obj, product):
    obj.btn_record = tki.Button(obj.root, text="record", command=lambda name=product: obj.event_manager(name))
    obj.btn_go_home = tki.Button(obj.root, text="go_home",
            command=lambda: obj.event_manager("go_home"))
    obj.panel1 = tki.Label(image=None)
    obj.panel2 = tki.Label(image=None)

def pack_calibrated(obj):
    obj.btn_record.pack(side="bottom", fill="both", expand="yes", padx=10,
                        pady=10)
    obj.btn_go_home.pack(side="bottom", fill="both", expand="yes", padx=10,
                        pady=10)
    obj.panel1.pack(side="left", padx=10, pady=10)
    obj.panel2.pack(side="left", padx=10, pady=10)

def hide_calibrated(obj):
    obj.btn_record.pack_forget()
    obj.btn_go_home.pack_forget()
    obj.panel1.pack_forget()
    obj.panel2.pack_forget()

def create_get_frames(obj, product):
    obj.btn_record = tki.Button(obj.root, text="record", command=lambda name=product: obj.event_manager(name))
    obj.btn_go_home = tki.Button(obj.root, text="go_home",
            command=lambda: obj.event_manager("go_home"))
    obj.panel = tki.Label(image=None)

def pack_get_frames(obj):
    obj.btn_record.pack(side="bottom", fill="both", expand="yes", padx=10,
                        pady=10)
    obj.btn_go_home.pack(side="bottom", fill="both", expand="yes", padx=10,
                        pady=10)
    obj.panel.pack(side="left", padx=10, pady=10)

def hide_get_frames(obj):
    obj.btn_record.pack_forget()
    obj.btn_go_home.pack_forget()
    obj.panel.pack_forget()

def create_recorded(obj, product):
    obj.btn_confirm = tki.Button(obj.root, text="confirm", command=lambda name=product: obj.event_manager(name))
    obj.btn_go_home = tki.Button(obj.root, text="go_home",
            command=lambda: obj.event_manager("go_home"))
    obj.panel = tki.Label(image=None)

def pack_recorded(obj):
    obj.btn_confirm.pack(side="bottom", fill="both", expand="yes", padx=10,
                        pady=10)
    obj.btn_go_home.pack(side="bottom", fill="both", expand="yes", padx=10,
                        pady=10)
    obj.panel.pack(side="left", padx=10, pady=10)
    
def hide_recorded(obj):
    obj.btn_confirm.pack_forget()
    obj.btn_go_home.pack_forget()
    obj.panel.pack_forget()

def create_admin_confirm(obj, product):
    obj.lab_confirm = tki.Label(text="adicionando %s"%product)
    obj.lab_loading = tki.Label(text=None)

def pack_admin_confirm(obj):
    obj.lab_loading.pack(side="bottom", fill="both", expand="yes", padx=10,
                        pady=10)
    obj.lab_confirm.pack(side="bottom", fill="both", expand="yes", padx=10,
                        pady=10)

def hide_admin_confirm(obj):
    obj.lab_loading.pack_forget()
    obj.lab_confirm.pack_forget()

def action0(obj):
    create_home_screen(obj)
    pack_home_screen(obj)

def action1(obj):
    hide_home_screen(obj)
    create_client_main(obj)
    pack_client_main(obj)
    obj.vs = cv2.VideoCapture(obj.input)

def action2(obj):
    obj.vs.release()
    hide_client_main(obj)
    create_client_show(obj)
    pack_client_show(obj)
    ts = datetime.datetime.now()
    filename = "{}.jpg".format(ts.strftime("%Y-%m-%d_%H:%M:%S"))
    p = os.path.sep.join((obj.outputPath, filename))
    frame = obj.frame.copy()
    cv2.imwrite(p, frame)
    obj.last_photo = p

    # YOLO
    frame = cv2.resize(frame, None, fx=0.4, fy=0.4)
    frame = frame.tolist()
    data = json.dumps(frame)
    res = requests.post('http://localhost:5000/api/prediction', json = data)
    #res = requests.post('http://aws-test.eba-gajbic4g.sa-east-1.elasticbeanstalk.com/api/prediction', json = data)
    if res.ok:
        res = res.json()
        obj.cart = res["cart"]
        img = res["data"]
        img = cv2.UMat(np.array(img, dtype=np.uint8))
        cv2.imwrite(p, img)
        obj.last_photo = p

def action3(obj):
    hide_client_show(obj)
    create_client_pay(obj)
    pack_client_pay(obj)

def action4(obj):
    obj.vs = cv2.VideoCapture(obj.input)
    hide_client_show(obj)
    pack_client_main(obj)

def action5(obj):
    obj.vs.release()
    hide_client_main(obj)
    pack_home_screen(obj)

def action6(obj):
    hide_client_show(obj)
    pack_home_screen(obj)

def action7(obj):
    hide_client_pay(obj)
    pack_home_screen(obj)

def action8(obj):
    hide_thanks(obj)
    pack_home_screen(obj)

def action9(obj):
    hide_client_pay(obj)
    create_thanks(obj)
    pack_thanks(obj)

def action10(obj):
    hide_home_screen(obj)
    create_admin_login(obj)
    pack_admin_login(obj)

def action11(obj):
    hide_admin_login(obj)
    pack_home_screen(obj)

def action12(obj):
    hide_admin_login(obj)
    create_admin_index(obj)
    pack_admin_index(obj)

def action13(obj):
    hide_admin_index(obj)
    pack_home_screen(obj)

def action14(obj, product):
    hide_admin_index(obj)
    create_show(obj, product)
    pack_show(obj)
    obj.vs = cv2.VideoCapture(obj.input)

def action15(obj):
    obj.vs.release()
    hide_show(obj)
    pack_home_screen(obj)

def action16(obj, product):
    price = obj.ent_price.get()
    try:
        price = float(price)
        hashtable = {"price":price}
        data = json.dumps(hashtable)
        #res = requests.post('http://localhost:5000/api/edit_product/%s'%product, json = data)
        res = requests.put('http://localhost:5000/api/database/%s'%product, json = data)
        #res = requests.post('http://aws-test.eba-gajbic4g.sa-east-1.elasticbeanstalk.com/api/prediction', json = data)
    except:
        print("fail")

    hide_show(obj)
    create_calibrated(obj, product)
    pack_calibrated(obj)
    ts = datetime.datetime.now()
    filename = "ref_%s/%s.jpg"%(product, ts.strftime("%Y-%m-%d_%H:%M:%S"))
    if not os.path.exists('%s/ref_%s'%(obj.dataLake, product)):
        os.makedirs('%s/ref_%s'%(obj.dataLake, product))
    p = os.path.sep.join((obj.dataLake, filename))
    frame = obj.frame.copy()
    cv2.imwrite(p, frame)
    obj.last_photo = p

def action17(obj):
    obj.vs.release()
    hide_calibrated(obj)
    pack_home_screen(obj)

def action18(obj, product):
    hide_calibrated(obj)
    create_get_frames(obj, product)
    pack_get_frames(obj)
    ts = datetime.datetime.now()
    filename = "frames_%s/%s.mp4"%(product, ts.strftime("%Y-%m-%d_%H:%M:%S"))
    if not os.path.exists('%s/frames_%s'%(obj.dataLake, product)):
        os.makedirs('%s/frames_%s'%(obj.dataLake, product))
    p = os.path.sep.join((obj.dataLake, filename))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    obj.video = cv2.VideoWriter(p, fourcc, obj.fps, obj.frameSize)
    obj.last_video = p

def action19(obj):
    obj.vs.release()
    hide_get_frames(obj)
    pack_home_screen(obj)
    obj.video.release()

def action20(obj, product):
    obj.vs.release()
    hide_get_frames(obj)
    create_recorded(obj, product)
    pack_recorded(obj)
    obj.video.release()

def action21(obj):
    hide_recorded(obj)
    pack_home_screen(obj)
    obj.cap.release()

def action22(obj, product):
    hide_recorded(obj)
    create_admin_confirm(obj, product)
    pack_admin_confirm(obj)
    obj.cap.release()
    obj.product = product
    

def action23(obj):
    hide_admin_confirm(obj)
    pack_home_screen(obj)


    

def state1(obj):
    _ret, frame = obj.vs.read()

    if frame is not None:
        obj.frame = frame
        # OpenCV represents images in BGR order; however PIL
        # represents images in RGB order, so we need to swap
        # the channels, then convert to PIL and ImageTk format
        obj.image = cv2.cvtColor(obj.frame, cv2.COLOR_BGR2RGB)
        obj.image = Image.fromarray(obj.image)
        obj.image = ImageTk.PhotoImage(obj.image)

        # if the panel is None, we need to initialize it
        #if obj.panel is None:
            #obj.panel = tki.Label(image=obj.image)
            #obj.panel.image = obj.image
            #obj.panel.pack(side="left", padx=10, pady=10)

        # otherwise, simply update the panel
        obj.panel.configure(image=obj.image)
        obj.panel.image = obj.image

def state2(obj):
    # aqui vai o yolo
    if obj.last_photo:
        obj.frame = cv2.imread(obj.last_photo)
        obj.last_photo = None
        
        # display yolo image 
        obj.image = cv2.cvtColor(obj.frame, cv2.COLOR_BGR2RGB)
        obj.image = Image.fromarray(obj.image)
        obj.image = ImageTk.PhotoImage(obj.image)
        obj.panel.configure(image=obj.image)
        obj.panel.image = obj.image
        msg = "CARRINHO\n\n"
        total = 0
        for product in obj.cart['productList']:
            msg += "%s: %d x %f\n"%(product['name'], product['quantity'], product['itemPrice'])
            total += product['quantity'] * product['itemPrice']
        msg += "-----------------------------------------\n"
        msg += "Total: %f"%(total)
        obj.lab_checkout.configure(text=msg)

def state4(obj):
    time0 = time.time()
    time1 = time.time()
    while time1 - time0 < 2: time1 = time.time()
    obj.event_manager()

def state7(obj):
    _ret, frame = obj.vs.read()

    if frame is not None:
        obj.frame = frame
        # OpenCV represents images in BGR order; however PIL
        # represents images in RGB order, so we need to swap
        # the channels, then convert to PIL and ImageTk format
        obj.image = cv2.cvtColor(obj.frame, cv2.COLOR_BGR2RGB)
        obj.image = Image.fromarray(obj.image)
        obj.image = ImageTk.PhotoImage(obj.image)

        # otherwise, simply update the panel
        obj.panel.configure(image=obj.image)
        obj.panel.image = obj.image

def state8(obj):
    # aqui vai o yolo
    if obj.last_photo:
        obj.frame = cv2.imread(obj.last_photo)
        obj.ref = obj.last_photo
        obj.last_photo = None

        # display yolo image
        obj.image = cv2.cvtColor(obj.frame, cv2.COLOR_BGR2RGB)
        obj.image = Image.fromarray(obj.image)
        obj.image = ImageTk.PhotoImage(obj.image)
        obj.panel1.configure(image=obj.image)
        obj.panel1.image = obj.image

    _ret, frame = obj.vs.read()

    if frame is not None:
        obj.frame = frame
        # OpenCV represents images in BGR order; however PIL
        # represents images in RGB order, so we need to swap
        # the channels, then convert to PIL and ImageTk format
        obj.image = cv2.cvtColor(obj.frame, cv2.COLOR_BGR2RGB)
        obj.image = Image.fromarray(obj.image)
        obj.image = ImageTk.PhotoImage(obj.image)

        # otherwise, simply update the panel
        obj.panel2.configure(image=obj.image)
        obj.panel2.image = obj.image

def state9(obj):
    _ret, frame = obj.vs.read()
    if frame is not None:
        obj.frame = frame
        obj.video.write(obj.frame)

        # OpenCV represents images in BGR order; however PIL
        # represents images in RGB order, so we need to swap
        # the channels, then convert to PIL and ImageTk format
        obj.image = cv2.cvtColor(obj.frame, cv2.COLOR_BGR2RGB)
        obj.image = Image.fromarray(obj.image)
        obj.image = ImageTk.PhotoImage(obj.image)

        # otherwise, simply update the panel
        obj.panel.configure(image=obj.image)
        obj.panel.image = obj.image

def state10(obj):
    if obj.last_video:
        try:
            obj.cap = cv2.VideoCapture(obj.last_video)
            obj.sample = obj.last_video
            obj.last_video = None
            obj.frame_counter = 0
        except:
            print("erro ao load video")
    else:
        if obj.cap.isOpened():
            _ret, obj.frame = obj.cap.read()
            obj.frame_counter += 1
            #If the last frame is reached, reset the capture and the frame_counter
            if obj.frame_counter == obj.cap.get(cv2.CAP_PROP_FRAME_COUNT):
                obj.frame_counter = 0 #Or whatever as long as it is the same as next line
                obj.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            try:
                obj.image = cv2.cvtColor(obj.frame, cv2.COLOR_BGR2RGB)
                obj.image = Image.fromarray(obj.image)
                obj.image = ImageTk.PhotoImage(obj.image)
                # otherwise, simply update the panel
                obj.panel.configure(image=obj.image)
                obj.panel.image = obj.image
            except:  
                print("eror")

def state11(obj):
    ts = datetime.datetime.now()
    date = ts.strftime("%Y-%m-%d_%H:%M:%S")
    frame = cv2.imread(obj.ref)
    hashtable = {"time_stamp": date, "frame_type": "ref", "number": "0", "frame": frame.tolist()}
    data = json.dumps(hashtable)
    res = requests.post('http://localhost:5000/api/datalake/%s'%obj.product, json = data)
    cap = cv2.VideoCapture(obj.sample)
    i = 0
    total = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    trigger = total // obj.frames_per_video
    while frame is not None and i < total:
        _ret, frame = cap.read()
        if i%trigger == 0:
            obj.lab_loading.configure(text="%d of %d"%(i//trigger, obj.frames_per_video))
            hashtable = {"time_stamp": date, "frame_type": "sample", "number": str(int(i//trigger)), "frame": frame.tolist()}
            data = json.dumps(hashtable)
            res = requests.post('http://localhost:5000/api/datalake/%s'%obj.product, json = data)
        i += 1
    cap.release()

    #time0 = time.time()
    #time1 = time.time()
    #while time1 - time0 < 2: time1 = time.time()
    obj.event_manager()


