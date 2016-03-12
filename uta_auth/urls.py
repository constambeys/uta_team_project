from django.conf.urls import patterns, include, url
from django.contrib import admin
from uta_auth import views

urlpatterns = patterns('',
        url(r'^user_login/$', views.user_login, name='user_login'),
        url(r'^register/(?P<user_type>.*)/$', views.register_user, name='register_user'),
        url(r'^register/$', views.register, name='register'),
        url(r'^logout/$', views.user_logout, name='logout'),
)
