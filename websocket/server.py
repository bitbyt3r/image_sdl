#!/usr/local/bin/python3
import subprocess
import websockets
import threading
import asyncio
import json
import time

image = {'ID': 1, 'Data': None}
speed = 10

def update(img, spd):
  global image, speed
  image = img
  speed = spd

class cameraThread:
  def __init__(self, update):
    self.update = update
    self.thread = threading.Thread(target=self.run)
    self.image = {}
    self.speed = {}

  def start(self):
    self.thread.daemon = True
    self.thread.start()

  def run(self):
    print("Running monitor thread")
    self.proc = subprocess.Popen(['python3', 'camera.py'], stdout=subprocess.PIPE)
    while True:
      line = self.proc.stdout.readline()
      try:
        data = json.loads(line.decode('ASCII'))
        if data['type'] == "image":
          self.image = data
        else:
          self.speed = data
        self.update(self.image, self.speed)
      except:
        print(line)

cam = cameraThread(update)
cam.start()

async def open(websocket, path):
  id = 0
  myspeed = 0
  while True:
    if image['ID'] > id:
      await websocket.send(json.dumps({'type': 'image', 'image': image['Data']}))
      id = image['ID']
    if speed != myspeed:
      await websocket.send(json.dumps({'type': 'speed', 'speed': speed}))
      myspeed = speed
    await asyncio.sleep(0.25)

ws_server = websockets.serve(open, 'localhost', 8000)

asyncio.get_event_loop().run_until_complete(ws_server)
asyncio.get_event_loop().run_forever()

