from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class LoginLogoutViewTests(TestCase):
    def setUp(self):
        User.objects.create_user(username='tester', password='secret')

    def test_login_view(self):
        response = self.client.post(reverse('common:login'), {
            'username': 'tester',
            'password': 'secret',
        })
        self.assertRedirects(response, reverse('index'))
        self.assertIn('_auth_user_id', self.client.session)

    def test_logout_view(self):
        self.client.login(username='tester', password='secret')
        response = self.client.get(reverse('common:logout'))
        self.assertRedirects(response, reverse('index'))
        self.assertNotIn('_auth_user_id', self.client.session)
