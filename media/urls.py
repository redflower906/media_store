
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
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))"""

from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from store import views #as store_views  #can add more here with, 
from store.views import update_item 

app_name = 'store'

urlpatterns = [

#main views

    url(r'^$', views.home, name='home'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^store/', views.home, name='home'),
    url(r'^login/', views.login, name='login'),
#   url(r'^logout', 'store_views.logout'),
#   url(r'^invalid', 'store_views.invalid_login'),
#   url(r'^hijack/', include('hijack.urls')), #to hijack other users


#user views
##services
    url(r'^inventory/$', views.inventory, name='inventory'),
#    $ allows you to build on the URL while using different views
    url(r'^inventory/new', views.create_item, name='new_item'),
    url(r'^inventory/(?P<id>[0-9]*)$', views.single_item, name='single_item'),
    url(r'^inventory/(?P<id>[0-9]*)/edit$', views.update_item, name='edit_single_item'),
    #url(r'^inventory/new', FormCreate.as_view(), name='new_item'),
    #url(r'^inventory/(?P<id>[0-9]*)/edit$', update_item.as_view(), name='edit_single_item'),


    url(r'^services/', views.services, name='services'),

##orders
    url(r'^order/$', views.order, name='order'),
    url(r'^order/new', views.create_order, name='create_order'),
    url(r'^order/(?P<id>[0-9]*)$', views.past_order, name='past_order'),
    url(r'^order/(?P<id>[0-9]*)$', views.edit_past_order, name='edit_past_order'),
    url(r'^order/(?P<id>[0-9]*)$', views.recurring_order, name='recurring_order'),

#add link to dump to Resource Matrix here


#Admin Interface
#	url(r'^admin_dashboard/$*', 'store_views.admin_dashboard', name = 'admin_dashboard'),
#	url(r'^order_delete', 'store_views.delete_order', name = 'delete_order')"""

#services
#	url(r'^service/$', 'media')


]