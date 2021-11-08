from os import name
import time
import paho.mqtt.client as mqtt
import base64
import time
import imutils
import cv2
import json

class alarm(object):
    def send_mqtt(msg, camera):
        redim = imutils.resize(camera,150)
        retval, buffer_img= cv2.imencode('.jpg', redim)
        
        img = base64.b64encode(buffer_img).decode('utf-8')
        print("############################")
        print(type(img))
        print("############################")
        d = {"nombre":msg, "image":img}
        imagenjson = json.dumps(d)
       
        alarmajson = {"alarma":True,"nombre":msg}
        client = mqtt.Client()
        client.username_pw_set(username="frr_dev",password="frr_dev123456")
        client.connect("ng.drexgen.com", 1883, 60)
        client.publish("frr/alarma/imajen", imagenjson, 1)
        client.publish("frr/alarma", json.dumps(alarmajson), 1)
        #time.sleep(2)
 
