from django.conf.urls import patterns, include, url
from django.contrib import admin
from uta_auth import views

urlpatterns = patterns('',
        url(r'^login/$', views.user_login, name='login'),
        url(r'^register/$', views.register, name='register'), # ADD NEW PATTERN!
        url(r'^logout/$', views.user_logout, name='logout'),
)
