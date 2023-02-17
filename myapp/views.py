from django.shortcuts import render,redirect
from . models import User
from django.conf import settings
from django.core.mail import send_mail
import random

# Create your views here.

def index(request):

	return render(request,'index.html')

def signup(request):

	if request.method=="POST":
		
		try:
			User.objects.get(email=request.POST['email'])
			msg = "Email Already Exist"
			return render(request,'signup.html',{'msg':msg})

		except:

			User.objects.create(fname= request.POST['fname'],
				lname=request.POST['lname'],
				email=request.POST['email'],
				pswd=request.POST['pswd'],
				address=request.POST['address'])

			msg1="Registration Sucessful"
			return render(request,'signup.html',{'msg1':msg1})


	else:
		return render(request,'signup.html')


def login(request):
	if request.method=="POST":
		
		try:
			var1 = ">>>>>>>>>>>>>>LOGIN DONE<<<<<<<<<<<<<<<<<"
			print(var1)
			user = User.objects.get(email=request.POST['email'])
			request.session['email'] = user.email
			request.session['fname'] = user.fname
			return render(request,'index.html')

		except:
			msg = "Email or Password Doen not Matched !!!"
			return render(request,'login.html',{'msg':msg})
	else:

		return render(request,'login.html')


def logout(request):
	try:
		var2 =">>>>>>>>>>>>>LOGED OUT<<<<<<<<<<<<<<<<<"
		print(var2)
		del request.session['email']
		del request.session['fname']
		return render(request,'login.html')

	except:
		return render(request,'login.html')


def change_pswd(request):
	if request.method=="POST":
		user=User.objects.get(email=request.session['email'])

		if user.pswd == request.POST['old_pswd']:
			if request.POST['new_pswd'] == request.POST['cnew_pswd']:
				user.pswd = request.POST['new_pswd']
				user.save()
				return redirect('logout')

			else:
				msg="New Password Confirm Password Does not match !!!"
				return render(request,'change_pswd.html',{'msg':msg})
		else:
			msg="Old Password Does not match !!!"
			return render(request,'change_pswd.html',{'msg':msg})

	else:
		return render(request,'change_pswd.html')

def forgot_pswd(request):
	if request.method=="POST":
		try:
			user= User.objects.get(email = request.POST['email'])
			otp = random.randint(1000,9999)
			subject = 'OTP For Forgot Password'
			message = 'Hello '+user.fname+" , Your OTP : "+str(otp)
			email_from = settings.EMAIL_HOST_USER
			recipient_list = [user.email, ]
			send_mail( subject, message, email_from, recipient_list )
			return render(request,'otp.html',{'email':user.email,'otp':otp})

		except:
			msg = "Email Does Not Exist !!!"
			print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>",msg)
			return render(request,'forgot_pswd.html',{'msg':msg})
	else:
		return render(request,'forgot_pswd.html')

def verify_otp(request):
	email=request.POST['email']
	otp=request.POST['otp']
	uotp=request.POST['uotp']

	if otp==uotp:
		return render(request,'new_pswd.html',{'email':email})

	else:
		msg="Invalid OTP"
		return render(request,'otp.html',{'email':email,'msg':msg,'otp':otp})

def new_pswd(request):
	email = request.POST['email']
	np = request.POST['new_pswd']
	cnp = request.POST['cnew_pswd']

	if np==cnp:
		user=User.objects.get(email=email)
		user.pswd=np
		user.save()
		msg1="Password Updated :) "
		return render(request,"login.html",{'msg1':msg1})

	else:
		msg="New Password & Confirm Password Does not match !!!"
		return render(request,"new_pswd.html",{'email':email,'msg':msg})
