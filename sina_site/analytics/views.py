from typing import Any
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from sina_site.analytics.controllers import Pump, Analytics
from sina_site.analytics.forms import PeriodFilterForm
from datetime import date, timedelta



class AnalyticsIndexView(TemplateView):
    template_name = 'analytics/index.html'

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        context = {}
        context['form'] = PeriodFilterForm
        context['data_for_chart'] = {'data': [0], 'periods': [0]}
        analytic = Analytics()
        form = PeriodFilterForm(request.GET)
        form.is_valid()
        if form.changed_data:
            selected_period = form.cleaned_data.get('period')
            date_from = form.cleaned_data.get('date_from')
            date_to = form.cleaned_data.get('date_to')
            period = {'weeks': 1}
            if selected_period == 'week':
                period = {'weeks': 1}
            if selected_period == 'month':
                period = {'months': 1}
            if selected_period == 'year':
                period = {'years': 1}

            returnability = analytic.get_returnability(date_from=date_from, date_to=date_to, **period)
            percents = list(map(lambda x: x['count'], returnability))
            periods = list(map(lambda x: f"{x['date_from']}-{x['date_to']}", returnability))
            count_transactions = list(map(lambda x: x['transactions'], returnability))

            context['form'] = form
            context['returnability'] = returnability
            context['data_for_chart'] = {'percents': percents, 'periods': periods, 'count_transactions': count_transactions}

        return render(request, self.template_name, context=context)
    
    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        context = {}
        pump = Pump()
        pump.synchronization_db()
        context['form'] = PeriodFilterForm
        return render(request, self.template_name, context=context)