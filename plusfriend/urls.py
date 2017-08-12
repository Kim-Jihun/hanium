from django.conf.urls import url
from . import views
from django.conf import settings

urlpatterns = [
    url(r'^keyboard$', views.on_init),
    url(r'^friend$', views.on_added),
    url(r'^friend/(?P<user_key>[\w-]+)$', views.on_block),
    url(r'^chat_room/(?P<user_key>[\w-]+)$', views.on_leave),
    url(r'^message$', views.on_message),
  

    ]
