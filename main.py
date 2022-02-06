from time import time
import cv2
from numpy import intersect1d
import torch
from gpiozero import Buzzer, Servo
from serial import Serial

model = torch.hub.load('ultralytics/yolov5', 'yolov5m')
danger = open('danger.txt').read().strip().split('\n')
gsm = Serial("/dev/ttyUSB0", 9600, timeout=0.5)
gsm.flush()
servo = Servo(4)
bz = Buzzer(3)

mobile = '##########'  # Mobile Number to send the SMS

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)


def sendSms(msg):
    print("Sending SMS\n")
    gsm.write(b'AT+CMGF=1\r\n')
    time.sleep(0.5)
    gsm.write(b'AT+CMGS=\"')
    gsm.write(mobile.encode())
    gsm.write(b'\"\r\n')
    time.sleep(0.5)
    data = msg
    gsm.write(data.encode())
    gsm.write(b'\x1A')
    time.sleep(3)


def detect(img):
    result = model(img)
    result.print()
    object = result.pandas().xyxy[0].name.unique()
    print(object)

    common = intersect1d(object, danger)

    if(len(common)):
        # Raise Alarm
        sendSms('There is an intrusion in the farm')
        bz.on()
        print("ALARM")


while True:
    t0 = time()
    val = -10
    add = 2

    frame = None
    success, frame = cap.read()
    if success:
        detect(frame)
    else:
        print('Error in Camera')  # For debugging purposes
        continue

    servo.value = val/10.0

    while(time()-t0 < 10):
        continue

    bz.off()
    val += add

    if(val == 10 or val == -10):
        add *= -1

    print('time taken:   ')
    print(time()-t0)
