from django.contrib.auth.models import AbstractUser
from django.db import models

from main.models import Doctor


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(verbose_name='почта', unique=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    phone = models.CharField(max_length=15, verbose_name='телефон')
    country = models.CharField(max_length=100, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Appointment(models.Model):
    patient = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return f"{self.patient} - {self.doctor} - {self.date} {self.time}"

    class Meta:
        verbose_name = 'Прием'
        verbose_name_plural = 'Приемы'

# Create your models here.
