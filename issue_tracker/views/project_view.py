from django.urls import reverse
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView
from issue_tracker.models import Project
from issue_tracker.helpers import SearchView
from issue_tracker.forms import SearchForm, ProjectForm
from django.contrib.auth.mixins import LoginRequiredMixin


class ListProjectView(SearchView):
    template_name = 'project/list_project.html'
    model = Project
    ordering = ('-created_at',)
    paginate_by = 5
    context_object_name = 'projects'
    search_form = SearchForm
    search_fields = {
        'project': 'icontains'
    }
    extra_context = {
        'title': 'Сприсок проектов'
    }


class CreateProjectView(LoginRequiredMixin, CreateView):
    model = Project
    template_name = 'project/create_project.html'
    fields = ['project', 'description', 'created_at']
    success_url = ''

    def form_valid(self, form):
        self.project = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('detail_project', kwargs={'pk': self.project.pk})


class DeleteProjectView(LoginRequiredMixin, DeleteView):
    model = Project

    def get(self, request, *args, **kwargs):
        return self.delete(request=request)

    def get_success_url(self):
        return reverse('list_project')


class DetailProjectView(DetailView):
    context_object_name = 'project'
    model = Project
    template_name = 'project/detail_project.html'


class UpdateProjectView(LoginRequiredMixin, UpdateView):
    template_name = 'project/update_project.html'
    model = Project
    form_class = ProjectForm

    def get_success_url(self):
        return reverse('detail_project', kwargs={'pk': self.get_object().pk})
