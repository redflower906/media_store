"""
All data models for Media Store
"""

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.forms import ModelForm
import decimal
import datetime

# Create your models here.

class Service(models.Model):
	service_text = models.CharField(max_length=100)


class ServiceSubType(models.Model):
	subservicetype_text = models.CharField(max_length=100)
	service = models.ForeignKey(Service,verbose_name="Service")
	qty = models.DecimalField(max_digits=10,decimal_places=2,blank=True,null=True)


class Job(models.Model):
	name = models.CharField(max_length=100)
	description = models.TextField(blank=True)
	is_active = models.BooleanField(blank=False,null=False,default=True)
	service = models.ForeignKey(Service, blank=False,null=False)
	date_created = models.DateField(auto_now_add=True)
	date_modified = models.DateTimeField(auto_now=True)
#	job_class = models.CharField(max_length=30,blank=False)




#	category = models.CharField(max_length=30,blank=True,null=True,choices = CATEGORY_CHOICES)
#note sure category choices should be the same but not sure if RM requires it to be the same?

# do we just copy this from Resource Matrix since we are trying to stay similar?