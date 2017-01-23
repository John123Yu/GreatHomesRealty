from django.conf.urls import url, include 
from . import views
from views import Register, Login

urlpatterns = [
	url(r'^$', views.index, name = "index"),
	url(r'^users$', Register.as_view(), name = "register"),
	url(r'^login$', Login.as_view(), name = "login"),
	url(r'^updateInfo/(?P<id>\d+)$', views.updateInfo, name = "updateInfo"),
	url(r'^updatePassword/(?P<id>\d+)$', views.updatePassword, name = "updatePassword"),
	url(r'^updateDescription$', views.updateDescription, name = "updateDescription"),
	url(r'^removeUser/(?P<id>\d+)$', views.removeUser, name = "removeUser"),
	url(r'^createUser$', views.createUser, name = "createUser")
	]
