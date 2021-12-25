from django.contrib import admin
from task_app.models import Task, TaskFile, TaskStatement, TaskStatementFile

admin.site.register(TaskStatement)
admin.site.register(TaskStatementFile)
admin.site.register(Task)
admin.site.register(TaskFile)
