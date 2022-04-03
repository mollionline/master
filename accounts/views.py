from django.contrib.auth import authenticate, login, logout, get_user_model, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, reverse

# Create your views here.
from django.views import View
from django.views.generic import DetailView, ListView, UpdateView

from accounts.forms import UserCreationForm, UserChangeForm, ProfileChangeForm, PasswordChangeForm, ProfileCreateForm


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
        profile_form = ProfileCreateForm()
        return render(request, 'registration/register.html',
                      context={'form': form,
                               'profile_form': profile_form})

    def post(self, request, *args, **kwargs):
        form = UserCreationForm(data=request.POST)
        profile_form = ProfileCreateForm(request.POST, request.FILES)
        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
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


class UserProfileUpdateView(UpdateView):
    model = get_user_model()
    form_class = UserChangeForm
    template_name = 'profile/user_profile_update.html'
    context_object_name = 'user_obj'

    def get_context_data(self, **kwargs):
        if 'profile_form' not in kwargs:
            kwargs['profile_form'] = self.get_profile_form()
        return super(UserProfileUpdateView, self).get_context_data(**kwargs)

    def get_profile_form(self):
        form_kwargs = {'instance': self.object.profile}
        if self.request.method == 'POST':
            form_kwargs['data'] = self.request.POST
            form_kwargs['files'] = self.request.FILES
        return ProfileChangeForm(**form_kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        profile_form = self.get_profile_form()
        if form.is_valid() and profile_form.is_valid():
            return self.form_valid(form, profile_form)
        else:
            return self.form_invalid(form, profile_form)

    def form_valid(self, form, profile_form):
        response = super().form_valid(form)
        profile_form.save()
        return response

    def form_invalid(self, form, profile_form):
        context = self.get_context_data(form=form, profile_form=profile_form)
        return self.render_to_response(context)

    def get_success_url(self):
        return reverse('profile', kwargs={'pk': self.object.pk})

    def get_object(self, queryset=None):
        return self.model.objects.get(id=self.request.user.id)


class ChangePasswordView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    template_name = 'registration/change_password.html'
    form_class = PasswordChangeForm
    context_object_name = 'user_obj'

    def form_valid(self, form):
        user = form.save()
        update_session_auth_hash(self.request, user)
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('profile', kwargs={'pk': self.object.pk})

    def get_object(self, queryset=None):
        return self.model.objects.get(id=self.request.user.id)
