from __future__ import unicode_literals
from django.db import models
from ..LoginAndReg.models import User, LoginManager, RegisterManager
from django.forms import ModelForm
from django.core.exceptions import ValidationError
import re
from django import forms

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
PHONE_REGEX = re.compile(r'^(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}$')

class ListingManager(models.Manager):
    def addListing(self, streetAddress, suite, city, state, zipcode, price, bedrooms, bathrooms, squarefootage, houseType, county, neighborhood, MLS, description, edit, createdBy, yearBuilt,status):
		errors = {}

		if any(x < 1 for x in (len(streetAddress), len(city), len(state), len(zipcode), len(price), len(bedrooms), len(bathrooms), len(squarefootage), len(houseType), len(county), len(neighborhood), len(MLS), len(status), len(yearBuilt), len(description) )):
			errors['allInputLengths'] = "All fields are required except Apt/Suite#."
		if len(errors) is not 0:
			return (False, errors)
		elif len(errors) == 0 and edit == "no":
			listing = Listing.listingMgr.create(addressStreet = streetAddress, addressCity = city, addressState = state, addressAptNumber = suite, addressZipcode = zipcode, price = price, bedrooms= bedrooms, bathrooms= bathrooms, squarefootage= squarefootage, houseType= houseType, county= county, neighborhood= neighborhood, MLS= MLS, description = description, createdById = createdBy, yearBuilt= yearBuilt, status = status )
			User_Listings.objects.create(user_id = createdBy, listing = listing)
			return (True, listing.id)
		elif len(errors) == 0 and edit != "no":
			OneListing = Listing.listingMgr.get(id = edit)
			listing = Listing.listingMgr.filter(id = edit).update(addressStreet = streetAddress, addressCity = city, addressState = state, addressAptNumber = suite, addressZipcode = zipcode, price = price, bedrooms= bedrooms, bathrooms= bathrooms, squarefootage= squarefootage, houseType= houseType, county= county, neighborhood= neighborhood, MLS= MLS, description = description, yearBuilt = yearBuilt, status = status )
			return (True, OneListing.id)

class ClientManager(models.Manager):
	def addClient(self, firstName, lastName, email):
		errors = {}

		try:
			client = Client.clientMgr.get(email = email)
		except:
			client = 0
		if client != 0:
			errors['EmailDuplicate'] = "Email already suscribed!"
		if any(x < 1 for x in (len(firstName), len(lastName), len(email) )):
			errors['allInputLengths'] = "All Fields are required"
		if not EMAIL_REGEX.match(email):
		    errors['InvalidEmail'] = ("Invalid Email")
		if firstName.isalpha() == False or lastName.isalpha() == False:
			errors['IsAlpha'] = ("First and last name must contain only alphabetic characters")
		if len(errors) is not 0:
			return (False, errors)
		elif len(errors) == 0:
			client = Client.clientMgr.create(firstName = firstName, lastName = lastName, email = email)
			return (True, client)

class SendMailManager(models.Manager):
	def sendMail(self, firstName, lastName, phone, email, question):
		errors = {}
		if any(x < 1 for x in (len(firstName), len(lastName), len(phone), len(email), len(question) )):
			errors['allInputLengths'] = "All fields are required"
		if not EMAIL_REGEX.match(email):
		    errors['InvalidEmail'] = ("Please enter a valid email address")
		if not PHONE_REGEX.match(phone):
			errors['InvalidPhone'] = ("Please enter a valid phone number in the format of (555)-555-5555")
		if len(errors) is not 0:
			return (False, errors)
		elif len(errors) == 0:
			return (True, 1)

class Listing(models.Model):
	addressStreet = models.CharField(max_length=255)
	addressCity = models.CharField(max_length=255, null = True)
	addressState = models.CharField(max_length=255, null = True)
	addressAptNumber = models.CharField(max_length=255, null = True)
	addressZipcode = models.IntegerField(null = True)
	price = models.DecimalField(max_digits = 12, decimal_places = 0)
	bedrooms = models.IntegerField()
	lat = models.DecimalField(max_digits = 20, decimal_places = 10, null = True)
	lon = models.DecimalField(max_digits = 20, decimal_places = 10, null = True)
	bathrooms = models.DecimalField(max_digits = 15, decimal_places = 1)
	squarefootage = models.IntegerField()
	houseType = models.CharField(max_length = 100)
	county = models.CharField(max_length = 100)
	neighborhood = models.CharField(max_length = 100)
	MLS = models.IntegerField()
	description = models.TextField(null = True)
	url = models.CharField(max_length = 128,  null = True)
	status = models.CharField(max_length = 100, null = True)
	yearBuilt = models.IntegerField(null = True)
	createdById = models.IntegerField()
	created_at = models.DateField(auto_now_add=True)
	updated_at = models.DateField(auto_now=True)
	listingMgr = ListingManager()

class User_Listings(models.Model):
	listing = models.ForeignKey(Listing)
	user = models.ForeignKey(User)
	created_at = models.DateField(auto_now_add=True, null = True)
	updated_at = models.DateField(auto_now=True, null = True)

class Image(models.Model):
	url = models.CharField(max_length = 128,  null = True)
	listing = models.ForeignKey(Listing, null = True, related_name = "images")
	created_at = models.DateField(auto_now_add=True)
	updated_at = models.DateField(auto_now=True,)

class Client(models.Model):
	firstName = models.CharField(max_length=100)
	lastName = models.CharField(max_length=100)
	email = models.CharField(max_length=100)
	clientMgr = ClientManager()
	sendMailMgr= SendMailManager()
	created_at = models.DateField(auto_now_add=True)
	updated_at = models.DateField(auto_now=True)
