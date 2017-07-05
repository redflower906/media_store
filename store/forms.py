from datetime import datetime
import time
import logging

from django import forms
from django.forms.extras.widgets import SelectDateWidget
from django.forms import widgets
from django.forms import ModelForm
from django.forms.widgets import TextInput, HiddenInput
from .models import Inventory, Vendor
from django.forms.models import inlineformset_factory,formset_factory,modelformset_factory
from djangoformsetjs.utils import formset_media_js
from django.forms.models import BaseInlineFormSet,BaseModelFormSet,BaseFormSet,BaseForm
from django.db import connections
from django.db.utils import ProgrammingError, OperationalError
from django.db.models import Q
from django.forms import ModelChoiceField
from django.utils import timezone


class NumInput(TextInput):
    input_type = 'number'

def item_model_formset_factory(extra):
    return modelformset_factory(Inventory,
        fields = ('inventory_text','cost','container', 'notes', 'vendor'),
        widgets = {
            'cost': forms.TextInput(attrs={'class': 'line_cost'}),
            'container': forms.TextInput(attrs={'class': 'line-container'}),
            'notes': forms.TextInput(attrs={'class': 'line-notes'}),
            'vendor': forms.TextInput(attrs={'class': 'line-container'})
        },
        extra=extra, can_delete=True,
    )
class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)
