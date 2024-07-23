from django.db import models

from users.models import CustomUser


# Create your models here.
class TaskList(models.Model):
    """
        Model for Task List
    """
    name = models.CharField(max_length=100, unique=True)
    owner = models.ForeignKey(CustomUser, related_name='task_lists', on_delete=models.CASCADE)
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Task(models.Model):
    """
        Model to create Task
    """
    status_type = (
        ("created", "Created"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
    )
    priority_type = (
        ("high", "High"),
        ("medium", "Medium"),
        ("low", "Low"),
    )
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    priority = models.CharField(max_length=30, choices=priority_type, default='low')
    status = models.CharField(max_length=30, choices=status_type, default='created')
    task_list = models.ForeignKey(TaskList, related_name='tasks', on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(CustomUser, related_name='assigned_user', on_delete=models.CASCADE, null=True)
    created_by = models.ForeignKey(CustomUser, related_name='created_user', on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Comment(models.Model):
    """
        Model to create Comment
    """
    comment = models.TextField()
    task = models.ForeignKey(Task, related_name='tasks', on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, related_name='users', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author.username} on {self.task.title}'
