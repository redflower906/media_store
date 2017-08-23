from datetime import datetime
#from dateutil.relativedata import relativedata
import time
import logging

from django import forms
from django.forms.extras.widgets import SelectDateWidget
from django.forms.widgets import TextInput, HiddenInput
from .models import Inventory, Vendor, Announcements, Order #, Department, UserProfile
from django.forms.models import inlineformset_factory,formset_factory,modelformset_factory
from djangoformsetjs.utils import formset_media_js
from django.forms.models import BaseInlineFormSet,BaseModelFormSet,BaseFormSet,BaseForm
from django.db import connections
from django.db.utils import ProgrammingError, OperationalError
from django.db.models import Q
from django.forms import ModelChoiceField, ChoiceField, widgets, ModelForm
from django.utils import timezone

logger = logging.getLogger('default')


class NumInput(TextInput):
    input_type = 'number'

class Item_Model_Form(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ('inventory_text','product','media_type','cost','container','volume','active','notes')
        labels = {
            'inventory_text': 'Descriptive name'
        }
        widgets = {
            'inventory_text': forms.TextInput(attrs={'class': 'form-text'}),
            'product': forms.TextInput(attrs={'class': 'form-text'}),
            'media_type': forms.Select(attrs={'class': 'form-text'}),
            'cost': forms.TextInput(attrs={'class': 'form-text'}),
            'container': forms.TextInput(attrs={'class': 'form-text'}),
            'volume': forms.TextInput(attrs={'class': 'form-text'}),
            'active': forms.Select(attrs={'class': 'form-text'}),
            'notes': forms.Textarea(attrs={'cols': 50, 'rows': 10, 'class': 'line-notes'}),            
            #'vendor': forms.TextInput(attrs={'class': 'line-container'})
        }
def item_model_formset_factory(extra):
    return modelformset_factory(Inventory,
    fields = ('inventory_text','product','media_type','cost','container','volume','active','notes'),
    labels = {
            'inventory_text': 'Descriptive name'
        },
    widgets = {
        'inventory_text': forms.TextInput(attrs={'class': 'form-text'}),
        'product': forms.TextInput(attrs={'class': 'form-text'}),
        'media_type': forms.Select(attrs={'class': 'form-text'}),
        'cost': forms.TextInput(attrs={'class': 'form-text'}),
        'container': forms.TextInput(attrs={'class': 'form-text'}),
        'volume': forms.TextInput(attrs={'class': 'form-text'}),
        'active': forms.Select(attrs={'class': 'form-text'}),
        'notes': forms.Textarea(attrs={'cols': 50, 'rows': 10, 'class': 'line-notes'}),
        #'vendor': forms.TextInput(attrs={'class': 'line-container'})
    },
    extra=extra, can_delete=False,
    )

'''
    def __init__(self, *args, **kwargs):()
        super(ServiceModelForm, self).__init__(*args, **kwargs)
        if 'department' in self.initial and self.initial['department']:
            if 'privileged' in self.initial and self.initial['privileged']:
                self.fields['department'].queryset = Department.objects.filter(Q(id=self.initial['department']) | Q(id__in=self.initial['alt_depts']))
            else:
                self.fields['department'].queryset = Department.objects.filter(id=self.initial['department'])
'''

'''class OrderLineForm(ModelForm):
    class Meta:
        model = OrderLine
        fields = ('inventory_text', 'container', 'notes', 'qty', 'unit', 'cost', 'inventory')'''

class DateInput(TextInput):
    input_type='date'

class OrderForm(forms.ModelForm): #create orders here
    #submitter = user_choice(queryset=User.objects.only('first_name','last_name'))
    #main_requester = user_choice(queryset=requester_queryset_generator())
    #department = forms.ModelChoiceField(queryset=Department.objects.all(), widget=forms.Select(attrs={'sytle': 'width:250'}))

    inventory = forms.ModelChoiceField(queryset=Inventory.objects.filter(active=True), required=False)
    date_complete = forms.DateField(widget=DateInput)

    class Meta:
        model = Order
        fields = '__all__'
        labels = {
            'inventory':'Item',
            'submitter':'Submitted by',
            'department':'Department',
            'special_instructions':'Instructions',
            'is_recurring':'Is this a recurring order?',
            'date_recurring_stop':'Last date for recurring order'
        }
        widgets = {
            'inventory': forms.Select(attrs={'class': 'form-text'}),
            'submitter': forms.TextInput(attrs={'class': 'form-text'}),
            'department': forms.Select(attrs={'class': 'form-text'}),
            'special_instructions': forms.TextInput(attrs={'class': 'form-text'}),
            'is_recurring': forms.Select(attrs={'class': 'form-text'}),
            'date_recurring_stop': forms.TextInput(attrs={'class': 'form-text'})
        }

'''    status = models.ForeignKey(OrderStatus, null=True)
    #had to make null to migrate CHANGE LATER
    inventory = models.ForeignKey(Inventory, blank=True, null=True)
#   submitter = models.ForeignKey(User, related_name='submitter')
    department = models.ForeignKey(Department, blank=True, null=True)
    special_instructions = models.TextField(blank=True)
    date_created = models.DateField(auto_now_add=True)
    date_modified = models.DateField(blank=True, null=True)
    date_submitted = models.DateField(blank=True, null=True)
    date_complete = models.DateField(blank=True, null=True)
    date_billed = models.DateField(blank=True, null=True)
#    objects = OrderManager()
    is_recurring = models.BooleanField(default=False)
    #had to set a default to migrate
    #make below an if statement if boolean is true and if boolean is false
    date_recurring_start = models.DateField(default=datetime.now, blank=True)
    date_recurring_stop = models.DateField(blank=True, null=True)'''

class AnnouncementsForm(forms.ModelForm):
    class Meta:
        model = Announcements
        fields = ('text', 'show')
        labels = {
            'text': '',
            'show': 'Display'
        }
        widgets = {
            'text': forms.Textarea (attrs={'rows': 5, 'class':'form-control'}),
            'show': forms.CheckboxInput(attrs={'class': 'checkbox-inline'})
        }

