from django.contrib import admin

# Register your models here.
from store.models import Department, Inventory, Order, Vendor, ServiceSubType, Job, Service


admin.site.register(Department)
admin.site.register(Inventory)
admin.site.register(Order)
admin.site.register(Vendor)
admin.site.register(Service)
admin.site.register(ServiceSubType)
admin.site.register(Job)