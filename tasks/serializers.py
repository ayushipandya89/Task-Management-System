from datetime import datetime

from rest_framework import serializers

from tasks.models import TaskList, Task, Comment


class TaskListSerializer(serializers.ModelSerializer):
    """
    Serializer for task lists.
    """

    class Meta:
        model = TaskList
        fields = ['id', 'name', 'is_public', 'owner']
        read_only_fields = ['owner']

    def to_representation(self, instance):
        """
        method to represent the owner's username
        """
        representation = super().to_representation(instance)
        representation['owner'] = instance.owner.username
        return representation


class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for tasks.
    """

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'created_date', 'due_date', 'priority', 'status', 'task_list',
                  'assigned_to', 'created_by']
        read_only_fields = ['created_date', 'created_by']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['assigned_to'] = instance.assigned_to.username if instance.assigned_to else None
        representation['created_by'] = instance.created_by.username if instance.created_by else None
        representation['task_list'] = instance.task_list.name if instance.task_list else None
        return representation

    def validate_due_date(self, value):
        """
        Check that the due date is not less than or equal to the created date.
        """
        my_value = value.strftime('%Y-%m-%d %I:%M:%S')
        now = datetime.now()
        formatted_time = now.strftime('%Y-%m-%d %I:%M:%S')
        if my_value <= formatted_time:
            raise serializers.ValidationError("Due date must be greater than the current date and time.")
        return value


class TaskAssignmentSerializer(serializers.ModelSerializer):
    """
    Serializer for assigning a task to a user.
    """

    class Meta:
        model = Task
        fields = ['assigned_to']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['assigned_to'] = instance.assigned_to.username
        representation['title'] = instance.title
        return representation


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for comments.
    """
    author = serializers.ReadOnlyField(source='author.username')
    read_only_fields = ['created_at', 'task', 'author']

    class Meta:
        model = Comment
        fields = ['id', 'comment', 'task', 'author', 'created_at']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['task'] = instance.task.title
        return representation
