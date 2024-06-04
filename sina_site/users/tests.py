from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from sina_site.tasks.models import Task
from sina_site.utils.test_helpers import build_fixture_path, get_content
from django.utils.translation import gettext as _
import json


class UserViewsTest(TestCase):
    fixtures = ['db.json']

    def setUp(self):
        self.client = Client()
        fixtures = json.loads(get_content(build_fixture_path('fixtures.json')))
        self.usertest = fixtures['usertest']
        self.task_name = fixtures['task']['name']
        userforlogin = fixtures['userforlogin']
        self.username = userforlogin['username']
        password = userforlogin['password']
        self.client.login(username=self.username, password=password)

    def test_user_create_view(self):
        response = self.client.post(reverse('user_create'), self.usertest, follow=True)
        self.assertContains(response, _('User successfully registered'))
        user_exists = get_user_model().objects.filter(username='testuser').exists()
        self.assertTrue(user_exists)

    def test_user_update_view(self):
        user = get_user_model().objects.get(username=self.username)
        response = self.client.post(reverse(
            'user_update',
            kwargs={'pk': user.pk}),
            self.usertest,
            follow=True)
        self.assertContains(response, _('User successfully changed'))
        user = get_user_model().objects.get(pk=user.pk)
        self.assertEqual(user.first_name, self.usertest['first_name'])

    def test_user_delete_view_used_user(self):
        user = get_user_model().objects.get(username=self.username)
        response = self.client.post(reverse('user_delete', kwargs={'pk': user.pk}), follow=True)
        self.assertContains(response, _('Cannot delete user because they have associated tasks'))
        user_exists = get_user_model().objects.filter(username=self.username).exists()
        self.assertTrue(user_exists)

    def test_user_delete_view(self):
        task = Task.objects.get(name=self.task_name)
        self.client.post(reverse('task_delete', args=[task.id]))
        user = get_user_model().objects.get(username=self.username)
        response = self.client.post(reverse('user_delete', kwargs={'pk': user.pk}), follow=True)
        self.assertContains(response, _('User successfully deleted'))
        user_exists = get_user_model().objects.filter(username=self.username).exists()
        self.assertFalse(user_exists)

    def test_user_update_view_forbidden(self):
        response = self.client.post(reverse(
            'user_update',
            kwargs={'pk': 2}),
            self.usertest,
            follow=True)
        self.assertContains(response, _('You do not have permission to change another user'))
        user = get_user_model().objects.get(pk=2)
        self.assertNotEqual(user.first_name, self.usertest['first_name'])

    def test_user_delete_view_forbidden(self):
        response = self.client.post(reverse('user_delete', kwargs={'pk': 2}), follow=True)
        self.assertContains(response, _('You do not have permission to change another user'))
        user_exists = get_user_model().objects.filter(pk=2).exists()
        self.assertTrue(user_exists)
