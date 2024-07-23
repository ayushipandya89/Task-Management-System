from django.urls import path

from tasks.views import TaskListCreateView, TaskListRetrieveUpdateDeleteView, TaskCreateView, \
    TaskRetrieveUpdateDeleteView, CommentCreateView, TaskAssignView

urlpatterns = [
    path('task-lists/', TaskListCreateView.as_view(), name='task_list_create'),
    path('task-lists/<int:id>/', TaskListRetrieveUpdateDeleteView.as_view(), name='task_list_detail'),

    # Task URLs
    path('tasks/', TaskCreateView.as_view(), name='task_create'),
    path('tasks/<int:id>/', TaskRetrieveUpdateDeleteView.as_view(), name='task_detail'),
    path('tasks/<int:id>/assign/', TaskAssignView.as_view(), name='task-assign'),

    # Comment URLs
    path('comments/', CommentCreateView.as_view(), name='comment_create'),
    path('tasks/<int:task_id>/comments/', CommentCreateView.as_view(), name='comment-create'),
]
