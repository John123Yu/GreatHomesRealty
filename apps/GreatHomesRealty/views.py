from django.shortcuts import render, HttpResponse, redirect
from ..LoginAndReg.models import User, LoginManager, RegisterManager
from ..UserDashboard.models import Messages
from .form import addListingForm, UserImageForm, MainImageForm, ImageForm
from models import Listing, User_Listings, Image, ListingManager, Client
from django.core.urlresolvers import reverse
try:
    from django.db.models.fields.related_descriptors import ReverseManyToOneDescriptor as ReverseDescriptor
except ImportError:
    from django.db.models.fields.related import ReverseManyRelatedObjectsDescriptor as ReverseDescriptor
from django.core.mail import send_mail, send_mass_mail
from django.conf import settings
import json 
from django.views.generic.edit import View
from django.views.generic import FormView
# from .forms import S3DirectUploadForm


def index(request):
	request.session['clientLogin'] = "false"
	allListings = Listing.listingMgr.all()[0:3]
	try:
		user = User.registerMgr.get(id = request.session['login'])
	except:
		user = 0
	context = {
		'allListings': allListings,
		'user':user,
	}
	return render(request, 'GreatHomesRealty/index.html', context)

def addListingDisplay(request):
	if request.session['login'] > 0:
		addListing = addListingForm()
		context = {
			'addListing': addListing,
		}
		return render(request, 'GreatHomesRealty/addListing.html', context)
	else:
		return redirect(reverse('GreatHomes:index'))

def addListing(request):
	if request.method == "POST":
		error_messages = {}
		result = Listing.listingMgr.addListing(request.POST['streetAddress'], request.POST['suite'], request.POST['city'], request.POST['state'], request.POST['zipcode'], request.POST['price'], request.POST['bedrooms'], request.POST['bathrooms'], request.POST['squarefootage'], request.POST['housetype'], request.POST['county'], request.POST['neighborhood'], request.POST['mls'], request.POST['description'], "no", request.session['login'], request.POST['yearBuilt'], request.POST['status'])
		if result[0]:
			listing = result[1]
			url = "/showListing/" + str(listing.id)
			return redirect(url)
		else:
			error_messages = result[1]
			return render(request, 'GreatHomesRealty/addListing.html',  error_messages )
	else: 
		return redirect(reverse('GreatHomes:addListingDisplay'))

def editListingDisplay(request, id):
	# editForm = editListingForm()
	if request.session['login'] > 0:
		listing = Listing.listingMgr.get(id = id)
		context = {
			'listing': listing
			# 'editForm': editForm
		}
		return render(request, 'GreatHomesRealty/editListing.html', context)
	else:
		return redirect(reverse('GreatHomes:index'))

def editListing(request, id):
	marker = False 
	admin = User.registerMgr.get(id = request.session['login'])
	user_listings = User_Listings.objects.filter(listing_id = id)
	currentUser = User.registerMgr.get(id = request.session['login'])
	for item in user_listings:
		if currentUser == item.user:
			marker = True
	if request.method == "POST" and (admin.user_level == "Admin" or marker == True):
		listingone = Listing.listingMgr.get(id = id)
		result = Listing.listingMgr.addListing(request.POST['streetAddress'], request.POST['suite'], request.POST['city'], request.POST['state'], request.POST['zipcode'], request.POST['price'], request.POST['bedrooms'], request.POST['bathrooms'], request.POST['squarefootage'], request.POST['housetype'], request.POST['county'], request.POST['neighborhood'], request.POST['mls'], request.POST['description'], listingone.id, listingone.createdById, request.POST['yearBuilt'], request.POST['status'])
		if result[0]:
			url = "/showListing/" + str(listingone.id)
			return redirect(url)
		else:
			context = result[1]
			context['listing'] = listingone
			print context
			return render(request, 'GreatHomesRealty/editListing.html',  context)
	else:
		return redirect(reverse('GreatHomes:index'))

def addMainImage(request, id):
	if request.method == "POST":
		listing = Listing.listingMgr.get(id = id)
		if request.method == 'POST':
			form = MainImageForm(request.POST, request.FILES)
			if form.is_valid():
				image = form.cleaned_data['mainPicture']
				listing.mainPicture = image
				listing.save()
				url = "/showListing/" + str(listing.id)
				return redirect(url)
		else:
			pass
		url = "/showListing/" + str(listing.id)
		return redirect(url)
	else: 
		url = "/showListing/" + str(id)
		return redirect(url)

def addListingImage(request, id):
	if request.method == "POST":
		listing = Listing.listingMgr.get(id = id)
		if request.method == 'POST':
			form = ImageForm(request.POST, request.FILES)
			if form.is_valid():
				image = form.cleaned_data['image']
				addImage = Image.objects.create(image = image, listing_id = listing.id)
				url = "/showListing/" + str(listing.id)
				return redirect(url)
		else:
			pass
		url = "/showListing/" + str(listing.id)
		return redirect(url)
	else: 
		url = "/showListing/" + str(id)
		return redirect(url)

def showListing(request, id):
	listing = Listing.listingMgr.get(id = id)
	addImage = ImageForm()
	try:
		currentUser = User.registerMgr.get(id = request.session['login'])
	except:
		currentUser = 0
	mainImage = MainImageForm()
	listingAddress = listing.addressStreet + " " +listing.addressCity + " " + listing.addressState
	context = {
		'listing': listing,
		'addImage': addImage,
		'mainImage': mainImage,
		'images': Image.objects.filter(listing_id = listing.id),
		'agents': User.registerMgr.all(),
		'primaryAgents': User_Listings.objects.filter(listing_id = id),
		'listingAddress':listingAddress,
		'currentUser': currentUser,
		'counter': 0
	}
	return render(request, 'GreatHomesRealty/showListing.html',  context )

def addAgent(request, id):
	if request.method == "POST":
		agent = User(id = request.POST['agent'])
		listing = Listing.listingMgr.get(id = id)
		notnew = User_Listings.objects.filter(user_id = agent.id, listing_id = listing.id)
		if notnew:
			pass
		else:
			User_Listings.objects.create(user_id = agent.id, listing_id = listing.id)
		url = "/showListing/" + str(listing.id)
		return redirect(url)
	else: 
		url = "/showListing/" + str(id)
		return redirect(url)

def showAllListing(request):
	allListings = Listing.listingMgr.all()
	context = {
		'allListings': allListings
	}
	return render(request, 'GreatHomesRealty/viewAllListing.html',  context )

def showAgentListing(request, id):
	user = User.registerMgr.get(id = id)
	listing = User_Listings.objects.filter(user = user)
	context = {
		'listings': listing,
		'user':user,
		'UserImage': UserImageForm()
	}
	return render(request, 'GreatHomesRealty/agentListings.html',  context )

def deleteListing(request, id):
	if request.method == "POST":
		listing = Listing.listingMgr.get(id = id).delete()
		return redirect(reverse('GreatHomes:showAllListing'))
	else:
		return redirect(reverse('GreatHomes:showAllListing'))

def deleteImage(request, id):
	listing = Listing.listingMgr.get(images__id = image.id)
	if request.method == "POST":
		image = Image.objects.get(id = id)
		image.delete()
		url = "/showListing/" + str(listing.id)
		return redirect(url)
	else:
		url = "/showListing/" + str(listing.id)
		return redirect(url)

def deleteMainImage(request, id):
	if request.method == "POST":
		listing = Listing.listingMgr.get(id = id)
		listing.mainPicture.delete()
		url = "/showListing/" + str(listing.id)
		return redirect(url)
	else: 
		url = "/showListing/" + str(id)
		return redirect(url)

def deleteListingAgent(request, id):
	if request.method == "POST":
		agent = User(id = request.POST['agent'])
		listing = Listing.listingMgr.get(id = id)
		User_Listings.objects.filter(user_id = agent.id, listing_id = listing.id).delete()
		url = "/showListing/" + str(listing.id)
		return redirect(url)
	else:
		url = "/showListing/" + str(id)
		return redirect(url)

sendMailMessages = {}
class SendMail(View):
	def get(self, request, id):
		if request.method == "GET":
			context = sendMailMessages
			return render(request, 'GreatHomesRealty/sendMailAjax.html', context)
		else:
			url = "/showListing/" + str(id)
			return redirect(url)

	def post(self, request, id):
		if request.method == "POST":
			emails = []
			global sendMailMessages
			sendMailMessages = {}
			if id == "0":
				pass
			else:
				listing = Listing.listingMgr.get(id = id)
				manyToMany = User_Listings.objects.filter(listing_id = id)
				for item in manyToMany:
					emails.append(item.user.email)
			emails.append("billyu99@gmail.com")
			emails.append("John123Yu@gmail.com")
			results = Client.sendMailMgr.sendMail(request.POST['first_name'], request.POST['last_name'],request.POST['phone'], request.POST['email'], request.POST['message'])
			if results[0]:
				sendMailMessages['success'] = "Your email has been sent"
				fromEmail = request.POST['email']
				subject = request.POST['first_name'] + " " + request.POST['last_name'] + " " + "Prospective Client"
				if id == "0":
					message =  request.POST['phone'] + " " + fromEmail + " "  + request.POST['message']
				else:
					message =  request.POST['phone'] + " " + fromEmail + " " + listing.addressStreet + " " + str(listing.MLS) + " " + request.POST['message']
				send_mail(
					subject,
					message,
					fromEmail,
					emails,
					fail_silently=False
				)
				url = "/sendMail/" + str(id)
				return redirect(url)
			else:
				sendMailMessages = results[1]
				url = "/sendMail/" + str(id)
				return redirect(url)
		else:
			url = "/showListing/" + str(id)
			return redirect(url)

def suscribeDisplay(request):
	try: 
		user = User.registerMgr.get(id = request.session['login'])
	except:
		user = "none"
	try:
		request.session['clientLogin']
	except:
		request.session['clientLogin'] = "false"
	if request.session['clientLogin'] == "true":
		context = {
		'all_messages': Messages.objects.all(),
		'Admin': user
		}
	elif user != "none":
		context = {
		'all_messages': Messages.objects.all(),
		'Admin': user
		}
	else: 
		context = {
		'all_messages': Messages.objects.all().order_by('created_at')[:2],
		'Admin': user
		}
	return render(request, 'GreatHomesRealty/suscribeDisplay.html',  context )

clientLoginMessage = {}
class ClientLogin(View):
	def get(self, request):
		if request.method == "GET":
			global clientLoginMessage
			print clientLoginMessage
			try: 
				user = User.registerMgr.get(id = request.session['login'])
			except:
				user = "none"
			if request.session['clientLogin'] == "true":
				clientLoginMessage['all_messages'] = Messages.objects.all()
				clientLoginMessage['Admin'] = user
			else:
				clientLoginMessage['all_messages'] = Messages.objects.all().order_by('created_at')[:2]
				clientLoginMessage['Admin'] = user
			return render(request, 'GreatHomesRealty/clientLoginAjax.html', clientLoginMessage)
		else:
			return redirect(reverse('GreatHomes:suscribeDisplay'))

	def post(self, request):
		if request.method == "POST":
			global clientLoginMessage
			clientLoginMessage = {}
			try:
				client = Client.clientMgr.get(email = request.POST['emailLogin'])
			except:
				client = 0
			if client == 0:
				clientLoginMessage['noEmail'] = "Entered email is not yet suscribed"
				return redirect(reverse('GreatHomes:clientLogin'))
			else:
				print "HEREEEEEE"
				clientLoginMessage['success'] = "You've successfully logged in"
				request.session['clientLogin'] = "true"
				return redirect(reverse('GreatHomes:clientLogin'))
		else:
			return redirect(reverse('GreatHomes:suscribeDisplay'))


suscribe_error_messages = {}
class Suscribe(View):
	def get(self, request):
		if request.method == "GET":
			context = suscribe_error_messages
			return render(request, 'GreatHomesRealty/suscribeAjax.html', context)
		else:
			return redirect(reverse('GreatHomes:suscribeDisplay'))

	def post(self, request):
		if request.method == "POST":
			global suscribe_error_messages
			suscribe_error_messages = {}
			results = Client.clientMgr.addClient(request.POST['first_name'], request.POST['last_name'],request.POST['email'])
			if results[0]:
				suscribe_error_messages['success'] = "You are suscribed"
				return redirect(reverse('GreatHomes:suscribe'))
			else:
				suscribe_error_messages = results[1]
				return redirect(reverse('GreatHomes:suscribe'))
		else:
			return redirect(reverse('GreatHomes:suscribeDisplay'))

unsuscribe_error_messages = {}
class Unsuscribe(View):
	def get(self, request):
		if request.method == "GET":
			context = unsuscribe_error_messages
			return render(request, 'GreatHomesRealty/unsuscribe.html', context)
		else:
			return redirect(reverse('GreatHomes:suscribeDisplay'))

	def post(self, request):
		if request.method == "POST":
			global unsuscribe_error_messages
			unsuscribe_error_messages = {}
			try:
				client = Client.clientMgr.get(email = request.POST['email']).delete()
			except:
				unsuscribe_error_messages['NoEmail'] = "Please enter a suscribed email"
			if 'NoEmail' in unsuscribe_error_messages:
				return redirect(reverse('GreatHomes:unsuscribe'))
			else:
				unsuscribe_error_messages['success'] = "You've successfully unsuscribed"
				return redirect(reverse('GreatHomes:unsuscribe'))
		else: 
			return redirect(reverse('GreatHomes:suscribeDisplay'))


def suscriptionEmail(request):
	if request.method == "POST":
		subject = request.POST['subject']
		message = request.POST['message'] 
		# + "\nunsuscribe: www.unsuscribe.com"

		clients = Client.objects.all()
		sentemails = []
		for client in clients:
			sentemails.append(client.email)
		message1 = (subject, message, 'John123Yu@gmail.com', sentemails)
		send_mass_mail(
			(message1,),
			fail_silently=False
		)
		return redirect(reverse('GreatHomes:suscribeDisplay'))
	else:
		return redirect(reverse('GreatHomes:suscribeDisplay'))

def displaySubscribers(request):
	if request.method == "POST":
		clients = Client.clientMgr.all()
		context = {
			'clients': clients
		}
		return render(request, 'GreatHomesRealty/displaySuscribers.html',  context )
	else:
		return redirect(reverse('GreatHomes:suscribeDisplay'))

def contact(request):
	return render(request, 'GreatHomesRealty/contact.html' )

def buying(request):
	return render(request, 'GreatHomesRealty/buy.html')

def selling(request):
	return render(request, 'GreatHomesRealty/sell.html')

def mortgage(request):
	return render(request, 'GreatHomesRealty/mortgage.html')

def investing(request):
	return render(request, 'GreatHomesRealty/investing.html')

def owningHome(request):
	return render(request, 'GreatHomesRealty/owningHome.html')

