from django.contrib import admin
from issue_tracker.models import Type, Status, Task


# Register your models here.
class TaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'summary', 'description', 'status', 'type', 'created_at', 'updated_at']
    list_filter = ['summary']
    search_fields = ['summary', 'status', 'type']
    fields = ['id', 'summary', 'description', 'status', 'type', 'created_at', 'updated_at']
    readonly_fields = ['id', 'created_at', 'updated_at']


class TypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'type']
    list_filter = ['type']
    search_fields = ['type']
    fields = ['type']


class StatusAdmin(admin.ModelAdmin):
    list_display = ['id', 'status']
    list_filter = ['status']
    search_fields = ['status']
    fields = ['status']


admin.site.register(Task, TaskAdmin)
admin.site.register(Type, TypeAdmin)
admin.site.register(Status, StatusAdmin)

