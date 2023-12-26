#Mouse Event
import cv2
import numpy as np
import pyrebase
import urllib
import urllib.request
   

LR = None

#url = 'http://192.168.195.74/640x480.jpg'
#im = None

def LorR(startX,endX):
    center = 320
    start = center-startX
    end = endX-center
    if start > end:
        LR =  "1" #"Left"
    elif start < end:
        LR =  "2"#"Right"
    
    return LR
    
firebaseConfig={  "apiKey": "AIzaSyDc-8VFnDPLkAPKoBCYlo-ffd7XVjUNjlM",
  "authDomain": "test-666a1.firebaseapp.com",
  "databaseURL": "https://test-666a1-default-rtdb.asia-southeast1.firebasedatabase.app",
  "projectId": "test-666a1",
  "storageBucket": "test-666a1.appspot.com",
  "messagingSenderId": "423503459287",
  "appId": "1:423503459287:web:40d825a46c58ea03595192"}    

firebase=pyrebase.initialize_app(firebaseConfig)

db=firebase.database()

CLASSES = ["BACKGROUND", "AEROPLANE", "BICYCLE", "BIRD", "BOAT",
	"BOTTLE", "BUS", "CAR", "CAT", "CHAIR", "COW", "DININGTABLE",
	"DOG", "HORSE", "MOTORBIKE", "PERSON", "POTTEDPLANT", "SHEEP",
	"SOFA", "TRAIN", "TVMONITOR"]

Color = np.random.uniform(0,100,size = (len(CLASSES),3))

net = cv2.dnn.readNetFromCaffe("./MobileNetSSD/MobileNetSSD.prototxt","./MobileNetSSD/MobileNetSSD.caffemodel")

cap = cv2.VideoCapture(0)

while True:

    ret,frame = cap.read()
    frameresizr = cv2.resize(frame,(600,640))
    if ret :
    
    

        (h,w) = frameresizr.shape[:2]
        blod = cv2.dnn.blobFromImage(frameresizr, 0.007843,(300,300),127.5)
        net.setInput(blod)
        detections = net.forward()

        for i in np.arange (0,detections.shape[2]):
            percent = detections[0,0,i,2]
            if percent > 0.7:
                clas_index = int(detections[0,0,i,1])
                box = detections[0,0,i,3:7]*np.array([w,h,w,h])
                (startX, startY,endX,endY) = box.astype("int")
                label = "{} [{:.2f}%]".format(CLASSES[clas_index],percent*100)
                cv2.rectangle(frameresizr,(startX,startY),(endX,endY),Color[clas_index],5)
                #cv2.rectangle(frame,(startX-1,startY-30),(endX+1,endY),Color[clas_index],cv2.FILLED)
                y = startX - 15 if startY-15>15 else startY+15
                cv2.putText(frameresizr,label,(startX+20,y+5),cv2.FONT_HERSHEY_DUPLEX,0.6,(255,255,255),1)
                direction = LorR(startX,endX)
                db.child("/Moter1Status").set(direction)
                print(direction)
            cv2.imshow("Output",frameresizr)
        if cv2.waitKey(1) & 0xff == ord("e"):
            break
    else:
        break




cv2.waitKey(delay=0)
cv2.destroyAllWindows()




