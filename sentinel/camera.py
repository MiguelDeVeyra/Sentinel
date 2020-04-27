import threading
import cv2

class video_camera(object):
    def __init__(self):
        self.video = cv2.VideoCapture()
        self.video.open("rtsp://admin:Admin123@192.168.1.2:554/Streaming/channels/101")
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        image = self.frame
        image = cv2.flip(image, 0)
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()

def generate(cam):
    while True:
        frame = cam.get_frame()
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
