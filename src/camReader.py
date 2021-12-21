import cv2

class CamReader:
    def __init__(self, fps, frameWidth, frameHeight):
        self.trainedData = cv2.CascadeClassifier("trained_data.xml")
        self.fps = fps
        self.vid = cv2.VideoCapture(0)
        self.vid.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
        self.vid.set(cv2.CAP_PROP_FRAME_WIDTH, frameWidth)
        self.vid.set(cv2.CAP_PROP_FRAME_HEIGHT, frameHeight)
        self.vid.set(cv2.CAP_PROP_FPS, self.fps)

    def readFrame(self):
        _, self.frame = self.vid.read()

    def displayFrame(self):
        cv2.imshow("frame", self.frame)

    def detectFaces(self):
        frameGray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        return  self.trainedData.detectMultiScale(frameGray, 1.1, 4)
