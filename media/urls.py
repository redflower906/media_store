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

from store import views #as store_views  #can add more here with , 

#urlpatterns = [
#   url(r'^store/', include('store.urls')),
#   url(r'^admin/', include(admin.site.urls)),
#]
app_name = 'store'
urlpatterns = [


	url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index, name='home'),
	url(r'^login/', views.login, name='login'),
    url(r'^inventory/', views.inventory, name='inventory'),

#	url(r'^logout', 'store_views.logout'),
#	url(r'^invalid', 'store_views.invalid_login'),
#	url(r'^hijack/', include('hijack.urls')), #to hijack other users

## from nameform


    url(r'^name/', views.get_name, name='name'),
]



#Inventory
#    url(r'^inventory/$', 'store_views.inventory', name = 'Inventory'),
#    url(r'^inventory/new', 'store_views.create_inventory', name = 'create_inventory'),
#    url(r'^inventory/(?P<id>[0-9]*)$', 'store_views.single_item', name = 'single_item'),
#    url(r'^inventory/(?P<id>[0-9]*)$', 'store_views.edit_single_item', name = 'edit_single_item'),

#add link to dump to Resource Matrix here


#Admin Interface
#	url(r'^admin_dashboard/$*', 'store_views.admin_dashboard', name = 'admin_dashboard'),
#	url(r'^order_delete', 'store_views.delete_order', name = 'delete_order')"""

#services
#	url(r'^service/$', 'media')