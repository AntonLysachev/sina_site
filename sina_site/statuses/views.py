from typing import Any
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.utils.translation import gettext as _
from .models import Status
from .forms import StatusForm
from django.db.models.deletion import ProtectedError
from sina_site.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin


class BaseStatusView(LoginRequiredMixin, SuccessMessageMixin):
    model = Status
    template_name = 'form.html'
    success_url = reverse_lazy('statuses')


class StatusesIndexView(BaseStatusView, TemplateView):

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:

        statuses = Status.objects.all()

        return render(request, 'statuses/index.html', context={'statuses': statuses})


class StatusCreateView(BaseStatusView, CreateView):
    form_class = StatusForm
    success_message = _('Status successfully created')
    extra_context = {'title': 'Create status', 'button': 'Create'}


class StatusUpdateView(BaseStatusView, UpdateView):
    form_class = StatusForm
    success_message = _('Status changed successfully')
    extra_context = {'title': 'Update status', 'button': 'Update'}


class StatusDeleteView(BaseStatusView, DeleteView):

    extra_context = {'title': 'Deleting a user',
                     'button': 'Yes, delete',
                     'question': 'Are you sure you want to delete'}

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        status = self.get_object()
        context['user_to_delete'] = f"{status.name}?"
        return context

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:

        status = self.get_object()
        try:
            status.delete()
            messages.success(request, _('Status deleted successfully'))
        except ProtectedError:
            messages.error(request, _('Cannot delete status because it is in use'))
        return redirect(self.success_url)
