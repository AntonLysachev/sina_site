from typing import Any
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from sina_site.shift_schedule.models import Shift
from django.contrib.auth.models import User

class Shift_scheduleIndexView(TemplateView):
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        shift = Shift.objects.all()
        users = User.objects.filter(is_active=True)
        week = range(7)
        days = range(1, 32)
        return render(request, 'shift_schedule/index.html', context={'shift': shift,
                                                                     'users': users,
                                                                     'week': week,
                                                                     'days': days})
