from camReader import CamReader
import cv2
import time
import numpy as np
from pynput.mouse import Button, Controller
import os 

class CamHandler:
    def __init__(self, fps, frameWidth, frameHeight):
        self.cam = CamReader(fps, frameWidth, frameHeight)
        self.prevTime = 0
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.calibratedCenter = False
        self.calibratedRadius = False
        self.quit = False
        self.center = []
        self.radius = 0

        os.system("open ../sheet_music/*.pdf")
        self.mouse = Controller()

    def scroll(self):
        self.mouse.scroll(0, -10)

    def getFacePosition(self):
        faces = self.cam.detectFaces()
        for (x, y, w, h) in faces:
            return x, y, w, h

    def drawFace(self):
        x, y, w, h = self.getFacePosition()
        cv2.rectangle(self.cam.frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

    def drawCenterLine(self, color):
        x0, y0, w0, h0 = self.center[0]
        x1, y1, w1, h1 = self.getFacePosition()
        cv2.line(self.cam.frame, (int(x0 + w0/2), int(y0 + h0/2)),
                                 (int(x1 + w1/2), int(y1 + h1/2)),
                                 color, 2)

    def drawNoFaceText(self):
        cv2.putText(self.cam.frame, "Could not detect face", (2, 10), self.font, 0.5,
                    (255, 0, 255), 1, cv2.LINE_AA)

    def drawRadius(self):
        x, y, w, h = self.center[0]
        cv2.circle(self.cam.frame, (int(x + w/2), int(y + h/2)), self.radius,
                (0, 0, 255), 2)

    def calibrateCenter(self):
        while not self.calibratedCenter:
            self.cam.readFrame()

            if time.time() - self.prevTime > 1. / self.cam.fps:
                self.prevTime = time.time()
                try:
                    self.drawFace()
                except:
                    self.drawNoFaceText()
                self.cam.displayFrame()

            if cv2.waitKey(1) & 0xFF == ord('o'):
                self.center.append(self.getFacePosition())
                self.calibratedCenter = True

    def calibrateRadius(self):
        assert(self.calibratedCenter)
        while not self.calibratedRadius:
            self.cam.readFrame()

            if time.time() - self.prevTime > 1. / self.cam.fps:
                self.prevTime = time.time()
                try: 
                    self.drawFace()
                    self.drawCenterLine((0, 255, 0))
                except:
                    self.drawNoFaceText()
                self.cam.displayFrame()

            if cv2.waitKey(1) & 0xFF == ord('o'):
                xr, yr, wr, hr = self.getFacePosition()

                self.radius = int(np.sqrt(self.distSquared(xr, yr, 
                                      self.center[0][0], self.center[0][1])))
                self.calibratedRadius = True

    def distSquared(self, x0, y0, x1, y1):
        return (x1-x0)**2 + (y1-y0)**2

    def mainLoop(self):
        assert(self.calibratedRadius)
        assert(self.calibratedCenter)
        centerLineColor = (0, 255, 0)
        while not self.quit:
            self.cam.readFrame()

            if time.time() - self.prevTime > 1. / self.cam.fps:
                self.prevTime = time.time()
                try: 
                    self.drawFace()
                    self.drawCenterLine(centerLineColor)
                    self.drawRadius()
                except:
                    self.drawNoFaceText()

                self.cam.displayFrame()
            
            try:
                x0, y0, w0, h0 = self.center[0]
                x1, y1, w1, h1 = self.getFacePosition()
                if self.distSquared(x0, y0, x1, y1) > self.radius * self.radius:
                    self.scroll()
            except:
                pass

            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.quit = True
