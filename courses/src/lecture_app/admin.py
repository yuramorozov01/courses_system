from django.contrib import admin
from lecture_app.models import Lecture, LectureFile
from simple_history.admin import SimpleHistoryAdmin

admin.site.register(Lecture, SimpleHistoryAdmin)
admin.site.register(LectureFile, SimpleHistoryAdmin)
