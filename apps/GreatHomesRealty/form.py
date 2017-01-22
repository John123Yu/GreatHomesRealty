from django import forms
from .models import Listing, User_Listings, Image
from ..LoginAndReg.models import User
from django.forms import ModelForm

class addListingForm(forms.ModelForm):
	class Meta:
		model = Listing
		fields = '__all__'

class S3ImageForm(forms.Form):
	file = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
