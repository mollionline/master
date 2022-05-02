from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import UpdateView, DeleteView, CreateView
from issue_tracker.models import Task, Project
from issue_tracker.forms import TaskForm, SearchForm
from django.urls import reverse
from issue_tracker.helpers import SearchView
from django.contrib.auth.mixins import PermissionRequiredMixin


# Create your views here.
class TaskListView(PermissionRequiredMixin, SearchView):
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
    permission_required = 'issue_tracker.view_task'

    def has_permission(self):
        for task in Task.objects.all():
            project = get_object_or_404(Project, pk=task.project_id)
            if super().has_permission() and self.request.user in project.user.all() \
                    or self.request.user.is_staff:
                return True


class DetailTaskView(TaskListView):
    template_name = 'task/detail_task.html'

    def get_context_data(self, **kwargs):
        kwargs['task'] = get_object_or_404(Task, pk=self.kwargs.get('pk'))
        return super().get_context_data(**kwargs)


class NewAddTaskView(PermissionRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'project/detail_project.html'
    permission_required = 'issue_tracker.add_task'

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

    def has_permission(self):
        project = get_object_or_404(Project, pk=self.kwargs.get('pk'))
        return super().has_permission() and self.request.user \
            in project.user.all() or self.request.user.is_staff


class EditTaskView(PermissionRequiredMixin, UpdateView):
    template_name = 'task/edit_task.html'
    form_class = TaskForm
    model = Task
    permission_required = 'issue_tracker.change_task'

    def get_success_url(self):
        return reverse('detail_project', kwargs={'pk': self.object.project.pk})

    def has_permission(self):
        task = get_object_or_404(Task, pk=self.kwargs.get('pk'))
        project = get_object_or_404(Project, pk=task.project_id)
        return super().has_permission() and self.request.user \
            in project.user.all() or self.request.user.is_staff


class DeleteTaskView(PermissionRequiredMixin, DeleteView):
    model = Task
    permission_required = 'issue_tracker.delete_task'

    def get(self, request, *args, **kwargs):
        return self.delete(request=request)

    def get_success_url(self):
        return reverse('detail_project', kwargs={'pk': self.object.project.pk})

    def has_permission(self):
        task = get_object_or_404(Task, pk=self.kwargs.get('pk'))
        project = get_object_or_404(Project, pk=task.project_id)
        return super().has_permission() and self.request.user \
            in project.user.all() or self.request.user.is_staff
