from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from accounts.views import logout_view, login_view

urlpatterns = []
accounts_urls = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout')
]

urlpatterns += accounts_urls
