from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
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


class CreateProjectView(CreateView):
    model = Project
    template_name = 'project/create_project.html'
    fields = ['project', 'description', 'created_at']
    success_url = ''

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.project = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('detail_project', kwargs={'pk': self.project.pk})


class DeleteProjectView(DeleteView):
    model = Project
    success_url = reverse_lazy('list_project')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)


class DetailProjectView(DetailView):
    context_object_name = 'project'
    model = Project
    template_name = 'project/detail_project.html'


class UpdateProjectView(UpdateView):
    template_name = 'project/update_project.html'
    model = Project
    form_class = ProjectForm

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('detail_project', kwargs={'pk': self.get_object().pk})
