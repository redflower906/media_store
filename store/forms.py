from datetime import datetime
#from dateutil.relativedata import relativedata
import time
import logging

from django import forms
from django.forms.extras.widgets import SelectDateWidget
from django.forms.widgets import TextInput, HiddenInput, NumberInput
from .models import Inventory, Vendor, Announcements, Order, OrderLine, MEDIA_CHOICES, Department, UserProfile
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

    
class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ('department', 'requester', 'submitter')


# inspired by: https://gist.github.com/nspo/cd26ae2716332234757d2c3b1f815fc2
class OrderLineInlineFormSet(
        inlineformset_factory(Order, OrderLine,
                              fields=('qty', 'line_cost', 'inventory'),
                              widgets={
                                  'qty': NumInput(attrs={'min': '0', 'step': 'any', 'class': 'line_calc line_qty'}),
                                  'line_cost': NumInput(attrs={'step': 'any', 'class': 'line_calc line_cost', 'readonly': '1'}),
                                  'inventory': forms.Select(),
                              },
                              extra=1, can_delete=True
                              )):
    def clean(self):
        """ Additional form validation
        """
        super(OrderLineInlineFormSet, self).clean()

        if any(self.errors):
            # Don't bother validating the formset unless each form is valid on its own
            return

        if not self.have_minimum():
            raise forms.ValidationError(
                "Please include at least one Order Line.")

        if not self.total_is_positive_nonzero():
            raise forms.ValidationError(
                "Total cost must be greater than zero")

    def have_minimum(self):
        line_count = 0
        for form in self:
            if form.is_valid():
                deleted = form.cleaned_data.get('DELETE')
                if deleted == False:
                    line_count = 1
        if line_count < 1:
            return False
        return True

    def total_is_positive_nonzero(self):
        total = 0
        for form in self:
            qty = form.cleaned_data.get('qty')
            cost = form.cleaned_data.get('line_cost')
            if qty and cost:
                total += qty * cost
        if total <= 0:
            return False
        return True


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


OrderStatusFormSet = modelformset_factory(
    Order, 
    fields=('status',),
    widgets={'status': forms.Select(choices=Order.STATUS_CHOICES)},
    extra=0
)

