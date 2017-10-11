from datetime import datetime
#from dateutil.relativedata import relativedata
import time
import logging

from django import forms
from django.forms.extras.widgets import SelectDateWidget
from django.forms.widgets import TextInput, HiddenInput, NumberInput
from .models import Inventory, Vendor, Announcements, Order, OrderLine #MEDIA_CHOICES, Department, UserProfile
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

class OrderLineForm(forms.ModelForm):
    class Meta:
        model = OrderLine
        fields = ('description', 'qty', 'unit', 'line_cost', 'inventory')#category)

class OrderForm(forms.ModelForm):
    #submitter = user_choice(queryset=User.objects.only('first_name','last_name'))
    #main_requester = user_choice(queryset=requester_queryset_generator())
    #department = forms.ModelChoiceField(queryset=Department.objects.all(), widget=forms.Select(attrs={'style' : 'width:250'}))
    inventory_type = forms.ModelChoiceField(queryset=Inventory.objects.filter(active=True), required=False)
    date_complete = forms.DateField(widget=DateInput)

    def clean_date_complete(self):
        data = self.cleaned_data['date_complete']
        last_billed = Order.objects.last_billed()
        if last_billed > data:
            raise forms.ValidationError(u'{0} is before the last billed date {1}'.format(data,last_billed))
        return data

    class Meta:
        model = Order
        fields = ('date_complete', 'special_instructions', 'date_billed')#'department', 'inventory_type' 'requester','submitter'

def order_inline_formset_factory():
    return inlineformset_factory(Order, OrderLine,
        fields = ('description', 'qty', 'unit', 'line_cost', 'inventory', 'media_type', 'cost', 'inventory_text'),#category, 'inventory_type'
        widgets = {
            'media_choice': forms.Select(attrs={'class': 'form-text'}),
            'qty': NumInput(attrs={'min':'0', 'step': 'any', 'class': 'line_calc line_qty'}),
            'line_cost': NumInput(attrs={'step':'any', 'class': 'line_calc line_cost'}),
            'inventory': HiddenInput(),
            'inventory_text': forms.Select(attrs={'class': 'form-text'}),
            'description': forms.TextInput(attrs={'class': 'form-text'}),
            'unit': forms.TextInput(attrs={'class': 'line unit'})
        },
        can_delete=True
        )

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

