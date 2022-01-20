from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, RedirectView
from issue_tracker.models import Task, Type, Status


# Create your views here.
class TaskListView(TemplateView):
    template_name = 'list_task.html'
    extra_context = {'title': 'Список задач'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = Task.objects.all()
        return context


class DetailTaskView(TaskListView):
    template_name = 'detail_task.html'

    def get_context_data(self, **kwargs):
        kwargs['task'] = get_object_or_404(Task, pk=self.kwargs.get('pk'))
        return super().get_context_data(**kwargs)
