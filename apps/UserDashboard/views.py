from django.shortcuts import render, HttpResponse, redirect
from models import Messages, Comments
from ..LoginAndReg.models import User, LoginManager, RegisterManager
from django.core.urlresolvers import reverse
from django.db.models import Count
from ..GreatHomesRealty.form import addListingForm, S3ImageForm
from django.views.generic.edit import CreateView
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from django.conf import settings
import mimetypes
import random

def index(request):
	if request.session['login'] > 0:
		context = {
		    'users' : User.registerMgr.all(),
		    'activeUser': User.registerMgr.get(id = request.session['login']),
		    'user': User.registerMgr.get(id = request.session['login'])
		}
		return render(request, 'UserDashboard/index.html', context)
	else:
		return redirect(reverse('GreatHomes:index'))

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
	def store_in_s3(filename, content): 
		conn = S3Connection(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
		b = conn.get_bucket('greathomesrealty')
		mime = mimetypes.guess_type(filename)[0]
		k = Key(b)
		k.key = filename
		k.set_metadata("Content-Type", mime)
		k.set_contents_from_string(content)
		# k.set_acl('public read')
	if request.session['login'] > 0 and request.method == "POST":
		user = User.registerMgr.get(id = id)
		if request.method == 'POST':
			form = S3ImageForm(request.POST, request.FILES)
			if form.is_valid():
				# user.picture = form.cleaned_data['picture']
				# user.save()
				file = request.FILES['file']
				filename = file.name
				specialNumber = random.randint(1,10000)
				specialName = str(specialNumber) + file.name
				content = file.read()
				store_in_s3(specialName, content)
				user.url = ('http://s3.amazonaws.com/greathomesrealty/' + specialName)
				user.save()
				url = "/showAgentListing/" + str(user.id)
				return redirect(url)
			else: 
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

