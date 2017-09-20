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
    url(r'^addkeywords/$',views.addkeywords),
    url(r'^edititems/$', views.edititems),
    url(r'^askforitems/$', views.askforitems),
    url(r'^explore/$', views.explore),
    url(r'^explore_first/$', views.explore_first),
    url(r'^explore_next/$', views.explore_repeat),
    url(r'^search/$', views.search),
    url(r'^mark_as_wanted/$', views.mark_as_wanted),
    url(r'^selectitem/$', views.tradescreen),
    url(r'^seenetwork/$', views.seenetwork),
    url(r'^sendmessage/$',views.sendmessage),
] 
