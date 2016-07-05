#!/usr/local/bin/python3
# Standard imports
import cv2
import numpy as np;

cap = cv2.VideoCapture(0)
#cap = cv2.VideoCapture('test.avi')
ret, start = cap.read()
start = cv2.GaussianBlur(start, (21, 21), 0)
start = cv2.cvtColor(start, cv2.COLOR_BGR2GRAY)

while(True):
    ret, frame = cap.read()
    frame = cv2.GaussianBlur(frame, (21, 21), 0)
    fgmask = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    fgmask = cv2.absdiff(start, fgmask)
    avg = max(np.average(fgmask), 10)
    fgmask = cv2.dilate(fgmask, None, iterations=2)
    ret, fgmask = cv2.threshold(fgmask, avg, 255, cv2.THRESH_BINARY)
    
    image, contours, hierarchy = cv2.findContours(fgmask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    bigContours = []
    for contour in contours:
        if cv2.contourArea(contour) >= 1000:
            bigContours.append(contour)

    vis = np.zeros((720,1280,3), np.uint8)
    contour_image = cv2.drawContours(frame, bigContours, -1, (255, 0, 0), 1)
    for contour in bigContours:
      (x, y, w, h) = cv2.boundingRect(contour)
      cv2.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 0), 2)

    cv2.imshow('frame',frame)
    cv2.imshow('mask',fgmask)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
 
