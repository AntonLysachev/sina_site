from typing import Any
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from django.utils.translation import gettext_lazy as _
from sina_site.mixins import LoginRequiredMixin
from sina_site.customers.models import Customer

class CustomersIndexView(LoginRequiredMixin, TemplateView):

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        customer = Customer.objects.all()
        return render(request, 'customers/index.html', context={'customers': customer})

