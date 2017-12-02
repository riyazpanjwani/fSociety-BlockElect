from block import block
from flask import render_template
from flask import request, Response
from twilio.rest import Client
import cv2
import random


name = None
village = None
contact_number = None
aadhar_card_number = None
bhamashah = None
otp = None
num_faces = 0

@block.route('/')
@block.route('/index')
def index():
	return render_template('index.html')

@block.route('/verify',methods=['POST'])
def verify():
	global name
	global village
	global contact_number
	global aadhar_card_number
	global bhamashah
	global otp
	name = request.form['name']
	village = request.form['village']
	contact_number = request.form['contact_number']
	aadhar_card_number = request.form['aadhar_card']
	bhamashah = request.form['bhamashah']
	ACCOUNT_SID = 'AC59850459deb51d114f6504d11ec65059'
	AUTH_TOKEN = '0afddb8124ffc433382f0f7219e91335'
	

	client = Client(ACCOUNT_SID, AUTH_TOKEN)


	otp = random.randint(10**5,10**6-1)
	#otps = 1234
	client.messages.create("+91"+contact_number,
                from_="+17192498194",
              body="Hello "+ name + ", Your OTP for Block Elect verification is: "+ str(otp))
	return render_template('verification.html')

@block.route('/qr_code',methods = ['POST'])
def qr_code_generator():
	global otp
	rec_otp = request.form['otp']
	if( int(rec_otp) == otp):
		return render_template('qr_code.html')
	else:
		check = 1
		return render_template('verification.html',check = check)

def gen_frames():
    faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    video_capture_instance = cv2.VideoCapture(0)
    global num_faces
    while(True):
        bool_ret, frame = video_capture_instance.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5,
                minSize=(30, 30), flags=cv2.cv.CV_HAAR_SCALE_IMAGE)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        frame = cv2.imencode('.jpg', frame)[1].tobytes()
        if(len(faces) > 1):
            num_faces = 2

            yield(b'--frame\r\n'+
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            break
        else:
            num_faces = 1
            yield(b'--frame\r\n'+
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    cap.release()
    cv2.destroyAllWindows()

@block.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@block.route('/candidate_list')
def candidate_list():
    candidate_list = ['Utkarsh', 'Riyaz', 'Tushalien']
    return render_template('voting_list.html', candidate_list=enumerate(candidate_list))
