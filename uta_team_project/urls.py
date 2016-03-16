from django.conf.urls import patterns, include, url
from django.contrib import admin
from uta_team_project import views

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index, name='index'),
    url(r'^home', views.home, name='home'),
    url(r'^assignment_create/', views.assignment_create, name='assignment_create'),
    url(r'^assignment_view/(?P<assignment_id>.*)/', views.assignment_view, name='assignment_view'),
    url(r'^group_create/(?P<assignment_id>.*)', views.group_create, name='group_create'),
    url(r'^requirements_create/', views.requirements_create, name='requirements_create'),
    url(r'^auth/', include('uta_auth.urls')),
    url(r'^restricted/', views.restricted, name='restricted'),
)
