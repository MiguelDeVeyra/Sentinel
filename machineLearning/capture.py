import cv2
#from hikvisionapi import Client

def ResizeWithAspectRatio(image, width=None, height=None, inter=cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))

    return cv2.resize(image, dim, interpolation=inter)

cap = cv2.VideoCapture()
cap.open("rtsp://admin:Admin123@192.168.0.17:554/Streaming/channels/101")

#response = cam.System.deviceInfo(method='get')
ret, frame = cap.read()
#frame = cv2.flip(frame, 1)
#resize = ResizeWithAspectRatio(frame, width=1200)

while(ret):
    # Capture frame-by-frame
    ret, frame = cap.read()
    frame = cv2.flip(frame, 0)
    resize = ResizeWithAspectRatio(frame, width=1200)

    # Display resulting frame
    cv2.imshow('HIKVISION', resize)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()


#cap.open('rtsp://admin:Admin123@192.168.254.2:554/Streaming/channels/1')
