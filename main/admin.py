from django.contrib import admin

from main.models import Doctor, Service


class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialization')
    search_fields = ('name', 'specialization')


admin.site.register(Doctor, DoctorAdmin)


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'doctor', 'description')
    search_fields = ('name', 'doctor__name')
    list_filter = ('doctor',)


admin.site.register(Service, ServiceAdmin)
