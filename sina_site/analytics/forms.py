from django.forms import Form
from django import forms
import calendar
from datetime import date, timedelta

MONTH_CHOICES = tuple((str(i), month) for i, month in enumerate(calendar.month_name) if month)

PERIOD_CHOICES = (
    ('week', 'Неделя'),
    ('month', 'Месяц'),
    ('year', 'Год'),
)

class PeriodFilterForm(Form):
    today = date.today()
    current_year = today.year
    years = range(2000, current_year+1)

    period = forms.ChoiceField(choices=PERIOD_CHOICES,
                               widget=forms.Select(attrs={'class': 'form-control'}), label='Период')
    date_from = forms.DateField(widget=forms.SelectDateWidget(years=years, attrs={'class': 'form-control'}), label='С')
    date_to = forms.DateField(widget=forms.SelectDateWidget(years=years, attrs={'class': 'form-control'}), label='По')
