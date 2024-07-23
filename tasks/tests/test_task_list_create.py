from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from tasks.models import TaskList


class TaskListCreateViewAdminTests(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(username='admin', password='adminpass', is_admin=True)
        self.client.login(username='admin', password='adminpass')

    def test_create_task_list_success(self):
        url = reverse('task-list-create')
        data = {'name': 'Test Task List', 'is_public': True}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TaskList.objects.count(), 1)
        self.assertEqual(TaskList.objects.get().name, 'Test Task List')

    def test_create_task_list_failure(self):
        url = reverse('task-list-create')
        data = {'name': ''}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
