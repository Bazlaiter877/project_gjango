from django.urls import path
from accounts.views import RegisterView, CustomLoginView, PasswordResetView, profile_view
from django.contrib.auth.views import LogoutView, PasswordResetConfirmView, PasswordResetCompleteView

app_name = 'accounts'

urlpatterns = [
    path('profile/', profile_view, name='profile'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
]
