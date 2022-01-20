from django.urls import path
from issue_tracker.views import (TaskListView,
                                 DetailTaskView,
                                 NewAddTaskView,
                                 EditTaskView)

urlpatterns = [
    path('', TaskListView.as_view(), name='list_task'),
    path('tasks/<int:pk>/', DetailTaskView.as_view(), name='detail_task'),
    path('tasks/<int:pk>/edit/', EditTaskView.as_view(), name='edit_task'),
    path('tasks/add/', NewAddTaskView.as_view(), name='new_task')
]
