from django.conf.urls import patterns, include, url
from django.contrib import admin
from uta_team_project import views

urlpatterns = patterns('',
                       # Examples:
    # url(r'^$', 'uta_team_project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index, name='index'),
    url(r'^home$', views.home, name='home'),
    url(r'^auth/', include('uta_auth.urls')),  # ADD THIS NEW TUPLE!
)
