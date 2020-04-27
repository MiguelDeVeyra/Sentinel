from PyQt5.QtWidgets import (QMessageBox, QPushButton, QWidget, QInputDialog,
                            QLineEdit, QApplication, QLabel)
from PyQt5.QtCore import (QCoreApplication, QObject, QRunnable, QThread,
                          QThreadPool, pyqtSignal, pyqtSlot, Qt)
from PyQt5.QtGui import (QImage, QPixmap)

#from camera import recognizeFace

#import cv2
#import sys

import numpy as np
import imutils
import pickle
import time
import cv2
import sys
import os

# float var to set minimum probability to filter weak face detections
CONFIDENCE = 0.5
# float var to set minimum threshold to filter our weak probabilities
THRESHOLD = 0.65

# face detector and pre-trained model
FACE_DETECTOR_DIR = os.path.sep.join(["faceDetectionModel", "deploy.prototxt"])
MODEL_DIR = os.path.sep.join(["faceDetectionModel", "res10_300x300_ssd_iter_140000.caffemodel"])

detector = cv2.dnn.readNetFromCaffe(FACE_DETECTOR_DIR, MODEL_DIR)

# face embedding model
embedder = cv2.dnn.readNetFromTorch("openface_nn4.small2.v1.t7")

# face recognition model
recognizer = pickle.loads(open("output/recognizer.pickle", "rb").read())

# label encoder
le = pickle.loads(open("output/le.pickle", "rb").read())

def recognizeFace(frame):
    # resize the frame
    frame = imutils.resize(frame, width=600)
    # maintain the aspect ratio and get image dimensions
    (h, w) = frame.shape[:2]

    # construct a blob from the image using mean substraction
    # blob = cv2.dnn.blobFromImage(image, scalefactor=1.0, size, mean, swapRB=True)
    imageBlob = cv2.dnn.blobFromImage(
        cv2.resize(frame, (300, 300)), 1.0, (300, 300),
        (104.0, 177.0, 123.0), swapRB=False, crop=False)

    # use OpenCV face detector to find faces in the image
    detector.setInput(imageBlob)
    detections = detector.forward()

    # loop over the detections
    for i in range(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]

        # filter out weak detections
        if confidence > CONFIDENCE:
            # compute x and y coordinates of the detected face
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            # extract the face ROI
            face = frame[startY:endY, startX:endX]
            (fH, fW) = face.shape[:2]

            # checks if spatial dimensions are the right size
            if fW < 20 or fH < 20:
                continue

            # create a blob for face ROI, then pass it through
            # the face embedding model to obtain the 128-d
            # embeddings of the face
            faceBlob = cv2.dnn.blobFromImage(face, 1.0 / 255,
				(96, 96), (0, 0, 0), swapRB=True, crop=False)

            embedder.setInput(faceBlob)

            # vector with the embedded face
            vec = embedder.forward()

            # pass vector to the recognizer model, the result will tell
            # who is in the face ROI
            preds = recognizer.predict_proba(vec)[0]
            # take highest probability index  from the predictions
            j = np.argmax(preds)
            # extract the probability
            proba = preds[j]
            # use the label encoder to find the name from the dataset
            name = le.classes_[j]

            # filter out weak recognitions using a threshold
            if proba < THRESHOLD:
                continue

            # draw the bounding box of the face along with the
			# associated probability
            text = "{}: {:.2f}%".format(name, proba * 100)
            y = startY - 10 if startY - 10 > 10 else startY + 10
            cv2.rectangle(frame, (startX, startY), (endX, endY),
                (0, 0, 255), 2)
            cv2.putText(frame, text, (startX, y),
                cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)

    # Not within for loop
    return frame

class Thread(QThread):
    changePixmap = pyqtSignal(QImage)

    def run(self):
        # For Webcam
        #cap = cv2.VideoCapture(0)
        # For IP Camera
        cap = cv2.VideoCapture()
        cap.open("rtsp://admin:Admin123@192.168.1.2:554/Streaming/channels/101")
        while True:
            ret, frame = cap.read()
            if ret:
                # flip camera view if using IP Camera
                frame = cv2.flip(frame, 0)
                frame = recognizeFace(frame)
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Sentinel'
        self.left = 0
        self.top = 0
        self.width = 640
        self.height = 480
        self.initUI()

    @pyqtSlot(QImage)
    def setImage(self, image):
        self.label.setPixmap(QPixmap.fromImage(image))

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        #self.resize(1800, 1200)
        self.resize(640,600)
        # create a label
        self.label = QLabel(self)
        #self.label.move(280, 120)
        self.label.resize(800, 600)
        th = Thread(self)
        th.changePixmap.connect(self.setImage)
        th.start()
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
