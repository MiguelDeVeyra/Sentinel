from imutils.video import VideoStream
import numpy as np
import imutils
import pickle
import time
import cv2
import os

# float variable to set minimum probability to filter weak detections
CONFIDENCE = 0.5
# float var to set minimum threshold to filter our weak probabilities
# adds an extra layer of
THRESHOLD = 0.65

# face detector and pre-trained model
FACE_DETECTOR_DIR = os.path.sep.join(["faceDetectionModel", "deploy.prototxt"])
MODEL_DIR = os.path.sep.join(["faceDetectionModel", "res10_300x300_ssd_iter_140000.caffemodel"])

detector = cv2.dnn.readNetFromCaffe(FACE_DETECTOR_DIR, MODEL_DIR)

# face embedding model
embedder = cv2.dnn.readNetFromTorch("openface_nn4.small2.v1.t7 ")

# face recognition model
recognizer = pickle.loads(open("output/recognizer.pickle", "rb").read())

# label encoder
le = pickle.loads(open("output/le.pickle", "rb").read())

# connect to camera
rtsp = u"rtsp://admin:Admin123@192.168.1.2:554/Streaming/channels/101"
vs = VideoStream(src=rtsp).start()
time.sleep(2.0)

while True:
    frame = vs.read()
    # flip camera view
    frame = cv2.flip(frame, 0)

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

            # check if spatial dimensions are the right size
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

    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

	# if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break

# cleanup
cv2.destroyAllWindows()
vs.stop()
