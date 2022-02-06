from django.urls import path
from issue_tracker.views.task_view import (TaskListView,
                                           DetailTaskView,
                                           NewAddTaskView,
                                           EditTaskView,
                                           DeleteTaskView)

urlpatterns = []

task_urls = [
    path('', TaskListView.as_view(), name='list_task'),
    path('tasks/<int:pk>/', DetailTaskView.as_view(), name='detail_task'),
    path('tasks/<int:pk>/edit/', EditTaskView.as_view(), name='edit_task'),
    path('tasks/<int:pk>/delete/', DeleteTaskView.as_view(), name='delete_task'),
    path('tasks/add/', NewAddTaskView.as_view(), name='new_task')
]

urlpatterns += task_urls
