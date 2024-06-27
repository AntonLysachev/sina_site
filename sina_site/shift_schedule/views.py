from typing import Any
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from sina_site.shift_schedule.models import Shift
from django.contrib.auth.models import User
from .controllers import group_shifts, group_forms_for_week, group_for_update, add_shifts, update_shifts, validation_shifts
from .forms import ShiftDateFromForm, ShiftsTryForm
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
import calendar
from django.contrib import messages
from django.db import IntegrityError


class ShiftScheduleTryView(TemplateView):
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        form = ShiftsTryForm
        return render(request, 'form.html', context={'form': form})

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        form = ShiftsTryForm(request.POST)
        if form.is_valid():
            print(request.POST)

        return render(request, 'form.html', context={'form': form})


class ShiftScheduleIndexView(TemplateView):
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        shifts = Shift.objects.all().order_by('-date')
        days_of_week = tuple((i, day) for i, day in enumerate(calendar.day_name))
        if shifts:
            groups = group_shifts(shifts)
        else:
            groups = []
        return render(request, 'shift_schedule/index.html', context={'groups': groups,
                                                                     'days_of_week': days_of_week,})


class ShiftScheduleCreateView(TemplateView):
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        users = User.objects.filter(is_active=True)
        form_date_from = ShiftDateFromForm()
        days_of_week = tuple((str(i), day) for i, day in enumerate(calendar.day_name))
        forms = group_forms_for_week(users)
        return render(request, 'shift_schedule/create.html', context={'forms': forms,
                                                                      'form_date_from': form_date_from,
                                                                      'days_of_week': days_of_week,})

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        date = ShiftDateFromForm(request.POST)
        date.is_valid()
        shifts = request.POST.getlist('shifts')
        if validation_shifts(shifts):
            date_from = date.cleaned_data.get('date_from')
            try:
                add_shifts(shifts, date_from)
                messages.success(request, _('Schedule add successfully'))
            except IntegrityError:
                messages.error(request, _('A schedule with such a period already exists'))
                return redirect(reverse_lazy('shift_schedule'))
        else:
            messages.error(request, _('Two workers cannot have one shift'))
            return redirect(reverse_lazy('shift_schedule'))
        return redirect(reverse_lazy('shift_schedule'))


class ShiftScheduleUpdateView(TemplateView):
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        start_of_week, end_of_week = kwargs.get('slug').split(' - ')
        shifts = Shift.objects.filter(date__range=[start_of_week, end_of_week])
        period = f'{start_of_week} - {end_of_week}'
        groups = group_shifts(shifts)
        forms = group_for_update(groups)
        days_of_week = tuple((i, day) for i, day in enumerate(calendar.day_name))
        form_date_from = ShiftDateFromForm(initial={'date_from': start_of_week})

        return render(request, 'shift_schedule/update.html', context={'forms': forms,
                                                                      'period': period,
                                                                      'form_date_from': form_date_from,
                                                                      'days_of_week': days_of_week,})

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:    

        form = ShiftDateFromForm(request.POST)
        if form.is_valid():
            shifts = request.POST.getlist('shifts')
            if validation_shifts(shifts):
                date_from = form.cleaned_data.get('date_from')
                update_shifts(shifts, date_from)
                messages.success(request, _('Schedule update successful'))
            else:
                messages.error(request, _('Two workers cannot have one shift'))
                return redirect(reverse_lazy('shift_schedule'))
        return redirect(reverse_lazy('shift_schedule'))
