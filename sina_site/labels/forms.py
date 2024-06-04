from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from .models import Label
from django import forms


class LabelForm(ModelForm):

    name = forms.CharField(label=_('Name'))

    class Meta:
        model = Label
        fields = ['name']
