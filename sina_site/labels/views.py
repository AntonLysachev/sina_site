from typing import Any
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.utils.translation import gettext as _
from .models import Label
from .forms import LabelForm
from sina_site.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin


class BaseLabelView(LoginRequiredMixin, SuccessMessageMixin):
    model = Label
    template_name = 'form.html'
    success_url = reverse_lazy('labels')


class LabelsIndexView(LoginRequiredMixin, TemplateView):

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:

        labels = Label.objects.all()

        return render(request, 'labels/index.html', context={'labels': labels})


class LabelCreateView(BaseLabelView, CreateView):
    form_class = LabelForm
    success_message = _('Label successfully created')
    extra_context = {'title': 'Create label', 'button': 'Create'}


class LabelUpdateView(BaseLabelView, UpdateView):
    form_class = LabelForm
    success_message = _('Label changed successfully')
    extra_context = {'title': 'Update label', 'button': 'Update'}


class LabelDeleteView(BaseLabelView, DeleteView):
    extra_context = {'title': 'Deleting a user',
                     'button': 'Yes, delete',
                     'question': 'Are you sure you want to delete'}

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        label = self.get_object()
        context['user_to_delete'] = f"{label.name}?"
        return context

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:

        label = self.get_object()
        if label.task_set.all():
            messages.error(request, _('Cannot delete label because it is in use'))
        else:
            label.delete()
            messages.success(request, _('Label deleted successfully'))
        return redirect(self.success_url)
