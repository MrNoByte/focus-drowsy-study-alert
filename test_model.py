# from ultralytics import YOLO
# import cv2


# modelPath = 'model/model-n.pt'
# testPath1 = 'test1.png'
# testPath2 = 'test2.png'

# mdl = YOLO(modelPath)
# res = mdl(testPath2)

# print(res[0])
# cv2.imshow("img", res[0].plot())
# cv2.waitKey(10000)


import cv2
from ultralytics import YOLO

# Load the YOLOv8 model
modelPath = 'model/model-n.pt'
model = YOLO(modelPath)

# Open the video file
cap = cv2.VideoCapture(0)

# Loop through the video frames
while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()

    if success:
        # Run YOLOv8 inference on the frame
        results = model(frame)

        # Visualize the results on the frame
        annotated_frame = results[0].plot()

        # Display the annotated frame
        cv2.imshow("YOLOv8 Inference", annotated_frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        # Break the loop if the end of the video is reached
        break

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()