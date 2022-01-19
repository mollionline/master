from django.urls import path
from issue_tracker.views import (TaskListView)


urlpatterns = [
    path('', TaskListView.as_view(), name='list_task')
]