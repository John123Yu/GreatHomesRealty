from django.shortcuts import render, HttpResponse, redirect
from models import User
from django.contrib import messages
from django.core.urlresolvers import reverse

# Create your views here.
def index(request):
    return render (request, 'LoginAndReg/index.html')

def register(request):
	error_messages = {}
	if request.method == "POST":
		result = User.registerMgr.userRegister(request.POST['first_name'], request.POST['last_name'], request.POST['email'], request.POST['password'], request.POST['confirm_password'], request.POST['phone'], 0, False)
		if request.POST['passcode'] != "Ellicott042":
			error_messages = {}
			error_messages['passcodeError'] = "Incorrect Passcode"
			return render(request, 'LoginAndReg/index.html',  error_messages )
		if result[0]:
			user = result[1]
			request.session['login'] = result[1].id
			if result[1].id == 1:
				user.user_level = "Admin"
				user.save()
			else:
				user.user_level = "Normal"
				user.save()
			return redirect(reverse('UserDashboard:index'))
		else:
			error_messages = result[1]
			return render(request, 'LoginAndReg/index.html',  error_messages )
	else:
		pass

def login(request):
	error_messages = {}
	if request.method == "POST":
		result = User.loginMgr.login(request.POST['email'], request.POST['password'])
		if result[0]:
			user = User.loginMgr.get(email = request.POST['email'])
			request.session['login'] = user.id
			# messages.info(request, 'Three Credits remain')
			# messages.error(request, "Entered BLA BLA BLA")
			print request.session['login']
			return redirect(reverse('UserDashboard:index'))
		else:
			error_messages = result[1]
			return render(request, 'LoginAndReg/index.html',  error_messages )
	else:
		return redirect ('/')

def updateInfo(request, id):
	if request.method == "POST" and request.session['login'] > 0:
		error_messages = {}
		if(id > str(0)):
			user = User.registerMgr.get(id = id)
		else:
			user = User.registerMgr.get(id = request.session['login'])
		if id == str(0):
			result = User.registerMgr.userRegister(request.POST['first_name'], request.POST['last_name'], request.POST['email'], user.password, user.password, request.POST['phone'], request.session['login'], False)
		else:
			result = User.registerMgr.userRegister(request.POST['first_name'], request.POST['last_name'], request.POST['email'], user.password, user.password, request.POST['phone'], id, False)
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
			result = User.registerMgr.userRegister(user.firstName, user.lastName, user.email, request.POST['password'], request.POST['confirm_password'], user.phone, request.session['login'], True)
		else:
			result = User.registerMgr.userRegister(user.firstName, user.lastName, user.email, request.POST['password'], request.POST['confirm_password'], user.phone, id, True)
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
