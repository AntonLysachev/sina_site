from django.test import TestCase, Client
from .models import Status
from django.urls import reverse
from sina_site.tasks.models import Task
from sina_site.utils.test_helpers import build_fixture_path, get_content
from django.utils.translation import gettext as _
import json


class StatusViewTest(TestCase):
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

    def test_status_index_view(self):
        response = self.client.get(reverse('statuses'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.status_name)

    def test_status_create_view(self):
        response = self.client.post(reverse('status_create'), {
            'name': 'New Status',
        }, follow=True)
        self.assertContains(response, _('Status successfully created'))
        self.assertTrue(Status.objects.filter(name='New Status').exists())

    def test_status_update_view(self):
        status = Status.objects.get(name=self.status_name)
        response = self.client.post(reverse('status_update', args=[status.id]), {
            'name': 'Updated Status',
        }, follow=True)
        self.assertContains(response, _('Status changed successfully'))
        self.assertTrue(Status.objects.filter(name='Updated Status').exists())

    def test_status_delete_view_used_status(self):
        status = Status.objects.get(name=self.status_name)
        response = self.client.post(reverse('status_delete', args=[status.id]), follow=True)
        self.assertContains(response, _('Cannot delete status because it is in use'))
        self.assertTrue(Status.objects.filter(id=status.id).exists())

    def test_status_delete_view(self):
        task = Task.objects.get(name=self.task_name)
        self.client.post(reverse('task_delete', args=[task.id]))
        status = Status.objects.get(name=self.status_name)
        response = self.client.post(reverse('status_delete', args=[status.id]), follow=True)
        self.assertContains(response, _('Status deleted successfully'))
        self.assertFalse(Status.objects.filter(id=status.id).exists())
