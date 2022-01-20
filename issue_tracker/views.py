from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, RedirectView
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
