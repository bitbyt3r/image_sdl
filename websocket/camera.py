#!/usr/local/bin/python3
import numpy as np
import random
import base64
import json
import time
import cv2
import sys

class Camera:
  def __init__(self):
    self.image = {'type': 'image', 'ID': 0, 'Data': None}
    self.speed = {'type': 'speed', 'Data': 0}
    
  def start(self):
    cap = cv2.VideoCapture(0)
    while True:
      frame = cap.read()[1]
      cnt = cv2.imencode('.jpg',frame)[1].tostring()
      b64 = base64.encodestring(cnt)
      self.image['ID'] += 1
      self.image['Data'] = b64.decode('ASCII')
      self.speed['Data'] = self.getSpeed(frame)
      print(json.dumps(self.speed))
      print(json.dumps(self.image))
      sys.stdout.flush()
      time.sleep(2)

  def getSpeed(frame):
    speed = 1
    
    return speed

cam = Camera()
cam.start()
