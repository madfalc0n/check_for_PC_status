import numpy as np
import cv2

def capture(mode=0):
    

    if mode == -1 : #initializing mode
        print("-----> Capture Test by webcam")
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        if cap.isOpened():
            ret, frame = cap.read()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            print(f"-----> Capture IMAGE shape : {len(frame)} {len(frame[0])}")
        else:
            print("-----> WEBCAM is not initializing")
            return
    else:
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        if cap.isOpened():
            ret, frame = cap.read()
        else:
            print("-----> WEBCAM is not initializing")
            return

    cap.release()
    return frame

if __name__ == "__main__":
    frame = capture()
    path = './log_pic/'
    cv2.imwrite(path + 'test_img.jpg',frame)
    