from django.conf.urls import patterns, include, url
from django.contrib import admin
from SecureWitness import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url('^$', 'SecureWitness.views.homePage'),
    url(r'^(?P<userId>[^/]+)/?$', 'SecureWitness.views.userPage'),
    url(r'^(?P<userId>[^/]+)/getFolder/(?P<folderId>[^/]+)/?$', 'SecureWitness.views.userFolder'),

    url(r'^(?P<userId>[^/]+)/createBulletin/?$', 'SecureWitness.views.createBulletin'),
    url(r'^(?P<userId>[^/]+)/renameBulletin/(?P<bulletinId>[^/]+)/?$', 'SecureWitness.views.renameBulletin'),
    url(r'^(?P<userId>[^/]+)/copyBulletin/(?P<bulletinId>[^/]+)/?$', 'SecureWitness.views.copyBulletin'),
    url(r'^(?P<userId>[^/]+)/deleteBulletin/(?P<bulletinId>[^/]+)/?$', 'SecureWitness.views.deleteBulletin'),
    url(r'^(?P<userId>[^/]+)/setBulletinFolder/(?P<bulletinId>[^/]+)/?$', 'SecureWitness.views.setBulletinFolder'),

    url(r'^(?P<userId>[^/]+)/createFolder/?$', 'SecureWitness.views.createFolder'),
    url(r'^(?P<userId>[^/]+)/renameFolder/(?P<folderId>[^/]+)/?$', 'SecureWitness.views.renameFolder'),
    url(r'^(?P<userId>[^/]+)/copyFolder/(?P<folderId>[^/]+)/?$', 'SecureWitness.views.copyFolder'),
    url(r'^(?P<userId>[^/]+)/deleteFolder/(?P<folderId>[^/]+)/?$', 'SecureWitness.views.deleteFolder')

)
