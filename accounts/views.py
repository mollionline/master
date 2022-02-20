from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View
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
