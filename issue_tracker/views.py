from urllib.parse import urlencode

from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, FormView, UpdateView, DeleteView, ListView
from issue_tracker.models import Task
from issue_tracker.forms import TaskForm, SearchForm
from django.urls import reverse, reverse_lazy
from django.db.models import Q
from django.http import HttpResponseRedirect, Http404, HttpResponseNotFound


# Create your views here.
class TaskListView(ListView):
    template_name = 'list_task.html'
    model = Task
    ordering = ('-created_at',)
    paginate_by = 10
    context_object_name = 'tasks'

    def get_search_form(self):
        return SearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data.get('search')

    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TaskListView, self).get_context_data(
            **kwargs
        )
        context['form'] = self.form
        if self.search_value:
            context['query'] = urlencode({
                'search': self.search_value
            })
            print(context)
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.search_value:
            query = (Q(summary__icontains=self.search_value) |
                     Q(description__icontains=self.search_value))
            queryset = queryset.filter(query)
        return queryset


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


class DeleteTaskView(DeleteView):
    model = Task
    success_url = reverse_lazy('list_task')
