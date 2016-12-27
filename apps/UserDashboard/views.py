from django.shortcuts import render, HttpResponse, redirect
from models import Messages, Comments
from ..LoginAndReg.models import User, LoginManager, RegisterManager
from django.core.urlresolvers import reverse
from django.db.models import Count
from ..GreatHomesRealty.form import addListingForm, ImageForm, MainImageForm, UserImageForm
from django.views.generic.edit import CreateView


def index(request):
	if request.session['login'] > 0:
		context = {
		    'users' : User.registerMgr.all(),
		    'activeUser': User.registerMgr.get(id = request.session['login']),
		    'user': User.registerMgr.get(id = request.session['login'])
		}
		return render(request, 'UserDashboard/index.html', context)
	else:
		return redirect(reverse('GreatHomesRealty:index'))

def createDisplay(request):
	try:
		user = User.registerMgr.get(id = request.session['login'])
	except:
		user = "none"
	if user.user_level == "Admin":
		return render(request, 'UserDashBoard/newUser.html')
	else:
		return redirect(reverse('GreatHomes:index'))

def editProfileDisplay(request):
	if request.session['login'] > 0:
		user = User.registerMgr.get(id = request.session['login'])
		context = {
			'User': user
		}
		return render(request, 'UserDashboard/editProfile.html',  context )
	else:
		return redirect(reverse('GreatHomesRealty:index'))

def addUserImage(request, id):
	if request.session['login'] > 0 and request.method == "POST":
		user = User.registerMgr.get(id = id)
		if request.method == 'POST':
			form = UserImageForm(request.POST, request.FILES)
			if form.is_valid():
				user.picture = form.cleaned_data['picture']
				user.save()
				url = "/showAgentListing/" + str(user.id)
				return redirect(url)
	else:
		return redirect(reverse('GreatHomesRealty:index'))


	return
def adminEdit(request, id):
	try:
		user = User.registerMgr.get(id = request.session['login'])
	except:
		user = "none"
	if user.user_level == "Admin":
		admin = User.registerMgr.get(id = request.session['login'])
		user = User.registerMgr.get(id = id)
		context = {
			'User': user
		}
		return render(request, 'UserDashboard/adminEdit.html', context )
	else:
		return redirect(reverse('GreatHomes:index'))
		
def logout(request):
	request.session['login'] = 0
	request.session['reciever'] = 0
	return redirect(reverse('login:index'))

class PostMessage(CreateView):
	def get(self, request):
		try: 
			user = User.registerMgr.get(id = request.session['login'])
		except:
			user = "none"
		context = {
			'all_messages': Messages.objects.all(),
			'Admin': user
		}
		return render(request, 'GreatHomesRealty/newsfeedAjax.html', context)
	def post(self, request):
		newMessage = Messages.objects.create(message = request.POST['message'], subject = request.POST['subject'], user_id = request.session['login'] )
		return redirect(reverse('UserDashboard:postMessage'))
		
def deleteMessage(request, id):
		Messages.objects.get(id = id).delete()
		return redirect(reverse('GreatHomes:suscribeDisplay'))

