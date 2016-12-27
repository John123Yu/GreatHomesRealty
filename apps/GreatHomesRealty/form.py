from django import forms
from .models import Listing, User_Listings, Image
from ..LoginAndReg.models import User
from django.forms import ModelForm


class addListingForm(forms.ModelForm):
	class Meta:
		model = Listing
		fields = '__all__'

class ImageForm(forms.ModelForm):
	class Meta:
		model = Image
		fields = ['image']

class MainImageForm(forms.ModelForm):
	class Meta:
		model = Listing
		fields = ['mainPicture']

class UserImageForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['picture']

# class editListingForm(forms.ModelForm):
# 	class Meta:
# 		model = Listing
# 		fields = '__all__'
# 		description = forms.CharField(widget=forms.Textarea)
