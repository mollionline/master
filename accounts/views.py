from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View
from django.views.generic import DetailView, ListView

from accounts.forms import UserCreationForm


class LoginView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'registration/login.html', context={
            'next': request.GET.get('next')
        })

    def post(self, request, *args, **kwargs):
        context = {}
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            next_page = request.GET.get('next')
            if user is not None:
                login(request, user)
                if next_page is not None:
                    return redirect(next_page)
                return redirect('/')
            else:
                context['has_error'] = True
        return render(request, 'registration/login.html', context=context)


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('/')


class RegisterView(View):
    def get(self, request, *args, **kwargs):
        form = UserCreationForm()
        return render(request, 'registration/register.html', context={'form': form})

    def post(self, request, *args, **kwargs):
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
        return render(request, 'registration/register.html', context={'form': form})


class UserProfileView(LoginRequiredMixin, DetailView):
    model = get_user_model()
    template_name = 'profile/profile.html'
    context_object_name = 'user_obj'
    paginate_related_by = 5
    paginate_related_orphans = 0

    def get_context_data(self, **kwargs):
        projects = self.object.projects.order_by('-created_at')
        paginator = Paginator(
            projects, self.paginate_related_by, self.paginate_related_orphans
        )
        page_number = self.request.GET.get('page', 1)
        page = paginator.get_page(page_number)
        kwargs['page_obj'] = page
        kwargs['projects'] = page.object_list
        kwargs['is_paginated'] = page.has_other_pages()
        return super().get_context_data(**kwargs)


class UsersListView(PermissionRequiredMixin, ListView):
    model = get_user_model()
    template_name = 'profile/user_list.html'
    context_object_name = 'users'
    paginate_related_by = 5
    paginate_related_orphans = 0
    permission_required = 'issue_tracker.view_user'

    def has_permission(self):
        return super().has_permission() or self.request.user.groups.all()[0].name == 'Project Manager' or \
               self.request.user.groups.all()[0].name == 'Team Lead'
