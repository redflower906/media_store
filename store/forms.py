from datetime import datetime
#from dateutil.relativedata import relativedata
import time
import logging

from django import forms
from django.forms.extras.widgets import SelectDateWidget
from django.forms.widgets import TextInput, HiddenInput, NumberInput, DateInput, Select
from .models import *
from django.forms.models import inlineformset_factory,formset_factory,modelformset_factory
from djangoformsetjs.utils import formset_media_js
from django.forms.models import BaseInlineFormSet,BaseModelFormSet,BaseFormSet,BaseForm
from django.db import connections
from django.db.utils import ProgrammingError, OperationalError
from django.db.models import Q
from django.forms import ModelChoiceField, ChoiceField, widgets, ModelForm
from django.utils import timezone
from djrichtextfield.widgets import RichTextWidget
from tinymce.widgets import TinyMCE

logger = logging.getLogger('default')

class NumInput(TextInput):
    input_type = 'number'

class Item_Model_Form(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ('inventory_text','product','media_type','cost','container','volume','active','notes_inv')
        labels = {
            'inventory_text': 'Descriptive name',
            'notes_inv': 'Item Notes'
        }
        widgets = {
            'inventory_text': forms.TextInput(attrs={'class': 'form-control form-text'}),
            'product': forms.TextInput(attrs={'class': 'form-control form-text'}),
            'media_type': forms.Select(attrs={'class': 'form-control form-text chosen-select'}),
            'cost': forms.TextInput(attrs={'class': 'form-control form-text'}),
            'container': forms.TextInput(attrs={'class': 'form-control form-text'}),
            'volume': forms.TextInput(attrs={'class': 'form-control form-text'}),
            'active': forms.Select(attrs={'class': 'form-control form-text'}),
            'notes_inv': forms.Textarea(attrs={'class': 'form-control line-notes'}),            
            #'vendor': forms.TextInput(attrs={'class': 'line-container'})
        }
        
class Email_Form(forms.Form):
    To = forms.EmailField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control email-form-text'}),
        label='To:',
    )
    From = forms.EmailField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control email-form-text'}),
        label = 'From:',
    )
    Text = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={'class':'form-control', 'rows':10}),
        label = 'Content:',
        )        
    
        

def item_model_formset_factory(extra):
    return modelformset_factory(Inventory,
    fields = ('inventory_text','product','media_type','cost','container','volume','active','notes_inv'),
    labels = {
            'inventory_text': 'Descriptive name',
            'notes_inv': 'Item Notes'
        },
    widgets = {
        'inventory_text': forms.TextInput(attrs={'class': 'form-control form-text'}),
        'product': forms.TextInput(attrs={'class': 'form-control form-text'}),
        'media_type': forms.Select(attrs={'class': 'form-control form-text chosen-select'}),
        'cost': forms.TextInput(attrs={'class': 'form-control form-text'}),
        'container': forms.TextInput(attrs={'class': 'form-control form-text'}),
        'volume': forms.TextInput(attrs={'class': 'form-control form-text'}),
        'active': forms.Select(attrs={'class': 'form-control form-text'}),
        'notes_inv': forms.Textarea(attrs={'class': 'form-control line-notes'}),
        #'vendor': forms.TextInput(attrs={'class': 'line-container'})
    },
    extra=extra, can_delete=False,
    )

class DateInput(TextInput):
    input_type='date'

# create data_text_search attribute in option for submitter + requester dropdowns to allow barcode scan/mag stripe reader to work.    
class OrderFormSelect(forms.Select):

    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):

        option_dict = super(OrderFormSelect, self).create_option(name, value, label, selected, index,
                                                                    subindex=subindex, attrs=attrs)
        if option_dict['value']:
            user = UserProfile.objects.get(user=option_dict['value'])
            option_dict['attrs']['data-text-search'] = user.data_text_search()
        return option_dict

class OrderForm(forms.ModelForm):

    #allow full names in [first_name last_name] format and exclude signout names for sub+req. Only list existing project IDs (with JVS)
    submitter = forms.ModelChoiceField(queryset=UserFullName.objects.all().exclude(id=17381).exclude(id=17380).exclude(id=17382).exclude(id=17622).exclude(id=17623).order_by('last_name'), widget=OrderFormSelect(attrs={'class':'chosen-select remover'}))
    requester = forms.ModelChoiceField(queryset=UserFullName.objects.all().exclude(id=17381).exclude(id=17380).exclude(id=17382).exclude(id=17622).exclude(id=17623).order_by('last_name'), widget=OrderFormSelect(attrs={'class': 'chosen-select'}))
    project_code = ProjectModelChoiceField(queryset=UserProfile.objects.filter(hhmi_project_id__icontains='JVS'), widget=forms.Select(attrs={'class': 'chosen-select'}), required=False)
    class Meta:
        model = Order
        fields = ('submitter', 'department', 'requester', 'is_recurring', 'location', 'date_recurring_start', 'date_recurring_stop', 'weeks', 'doc', 'notes_order','project_code')
        labels = {
            'notes_order': 'Special Instructions'
        }
        widgets={
        'department': forms.Select(attrs={'required': False, 'class': 'chosen-select'}),
        'is_recurring': forms.RadioSelect(choices=[
            (True, 'Yes'),
            (False, 'No')             
        ], attrs={'class': 'form-contorl'}),
        'location': forms.Select(choices=Order.LOCATION_CHOICES, attrs={'class': 'form-control'}),
        'date_recurring_start': forms.DateInput(attrs={'class': 'datepicker form-control'}),
        'date_recurring_stop': forms.DateInput(attrs={'class': 'datepicker form-control'}),
        'weeks': forms.Select(choices=Order.WEEK_CHOICES, attrs={'required': False, 'class': 'form-control'}),
        'notes_order': forms.Textarea(attrs={'class': 'line-notes form-control'}), 
        }

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['submitter'].empty_label = "Select a submitter"
        # following line needed to refresh widget copy of choice list
        self.fields['submitter'].widget.choices = self.fields['submitter'].choices
        self.fields['department'].empty_label = "Select a department"
        # following line needed to refresh widget copy of choice list
        self.fields['department'].widget.choices = self.fields['department'].choices
        self.fields['requester'].empty_label = "Select a requester"
        # following line needed to refresh widget copy of choice list
        self.fields['requester'].widget.choices = self.fields['requester'].choices
        self.fields['project_code'].empty_label = "Select a project code"
        # following line needed to refresh widget copy of choice list
        self.fields['project_code'].widget.choices = self.fields['project_code'].choices



# inspired by: https://gist.github.com/nspo/cd26ae2716332234757d2c3b1f815fc2
class OrderLineInlineFormSet(
    inlineformset_factory(Order, OrderLine,
        fields=('qty', 'line_cost', 'inventory'),
        widgets={
        'qty': NumInput(attrs={'min': '0', 'step': 'any', 'class': 'form-control col-centered line_calc line_qty'}),
        'line_cost': NumInput(attrs={'step': 'any', 'class': 'form-control col-centered line_calc line_cost', 'readonly':'readonly'}),
        'inventory': forms.Select(attrs={'class': 'form-control'}),
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

        # if not self.total_is_positive_nonzero():
        #     raise forms.ValidationError(
        #         "Total cost must be greater than zero")
        
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

    def copy_orderline_data(self, order):
        """ build initial formset data given the order to be copied
        """
        orderlines = order.orderline_set.all()
        data = [{'qty': ol.qty, 'line_cost': ol.line_cost,
                 'inventory': ol.inventory.id} for ol in orderlines]
        self.extra = len(orderlines)
        self.initial = data

class AnnouncementsForm(forms.ModelForm):
    
    # text = forms.CharField(widget=TinyMCE(attrs={'rows': 5, 'class':'form-control'}))


    class Meta:
        model = Announcements
        fields = ('text', 'show')
        labels = {
            'text': '',
            'show': 'Display'
        }
        widgets = {
            'text': forms.Textarea(attrs={'rows': 5, 'class':'form-control'}),
            'show': forms.CheckboxInput(attrs={'class': 'checkbox-inline'})
        }
        


OrderStatusFormSet = modelformset_factory(
Order, 
fields=('status',),
widgets={
    'status': forms.Select(choices=Order.STATUS_CHOICES, attrs={'class': 'form-control'})
    },
extra=0,
)


class Bottles_VialsForm(forms.ModelForm):
    
    class Meta:    
        
        model = Bottles_Vials
        fields = ('item', 'amnt')
        labels = {
            'item': 'Item',
            'amnt': 'QTY'
        }
        widgets = {
            'item': forms.Select(choices=Bottles_Vials.ITEM_CHOICES, attrs={'class':'form-control', 'disabled':'disabled'}),
            'amnt': forms.NumberInput(attrs={'class':' amnt form-control'})
        }
    
    def __init__(self, *args, **kwargs):
        super(Bottles_VialsForm, self).__init__(*args, **kwargs)
        self.fields['item'].choices = Bottles_Vials.ITEM_CHOICES


B_VFormSet = modelformset_factory(
Bottles_Vials,
form=Bottles_VialsForm,
extra=0,
)


class OrderSearchForm(forms.Form):
    
    DATE_CHOICES = (
    ('', 'Select a Date Range'),
    ('Order Submitted', 'Order Submitted'), 
    ('Order Completed', 'Order Completed'), 
    ('Order Billed', 'Order Billed'),
    )

    BOOL_CHOICES = (
        ('AND', 'AND'),
        ('OR', 'OR'),
    )

    date_type = forms.ChoiceField(
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        choices=DATE_CHOICES,
        label = 'Date Range'
        )
    search_date_from = forms.CharField(
        required=False,
        widget=forms.DateInput(format=('%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y'), attrs={'class': 'datepicker form-control'}),
        label = 'From'
        )
    search_date_to = forms.CharField(
        required=False,
        widget=forms.DateInput(format=('%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y'), attrs={'class': 'datepicker form-control'}),
        label = 'To'
        )
    search_keyword = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class':'form-control'}),
        label = 'Keyword Search',
        )
    and_or = forms.ChoiceField(
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        choices=BOOL_CHOICES,
        )

    def clean (self):
        date_from = self.cleaned_data.get('search_date_from')
        date_to = self.cleaned_data.get('search_date_to')
        date_type = self.cleaned_data.get('date_type')
        msg = forms.ValidationError("This field is required.")


        if (date_from and date_to and date_type):
            return self.cleaned_data
        elif date_from and date_to:
            self.add_error('date_type', msg)
        elif date_from and date_type:
            self.add_error('search_date_to', msg)
        elif date_to and date_type:
            self.add_error('search_date_from', msg)
        elif date_to:
            self.add_error('date_type', msg)
            self.add_error('search_date_from', msg)
        elif date_from:
            self.add_error('date_type', msg)
            self.add_error('search_date_to', msg)
        elif date_type:
            self.add_error('search_date_from', msg)
            self.add_error('search_date_to', msg)
        else:
            return self.cleaned_data
            # # Keep the database consistent. The user may have
            # # submitted a shipping_destination even if shipping
            # # was not selected
            # self.cleaned_data['date_type'] = ''
            # self.cleaned_data['search_date_to'] = ''

        return self.cleaned_data


class OrderSearchForm2(forms.Form):
        
    DATE_CHOICES = (
    ('', 'Select a Date Range'),
    ('Order Submitted', 'Order Submitted'), 
    ('Order Completed', 'Order Completed'), 
    ('Order Billed', 'Order Billed'),
    )

    BOOL_CHOICES = (
        ('AND', 'AND'),
        ('OR', 'OR'),
    )

    FIELD_CHOICES = (
        ('order__notes_order', 'Order Notes'),
        ('inventory__inventory_text', 'Product'),
    )

    date_type = forms.ChoiceField(
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        choices=DATE_CHOICES,
        label = 'Date Range'
        )
    search_date_from = forms.CharField(
        required=False,
        widget=forms.DateInput(format=('%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y'), attrs={'class': 'datepicker form-control'}),
        label = 'From'
        )
    search_date_to = forms.CharField(
        required=False,
        widget=forms.DateInput(format=('%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y'), attrs={'class': 'datepicker form-control'}),
        label = 'To'
        )
    search_keyword = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class':'form-control'}),
        label = 'Keyword Search',
        )
    and_or = forms.ChoiceField(
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        choices=BOOL_CHOICES,
        )
    field_choice = forms.ChoiceField(
        required=False,
        widget=forms.SelectMultiple(attrs={
            'class': 'chosen-select', 
            'multiple': True,
            'placeholder': 'Choose one or more fields'
        }),
        choices=FIELD_CHOICES,
    )

    def clean (self):
        date_from = self.cleaned_data.get('search_date_from')
        date_to = self.cleaned_data.get('search_date_to')
        date_type = self.cleaned_data.get('date_type')
        msg = forms.ValidationError("This field is required.")


        if (date_from and date_to and date_type):
            return self.cleaned_data
        elif date_from and date_to:
            self.add_error('date_type', msg)
        elif date_from and date_type:
            self.add_error('search_date_to', msg)
        elif date_to and date_type:
            self.add_error('search_date_from', msg)
        elif date_to:
            self.add_error('date_type', msg)
            self.add_error('search_date_from', msg)
        elif date_from:
            self.add_error('date_type', msg)
            self.add_error('search_date_to', msg)
        elif date_type:
            self.add_error('search_date_from', msg)
            self.add_error('search_date_to', msg)
        else:
            return self.cleaned_data
            # # Keep the database consistent. The user may have
            # # submitted a shipping_destination even if shipping
            # # was not selected
            # self.cleaned_data['date_type'] = ''
            # self.cleaned_data['search_date_to'] = ''

        return self.cleaned_data