from django import forms
from datetime import date


PERIOD_CHOICES = (
    ('weeks', 'Неделя'),
    ('months', 'Месяц'),
    ('years', 'Год'),
)


class PeriodFilterForm(forms.Form):
    today = date.today()
    current_year = today.year
    years = range(2010, current_year+1)

    period = forms.ChoiceField(choices=PERIOD_CHOICES,
                               widget=forms.Select(attrs={'class': "form-select"}), label='Период')
    date_from = forms.DateField(widget=forms.SelectDateWidget(years=years, attrs={'class': "form-select"}), label='С', initial='2010-01-01')
    date_to = forms.DateField(widget=forms.SelectDateWidget(years=years, attrs={'class': "form-select"}), label='По', initial=today)
