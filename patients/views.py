from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetView, PasswordResetDoneView, \
    PasswordResetCompleteView
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_decode
from django.views import generic, View
from django.views.generic import FormView
from django import forms

from config import settings
from main.models import Doctor
from patients.forms import UserForm, UserRegisterForm, CustomPasswordResetForm, PasswordResetConfirmForm, \
    AppointmentForm
from patients.models import Appointment


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor', 'date',
                  'time']  # Уберем 'patient', так как он будет автоматически установлен в представлении
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }


class AppointmentFormView(FormView):
    def get(self, request):
        form = AppointmentForm()  # Уберем передачу request здесь
        doctors = Doctor.objects.all()
        return render(request, 'appointment_form.html', {'form': form, 'doctors': doctors})

    def post(self, request):
        form = AppointmentForm(request.POST)  # Уберем передачу request здесь
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user
            appointment.save()
            return redirect('main:index')
        doctors = Doctor.objects.all()
        return render(request, 'appointment_form.html', {'form': form, 'doctors': doctors})


# class AppointmentView(View):
#     def get(self, request):
#         appointments = Appointment.objects.filter(patient=request.user)
#         form = AppointmentForm()
#         return render(request, 'appointment.html', {'form': form, 'appointments': appointments})
#
#     def post(self, request):
#         form = AppointmentForm(request.POST)
#         if form.is_valid():
#             appointment = form.save(commit=False)
#             appointment.patient = request.user
#             appointment.save()
#             return redirect('patients:appointments')  # Перенаправляем на страницу с записями на прием
#         appointments = Appointment.objects.filter(patient=request.user)
#         return render(request, 'appointment.html', {'form': form, 'appointments': appointments})


class ProfileUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = User
    form_class = UserForm
    success_url = reverse_lazy('patients:profile')
    template_name = 'user_form.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['appointments'] = Appointment.objects.filter(patient=self.request.user)
        return context


class RegisterView(generic.CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('patients:login')
    template_name = 'user_form.html'

    # def form_valid(self, form):
    #     response = super().form_valid(form)
    #     user = form.save()
    #     send_mail_for_verify(self.request, user)
    #     return response


class EmailVerify(generic.View):
    template_name = 'verify_email.html'

    def get(self, request, uidb64, token):
        user = self.get_user(uidb64)

        if user is not None and default_token_generator.check_token(user, token):
            user.email_verify = True
            user.save()
            login(request, user)
            return redirect('patients:login')
        return redirect('users:invalid_verify')

    @staticmethod
    def get_user(uidb64):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist, ValidationError):
            user = None
        return user


class CustomPasswordResetView(PasswordResetView):
    template_name = 'password_reset_form.html'
    form_class = CustomPasswordResetForm
    success_url = reverse_lazy('patients:password_reset_done')
    email_template_name = 'email_reset.html'
    from_email = settings.EMAIL_HOST_USER


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = PasswordResetConfirmForm
    template_name = 'password_reset_confirm.html'
    success_url = reverse_lazy('patients:password_reset_complete')


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'password_reset_done.html'

    def form_valid(self, form):
        if form.is_valid():
            self.object = form.save()
            if form.data.get('need_generate', False):
                self.object.set_passeword(
                    self.object.make_random_password(12)
                )
                self.object.save()

        return super().form_valid(form)


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'blog/blog_list.html'
