"""media URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
#admin.autodiscover()
from django.conf import settings
#from django.views.generic import TemplateViews

from store import views #can add more here with , 

#urlpatterns = [
#	url(r'^store/', include('store.urls')),
#   url(r'^admin/', include(admin.site.urls)),
#]
app_name = 'store'
urlpatterns = [

	url(r'^admin/', include(admin.site.urls)),
    url(r'^store/', views.index, name='home'),
	url(r'^login/', views.login, name='login'),
	url(r'^$', views.index, name='store'),

## from nameform

    url(r'^name/', views.get_name, name='name'),
]
#services
#	url(r'^service/$', 'media')	