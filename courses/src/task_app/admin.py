from django.contrib import admin
from task_app.models import Task, TaskFile, TaskStatement, TaskStatementFile
from simple_history.admin import SimpleHistoryAdmin

admin.site.register(TaskStatement, SimpleHistoryAdmin)
admin.site.register(TaskStatementFile, SimpleHistoryAdmin)
admin.site.register(Task, SimpleHistoryAdmin)
admin.site.register(TaskFile, SimpleHistoryAdmin)
