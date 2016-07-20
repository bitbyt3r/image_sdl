#!/usr/local/bin/python3
import cv2
from PIL import Image
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
from io import BytesIO
import time
capture=None
import websockets
import asyncio
import json
import random
import math
import numpy as np

def process(img):
  """Takes an image and assigns a speed from 0-1 based upon it."""
  global start
  frame = cv2.GaussianBlur(img, (21, 21), 0)
  fgmask = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
  fgmask = cv2.absdiff(start, fgmask)
  avg = max(np.average(fgmask), 10)
  fgmask = cv2.dilate(fgmask, None, iterations=2)
  ret, fgmask = cv2.threshold(fgmask, avg, 255, cv2.THRESH_BINARY)
  image, contours, hierarchy = cv2.findContours(fgmask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

  bigContours = []
  for contour in contours:
    if cv2.contourArea(contour) >= 3000:
      bigContours.append(contour)

  ax = 0
  ay = 0
  for contour in bigContours:
    moments = cv2.moments(contour)
    cx = int(moments['m10']/moments['m00'])
    cy = int(moments['m01']/moments['m00'])
    ax += cx
    ay += cy
  if not bigContours:
    speed = 0
  else:
    ax /= len(bigContours)
    ay /= len(bigContours)
    my, mx, channels = img.shape
    my /= 2
    mx /= 2
    dist = math.sqrt((ax - mx)**2 + (ay - my)**2)
    speed = max(min((mx - dist) / my, 1), 0.1)
    if speed > 0.8:
      speed = 1
  return speed

class CamHandler(BaseHTTPRequestHandler):
  def do_GET(self):
    if self.path.endswith('.mjpg'):
      self.send_response(200)
      self.send_header('Content-type','multipart/x-mixed-replace; boundary=--jpgboundary')
      self.end_headers()
      while True:
        try:
          rc,img = capture.read()
          if not rc:
            continue
          imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
          jpg = Image.fromarray(imgRGB)
          tmpFile = BytesIO()
          jpg.save(tmpFile,'JPEG')
          self.wfile.write("--jpgboundary".encode('UTF-8'))
          self.send_header('Content-type','image/jpeg')
          self.send_header('Content-length',str(tmpFile.getbuffer().nbytes))
          self.end_headers()
          jpg.save(self.wfile,'JPEG')
          global updater
          updater(process(img))
        except KeyboardInterrupt:
          break
      return
    if self.path.endswith('.html'):
      self.send_response(200)
      self.send_header('Content-type','text/html')
      self.end_headers()
      with open(self.path[1:], "rb") as FILE:
        self.wfile.write(FILE.read())
      return
    else:
      self.send_response(200)
      self.send_header('Content-type','text/html')
      self.end_headers()
      with open("./index.html", "rb") as FILE:
        self.wfile.write(FILE.read())
      return

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
  """Handle requests in a separate thread."""

class WebsocketServer:
  def __init__(self, loop, port=8000):
    self.port = port
    self.thread = threading.Thread(target=self.run)
    self.loop = loop
    self.speed = 0

  def update(self, speed):
    self.speed = speed

  def get_updater(self):
    return self.update

  def start(self):
    self.thread.start()

  def run(self):
    print("Serving Websockets")
    self.server = websockets.serve(self.open, 'localhost', self.port)
    asyncio.set_event_loop(self.loop)
    self.loop.run_until_complete(self.server)
    self.loop.run_forever()

  async def open(self, websocket, path):
    myspeed = -1
    while True:
      if self.speed != myspeed:
        await websocket.send(json.dumps({'type': 'speed', 'speed': self.speed}))
        myspeed = self.speed
      await asyncio.sleep(0.25)

def main():
  global updater
  global capture
  capture = cv2.VideoCapture(0)
  global start
  ret, start = capture.read()
  start = cv2.GaussianBlur(start, (21, 21), 0)
  start = cv2.cvtColor(start, cv2.COLOR_BGR2GRAY)
  global img
  try:
    server = ThreadedHTTPServer(('localhost', 8080), CamHandler)
    print("server started")
    loop = asyncio.get_event_loop()
    wsserver = WebsocketServer(loop)
    updater = wsserver.get_updater()
    wsserver.start()
    server.serve_forever()
  except KeyboardInterrupt:
    capture.release()
    server.socket.close()

if __name__ == '__main__':
  main()
