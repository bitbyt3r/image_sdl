#!/usr/bin/python
# Standard imports
import cv2
import numpy as np;


cap = cv2.VideoCapture(0)
fgbg = cv2.createBackgroundSubtractorMOG2()

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Set up the detector with default parameters.
    detector = cv2.SimpleBlobDetector_create()
 
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Detect blobs.
    fgmask = fgbg.apply(gray)
    keypoints = detector.detect(fgmask)
 
    # Draw detected blobs as red circles.
    # cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
    im_with_keypoints = cv2.drawKeypoints(frame, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    print([(x.pt, x.size, x.angle) for x in keypoints])
    # Display the resulting frame
    cv2.imshow('frame',im_with_keypoints)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
 
