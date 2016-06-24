#!/usr/local/bin/python
# Standard imports
import cv2
import numpy as np;

cap = cv2.VideoCapture(0)
#cap = cv2.VideoCapture('test.avi')
fgbg = cv2.BackgroundSubtractorMOG2(10, 5, False)
ret, base = cap.read()

while(True):
    ret, frame = cap.read()
    detector = cv2.SimpleBlobDetector()
    fgmask = fgbg.apply(frame)
    diff = np.zeros((720,1280,3), np.uint8)
    cv2.absdiff(base, frame, diff)
    fgmask = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    ret, fgmask = cv2.threshold(fgmask, 15, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(fgmask.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    bigContours = []
    for contour in contours:
        if cv2.contourArea(contour) >= 1000:
            bigContours.append(contour)

    vis = np.zeros((720,1280,3), np.uint8)
    contour_image = cv2.drawContours(frame, bigContours, -1, (255, 0, 0), 1)

    cv2.imshow('frame',frame)
    cv2.imshow('mask',fgmask)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
 
