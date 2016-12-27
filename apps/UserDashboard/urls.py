from django.conf.urls import url, include # Notice we added include
from . import views
from views import PostMessage

urlpatterns = [
	url(r'^$', views.index, name = "index"),
	url(r'^users/new$', views.createDisplay, name = "createDisplay"),
	url(r'^users/edit$', views.editProfileDisplay, name = "editProfileDisplay"),
	url(r'^logout$', views.logout, name = "logout"),
	url(r'^users/edit/(?P<id>\d+)$', views.adminEdit, name = "adminEdit"),
	url(r'^postMessage$', PostMessage.as_view(), name = "postMessage"),
	url(r'^deleteMessage/(?P<id>\d+)$', views.deleteMessage, name = "deleteMessage"),
	url(r'^addUserImage/(?P<id>\d+)$', views.addUserImage, name = "addUserImage")
]