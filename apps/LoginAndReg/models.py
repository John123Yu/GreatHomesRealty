from __future__ import unicode_literals
from django.db import models
import re
from datetime import datetime
import bcrypt
import random

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
PASSWORD_REGEX = re.compile(r'^(?=.*[A-Z])(?=.*\d)')
PHONE_REGEX = re.compile(r'^(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}$')

class RegisterManager(models.Manager):
    def userRegister(self, firstName, lastName, email, password, confirmPassword, phone, session, changePassword, passcode):
		errors = {}

		try:
			user = User.registerMgr.get(email = email)
		except:
			user = 0
		if len(email) == 0:
		    errors['EmailRequired'] = ("Email is required")
		elif not EMAIL_REGEX.match(email):
		    errors['InvalidEmail'] = ("Invalid Email")
		if user != 0 and session == 0:
			errors['EmailDuplicate'] = "Email Already In Use!"
		if len(firstName) < 2 or len(lastName) < 2:
			errors['TwoCharacters'] = ("First name and last name must be at least two characters")
		if firstName.isalpha() == False or lastName.isalpha() == False:
			errors['IsAlpha'] = ("First and last name must contain only alphabetic characters")
		if len(password) < 1 or len(confirmPassword) < 1:
			errors['PasswordRequired'] = ("Password and confirm password is required")
		if len(password) < 8:
			errors['PasswordLength'] = ("Password needs to be at least 8 characters")
		if not PASSWORD_REGEX.match(password):
			errors['InvalidPassword'] = ("Password requires one uppercase letter and one number")
		if not PHONE_REGEX.match(phone):
			errors['InvalidPhone'] = ("Please enter a valid phone number")
		if password != confirmPassword:
			errors['PasswordNonmatch'] = ("Confirm password must match password")
		if passcode != "Ellicott042":
			errors['passcodeError'] = "Incorrect Passcode"
		if len(errors) is not 0:
			return (False, errors)
		elif len(errors) == 0 and session == 0:
			pw_bytes = password.encode('utf-8')
			hashed = bcrypt.hashpw(pw_bytes, bcrypt.gensalt())
			user = User.registerMgr.create(firstName = firstName, lastName = lastName, email=email, password = hashed, phone = phone)
			user.save()
			return (True, user)
		elif len(errors) == 0 and session > 0 and changePassword == False:
			User.registerMgr.filter(id = session).update(firstName = firstName, lastName = lastName, email = email, phone = phone, password = password)
			return (True, 1)
		elif len(errors) == 0 and  session > 0 and changePassword == True: 
			pw_bytes = password.encode('utf-8')
			hashed = bcrypt.hashpw(pw_bytes, bcrypt.gensalt())
			User.registerMgr.filter(id = session).update(password = hashed)
			return (True, 1)


class LoginManager(models.Manager):
	def login(self, email, password):
		errors = {}
		try:
			user = User.loginMgr.get(email = email)
		except:
			user = 0
		if user != 0:
			hashed = user.password.encode('utf-8')
			pw_bytes = password.encode('utf-8')
			if bcrypt.hashpw(pw_bytes, hashed) == hashed:
				a = 1
			else:
				errors["IncorrectLogin"] = "Incorrect Password"
		else:
			errors["NoEmail"] = "Entered Email Not in Database"
		print errors
		if len(errors) is not 0:
			return (False, errors)
		else:
			return (True, user)

class PasscodeManager(models.Manager):
	def resetPassword(self, passcode, password, confirmPassword):
		newPasscode = str(random.randint(1,10)) + str(random.randint(1,10)) + str(random.randint(1,10)) + str(random.randint(1,10))  + str(random.randint(1,10)) + str(random.randint(1,10)) 
		errors = {}
		if password != confirmPassword:
			errors['PasswordNonmatch'] = ("Confirm password must match password")
		if len(password) < 8:
			errors['PasswordLength'] = ("Password needs to be at least 8 characters")
		if not PASSWORD_REGEX.match(password):
			errors['InvalidPassword'] = ("Password requires one uppercase letter and one number")
		try:
			user = User.passcodeMgr.get(passcode = passcode)
		except:
			user = 0
		if user == 0:
			errors["IncorrectPasscode"] = "Incorrect Passcode"
		if user != 0 and len(errors) is 0:
			pw_bytes = password.encode('utf-8')
			hashed = bcrypt.hashpw(pw_bytes, bcrypt.gensalt())
			User.registerMgr.filter(passcode = passcode).update(password = hashed)
		if len(errors) is not 0:
			return (False, errors)
		else:
			return (True, user)

class User(models.Model):
	firstName = models.CharField(max_length=100)
	lastName = models.CharField(max_length=100)
	email = models.CharField(max_length=100)
	phone = models.CharField(null = True, max_length = 100)
	picture =  models.ImageField(null = True, upload_to = 'uploads/')
	url = models.CharField(max_length = 128,  null = True)
	user_level = models.CharField(max_length = 100, null = True)
	password = models.CharField(max_length=250)
	profileInformation = models.TextField(null = True)
	created_at = models.DateField(auto_now_add=True)
	updated_at = models.DateField(auto_now=True)
	registerMgr = RegisterManager()
	passcodeMgr = PasscodeManager()
	loginMgr = LoginManager()
	passcode = models.CharField(max_length= 50, null = True)
