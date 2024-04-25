from django.contrib.auth.forms import UserChangeForm, UserCreationForm, SetPasswordForm, PasswordResetForm
from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from patients.models import CustomUser, Appointment

User = get_user_model()


class FormStyleMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class UserForm(FormStyleMixin, UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'avatar', 'phone', 'country')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.HiddenInput()


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'password1', 'password2')


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label=_("Email"),
        max_length=50,
        widget=forms.EmailInput(attrs={"autocomplete": "email"}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = CustomUser


class PasswordResetConfirmForm(SetPasswordForm):
    class Meta:
        model = CustomUser


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['patient', 'doctor', 'date', 'time']  # Поля, которые должны отображаться в форме
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),  # Используем виджет для выбора даты
            'time': forms.TimeInput(attrs={'type': 'time'})  # Используем виджет для выбора времени
        }
