import numpy as np
import imutils
import paho.mqtt.client as mqtt
import cv2
import os
import json
from imutils.video import VideoStream
from imutils.video import FPS
import face_recognition
import pickle
import time

from datetime import datetime

from common import clock, draw_str, draw_strApe, draw_rects, overlay_transparent

class VideoCamera(object):
    def __init__(self, camara=1):
        self.detector = cv2.CascadeClassifier('model/haarcascade_frontalface_default.xml')
        self.data = pickle.loads(open('encodings/encodings.pickle', "rb").read())
        self.input_cam = camara #indice de la Camara
        self.video = cv2.VideoCapture(camara) #Cap de la camara
        self.ban = False #Bandera Para que cargue una sola Vez el Modelo YOLO
    
    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, frame = self.video.read()
        if success:
            image = frame
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            #marco = self.stream(frame)
            #marco = self.face_reco(image, gray, rgb)
            marco = self.face_demo(image, gray, rgb)
            ret, jpeg = cv2.imencode('.jpg', marco)
            return jpeg.tobytes()
        else:
            print ("error")

    def get_img(self):
        success, frame = self.video.read()
        if success:
            image = frame
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            #marco = self.stream(frame)
            #marco = self.face_reco(image, gray, rgb)
            marco = self.face_demo(image, gray, rgb)
            
            return marco
        else:
            print ("error")

    def stream(self, camera):
        #Por unica vez
        if self.ban == False:
            self.ban = True
        #Bucle    
        return camera

    def face_demo(self, camera,gray,rgb):
        ##########################Por unica vez###########################
        if self.ban == False:
            
            self.ban = True
        ##############################Bucle#####################################
        #camera = cv2.flip(camera,1)
        
        rects = self.detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=6, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)

        boxes = [(y, x + w, y + h, x) for (x, y, w, h) in rects]

        t = clock()
        dt = clock() - t
        valor = ('%sK' % (dt/1000))[:4]
        
        if len(rects) > 0:
            rects[:,2:] += rects[:,:2]
            for x1, y1, x2, y2 in rects:
                centrox = int((x1 + x2 ) / 2)
                centroy = int((y1 + y2 ) / 2)
                draw_rects(camera, rects, (0, 255, 0))
                overlay = cv2.imread('img/ventana.png', cv2.IMREAD_UNCHANGED)
                overlay_transparent(camera, overlay, centrox + 80, centroy + 10)
                draw_str(camera, (centrox + 195, centroy + 28), valor)

        encodings = face_recognition.face_encodings(rgb, boxes)
        names = []
        for encoding in encodings:

            matches = face_recognition.compare_faces(self.data["encodings"],
                encoding,tolerance=0.5)
            name = "Unknown"

            
            if True in matches:

                matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                counts = {}

                
                for i in matchedIdxs:
                    name = self.data["names"][i]
                    counts[name] = counts.get(name, 0) + 1

                
                name = max(counts, key=counts.get)
            
            
            names.append(name)

            for x1, y1, x2, y2 in rects:
                centrox = int((x1 + x2 ) / 2)
                centroy = int((y1 + y2 ) / 2)
                draw_strApe(camera, (centrox + 110, centroy + 45), name)
        
        for ((top, right, bottom, left), name) in zip(boxes, names):
            pass


        

        return camera

"""if __name__=='__main__':
    vid=VideoCamera(1)
    while True:
        capt=vid.get_img()
        cv2.imshow("fra",capt)
        if cv2.waitKey(1)&0xFF == ord("q"):
            break"""