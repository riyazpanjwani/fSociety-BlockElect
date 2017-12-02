from block import block
from flask import render_template
from flask import request, redirect,send_file, url_for, Response
from twilio.rest import Client
import random
import os
import qrtools
from qrtools import QR
import qrcode
from io import BytesIO
import cv2
from mimetypes import types_map

ACCOUNT_SID = 'AC59850459deb51d114f6504d11ec65059'
AUTH_TOKEN = '0afddb8124ffc433382f0f7219e91335'
UPLOAD_FOLDER = '/home/tushalien/Desktop/hack/fSociety-BlockElect/block/qrcodes'
block.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

name = None
village = None
contact_number = None
aadhar_card_number = None
bhamashah = None
otp = None

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

	

	client = Client(ACCOUNT_SID, AUTH_TOKEN)


	otp = random.randint(10**5,10**6-1)
	#otps = 1234
	print otp
	# client.messages.create("+91"+contact_number,
 #                from_="+17192498194",
 #              body="Hello "+ name + ", Your OTP for Block Elect verification is: "+ str(otp))
	return render_template('verification.html')

@block.route('/qr_code',methods = ['POST'])
def qr_code_generator():
	global otp
	rec_otp = request.form['otp']
	if( int(rec_otp) == otp):
		return redirect(url_for('qr_code_print', id="blah blah"))
	else:
		check = 1
		return render_template('verification.html',check = check)


@block.route('/qr_print',methods = ['GET'])
def qr_code_print():
	global name
	global village
	global contact_number
	global aadhar_card_number
	global bhamashah
	data =name+"&"+village+"&"+contact_number+"&"+aadhar_card_number+"&"+bhamashah
	#print data
	#qrdata = QR(data=data, pixel_size=10)
	#qrdata.encode()
	#print qrdata
	#return qrdata
	qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
	)
	qr.add_data(data)
	qr.make(fit=True)

	img = qr.make_image()
	mimetype = types_map['.' + "png"]
	io = BytesIO()
	img.save(io, "PNG")
	io.seek(0)
	return send_file(io, mimetype=mimetype, conditional=True)

@block.route('/login')
def login():
	return render_template('login.html')


@block.route('/authenticate', methods=['POST'])
def authenticate():
	file= request.files['file']
	print file
	file.save(os.path.join(block.config['UPLOAD_FOLDER'], 'tmp.png'))
	qr = qrtools.QR()
	#print img
	#print filejpeg
	qr.decode(os.path.join(block.config['UPLOAD_FOLDER'], 'tmp.png'))
	# d=qrcode.Decoder()
	# if d.decode(qr):
	qrcode_detail = qr.data
	print qrcode_detail

	global name
	global village
	global contact_number
	global aadhar_card_number
	global bhamashah
	global otp
	qrcode_detail= qrcode_detail.split("&")
	name=qrcode_detail[0]
	vilage=qrcode_detail[1]
	contact_number=qrcode_detail[2]
	aadhar_card_number=qrcode_detail[3]
	#name=qrcode_detail[0]

	client = Client(ACCOUNT_SID, AUTH_TOKEN)


	otp = random.randint(10**5,10**6-1)
	#otps = 1234
	print otp
	# client.messages.create("+91"+contact_number,
 #                from_="+17192498194",
 #              body="Hello "+ name + ", Your OTP for Block Elect verification is: "+ str(otp))
	

	return render_template('authenticate.html')

@block.route('/resend_otp',methods=['GET'])
def resend_otp():
	global name
	global contact_number
	global otp	

	client = Client(ACCOUNT_SID, AUTH_TOKEN)

	resend = 1
	otp = random.randint(10**5,10**6-1)
	#otps = 1234
#	client.messages.create("+91"+contact_number,
#                from_="+17192498194",
#              body="Hello "+ name + ", Your OTP for Block Elect verification is: "+ str(otp))
	return render_template('verification.html',resent = resend)


def gen_frames():
    faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    print faceCascade
    video_capture_instance = cv2.VideoCapture(0)
    global num_faces
    while(True):
        bool_ret, frame = video_capture_instance.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5,
                minSize=(15, 15), flags=cv2.cv.CV_HAAR_SCALE_IMAGE)
        print(len(faces))
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        frame = cv2.imencode('.jpg', frame)[1].tobytes()
        if(len(faces) > 1):
            num_faces = 2
            print(num_faces)
            yield(b'--frame\r\n'+
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


            break
        

        else:
            num_faces = 1
            yield(b'--frame\r\n'+
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    print "DSgf"
    #return redirect(url_for('index'))
    video_capture_instance.release()
    cv2.destroyAllWindows()
    yield ''


@block.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@block.route('/candidate_list')
def candidate_list():
    candidate_list = ['Utkarsh', 'Riyaz', 'Tushalien']
    return render_template('voting_list.html', candidate_list=enumerate(candidate_list))



@block.route('/final_vote', methods=['POST'])
def final_vote():
	return render_template('final_vote.html')

