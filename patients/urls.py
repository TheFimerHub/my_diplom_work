from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from django.views.generic import TemplateView

from patients.views import ProfileUpdateView, RegisterView, CustomPasswordResetView, CustomPasswordResetConfirmView, \
    CustomPasswordResetDoneView, CustomPasswordResetCompleteView, AppointmentFormView

app_name = 'patients'

urlpatterns = [
    path('', LoginView.as_view(template_name='login.html'), name='login'),
    path('appointment/', AppointmentFormView.as_view(), name='appointment'),
    # Добавлен URL для создания новых записей на прием

    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileUpdateView.as_view(), name='profile'),
    path('register/', RegisterView.as_view(), name='register'),
    path('password/reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('confirm_email/', TemplateView.as_view(template_name='users/confirm_email.html'), name='confirm_email'),
    path('invalid_verify/', TemplateView.as_view(template_name='users/invalid_verify.html'), name='invalid_verify'),
    path('password/reset/confirm/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('password/reset/done', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete')
]