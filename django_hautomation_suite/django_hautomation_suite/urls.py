from django.conf.urls import patterns, include, url
from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
urlpatterns = patterns("",
    url(r'^admin/', include(admin.site.urls)),)

if settings.DJANGO_HAUTOMATION_DEPLOYED:
    urlpatterns = urlpatterns + patterns('',
       
        url(r'^rest/', include('harest.urls')),
    )
if settings.DJANGO_HAWEB_DEPLOYED:
    urlpatterns = urlpatterns + patterns('',        
        url(r'^ha/', include("haweb.urls")),
    )
if settings.DJANGO_THERMOMETER_DEPLOYED:
    urlpatterns = urlpatterns + patterns('',        
        url(r'^thermometer/', include("django_thermometer.urls")),
    )    
if settings.DJANGO_THERMOSTAT_DEPLOYED:
    urlpatterns = urlpatterns + patterns('',        
        url(r'^thermostat/', include('django_thermostat.urls')),
    # url(r'^dev_therm/', include('dev_therm.foo.urls')),
    )   