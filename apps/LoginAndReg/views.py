from django.shortcuts import render, HttpResponse, redirect
from models import User
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.views.generic.edit import View
from django.http import JsonResponse
from django.core.mail import send_mail
import random
import json 
error_messages = {}
# Create your views here.
def index(request):
    return render (request, 'LoginAndReg/index.html')

class Register(View):
	def get(self, request):
		if request.method == "GET":
			context = error_messages
			return render(request, 'LoginAndReg/registerAjax.html', context)
		else: 
			return redirect ('/')
	def post(self, request):
		if request.method == "POST":
			global error_messages
			error_messages = {}
			result = User.registerMgr.userRegister(request.POST['first_name'], request.POST['last_name'], request.POST['email'], request.POST['password'], request.POST['confirm_password'], request.POST['phone'], 0, False, request.POST['passcode'])
			if result[0]:
				user = result[1]
				request.session['login'] = result[1].id
				if result[1].email == "billyu99@gmail.com" or result[1].email == "john123yu@gmail.com":
					user.user_level = "Admin"
					user.save()
				else:
					user.user_level = "Normal"
					user.save()
				return JsonResponse({"data": "true"})
			else:
				error_messages = result[1]
				error_messages['FN'] = request.POST['first_name']
				error_messages['LN'] = request.POST['last_name']
				error_messages['E'] = request.POST['email']
				error_messages['P'] = request.POST['phone']
				return redirect(reverse('login:register'))
		else:
			pass

class Login(View):
	def get(self, request):
		if request.method == "GET":
			context = error_messages
			return render(request, 'LoginAndReg/loginAjax.html', context)
		else: 
			return redirect ('/')

	def post(self, request):
		if request.method == "POST":
			global error_messages
			error_messages = {}
			result = User.loginMgr.login(request.POST['email'], request.POST['password'])
			if result[0]:
				user = User.loginMgr.get(email = request.POST['email'])
				request.session['login'] = user.id
				return JsonResponse({"data": "true"})
			else:
				error_messages = result[1]
				error_messages['E'] = request.POST['email']
				return redirect(reverse('login:login'))
		else:
			return redirect ('/')

def resetPasswordDisplay(request):
	return render(request, 'LoginAndReg/resetPassword.html')

class ResetPassword(View):
	def get(self, request):
		if request.method == "GET":
			context = error_messages
			return render(request, 'LoginAndReg/resetPasswordAjax.html', context)
		else: 
			return redirect ('/')

	def post(self, request):
		if request.method == "POST":
			global error_messages
			error_messages = {}
			user = User.loginMgr.filter(email = request.POST['email'])
			if user:
				passcode = str(random.randint(1,10)) + str(random.randint(1,10)) + str(random.randint(1,10)) + str(random.randint(1,10))  + str(random.randint(1,10)) + str(random.randint(1,10))
				user[0].passcode = passcode
				print passcode
				user[0].save()
				fromEmail = "BillYu99@gmail.com"
				subject = "Great Homes Realty Password Reset"
				message =  "Someone requested a password reset for this email. Your passcode is " + str(passcode)
				emails = []
				emails.append(request.POST['email'])
				send_mail(
					subject,
					message,
					fromEmail,
					emails,
					fail_silently=False
				)
				print passcode
				error_messages['Success'] = "Check your email for a passcode and then fill out the form on the right. "
			else:
				error_messages['NoEmail'] = "Entered email not in database"
			return redirect(reverse('login:resetPassword'))

class ChangePassword(View):
	def get(self, request):
		if request.method == "GET":
			context = error_messages
			return render(request, 'LoginAndReg/changePasswordAjax.html', context)
		else: 
			return redirect ('/')

	def post(self, request):
		if request.method == "POST":
			global error_messages
			error_messages = {}
			result = User.passcodeMgr.resetPassword(request.POST['passcode'], request.POST['password'], request.POST['confirmPassword'])
			if result[0]:
				# user = User.loginMgr.get(passcode = request.POST['passcode'])
				request.session['login'] = result[1].id
				return JsonResponse({"data": "true"})
			else:
				error_messages = result[1]
				error_messages['Success'] = ""
				return redirect(reverse('login:changePassword'))

def updateInfo(request, id):
	if request.method == "POST" and request.session['login'] > 0:
		error_messages = {}
		if(id > str(0)):
			user = User.registerMgr.get(id = id)
		else:
			user = User.registerMgr.get(id = request.session['login'])
		if id == str(0):
			result = User.registerMgr.userRegister(request.POST['first_name'], request.POST['last_name'], request.POST['email'], user.password, user.password, request.POST['phone'], request.session['login'], False, "Ellicott042")
		else:
			result = User.registerMgr.userRegister(request.POST['first_name'], request.POST['last_name'], request.POST['email'], user.password, user.password, request.POST['phone'], id, False, "Ellicott042")
		if result[0]:
			url = "/showAgentListing/" + str(user.id)
			return redirect(url)
		elif result[0] == False and id == str(0):
			error_messages = result[1]
			context = {
				'User': user,
				'error_messages': error_messages
			}
			print context['error_messages']
			return render(request, 'UserDashboard/editProfile.html',  context )
		elif result[0] == False and id > 0:
			error_messages = result[1]
			user = User.registerMgr.get(id = id)
			context = {
				'User': user,
				'error_messages': error_messages
			}
			print context['error_messages']
		return render(request, 'UserDashboard/adminEdit.html', context)
	else: 
		return redirect(reverse('login:index'))

def updatePassword(request, id):
	if request.method == "POST":
		error_messages = {}
		user = User.registerMgr.get(id = request.session['login'])
		if id == str(0):
			result = User.registerMgr.userRegister(user.firstName, user.lastName, user.email, request.POST['password'], request.POST['confirm_password'], user.phone, request.session['login'], True, "Ellicott042")
		else:
			result = User.registerMgr.userRegister(user.firstName, user.lastName, user.email, request.POST['password'], request.POST['confirm_password'], user.phone, id, True, "Ellicott042")
		if result[0]:
			url = "/showAgentListing/" + str(user.id)
			return redirect(url)
		elif result[0] == False and id == str(0):
			error_messages = result[1]
			return render(request, 'UserDashboard/editProfile.html',  error_messages )
		elif result[0] == False and id > 0:
			error_messages = result[1]
			user = User.registerMgr.get(id = id)
			context = {
				'User': user,
				'error_messages': error_messages
			}
			print context['error_messages']
		return render(request, 'UserDashboard/adminEdit.html', context)
			# url = "/UserDashboard/users/edit/" + str(id)
			# return redirect(url)
	else: 
		return redirect(reverse('login:index'))

def updateDescription(request):
	if request.method == "POST":
		user = User.registerMgr.get(id = request.session['login'])
		user.profileInformation = request.POST['description']
		user.save()
		url = "/showAgentListing/" + str(user.id)
		return redirect(url)
	else: 
		return redirect(reverse('login:index'))

def removeUser(request, id):
	try:
		user = User.registerMgr.get(id = request.session['login'])
	except:
		user = 0
	if user.user_level == "Admin":
		User.registerMgr.get(id = id).delete()
		return redirect(reverse('UserDashboard:index'))
	else:
		return redirect(reverse('login:index'))

def createUser(request):
	error_messages = {}
	try:
		user = User.registerMgr.get(id = request.session['login'])
	except:
		user = 0
	if request.method == "POST" and user.user_level == "Admin":
		result = User.registerMgr.userRegister(request.POST['first_name'], request.POST['last_name'], request.POST['email'], request.POST['password'], request.POST['confirm_password'], request.POST['phone'], 0, False)
		if result[0]:
			user = result[1]
			user.user_level = "Normal"
			user.save()
			return redirect(reverse('UserDashboard:index'))
		else:
			error_messages = result[1]
			return render(request, 'UserDashboard/newUser.html',  error_messages )
	else:
		return redirect(reverse('login:index'))
