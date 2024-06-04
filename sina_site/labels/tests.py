from django.test import TestCase, Client
from .models import Label
from django.urls import reverse
from sina_site.tasks.models import Task
from sina_site.utils.test_helpers import build_fixture_path, get_content
from django.utils.translation import gettext as _
import json


class LabelViewTest(TestCase):
    fixtures = ['db.json']

    def setUp(self):
        self.client = Client()
        fixtures = json.loads(get_content(build_fixture_path('fixtures.json')))
        self.usertest = fixtures['usertest']
        self.task_name = fixtures['task']['name']
        self.label_name = fixtures['label']['name']
        userforlogin = fixtures['userforlogin']
        username = userforlogin['username']
        password = userforlogin['password']
        self.client.login(username=username, password=password)

    def test_label_index_view(self):
        response = self.client.get(reverse('labels'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.label_name)

    def test_label_create_view(self):
        response = self.client.post(reverse('label_create'), {
            'name': 'New Label',
        }, follow=True)
        self.assertContains(response, _('Label successfully created'))
        self.assertTrue(Label.objects.filter(name='New Label').exists())

    def test_label_update_view(self):
        label = Label.objects.get(name=self.label_name)
        response = self.client.post(reverse('label_update', args=[label.id]), {
            'name': 'Updated Label',
        }, follow=True)
        self.assertContains(response, _('Label changed successfully'))
        self.assertTrue(Label.objects.filter(name='Updated Label').exists())

    def test_label_delete_view_used_label(self):
        label = Label.objects.get(name=self.label_name)
        response = self.client.post(reverse('label_delete', args=[label.id]), follow=True)
        self.assertContains(response, _('Cannot delete label because it is in use'))
        self.assertTrue(Label.objects.filter(id=label.id).exists())

    def test_label_delete_view(self):
        task = Task.objects.get(name=self.task_name)
        self.client.post(reverse('task_delete', args=[task.id]))
        label = Label.objects.get(name=self.label_name)
        response = self.client.post(reverse('label_delete', args=[label.id]), follow=True)
        self.assertContains(response, _('Label deleted successfully'))
        self.assertFalse(Label.objects.filter(id=label.id).exists())
