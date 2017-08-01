from datetime import datetime
import time
import logging

from django import forms
from django.forms.extras.widgets import SelectDateWidget
from django.forms.widgets import TextInput, HiddenInput
from .models import Inventory, Vendor
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

def item_model_formset_factory(extra):
    return modelformset_factory(Inventory,
        fields = ('product','media_type','cost','container','volume','notes'),
        widgets = {
            'cost': forms.TextInput(attrs={'class': 'line_cost'}),
            'container': forms.TextInput(attrs={'class': 'line-container'}),
            'volume': forms.TextInput(attrs={'class': 'line-volume'}),
            'notes': forms.Textarea(attrs={'cols': 20, 'rows': 10, 'class': 'line-notes'}),
            #'vendor': forms.TextInput(attrs={'class': 'line-container'})
        },
        extra=extra, can_delete=True,
    )

class Item_Model_Form(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ('product','media_type','cost','container','volume','notes')
        widgets = {
            'cost': forms.TextInput(attrs={'class': 'line_cost'}),
            'container': forms.TextInput(attrs={'class': 'line-container'}),
            'volume': forms.TextInput(attrs={'class': 'line-volume'}),
            'notes': forms.Textarea(attrs={'cols': 20, 'rows': 10, 'class': 'line-notes'}),
            #'vendor': forms.TextInput(attrs={'class': 'line-container'})
        }

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