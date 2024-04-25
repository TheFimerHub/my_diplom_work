from django.db import models


class Doctor(models.Model):
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Врач'
        verbose_name_plural = 'Врачи'


class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='services')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'
