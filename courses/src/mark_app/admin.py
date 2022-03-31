from django.contrib import admin
from mark_app.models import Mark, Message
from simple_history.admin import SimpleHistoryAdmin

admin.site.register(Mark, SimpleHistoryAdmin)
admin.site.register(Message, SimpleHistoryAdmin)
