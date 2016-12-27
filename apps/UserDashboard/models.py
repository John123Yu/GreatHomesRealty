from __future__ import unicode_literals
from django.db import models
from ..LoginAndReg.models import User, LoginManager, RegisterManager
# Create your models here.

class Messages(models.Model):
	subject = models.TextField(null = True)
	message = models.TextField()
	user = models.ForeignKey(User, related_name = "poster")
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

class Comments(models.Model):
	comment = models.TextField()
	message = models.ForeignKey(Messages)
	user = models.ForeignKey(User)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)