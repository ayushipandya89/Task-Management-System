from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from tasks.models import Task


class TaskCreateViewAdminTests(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(username='admin', password='adminpass', is_admin=True)
        self.client.login(username='admin', password='adminpass')

    def test_create_task_success(self):
        url = reverse('task-create')
        data = {
            'title': 'Admin Created Task',
            'status': 'To Do',
            'priority': 'High',
            'due_date': '2024-12-31'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.get().title, 'Admin Created Task')

    def test_create_task_failure(self):
        url = reverse('task-create')
        data = {'title': ''}  # Missing required fields
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
