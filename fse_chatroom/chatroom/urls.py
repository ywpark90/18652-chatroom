from django.conf.urls import patterns, url
from chatroom import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^(?P<chatroom_id>\d+)/$', views.chatroom, name='chatroom'),
)
