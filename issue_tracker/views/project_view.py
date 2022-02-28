from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView
from issue_tracker.models import Project
from issue_tracker.helpers import SearchView
from issue_tracker.forms import SearchForm, ProjectForm
from django.contrib.auth.mixins import PermissionRequiredMixin


class ListProjectView(PermissionRequiredMixin, SearchView):
    template_name = 'project/list_project.html'
    model = Project
    ordering = ('-created_at',)
    paginate_by = 5
    paginate_orphans = 1
    context_object_name = 'projects'
    search_form = SearchForm
    search_fields = {
        'project': 'icontains'
    }
    extra_context = {
        'title': 'Сприсок проектов'
    }
    permission_required = 'issue_tracker.view_project'

    def has_permission(self):
        for project in Project.objects.all():
            if super().has_permission() and self.request.user in project.user.all() or str(
                    self.request.user) == 'admin':
                return True


class CreateProjectView(PermissionRequiredMixin, CreateView):
    model = Project
    template_name = 'project/create_project.html'
    form_class = ProjectForm
    permission_required = 'issue_tracker.add_project'

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            user = request.user
            project = Project.objects.create(
                project=form.cleaned_data.get('project'),
                description=form.cleaned_data.get('description'),
                created_at=form.cleaned_data.get('created_at'),
                updated_at=form.cleaned_data.get('updated_at')
            )
            project.user.add(user)
            url = reverse('detail_project', kwargs={'pk': project.pk})
            return HttpResponseRedirect(url)
        return render(request, self.template_name, context={
            'form': form
        })


class DeleteProjectView(PermissionRequiredMixin, DeleteView):
    model = Project
    permission_required = 'issue_tracker.delete_project'

    def get(self, request, *args, **kwargs):
        return self.delete(request=request)

    def get_success_url(self):
        return reverse('list_project')

    def has_permission(self):
        return super().has_permission() and self.request.user in self.get_object().user.all() or str(
            self.request.user) == 'admin' or str(
            self.request.user) == 'manager'


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
        if super().has_permission() or str(self.request.user) == 'admin' or \
                self.request.user.groups.all()[0].name == 'Project Manager':
            return True
        return False


class AddUsersToProject(PermissionRequiredMixin, UpdateView):
    model = Project
    template_name = 'project/add_users_to_project.html'
    fields = ['user']
    permission_required = 'auth.change_user'

    def get_success_url(self):
        return reverse('detail_project', kwargs={'pk': self.get_object().pk})

    def has_permission(self):
        return super().has_permission() and self.request.user in self.get_object().user.all() or str(
            self.request.user) == 'admin'
