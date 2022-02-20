from django.urls import path
from accounts.views import LoginView, LogoutView, RegisterView

urlpatterns = []
accounts_urls = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register')
]

urlpatterns += accounts_urls
