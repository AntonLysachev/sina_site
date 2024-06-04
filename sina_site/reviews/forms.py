from django.forms import Form
from django import forms
from django.utils.translation import gettext_lazy as _


class ReviewsFilterForm(Form):
    type_full = forms.BooleanField(required=False, label=_('Full review'))
    type_only_grade = forms.BooleanField(required=False, label=_('Only grade'))