from block import block
from flask import render_template
from flask import request
from twilio.rest import Client
import random


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
	