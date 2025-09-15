from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import Task

User = get_user_model()

class ToggleActionTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="ivojr", password="senha123")
        # autentica todas as requisições deste client
        self.client.force_authenticate(user=self.user)

    def test_toggle_action(self):
        # cria task do próprio usuário
        t = Task.objects.create(title='Toggle me', status='Pending', owner=self.user)

        # toggle -> Completed
        r1 = self.client.post(f'/api/tasks/{t.id}/toggle/')
        self.assertEqual(r1.status_code, status.HTTP_200_OK)
        self.assertEqual(r1.data['status'], 'Completed')

        # toggle -> Pending
        r2 = self.client.post(f'/api/tasks/{t.id}/toggle/')
        self.assertEqual(r2.status_code, status.HTTP_200_OK)
        self.assertEqual(r2.data['status'], 'Pending')

class ListIsolationTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.a = User.objects.create_user(username="a", password="x")
        self.b = User.objects.create_user(username="b", password="x")
        Task.objects.create(title='A1', owner=self.a)
        Task.objects.create(title='B1', owner=self.b)

    def test_user_sees_only_own_tasks(self):
        self.client.force_authenticate(user=self.a)
        r = self.client.get('/api/tasks/')
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        titles = [item['title'] for item in r.data['results']]
        self.assertEqual(titles, ['A1'])

class OwnershipProtectionTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.a = User.objects.create_user(username="a", password="x")
        self.b = User.objects.create_user(username="b", password="x")
        self.task_b = Task.objects.create(title='B1', owner=self.b)

    def test_cannot_edit_others_task(self):
        self.client.force_authenticate(user=self.a)
        r = self.client.patch(f'/api/tasks/{self.task_b.id}/', data={'title': 'Hacked'}, format='json')
        self.assertEqual(r.status_code, status.HTTP_404_NOT_FOUND)

    def test_cannot_toggle_others_task(self):
        self.client.force_authenticate(user=self.a)
        r = self.client.post(f'/api/tasks/{self.task_b.id}/toggle/')
        self.assertEqual(r.status_code, status.HTTP_404_NOT_FOUND)

class CreateSetsOwnerTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="ivojr", password="x")
        self.client.force_authenticate(user=self.user)

    def test_create_sets_owner(self):
        r = self.client.post('/api/tasks/', data={'title': 'Nova', 'done': False}, format='json')
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        task_id = r.data['id']
        task_db = Task.objects.get(id=task_id)
        self.assertEqual(task_db.owner, self.user)