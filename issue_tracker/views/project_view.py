from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView
from issue_tracker.models import Project
from issue_tracker.helpers import SearchView
from issue_tracker.forms import SearchForm, ProjectForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


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


class CreateProjectView(PermissionRequiredMixin, CreateView):
    model = Project
    template_name = 'project/create_project.html'
    permission_required = 'issue_tracker.add_project'
    fields = ['project', 'description', 'created_at', 'updated_at']
    success_url = ''

    def form_valid(self, form):
        self.project = form.save()
        print(form)
        return super(CreateProjectView, self).form_valid(form)

    def get_success_url(self):
        return reverse('detail_project', kwargs={'pk': self.project.pk})


class DeleteProjectView(PermissionRequiredMixin, DeleteView):
    model = Project
    permission_required = 'issue_tracker.delete_project'

    def get(self, request, *args, **kwargs):
        return self.delete(request=request)

    def get_success_url(self):
        return reverse('list_project')


class DetailProjectView(DetailView):
    context_object_name = 'project'
    model = Project
    template_name = 'project/detail_project.html'


class UpdateProjectView(PermissionRequiredMixin, UpdateView):
    template_name = 'project/update_project.html'
    model = Project
    form_class = ProjectForm
    permission_required = 'issue_tracker.change_project'

    def get_success_url(self):
        return reverse('detail_project', kwargs={'pk': self.get_object().pk})

    def has_permission(self):
        if self.request.user.groups.all()[0].name == 'Team Lead':
            return False
        elif super().has_permission() and self.request.user in self.get_object().user.all() or str(
                self.request.user) == 'admin':
            return True
        return False


class AddUsersToProject(PermissionRequiredMixin, UpdateView):
    model = Project
    template_name = 'project/add_users_to_project.html'
    fields = ['user']
    permission_required = 'issue_tracker.change_project'

    def get_success_url(self):
        return reverse('detail_project', kwargs={'pk': self.get_object().pk})

    def has_permission(self):
        return super().has_permission() and self.request.user in self.get_object().user.all() or str(
            self.request.user) == 'admin'

