from django.conf.urls import url, include
from . import views
from django.views.generic import ListView, DetailView


urlpatterns = [
    url(r'^$', views.index),
    url(r'^signin/$', views.signIn),
    url(r'^signup/$', views.signUp),
    url(r'^logout/$', views.log_out),
    url(r'^product/$', views.product),
    url(r'^additem/$', views.additem),
    url(r'^edititems/$', views.edititems),
    url(r'^network/$', views.network),
    url(r'^explore/$', views.explore),
    url(r'^explore_step1/$', views.explore_step1),
    url(r'^explore_step2/$', views.explore_step1),
    url(r'^search/$', views.search),
    url(r'^selectitem/$', views.tradescreen),
    url(r'^seenetwork/$', views.seenetwork),
] 
    #url(r'^contact/$', views.contact, name='contact') ]