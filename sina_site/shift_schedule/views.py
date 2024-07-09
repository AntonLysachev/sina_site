from typing import Any
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from sina_site.shift_schedule.models import Shift
from .controllers import group_shifts, get_dates_of_week, initialize_shift_formsets, get_weeks_for_year
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
import calendar
from django.contrib import messages
from datetime import datetime
from .forms import YearForm
from sina_site.mixins import LoginRequiredMixin


class ShiftScheduleIndexView(LoginRequiredMixin, TemplateView):
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        days_of_week = tuple((i, day) for i, day in enumerate(calendar.day_name))
        groups = group_shifts()
        year_form = YearForm
        return render(request, 'shift_schedule/index.html', context={'groups': groups,
                                                                     'year_form': year_form,
                                                                     'days_of_week': days_of_week})

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        period = request.POST.get('period')
        week_start, week_end = period.split(' - ')
        start_date = datetime.strptime(week_start, "%d-%m-%Y").date()
        end_date = datetime.strptime(week_end, "%d-%m-%Y").date()
        shifts = Shift.objects.filter(date__range=[start_date, end_date])
        for shift in shifts:
            shift.delete()
        messages.success(request, _('Schedule deleted'))
        return redirect('shift_schedule')


class ChuseWeekView(LoginRequiredMixin, TemplateView):
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        button = [key for key, value in request.GET.items() if value == 'on']
        if button:
            week_start, week_end = button[0].split(' - ')
            start = datetime.strptime(week_start, "%d-%m-%Y").date()
            end = datetime.strptime(week_end, "%d-%m-%Y").date()
            is_exists = Shift.objects.filter(date__range=[start, end]).exists()
            if is_exists:
                return redirect('shift_update', slug=f'{week_start} - {week_end}')
            else:
                return redirect('shift_create', slug=f'{week_start} - {week_end}')
        year = int(request.GET.get('select_year'))
        weeks = get_weeks_for_year(year)
        context = {}
        context['weeks'] = [weeks[i:i + 8] for i in range(0, len(weeks), 8)]
        context['year'] = year
        return render(request, 'shift_schedule/chuse_week.html', context=context)


class ShiftBaseView(LoginRequiredMixin, TemplateView):
    title = ''
    messages_success = ''

    def get_context(self, request: HttpRequest, formset=None, **kwargs):
        slug = kwargs.get('slug')
        week_start, _ = slug.split(' - ')
        start_date = datetime.strptime(week_start, "%d-%m-%Y").date()
        initialize = initialize_shift_formsets(start_date, request.POST if formset else None)
        context = {
            'slug': slug,
            'title': self.title,
            'management_form': initialize['management_form'],
            'formsets': initialize['formsets'],
            'formset': initialize['formset'],
            'days_of_week': get_dates_of_week(start_date),
        }
        return context

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        context = self.get_context(request, **kwargs)
        return render(request, 'shift_schedule/form.html', context=context)

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        context = self.get_context(request, formset=True, **kwargs)
        formset = context['formset']

        if formset.is_valid():
            for form in formset.cleaned_data:
                worker = form['worker']
                date = form['date']
                if form['state_1'] and not form['shift_1']:
                    shift = Shift.objects.get(date=date, shift=1)
                    shift.delete()
                if form['state_2'] and not form['shift_2']:
                    shift = Shift.objects.get(date=date, shift=2)
                    shift.delete()
            for form in formset.cleaned_data:
                worker = form['worker']
                date = form['date']
                if not form['state_1'] and form['shift_1']:
                    Shift.objects.create(worker=worker, date=date, shift=1)
                if not form['state_2'] and form['shift_2']:
                    Shift.objects.create(worker=worker, date=date, shift=2)

            messages.success(request, self.messages_success)
            return redirect(reverse_lazy('shift_schedule'))

        return render(request, 'shift_schedule/form.html', context=context)


class ShiftScheduleCreateView(ShiftBaseView):
    title = _('Create')
    messages_success = _('Schedule add successfully')


class ShiftScheduleUpdateView(ShiftBaseView):
    title = _('Update')
    messages_success = _('Schedule update successful')
