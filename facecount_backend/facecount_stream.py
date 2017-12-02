import cv2

class CaptureVideo(object):
    def __init__(self):
        self.face_count = 0

    def live_stream_counter(self):
        faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

        video_capture_instance = cv2.VideoCapture(0)

        while(True):
            bool_ret, frame = video_capture_instance.read()

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            faces = faceCascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5,
                    minSize=(30, 30), flags=cv2.CV_HAAR_SCALE_IMAGE)

            self.face_count = len(faces)
            print(len(faces))
            cv2.imshow('Video', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
