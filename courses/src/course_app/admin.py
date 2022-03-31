from course_app.models import Course
from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

admin.site.register(Course, SimpleHistoryAdmin)
