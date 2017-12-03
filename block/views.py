from block import block
from flask import render_template
from flask import request, redirect,send_file, url_for, Response, jsonify
from twilio.rest import Client
import random
import os
import qrtools
from qrtools import QR
import qrcode
from io import BytesIO
import cv2
from mimetypes import types_map
import json
import urllib2
from cryptography.fernet import Fernet
import multiprocessing
name = None
village = None
contact_number = None
aadhar_card_number = None
bhamashah = None
mid = None
familyId = None
ACCOUNT_SID = 'AC59850459deb51d114f6504d11ec65059'
AUTH_TOKEN = '0afddb8124ffc433382f0f7219e91335'
UPLOAD_FOLDER = '/home/tushalien/Desktop/hack/fSociety-BlockElect/block/qrcodes'
# UPLOAD_FOLDER = 'C:/Users/Aryan/Desktop'
block.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
num_faces = multiprocessing.Manager().Value(int, 1)

class Person:
	global name
	global village
	global contact_number
	global aadhar_card_number
	global bhamashah
	global mid
	global familyId

	def __init__(self):
		self.name = name
		self.village = village
		self.contact_number = contact_number
		self.aadhar_card_number = aadhar_card_number
		self.bhamashah = bhamashah
		self.mid = mid
		self.familyId = familyId

person = Person()
otp = None
cipher_key = Fernet.generate_key()
cipher = Fernet(cipher_key)


url = "https://apitest.sewadwaar.rajasthan.gov.in/app/live/Service/hofAndMember/ForApp"
post_url = "?client_id=ad7288a4-7764-436d-a727-783a977f1fe1"


@block.route('/')
@block.route('/index')
def index():
	return render_template('index.html')

@block.route('/profile',methods=['POST'])
def profile():
	global name
	global village
	global contact_number
	global aadhar_card_number
	global bhamashah
	global mid
	global familyId
	global person

	fid = request.form['fid']
	tar_url = url+"/"+fid+post_url
	data = json.load(urllib2.urlopen(tar_url))

	#print data


	hof = request.form['hof']
	mid = request.form['mid']

	if(hof):
		person.name = data.get("hof_Details").get("NAME_ENG")
		person.village = data.get("hof_Details").get("VILLAGE_NAME")
		person.bhamashah = data.get("hof_Details").get("BHAMASHAH_ID")
		person.contact_number = data.get("hof_Details").get("MOBILE_NO")
		person.aadhar_card_number = data.get("hof_Details").get("AADHAR_ID")
	else:
		members = data.get("family_Details")
		for member in members:
			if(member.get("M_ID") == mid):
				person.name = data.get("NAME_ENG")
				person.village = data.get("VILLAGE_NAME")
				person.bhamashah = data.get("BHAMASHAH_ID")
				person.contact_number = data.get("MOBILE_NO")
				person.aadhar_card_number = data.get("AADHAR_ID")
	print person.name
	return render_template('profile.html',person = person)

@block.route('/verify',methods=['POST'])
def verify():
	global name
	global village
	global contact_number
	global aadhar_card_number
	global bhamashah
	global otp
	global person

	name = person.name
	village = person.village
	contact_number = person.contact_number
	aadhar_card_number = person.aadhar_card_number
	bhamashah = person.bhamashah

	

	client = Client(ACCOUNT_SID, AUTH_TOKEN)


	otp = random.randint(10**5,10**6-1)
	#otps = 1234
	print otp
	client.messages.create("+91"+contact_number,
                from_="+17192498194",
              body="Hello "+ name + ", Your OTP for Block Elect verification is: "+ str(otp))
	return render_template('verification.html')

@block.route('/qr_code',methods = ['POST'])
def qr_code_generator():
	global otp
	rec_otp = request.form['otp']
	if( int(rec_otp) == otp):
		return redirect(url_for('qr_code_print', id="qr_download"))
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
	print data
	#encrypted_data = cipher.encrypt(data)
	encrypted_data=data
	qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
	)
	qr.add_data(encrypted_data)
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
	
	global name
	global village
	global contact_number
	global aadhar_card_number
	global bhamashah
	global otp
	global cipher

	file= request.files['file']
	print file
	file.save(os.path.join(block.config['UPLOAD_FOLDER'], 'tmp.png'))
	qr = qrtools.QR()
	#print img
	#	print filejpeg
	qr.decode(os.path.join(block.config['UPLOAD_FOLDER'], 'tmp.png'))
	#d=qrcode.Decoder()
	#if d.decode(qr):
	qrcode_detail = qr.data
	print qrcode_detail

	#decrypted_text = cipher.decrypt(qrcode_detail)

	qrcode_detail= qrcode_detail.split("&")
	name=qrcode_detail[0]
	vilage=qrcode_detail[1]
	contact_number=qrcode_detail[2]
	aadhar_card_number=qrcode_detail[3]

	client = Client(ACCOUNT_SID, AUTH_TOKEN)


	otp = random.randint(10**5,10**6-1)
	otps = 1234
	print otp
	client.messages.create("+91"+contact_number,
                from_="+17192498194",
              body="Hello "+ name + ", Your OTP for Block Elect verification is: "+ str(otp))
	

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
	client.messages.create("+91"+contact_number,
               from_="+17192498194",
             body="Hello "+ name + ", Your OTP for Block Elect verification is: "+ str(otp))
	return render_template('verification.html',resent = resend)

@block.route('/_getnumfaces',methods=['POST'])
def getnumfaces():
	global num_faces

	return jsonify(num_faces.get())


video_capture_instance = None
def gen_frames():
    faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    print faceCascade
    global video_capture_instance
    video_capture_instance = cv2.VideoCapture(0)
    global num_faces
    count = 0
    while(True and count < 100):
        bool_ret, frame = video_capture_instance.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5,
                minSize=(15, 15), flags=cv2.cv.CV_HAAR_SCALE_IMAGE)
        print(len(faces))
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        frame = cv2.imencode('.jpg', frame)[1].tobytes()
        count += 1
        if(len(faces) > 1):
            num_faces.set(2)
            print(num_faces)
            yield(b'--frame\r\n'+
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            break
        else:
            num_faces.set(1)
            yield(b'--frame\r\n'+
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    #return redirect(url_for('index'))
    video_capture_instance.release()
    yield ''


@block.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@block.route('/candidate_list')
def candidate_list():
    candidate_list = ['Utkarsh', 'Riyaz', 'Tushalien']
    return render_template('final1.html', candidate_list='Riyaz')


@block.route('/display_val', methods=['POST', 'GET'])
def display_val():
	global num_faces
	if num_faces > 1:
		global video_capture_instance
		video_capture_instance.release()
		cv2.destroyAllWindows()
		return render_template('login.html')
	else:
		global video_capture_instance
		video_capture_instance.release()
		cv2.destroyAllWindows()
		return render_template('final.html')


@block.route('/final_vote', methods=['POST'])
def final_vote():
	return redirect(url_for('candidate_list'))

@block.route('/final1')
def final1():
	return render_template('final1.html')

@block.route('/final2')
def final2():
	return render_template('final2.html')