from django.urls import path
from api_v1.views import (ApiProjectListView, ApiTaskListView,
                          ApiProjectView,
                          ApiTaskView)

urlpatterns = [
    path('project/list', ApiProjectListView.as_view()),
    path('task/list', ApiTaskListView.as_view()),
    path('project/<int:pk>', ApiProjectView.as_view()),
    path('task/<int:pk>', ApiTaskView.as_view())
]
