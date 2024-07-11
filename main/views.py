from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, DeleteView

from main.forms import ServiceForm
from main.models import Doctor, Service


def index(request):
    return render(request, 'index.html')


class DoctorListView(ListView):
    model = Doctor
    template_name = 'doctor_list.html'
    context_object_name = 'doctors'


class ServiceListView(ListView):
    model = Service
    template_name = 'service_list.html'
    context_object_name = 'services'


class ServiceDetailView(DetailView):
    model = Service
    template_name = 'service_detail.html'
    context_object_name = 'service'
    pk_url_kwarg = 'service_id'


class ServiceUpdateView(UpdateView):
    model = Service
    form_class = ServiceForm
    template_name = 'service_update.html'
    success_url = reverse_lazy('main:service-list')


class ServiceDeleteView(DeleteView):
    model = Service
    template_name = 'service_delete.html'
    success_url = reverse_lazy('main:service-list')
