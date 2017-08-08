from datetime import datetime
import time
import logging

from django import forms
from django.forms.extras.widgets import SelectDateWidget
from django.forms.widgets import TextInput, HiddenInput
<<<<<<< HEAD
from .models import Inventory, Vendor, Order
=======
from .models import Inventory, Vendor, Announcements
>>>>>>> f31b3581c60c47620f351e328b4540bb1c6194b8
from django.forms.models import inlineformset_factory,formset_factory,modelformset_factory
from djangoformsetjs.utils import formset_media_js
from django.forms.models import BaseInlineFormSet,BaseModelFormSet,BaseFormSet,BaseForm
from django.db import connections
from django.db.utils import ProgrammingError, OperationalError
from django.db.models import Q
from django.forms import ModelChoiceField, ChoiceField, widgets, ModelForm
from django.utils import timezone


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
    def __init__(self, *args, **kwargs):
        super(ServiceModelForm, self).__init__(*args, **kwargs)
        if 'department' in self.initial and self.initial['department']:
            if 'privileged' in self.initial and self.initial['privileged']:
                self.fields['department'].queryset = Department.objects.filter(Q(id=self.initial['department']) | Q(id__in=self.initial['alt_depts']))
            else:
                self.fields['department'].queryset = Department.objects.filter(id=self.initial['department'])
'''


class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)

#class 
Update product: 4% agar, 100 mm (sleeve)
Descriptive name:   
Product:    
Media type: 
Cost:   
Container:  
Volume: 
Notes:  

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('')

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
