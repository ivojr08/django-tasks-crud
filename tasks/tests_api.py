from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Task

class ToggleActionTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_toggle_action(self):
        t = Task.objects.create(title='Toggle me', status='Pending')
        # toggle -> Completed
        r1 = self.client.post(f'/api/tasks/{t.id}/toggle/')
        self.assertEqual(r1.status_code, status.HTTP_200_OK)
        self.assertEqual(r1.data['status'], 'Completed')
        # toggle -> Pending
        r2 = self.client.post(f'/api/tasks/{t.id}/toggle/')
        self.assertEqual(r2.status_code, status.HTTP_200_OK)
        self.assertEqual(r2.data['status'], 'Pending')