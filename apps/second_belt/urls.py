from django.conf.urls import url
from . import views

urlpatterns = [
  url(r'^$', views.index), 
  url(r'^regi$', views.register), 
  url(r'^login$', views.login), 
  url(r'^dashboard$', views.dashboard), 
  url(r'^wish_items/create$', views.showadd), 
  url(r'^addnew$', views.create),
  url(r'^addlist/(?P<otheritem_id>[0-9]+)$', views.addlist),
  url(r'^remove/(?P<myadditem_id>[0-9]+)$', views.remove), 
  url(r'^delete/(?P<mycreateditem_id>[0-9]+)$', views.delete), 
  url(r'^wish_items/(?P<showitem_id>[0-9]+)$', views.showitem),
  url(r'^$', views.logout), 



]
