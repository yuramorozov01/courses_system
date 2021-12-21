from django.contrib import admin
from task_app.models import TaskStatement, TaskStatementFile, Task, TaskFile

admin.site.register(TaskStatement)
admin.site.register(TaskStatementFile)
admin.site.register(Task)
admin.site.register(TaskFile)
