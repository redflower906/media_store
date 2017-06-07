from django.contrib import admin

# Register your models here.
from store.models import Service, ServiceSubType, Job


admin.site.register(Service)
admin.site.register(ServiceSubType)
admin.site.register(Job)