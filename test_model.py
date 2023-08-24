from ultralytics import YOLO
import cv2


modelPath = 'model/model-n.pt'
testPath1 = 'test1.png'
testPath2 = 'test2.png'

mdl = YOLO(modelPath)
res = mdl(testPath2)

print(res[0])
cv2.imshow("img", res[0].plot())
cv2.waitKey(10000)