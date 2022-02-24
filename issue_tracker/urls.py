from django.urls import path
from issue_tracker.views.task_view import (TaskListView,
                                           DetailTaskView,
                                           NewAddTaskView,
                                           EditTaskView,
                                           DeleteTaskView)

from issue_tracker.views.project_view import (ListProjectView,
                                              CreateProjectView,
                                              DeleteProjectView,
                                              DetailProjectView,
                                              UpdateProjectView,
                                              AddUsersToProject)

urlpatterns = []

project_urls = [
    path('projects/add/', CreateProjectView.as_view(), name='create_project'),
    path('projects/<int:pk>/delete', DeleteProjectView.as_view(), name='delete_project'),
    path('projects/<int:pk>/edit', UpdateProjectView.as_view(), name='update_project'),
    path('projects/<int:pk>/', DetailProjectView.as_view(), name='detail_project'),
    path('projects/<int:pk>/add_user', AddUsersToProject.as_view(), name='add_users_to_project'),
    path('', ListProjectView.as_view(), name='list_project')
]

task_urls = [
    path('tasks/', TaskListView.as_view(), name='list_task'),
    path('tasks/<int:pk>/', DetailTaskView.as_view(), name='detail_task'),
    path('tasks/<int:pk>/edit/', EditTaskView.as_view(), name='edit_task'),
    path('tasks/<int:pk>/delete/', DeleteTaskView.as_view(), name='delete_task'),
    path('projects/<int:pk>/', NewAddTaskView.as_view(), name='new_task')
]

urlpatterns += task_urls
urlpatterns += project_urls
