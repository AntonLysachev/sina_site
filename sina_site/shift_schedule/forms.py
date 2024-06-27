from django.forms import ModelForm, Form
from django.utils.translation import gettext_lazy as _
from django import forms
from django.contrib.auth.models import User
from datetime import date
from .models import Shift
from django.utils.html import format_html
from django.forms import MultiWidget, TextInput




class ShiftForm(Form):
    def __init__(self, *args, **kwargs):
        self.choices = kwargs.pop('choices', None)
        self.selected = kwargs.pop('selected', None)
        super().__init__(*args, **kwargs)
        self.fields['shifts'].choices = self.choices
        self.fields['shifts'].initial = self.selected

    shifts = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple(),
        label=''
    )


class ShiftDateFromForm(Form):

    today = date.today()
    current_year = today.year
    years = range(current_year + 1, 10)

    date_from = forms.DateField(
        widget=forms.SelectDateWidget(years=years, attrs={'class': "form-select"}),
        label='Преиод',
        initial=today)






class CustomCheckboxSelectMultiple(forms.CheckboxSelectMultiple):
    CHOICES = [(1, 'Shift 1'),
               (2, 'Shift 2')]
    def render(self, name, value, renderer=None, attrs=None):
        output = []
        for choice in self.CHOICES:
            checkbox = forms.CheckboxInput().render(name, choice[0], attrs={'class': 'form-check-input'})
            label = format_html('<label>{}</label>', choice[1])
            output.append(format_html('<div class="form-check form-check-inline">{}</div>', checkbox + label))
        return format_html('\n'.join(output))


class UserChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.first_name} {obj.last_name}"

class CheckboxWidget(MultiWidget):
    def __init__(self, attrs=None):
        widgets = [
            forms.CheckboxInput(attrs=attrs),
            forms.CheckboxInput(attrs=attrs),
        ]
        super().__init__(widgets, attrs)

    def decompress(self, value):
        if isinstance(value, list):
            return value
        return [None, None]

    def value_from_datadict(self, data, files, name):
        checkbox1, checkbox2 = super().value_from_datadict(data, files, name)
        return [checkbox1, checkbox2]


class ShiftsTryForm(ModelForm):
    class Meta:
        model = Shift

        fields = [
            'shift',
        ]

        widgets = {
            'shift': CheckboxWidget(),
        }
