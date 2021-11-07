from FRs import VideoCamera
import json
import cv2
 

def read():
    f = open('data/data.json')
    data = json.load(f)
    for i in data['configuracion']:
        camera = i['cap']
    f.close()
    return camera


if __name__=='__main__':
    camera = read()
    VS = VideoCamera(camera)
    while True:
        capt=VS.get_img()
        cv2.imshow("fra",capt)
        if cv2.waitKey(1)&0xFF == ord("q"):
            break