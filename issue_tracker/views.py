from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import TemplateView
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


class NewAddTaskView(TemplateView):
    template_name = 'new_task.html'

    def get_context_data(self, **kwargs):
        context = super(NewAddTaskView, self).get_context_data(**kwargs)
        context['statuses'] = Status.objects.all()
        context['types'] = Type.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        form = TaskForm(data=request.POST)
        if form.is_valid():
            task, is_not_new = Task.objects.get_or_create(
                summary=form.cleaned_data.get('summary'),
                description=form.cleaned_data.get('description'),
                status=form.cleaned_data.get('status'),
                type=form.cleaned_data.get('type')
            )
            url = reverse('detail_task', kwargs={'pk': task.pk})
            return HttpResponseRedirect(url)
        return render(request, self.template_name, context={'errors': form.errors,
                                                            'form': form,
                                                            'statuses': Status.objects.all(),
                                                            'types': Type.objects.all()})


class EditTaskView(TemplateView):
    template_name = 'edit_task.html'

    def get(self, request, *args, **kwargs):
        task = get_object_or_404(Task, pk=self.kwargs.get('pk'))
        form = TaskForm(initial={
            'summary': task.summary,
            'description': task.description,
            'status': task.status,
            'type': task.type
        })
        return render(request, self.template_name, context={
            'task': task,
            'form': form,
            'statuses': Status.objects.all(),
            'types': Type.objects.all()
        })

    def post(self, request, *args, **kwargs):
        task = get_object_or_404(Task, pk=self.kwargs.get('pk'))
        form = TaskForm(data=request.POST)
        if form.is_valid():
            task.summary = form.cleaned_data['summary']
            task.description = form.cleaned_data['description']
            task.status = form.cleaned_data['status']
            task.type = form.cleaned_data['type']
            task.save(update_fields=['summary', 'description', 'status', 'type', 'updated_at'])
            return redirect('detail_task', pk=task.pk)
        return render(request, 'edit_task.html', context={
            'task': task,
            'form': form,
            'errors': form.errors,
            'statuses': Status.objects.all(),
            'types': Type.objects.all()
        })


class DeleteTaskView(View):
    template_name = 'list_task'

    def post(self, request, *args, **kwargs):
        task = get_object_or_404(Task, pk=kwargs.get('pk'))
        task.delete()
        return redirect(self.template_name)
