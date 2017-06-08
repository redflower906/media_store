from django.contrib import admin

# Register your models here.
from store.models import ServiceSubType, Job, Service


admin.site.register(Service)
admin.site.register(ServiceSubType)
admin.site.register(Job)