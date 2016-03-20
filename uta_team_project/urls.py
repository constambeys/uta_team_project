from django.conf.urls import patterns, include, url
from django.contrib import admin
from uta_team_project import views

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index, name='index'),
    url(r'^home', views.home, name='home'),
    url(r'^find_team/(?P<assignment_id>.*)/', views.find_team, name='find_team'),
    url(r'^select_team/(?P<team_id>.*)/', views.select_team, name='select_team'),
    url(r'^assignment_create/', views.assignment_create, name='assignment_create'),
    url(r'^assignment_view/(?P<assignment_id>.*)/', views.assignment_view, name='assignment_view'),
    url(r'^team_create/(?P<assignment_id>.*)/', views.team_create, name='team_create'),
    url(r'^notifications_view/', views.notifications_view, name='notifications_view'),
    url(r'^notification_accept/(?P<group_id>.*)/', views.notification_accept, name='notification_accept'),
    url(r'^auth/', include('uta_auth.urls')),
    url(r'^restricted/', views.restricted, name='restricted'),
    url(r'^about-us/', views.about_us, name='about-us'),
    url(r'^uta_users/', views.uta_users, name='uta_users'),
    url(r'^help/', views.help, name='help'),
)
