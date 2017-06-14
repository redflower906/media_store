from django.contrib import admin

# Register your models here.
from store.models import Department, Inventory, Order, Vendor


admin.site.register(Department)
admin.site.register(Inventory)
admin.site.register(Order)
admin.site.register(Vendor)
