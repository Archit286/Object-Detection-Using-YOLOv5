from time import time
import cv2
from numpy import intersect1d
import torch

model = torch.hub.load('ultralytics/yolov5', 'yolov5m')
danger = open('danger.txt').read().strip().split('\n')
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)


def detect(img):
    result = model(img)
    result.print()
    object = result.pandas().xyxy[0].name.unique()
    print(object)

    common = intersect1d(object, danger)

    if(len(common)):
        # Raise Alarm
        print("ALARM")


while True:
    t0 = time()

    frame = None
    success, frame = cap.read()
    if success:
        detect(frame)
    else:
        print('Error in Camera')  # For debugging purposes
        continue

    while(time()-t0 < 10):
        continue

    print('time taken:   ')
    print(time()-t0)
