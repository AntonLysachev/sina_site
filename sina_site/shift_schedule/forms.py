from typing import Any
from django.forms import BaseFormSet, Form
from django.utils.translation import gettext_lazy as _
from django import forms
from django.contrib.auth.models import User
from datetime import date


class YearForm(Form):
    current_year = date.today().year
    years = [(year, year) for year in range(2000, 2100)]
    select_year = forms.CharField(
        widget=forms.Select(choices=years, attrs={'class': "form-select"}),
        label = _('year'),
        initial= current_year
    )


class ShiftDateFromForm(Form):

    today = date.today()
    current_year = today.year
    years = range(current_year + 1, 10)

    date_from = forms.DateField(
        widget=forms.SelectDateWidget(years=years, attrs={'class': "form-select"}),
        label='Преиод',
        initial=today)

#TODO поменять селект worker на строчку
class ShiftForm(forms.Form):
    state_1 = forms.Field(
        widget=forms.CheckboxInput()
    )
    state_2 = forms.Field(
        widget=forms.CheckboxInput()
    )
    worker = forms.ModelChoiceField(queryset=User.objects.filter(is_active=True))
    date = forms.DateField(widget=forms.DateInput)
    shift_1 = forms.Field(
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        required=False,
        label=f'{_('Shift')} 1')
    shift_2 = forms.Field(
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        required=False,
        label=f'{_('Shift')} 2')

    
class BaseShiftDayFormset(BaseFormSet):
    def clean(self) -> None:
        if any(self.errors):
            return
        shifts = set()
        for form in self.forms:
            date = form.cleaned_data.get('date')
            shift_1 = form.cleaned_data.get('shift_1')
            shift_2 = form.cleaned_data.get('shift_2')
            date_shift_1 = (date, shift_1, 1)
            date_shift_2 = (date, shift_2, 2)

            if date_shift_1 in shifts:
                form.add_error('shift_1', _('There cannot be two or more identical shifts'))
            if date_shift_2 in shifts:
                form.add_error('shift_2', _('There cannot be two or more identical shifts'))

            if shift_1:
                shifts.add(date_shift_1)
            if shift_2:
                shifts.add(date_shift_2)
