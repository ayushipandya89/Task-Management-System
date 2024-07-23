from django.db.models import Q
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAdminUser

from tasks.constants import TASK_LIST_CREATED, TASK_LIST_UPDATED, TASK_LIST_DELETED, TASK_CREATED, TASK_DELETED, \
    TASK_UPDATED, TASK_ASSIGNED, COMMENT_ADDED
from tasks.models import Task, TaskList, Comment
from tasks.permissions import IsAuthorizedForTaskList, IsAuthorizedForTask, IsOwnerOrAdminForTaskList, \
    IsOwnerOrAdminForTask
from tasks.serializers import TaskSerializer, TaskListSerializer, CommentSerializer, TaskAssignmentSerializer
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend


# Create your views here.
class TaskListCreateView(generics.ListCreateAPIView):
    """
    View to create a new task list and retrieve existing task lists.
    The logged-in user is automatically set as the owner of the task list.
    """
    queryset = TaskList.objects.all()
    serializer_class = TaskListSerializer
    permission_classes = [IsAuthenticated, IsAuthorizedForTaskList]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['name', 'owner__username']
    filterset_fields = ['is_public']
    ordering_fields = ['id', 'name', 'owner__username', 'is_public', '-id', '-name', '-owner__username', 'is_public']

    def get_queryset(self):
        """
        Restrict the returned task lists to the current user's task lists.
        Apply search and filtering based on query parameters.
        """
        if self.request.user.is_admin:
            queryset = TaskList.objects.all()
        else:
            queryset = TaskList.objects.filter(owner=self.request.user)
        queryset = self.filter_queryset(queryset)
        return queryset

    def post(self, request, *args, **kwargs):
        """
        Handle POST request to create a new task list.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['owner'] = request.user
        self.perform_create(serializer)
        return Response({"message": TASK_LIST_CREATED, 'data': serializer.data}, status=status.HTTP_201_CREATED)


class TaskListRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """
    View to retrieve, update, or delete a task list.
    Only the owner of the task list or an admin can perform these actions.
    """
    queryset = TaskList.objects.all()
    serializer_class = TaskListSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdminForTaskList, IsAuthorizedForTaskList]
    lookup_field = 'id'

    def put(self, request, *args, **kwargs):
        """
        put request to update a task list
        Only the `name` and `is_public` fields are allowed to be updated.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": TASK_LIST_UPDATED, "data": serializer.data}, status=status.HTTP_200_OK)

    def perform_destroy(self, instance):
        """
        Handle the deletion of a task list.
        """
        self.check_object_permissions(self.request, instance)
        instance.delete()
        return Response({"message": TASK_LIST_DELETED}, status=status.HTTP_204_NO_CONTENT)


class TaskCreateView(generics.ListCreateAPIView):
    """
    View to create a new task and retrieve existing tasks.
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsAuthorizedForTask]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['title', 'assigned_to__username', 'created_by__username']
    filterset_fields = ['status', 'priority', 'due_date']
    ordering_fields = ['id', 'title', 'due_date', 'priority', 'status', '-id', '-title', '-due_date', '-priority',
                       '-status']

    def get_queryset(self):
        """
        Restrict the returned tasks to the current user's tasks.
        Apply search and filtering based on query parameters.
        """
        if self.request.user.is_admin:
            queryset = Task.objects.all()
        else:
            queryset = Task.objects.filter(Q(created_by=self.request.user) | Q(assigned_to=self.request.user))
        queryset = self.filter_queryset(queryset)
        return queryset

    def post(self, request, *args, **kwargs):
        """
        Handle POST request to create a new task.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=self.request.user)
        return Response({"message": TASK_CREATED, 'data': serializer.data}, status=status.HTTP_201_CREATED)


class TaskRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """
    View to retrieve, update, or delete a task.
    Only the owner of the task or an admin can perform these actions.
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdminForTask]
    lookup_field = 'id'

    def put(self, request, *args, **kwargs):
        """
        PUT request to update a task.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": TASK_UPDATED, "data": serializer.data}, status=status.HTTP_200_OK)

    def perform_destroy(self, instance):
        """
        Handle the deletion of a task.
        """
        self.check_object_permissions(self.request, instance)
        instance.delete()
        return Response({"message": TASK_DELETED}, status=status.HTTP_204_NO_CONTENT)


class TaskAssignView(generics.UpdateAPIView):
    """
    View to assign a task to a user. Only accessible by admins.
    """
    queryset = Task.objects.all()
    serializer_class = TaskAssignmentSerializer
    permission_classes = [IsAdminUser]
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        """
        Handle PUT request to assign a task to a user.
        """
        partial = True
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": TASK_ASSIGNED, "data": serializer.data}, status=status.HTTP_200_OK)


class CommentCreateView(generics.ListCreateAPIView):
    """
    View to create a new comment and retrieve existing comments.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Restrict the returned comments to the current task.
        """
        task_id = self.kwargs.get('task_id')
        return Comment.objects.filter(task_id=task_id)

    def post(self, request, *args, **kwargs):
        """
        Handle POST request to create a new comment for a specific task.
        """
        task_id = self.kwargs.get('task_id')
        data = request.data.copy()
        data['task'] = task_id

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response({"message": COMMENT_ADDED, "data": serializer.data}, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        """
        Automatically set the logged-in user as the author of the comment.
        """
        serializer.save(author=self.request.user)
