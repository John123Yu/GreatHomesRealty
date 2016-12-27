from django.conf.urls import url, include
from django.conf.urls.static import static 
from django.conf import settings
from . import views
from views import Suscribe, Unsuscribe, SendMail

urlpatterns = [
	url(r'^$', views.index, name = "index"),
	url(r'^addListingDisplay$', views.addListingDisplay, name = "addListingDisplay"),
	url(r'^addListing$', views.addListing, name = "addListing"),
	url(r'^addListingImage/(?P<id>\d+)$', views.addListingImage, name = "addListingImage"),
	url(r'^addMainImage/(?P<id>\d+)$', views.addMainImage, name = "addMainImage"),
	url(r'^editListingDisplay/(?P<id>\d+)$', views.editListingDisplay, name = "editListingDisplay"),
	url(r'^editListing/(?P<id>\d+)$', views.editListing, name = "editListing"),
	url(r'^showListing/(?P<id>\d+)$', views.showListing, name = "showListing"),
	url(r'^showAllListing$', views.showAllListing, name = "showAllListing"),
	url(r'^showAgentListing/(?P<id>\d+)$', views.showAgentListing, name = "showAgentListing"),
	url(r'^addAgent/(?P<id>\d+)$', views.addAgent, name = "addAgent"),
	url(r'^deleteListing/(?P<id>\d+)$', views.deleteListing, name = "deleteListing"),
	url(r'^deleteImage/(?P<id>\d+)$', views.deleteImage, name = "deleteImage"),
	url(r'^deleteListingAgent/(?P<id>\d+)$', views.deleteListingAgent, name = "deleteListingAgent"),
	url(r'^sendMail/(?P<id>\d+)$', SendMail.as_view(), name = "sendMail"),
	url(r'^deleteMainImage/(?P<id>\d+)$', views.deleteMainImage, name = "deleteMainImage"),
	url(r'^suscribeDisplay$', views.suscribeDisplay, name = "suscribeDisplay"),
	url(r'^suscribe$', Suscribe.as_view(), name = "suscribe"),
	url(r'^unsuscribe$', Unsuscribe.as_view(), name = "unsuscribe"),
	url(r'^suscriptionEmail$', views.suscriptionEmail, name = "suscriptionEmail"),
	url(r'^displaySubscribers$', views.displaySubscribers, name = "displaySubscribers"),
	url(r'^contact$', views.contact, name = "contact")

	# url(r'^showWall/(?P<id>\d+)$', views.showWall, name = "showWall"),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)