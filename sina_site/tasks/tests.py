from django.test import TestCase, Client
from .models import Task
from sina_site.statuses.models import Status
from django.urls import reverse
from sina_site.utils.test_helpers import build_fixture_path, get_content
from django.utils.translation import gettext as _
import json


class TaskViewTest(TestCase):
    fixtures = ['db.json']

    def setUp(self):
        self.client = Client()
        fixtures = json.loads(get_content(build_fixture_path('fixtures.json')))
        self.usertest = fixtures['usertest']
        self.task_name = fixtures['task']['name']
        self.status_name = fixtures['status']['name']
        userforlogin = fixtures['userforlogin']
        username = userforlogin['username']
        password = userforlogin['password']
        self.client.login(username=username, password=password)

    def test_task_index_view(self):
        response = self.client.get(reverse('tasks'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.task_name)

    def test_task_show_view(self):
        response = self.client.get(reverse('task_show', args=[4]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.task_name)

    def test_task_create_view(self):
        status = Status.objects.get(name=self.status_name)
        response = self.client.post(reverse('task_create'), {
            'name': 'New Task',
            'status': status.id,
        }, follow=True)
        self.assertContains(response, _('Task created successfully'))
        self.assertTrue(Task.objects.filter(name='New Task').exists())

    def test_task_update_view(self):
        task = Task.objects.get(name=self.task_name)
        status = Status.objects.get(name=self.status_name)
        response = self.client.post(reverse('task_update', args=[task.id]), {
            'name': 'Updated Task',
            'status': status.id,
        }, follow=True)
        self.assertContains(response, _('The task was successfully modified'))
        self.assertTrue(Task.objects.filter(name='Updated Task').exists())

    def test_task_delete_view(self):
        task = Task.objects.get(name=self.task_name)
        response = self.client.post(reverse('task_delete', args=[task.id]), follow=True)
        self.assertContains(response, _('Task successfully deleted'))
        self.assertFalse(Task.objects.filter(id=task.id).exists())
