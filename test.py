from time import time
import cv2
from numpy import intersect1d
import torch

model = torch.hub.load('ultralytics/yolov5', 'yolov5m')
danger = open('danger.txt').read().strip().split('\n')


def detect(img):
    result = model(img)
    result.print()
    object = result.pandas().xyxy[0].name.unique()
    print(object)

    common = intersect1d(object, danger)

    if(len(common)):
        # Raise Alarm
        print("ALARM")


for i in range(25):
    t0 = time()

    path = './test/s' + str(i+1) + '.jpg'
    img = cv2.imread(path)

    detect(img)

    print('time taken:   ')
    print(time()-t0)
