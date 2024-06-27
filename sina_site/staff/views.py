from typing import Any
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import UserFormCreated
from django.utils.translation import gettext_lazy as _
from sina_site.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models.deletion import ProtectedError
from django.contrib.auth.mixins import UserPassesTestMixin


class StaffChangePermissionMixin(UserPassesTestMixin):
    model = User
    template_name = 'form.html'
    success_url = reverse_lazy('staff')

    def test_func(self):
        return self.get_object() == self.request.user or self.request.user.is_superuser

    def handle_no_permission(self):
        messages.error(self.request, _('You do not have permission to change another user'))
        return redirect('staff')


class StaffIndexView(LoginRequiredMixin, TemplateView):

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        staff = User.objects.filter(is_active=True)
        return render(request, 'staff/index.html', context={'staff': staff})


class StaffCreateView(SuccessMessageMixin,
                     LoginRequiredMixin,
                     CreateView):
    model = User
    template_name = 'form.html'
    form_class = UserFormCreated
    success_url = reverse_lazy('staff')
    success_message = _("User successfully registered")
    extra_context = {'title': 'Sign up', 'button': 'Register'}


class StaffUpdateView(StaffChangePermissionMixin,
                     SuccessMessageMixin,
                     LoginRequiredMixin,
                     UpdateView):
    form_class = UserFormCreated
    success_message = _("User successfully changed")
    extra_context = {'title': 'Change user', 'button': 'Update'}


class StaffDeleteView(StaffChangePermissionMixin,
                     SuccessMessageMixin,
                     LoginRequiredMixin,
                     DeleteView):

    extra_context = {'title': 'Deleting a user',
                     'button': 'Yes, delete',
                     'question': 'Are you sure you want to delete'}

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        context['user_to_delete'] = f"{user.first_name} {user.last_name}?"
        return context

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:

        user = self.get_object()
        try:
            user.delete()
            messages.success(request, _('User successfully deleted'))
        except ProtectedError:
            messages.error(request, _('Cannot delete user because they have associated tasks'))
            return redirect('staff')
        return redirect(self.success_url)
