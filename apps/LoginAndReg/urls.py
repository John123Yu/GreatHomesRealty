from django.conf.urls import url, include # Notice we added include
from . import views

urlpatterns = [
	url(r'^$', views.index, name = "index"),
	url(r'^users$', views.register, name = "register"),
	url(r'^login$', views.login, name = "login"),
	url(r'^updateInfo/(?P<id>\d+)$', views.updateInfo, name = "updateInfo"),
	url(r'^updatePassword/(?P<id>\d+)$', views.updatePassword, name = "updatePassword"),
	url(r'^updateDescription$', views.updateDescription, name = "updateDescription"),
	url(r'^removeUser/(?P<id>\d+)$', views.removeUser, name = "removeUser"),
	url(r'^createUser$', views.createUser, name = "createUser")
	]
