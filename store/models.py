"""
All data models for Media Store
"""

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.forms import ModelForm
import decimal
import datetime

CATEGORY_CHOICES = (
	('labor', 'labor'),
	('equipment', 'equipment'),
	('materials', 'materials'),
	('service', 'service'),
	('sample', 'sample'),
)

# Create your models here.

class Service(models.Model):
	service_text = models.CharField(max_length=100)


class ServiceSubType(models.Model):
	servicesubtype_text = models.CharField(max_length=100)
	service = models.ForeignKey(Service,verbose_name="Service")
	cost = models.DecimalField(max_digits=10,decimal_places=2,blank=True,null=True)
	unit = models.CharField(max_length=30,blank=True,null=True)
	jm_category = models.CharField(max_length=50, blank=True, null=True, choices=CATEGORY_CHOICES)
	category = models.CharField(max_length=50, blank=True,null=True, 
		choices=(
		('Agar', 'Agar'),
		('Antibiotics', 'Antibiotics'),
		('Dextrose Food', 'Dextrose Food'),
		('Liquid Media', 'Liquid Media'),
		('Miscellaneous', 'Micellaneous'),
		('Power Food', 'Power Food'),
		('Solutions & Buffers', 'Solutions & Buffers'),
		('Standard Food', 'Standard Food'),
		('Sylgard', 'Sylgard'),
		('Wurzburg Food', 'Wurzburg Food')),
		default='Miscellaneous'
	)
	
	qty = models.DecimalField(max_digits=10,decimal_places=2,blank=True,null=True)
	date_created = models.DateField(auto_now_add=True)
	notes = models.TextField(blank=True)

	def category_choices(self):
		return CATEGORY_CHOICES


class Job(models.Model):
	name = models.CharField(max_length=100)
	description = models.TextField(blank=True)
	is_active = models.BooleanField(blank=False,null=False,default=True)
	service = models.ForeignKey(Service, blank=False,null=False)
	date_created = models.DateField(auto_now_add=True)
	date_modified = models.DateTimeField(auto_now=True)
#	job_class = models.CharField(max_length=30,blank=False)

#WTF----------------------------------------------------------------------------------------
class Department(models.Model):
	name = models.CharField(max_length=100)
	number = models.CharField(unique=True, max_length=6)
	account_code = models.IntegerField(null=True, blank=True)
	is_shared_resource = models.BooleanField(default=False)
	active = models.BooleanField(default=True)

#	objects = ActiveDepartmentManager()
#	all_objects = models.Manager()

	def __unicode__(self):
		return self.number + " " + self.name

	class Meta:
		ordering = ('number',)


"""class UserProfile(models.Model):
#	user = models.ForeignKey(User, related_name='user_profile')
#	department = models.ForeignKey(Department, blank=True, null=True)
#	alt_departments = models.ManyToManyField(Department, related_name='alt_departments', blank=True, null=True)
	hhmi_project_id = models.CharField(max_length=30, blank=True, null=True)
	employee_id = models.CharField(max_length=20, blank=True, null=True)
	email_address = models.CharField(max_length=255, blank=True, null=True)
	first_name = models.CharField(max_length=30, blank=True, null=True)
	last_name = models.CharField(max_length=30, blank=True, null=True)
#	manager = models.ForeignKey(User, related_name='user_manager', blank=True, null=True, on_delete=models.SET_NULL)
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
	email_address = models.CharField(max_length=225)


class Inventory(models.Model):
	class Meta:
		verbose_name_plural = 'Inventory'

	inventory_text = models.CharField(max_length=75)
	cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
	date_created = models.DateField(auto_now_add=True)
#NEW	date_modified = models.DateTimeField(auto_now=True)
	notes = models.CharField(max_length=500, blank=True)
	vendor = models.ForeignKey(Vendor, blank=False, null=False)
#	deposit = models.


class Order(models.Model):
	inventory = models.ForeignKey(Inventory, blank=False, null=False)
#	submitter = models.ForeignKey(User, related_name='submitter')
#	department = models.ForeignKey(Department, blank=False, null=False)
	special_instructions = models.TextField(blank=True)
	date_created = models.DateField(auto_now_add=True)
	date_modified = models.DateField(blank=True, null=True)
	date_submitted = models.DateField(blank=True, null=True)
	date_complete = models.DateField(blank=True, null=True)


		




			

