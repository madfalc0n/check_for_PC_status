import numpy as np
import cv2


print("start caputer")
# cap = cv2.VideoCapture(0)
# print(cap.isOpened())
width, height = cap.get(3), cap.get(4)

if cap.isOpened():
    print("capture")
    print(width,height)
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # print(gray.shape)
    # cv2.imshow(gray)
    cv2.imwrite('test_img.jpg',gray)

cap.release()
   