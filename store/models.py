"""
All data models for Media Store
"""

from django.db import models
#from django.contrib.admin.models import LogEntry
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.forms import ModelForm
import decimal
import datetime



# Create your models here.

# MEDIA_CHOICES = (
#     #('','---------'),
#     ('Agar','Agar'),
#     ('Antibiotics','Antibiotics'),
#     ('Cornmeal Food','Cornmeal Food'),
#     ('Dextrose Food','Dextrose Food'),
#     ('Liquid Media','Liquid Media'),
#     ('Miscellaneous','Miscellaneous'),
#     ('Power Food','Power Food'),
#     ('Solutions & Buffers','Solutions & Buffers'),
#     ('Sylgard','Sylgard'),
#     ('Wurzburg Food','Wurzburg Food')

# )

class Department(models.Model):
    name = models.CharField(max_length=100)
    number = models.CharField(unique=True, max_length=6)
    account_code = models.IntegerField(null=True, blank=True)
    is_shared_resource = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

#   objects = ActiveDepartmentManager()
#   all_objects = models.Manager()

    def __unicode__(self):
        return self.number + " " + self.name
#	category = models.CharField(max_length=30,blank=True,null=True,choices = CATEGORY_CHOICES)
#note sure category choices should be the same but not sure if RM requires it to be the same?


    class Meta:
        ordering = ('number',)

"""class UserProfile(models.Model):
#   user = models.ForeignKey(User, related_name='user_profile')
#   department = models.ForeignKey(Department, blank=True, null=True)
#   alt_departments = models.ManyToManyField(Department, related_name='alt_departments', blank=True, null=True)
    hhmi_project_id = models.CharField(max_length=30, blank=True, null=True)
    employee_id = models.CharField(max_length=20, blank=True, null=True)
    email_address = models.CharField(max_length=255, blank=True, null=True)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
#   manager = models.ForeignKey(User, related_name='user_manager', blank=True, null=True, on_delete=models.SET_NULL)
    is_manager = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_janelia = models.BooleanField(default=False)
    is_visitor = models.BooleanField(default=False)

    skip_updates = models.BooleanField(default=False)


    is_privileged = models.BooleanField(default=False)


    offboard_date = models.DateField(blank=True, null=True)

    def __unicode__(self):
        return str(self.user)

    def department_id_list(self):
        deparment_ids = [dept.id for dept in self.alt_departments.all()]
        deparment_ids.append(self.department_id)
        return deparment_ids

    def name(self):
        return self.last_name + ", " + self.first_name

    def manager_name(self):
        if self.manager:
            return ' '.join([self.manager.first_name, self.manager.last_name])
        return ''

    def has_job_privileges(self):
        return (self.user.is_superuser or
            (self.is_manager and self.department.number == '093098'))"""



class Vendor(models.Model):
    email_address = models.CharField(max_length=225, blank=True, null=True)
    company = models.CharField(max_length=50, blank=True, null=True)
    contact = models.CharField(max_length=100, blank=True, null=True)
    notes = models.CharField(max_length=500, blank=True, null=True)
    active = models.BooleanField(default=True)



class Inventory(models.Model):
    MEDIA_CHOICES = (
        #('','---------'),
        ('Agar','Agar'),
        ('Antibiotics','Antibiotics'),
        ('Cornmeal Food','Cornmeal Food'),
        ('Dextrose Food','Dextrose Food'),
        ('Liquid Media','Liquid Media'),
        ('Miscellaneous','Miscellaneous'),
        ('Power Food','Power Food'),
        ('Solutions & Buffers','Solutions & Buffers'),
        ('Sylgard','Sylgard'),
        ('Wurzburg Food','Wurzburg Food')

    )
    class Meta:
        verbose_name_plural = 'Inventory'

    inventory_text = models.CharField(max_length=75)
    product = models.CharField(max_length=40, blank=True, null=True)
    media_type = models.CharField(max_length=30, blank=True, null=True, choices=MEDIA_CHOICES)
    cost = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    container = models.CharField(max_length=50, blank=True, null=True)
    volume = models.CharField(max_length=15, blank=True, null=True)
    date_created = models.DateField(auto_now_add=True)
    notes = models.CharField(max_length=500, blank=True, null=True)
    vendor = models.ForeignKey(Vendor, blank=True, null=True)
    date_modified = models.DateTimeField(auto_now_add=True)
    deposit = models.IntegerField(default=0, blank=True,null=True)
    minimum_amt = models.IntegerField(blank=True, null=True)
    part_num = models.CharField(max_length=20, blank=True, null=True)
    withdrawal = models.IntegerField(default=0, blank=True, null=True)
#    current_amt = deposit - withdrawal
    active = models.BooleanField(default=True)


    def __str__(self):
        return self.inventory_text


class Order(models.Model):
    inventory = models.ForeignKey(Inventory, blank=True, null=True)
#   submitter = models.ForeignKey(User, related_name='submitter')
    department = models.ForeignKey(Department, blank=True, null=True)
    special_instructions = models.TextField(blank=True)
    date_created = models.DateField(auto_now_add=True)
    date_modified = models.DateField(blank=True, null=True)
    date_submitted = models.DateField(blank=True, null=True)
    date_complete = models.DateField(blank=True, null=True)


class Item_Model_Form_two(ModelForm):
    class Meta:
        model = Inventory
        fields = ['product','media_type','cost','container', 'volume', 'notes','active']
        #product = forms.CharField(required=True, max_length=200)

