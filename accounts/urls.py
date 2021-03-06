from django.urls import path
from accounts.views import (LoginView, LogoutView,
                            RegisterView, UserProfileView,
                            UsersListView, UserProfileUpdateView,
                            ChangePasswordView)

urlpatterns = []

accounts_urls = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/<int:pk>', UserProfileView.as_view(), name='profile'),
    path('profiles/', UsersListView.as_view(), name='profile_users'),
    path('profile/update', UserProfileUpdateView.as_view(), name='update_profile'),
    path('profile/change_password', ChangePasswordView.as_view(), name='change_password')
]

urlpatterns += accounts_urls
