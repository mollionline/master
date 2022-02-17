from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import UpdateView, DeleteView, CreateView
from issue_tracker.models import Task, Project
from issue_tracker.forms import TaskForm, SearchForm
from django.urls import reverse, reverse_lazy
from issue_tracker.helpers import SearchView
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
class TaskListView(SearchView):
    template_name = 'task/list_task.html'
    model = Task
    ordering = ('-created_at',)
    paginate_by = 10
    context_object_name = 'tasks'
    search_form = SearchForm
    search_fields = {
        'summary': 'icontains',
        'description': 'startswith'
    }
    extra_context = {
        'title': 'Список задач'
    }


class DetailTaskView(TaskListView):
    template_name = 'task/detail_task.html'

    def get_context_data(self, **kwargs):
        kwargs['task'] = get_object_or_404(Task, pk=self.kwargs.get('pk'))
        return super().get_context_data(**kwargs)


class NewAddTaskView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'project/detail_project.html'

    def get_success_url(self):
        return reverse('detail_project', kwargs={'pk': self.kwargs.get('pk')})

    def post(self, request, *args, **kwargs):
        project = get_object_or_404(Project, pk=kwargs.get('pk'))
        form = self.form_class(data=request.POST)
        if form.is_valid():
            type = form.cleaned_data.get('type')
            task, is_not_new = Task.objects.get_or_create(
                summary=form.cleaned_data.get('summary'),
                description=form.cleaned_data.get('description'),
                status=form.cleaned_data.get('status'),
                project=project
            )
            task.type.set(type)
            return redirect(self.get_success_url())
        return render(request, self.template_name, context={
            'project': project,
            'form': form
        })

    def get(self, request, *args, **kwargs):
        project = get_object_or_404(Project, pk=kwargs.get('pk'))
        form = self.form_class()
        return render(request, self.template_name, context={
            'project': project,
            'form': form
        })


class EditTaskView(LoginRequiredMixin, UpdateView):
    template_name = 'task/edit_task.html'
    form_class = TaskForm
    model = Task

    def get_success_url(self):
        return reverse('detail_project', kwargs={'pk': self.object.project.pk})


class DeleteTaskView(LoginRequiredMixin, DeleteView):
    model = Task

    def get(self, request, *args, **kwargs):
        return self.delete()

    def get_success_url(self):
        return reverse('detail_project', kwargs={'pk': self.object.project.pk})
