import cv2

class CaptureVideo(object):
    def __init__(self):
        pass

    def live_stream_counter(self, share_inst):
        faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

        video_capture_instance = cv2.VideoCapture(0)

        while(True):
            bool_ret, frame = video_capture_instance.read()

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            faces = faceCascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5,
                    minSize=(30, 30), flags=cv2.cv.CV_HAAR_SCALE_IMAGE)

            if(len(faces) > 1):
                share_inst.set(2)
                break
            else:
                share_inst.set(1)
        cap.release()
        cv2.destroyAllWindows()
