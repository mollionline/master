from django.urls import path
from issue_tracker.views import (TaskListView,
                                 DetailTaskView)

urlpatterns = [
    path('', TaskListView.as_view(), name='list_task'),
    path('tasks/<int:pk>/', DetailTaskView.as_view(), name='detail_task')
]
