from django.contrib import admin

from tasks.models import Comment, TaskList, Task

# Register your models here.
admin.site.register(TaskList)
admin.site.register(Task)
admin.site.register(Comment)
