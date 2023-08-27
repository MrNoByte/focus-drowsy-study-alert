import cv2 as cv
import uuid
import time
import os
from playsound import playsound

PATH = "data/"
CAMERA_PATH = "assets/music/camera.mp3"
DONE_PATH = "assets/music/done.mp3"

labels = ["focus","studying","yawn-open", "yawn-covered", "head-down"]

isRunning = True

curIndex = 0
delay = 2
clickTime = 0
cTime = 0
catLen = 5
cCatItem = 0


def saveImg(img,label):
    if not os.path.exists(PATH):
        os.mkdir(PATH)
        print(f"{PATH}\ncreated successfully")

    name = f"{PATH}{label}-{uuid.uuid1()}.jpg"
    cv.imwrite(name,img)
    print(name)
    

vid = cv.VideoCapture(0)
vid.set(cv.CAP_PROP_FRAME_HEIGHT, 480)
vid.set(cv.CAP_PROP_FRAME_WIDTH, 640)
clickTime = time.time()
while vid.isOpened() and isRunning:
    _, img = vid.read()
    cTime = time.time()
    

    key = cv.waitKey(1)
    if key == ord(' ') or cTime - clickTime >= delay:
        print("space pressed")
        saveImg(img,labels[curIndex])
        clickTime = cTime
        cCatItem += 1

        
        if cCatItem >= catLen:
            cCatItem = 0
            curIndex += 1
            clickTime += delay * 2
            playsound(DONE_PATH)
            
            if(curIndex >= len(labels)):
                break
        else:
            playsound(CAMERA_PATH)
        
    elif key == ord('q'):
        break


    cv.putText(img, f"{labels[curIndex]} | {cCatItem} | {round(cTime-clickTime,2)}"  ,(10,30),cv.FONT_HERSHEY_COMPLEX,1,(255,255,255),1)
    cv.imshow('vid',img)

    if cv.getWindowProperty('vid',cv.WND_PROP_VISIBLE) < 1:
        isRunning = False
        print("we are closed")
        break

    # print("loop completed")

vid.release()
cv.destroyAllWindows()