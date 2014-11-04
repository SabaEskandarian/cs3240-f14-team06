from django.conf.urls import patterns, include, url
from django.contrib import admin
from SecureWitness import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^admin/', include(admin.site.urls)),
    url('^$', 'SecureWitness.views.homePage'),
    url(r'^(?P<userId>[^/]+)/?$', 'SecureWitness.views.userPage'),
    url(r'^(?P<userId>[^/]+)/getBulletins/?$', 'SecureWitness.views.getBulletins'),
    #url(r'^(<userId>[^/]+)/bulletins/(<bulletinId>[^/]+)?$', views.getBulletin),
    url(r'^(?P<userId>[^/]+)/createBulletin/?$', 'SecureWitness.views.createBulletin'),
    url(r'^(?P<userId>[^/]+)/renameBulletin/(?P<bulletinId>[^/]+)/?$', 'SecureWitness.views.renameBulletin'),
    url(r'^(?P<userId>[^/]+)/copyBulletin/(?P<bulletinId>[^/]+)/?$', 'SecureWitness.views.copyBulletin'),
    url(r'^(?P<userId>[^/]+)/deleteBulletin/(?P<bulletinId>[^/]+)/?$', 'SecureWitness.views.deleteBulletin'),
    #url(r'^steve/bulletins/', views.createBulletin)
)
