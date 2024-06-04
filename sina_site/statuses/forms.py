from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from .models import Status
from django import forms


class StatusForm(ModelForm):
    name = forms.CharField(label=_('Name'))

    class Meta:
        model = Status
        fields = ['name']
