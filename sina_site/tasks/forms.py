from django import forms
from django.forms import ModelForm, Form
from django.utils.translation import gettext_lazy as _
from .models import Task
from django.contrib.auth.models import User
from sina_site.labels.models import Label
from sina_site.statuses.models import Status


class UserChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.first_name} {obj.last_name}"


class TaskForm(ModelForm):
    name = forms.CharField(label=_("Name"))
    status = forms.ModelChoiceField(queryset=Status.objects.all(), label=_("Status"))
    description = forms.CharField(widget=forms.Textarea, required=False, label=_("Description"))
    executor = UserChoiceField(queryset=User.objects.filter(is_active=True),
                               required=False, label=_("Executor"))
    labels = forms.ModelMultipleChoiceField(queryset=Label.objects.all(),
                                            required=False, label=_("Labels"))

    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor', 'labels']


class TaskFilterForm(Form):
    status = forms.ModelChoiceField(queryset=Status.objects.all(),
                                    required=False,
                                    label=_('Status'))
    executor = UserChoiceField(queryset=User.objects.filter(is_active=True),
                               required=False, label=_('Executor'))
    labels = forms.ModelChoiceField(queryset=Label.objects.all(), required=False, label=_('Label'))
    self_tasks = forms.BooleanField(required=False, label=_('Only self tasks'))
