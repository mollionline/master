from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import TemplateView, FormView, UpdateView
from issue_tracker.models import Task, Type, Status
from issue_tracker.forms import TaskForm
from django.urls import reverse
from django.http import HttpResponseRedirect


# Create your views here.
class TaskListView(TemplateView):
    template_name = 'list_task.html'
    extra_context = {'title': 'Список задач'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = Task.objects.all().order_by('-created_at')
        return context


class DetailTaskView(TaskListView):
    template_name = 'detail_task.html'

    def get_context_data(self, **kwargs):
        kwargs['task'] = get_object_or_404(Task, pk=self.kwargs.get('pk'))
        return super().get_context_data(**kwargs)


class NewAddTaskView(FormView):
    template_name = 'new_task.html'
    form_class = TaskForm

    def form_valid(self, form):
        self.task = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('detail_task', kwargs={'pk': self.task.pk})


class EditTaskView(UpdateView):
    template_name = 'edit_task.html'
    form_class = TaskForm
    model = Task

    def get_success_url(self):
        return reverse('detail_task', kwargs={'pk': self.get_object().pk})


class DeleteTaskView(View):
    template_name = 'list_task'

    def post(self, request, *args, **kwargs):
        task = get_object_or_404(Task, pk=kwargs.get('pk'))
        task.delete()
        return redirect(self.template_name)
