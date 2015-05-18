from django.conf.urls import patterns, include, url
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static
from secTable.views import grabByDate

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$'           , 'signups.views.home', name='home'),
    url(r'^polls/'      , include('polls.urls', namespace="polls")),
    url(r'^thank-you/'  , 'signups.views.thankyou', name='thankyou'),
    url(r'^contact/'    , 'signups.views.contact', name='contact'),
    url(r'^admin/'      , include(admin.site.urls)),
    url(r'^retrieve?'   , grabByDate),
    
    url(r'^login/$'      , 'signups.views.login', name='login'),
    url(r'^auth/$'       , 'signups.views.auth_view', name='auth'),
    url(r'^logout/$'     , 'signups.views.logout', name='logout'),
    url(r'^loggedin/$'   , 'signups.views.loggedin', name='loggedin'),
    url(r'^invalid/$'    , 'signups.views.invalid_login', name='invalid'),
    url(r'^register/$'   , 'signups.views.invalid_login', name='register'),
    url(r'^register_success/$'    , 'signups.views.invalid_login', name='register_success'),
)

if(settings.DEBUG):
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    #urlpatterns += static(settings.MEDIA_URL,
    #                      document_root=settings.MEDIA_ROOT)