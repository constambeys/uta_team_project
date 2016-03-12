from django.conf.urls import patterns, include, url
from django.contrib import admin
from uta_team_project import views

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index, name='index'),
    url(r'^student_home', views.student_home, name='student_home'),
    url(r'^instructor_home', views.student_home, name='instructor_home'),
    url(r'^assignment_create/', views.assignment_create, name='assignment_create'),
    url(r'^assignment_view/(?P<assignment_id>.*)/', views.assignment_view, name='assignment_view'),
    url(r'^auth/', include('uta_auth.urls')),
    url(r'^restricted/', views.restricted, name='restricted'),
)
