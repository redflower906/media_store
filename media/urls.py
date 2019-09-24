
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

#IF MAKING A TEST PAGE MAKE SURE THE URL DOESN'T START THE SAME WAY THE REAL PAGE DOES, OR IT WILL JUST KEEP RELOADING THE REAL PAGE

from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.edit import DeleteView
from django.views.generic.list import ListView
from store.models import Order
from store import views 
admin.autodiscover()


app_name = 'store'



urlpatterns = [

# richtextfield    
    url(r'^djrichtextfield/', include('djrichtextfield.urls')),

#main views
    url(r'^$', views.home, name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^store/', views.home, name='home'),
#   url(r'^invalid', 'store_views.invalid_login'),
#   url(r'^hijack/', include('hijack.urls')), #to hijack other users


##Inventory
    url(r'^inventory/$', views.inventory, name='inventory'),
    url(r'^inventory/new', views.create_item, name='new_item'),
    url(r'^inventory/(?P<id>[0-9]*)$', views.single_item, name='single_item'),
    url(r'^inventory/(?P<id>[0-9]*)/edit$', views.update_item, name='edit_single_item'),
    url(r'^services/', views.services, name='services'),

##orders
    url(r'^order/new', views.create_order, name='create_order'),
    url(r'^order/uploadtest', views.upload_test, name='upload_test'),
    url(r'^order/edit/(?P<id>[0-9]*)$', views.edit_order, name='edit_order'),
    url(r'^order/copy/(?P<copy_id>[0-9]*)$', views.create_order, name='copy_order'),
    url(r'^order/view', views.view_order, name='view_order'),
    url(r'^order/test_view', views.testing_view_order, name='testing_view_order'),
    url(r'^order', views.view_order, name='view_order'),
    url(r'^export/csv/complete$', views.export_ordersCNB, name='export_ordersCNB'),
    url(r'^export/csv/progress$', views.export_ordersIP, name='export_ordersIP'),
    url(r'^order/delete/(?P<id>[0-9]*)$', views.delete_order, name='delete_order'),
    url(r'^order/delete/(?P<pk>\d+)/$', views.OrderDelete.as_view(), name='order_delete'),


##Search
    url(r'^search$', views.search, name='search'),
    url(r'^search/csv$', views.search, name='search_export'),
    url(r'^search2/csv$', views.searchtest, name='search2_export'),
    url(r'^search2$', views.searchtest, name='search2'),

##email
    url(r'^(?P<id>[0-9]*)/email$', views.email_form, name='email'),

##sign-out
    url(r'^signout/view', views.current_sign_outs, name='signout'),
    url(r'^signout/remainder', views.sign_outs_remainder, name='remainder'),
    url(r'^signout/new', views.create_signout, name='create_signout'),
    url(r'^signout/remtest', views.auto_bv_so, name='remtest'),    
    url(r'^signout/qtytest', views.qty_buttons_test, name='qty_test'),

#tiny mce?
    url(r'^tinymce/', include('tinymce.urls')),

#Ajax calls
    url(r'^ajax', views.ajax, name='ajax'), #json for user department and project codes

]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns=[
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#Add Django site authentication urls (for login, logout, password management)
urlpatterns += [
    url(r'^accounts/', include('django.contrib.auth.urls')),
]
