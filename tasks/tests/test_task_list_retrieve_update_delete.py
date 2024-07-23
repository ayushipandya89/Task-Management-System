from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from tasks.models import TaskList


class TaskListRetrieveUpdateDeleteViewAdminTests(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(username='admin', password='adminpass', is_admin=True)
        self.client.login(username='admin', password='adminpass')
        self.task_list = TaskList.objects.create(name='Initial Task List', owner=self.admin_user)

    def test_update_task_list_success(self):
        url = reverse('task-list-detail', kwargs={'id': self.task_list.id})
        data = {'name': 'Updated Task List', 'is_public': False}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task_list.refresh_from_db()
        self.assertEqual(self.task_list.name, 'Updated Task List')

    def test_delete_task_list_success(self):
        url = reverse('task-list-detail', kwargs={'id': self.task_list.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(TaskList.objects.count(), 0)
