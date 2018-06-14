from django.contrib import admin

# Register your models here.
from store.models import Department, Inventory, Order, Vendor

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('department_name', 'number', 'account_code', 'is_shared_resource', 'active')
    search_fields = ['department_name', 'number']
    actions = ['make_inactive']

    def make_inactive(self, request, queryset):
        rows_updated = queryset.update(active=False)
        if rows_updated == 1:
            message_bit = '1 department was'
        else:
            message_bit = '{0} departments were'.format(rows_updated)
        self.message_user(request, '{0} successfully marked inactive'.format(message_bit))
    make_inactive.short_description = 'Mark selected departments as inactive'

    def get_queryset(self, request):
        qs = Department.all_objects
        return qs

class InventoryAdmin(admin.ModelAdmin):
    list_display = ('inventory_text', 'cost', 'notes_inv', 'active', 'media_type')
    list_filter = ('inventory_text', 'media_type')
    search_fields = ['inventory_text', 'cost']

#class OrderAdmin(admin.ModelAdmin):
#    list_display = []

class VendorAdmin(admin.ModelAdmin):
    list_display = ['email_address', 'company', 'contact', 'notes_ven', 'active']
    search_fields = ['email_address', 'company', 'contact', 'notes_ven', 'active']

class UserProfile(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'employee_id', 'department', 'is_active')
    list_filter = ('is_active', 'is_janelia')
    search_fields = ['user_username', 'first_name', 'last_name', 'department_number', 'employee_id']



admin.site.register(Department, DepartmentAdmin)
admin.site.register(Inventory, InventoryAdmin)
admin.site.register(Order)#, OrderAdmin)
admin.site.register(Vendor, VendorAdmin)
