from django.urls import path

from main.views import index, DoctorListView, ServiceListView, ServiceDetailView, ServiceUpdateView, ServiceDeleteView

app_name = 'main'

urlpatterns = [
    # URL для главной страницы
    path('', index, name='index'),

    # URL для списка врачей
    path('doctors/', DoctorListView.as_view(), name='doctor-list'),

    # URL для списка медицинских услуг
    path('services/', ServiceListView.as_view(), name='service-list'),

    path('services/<int:service_id>/', ServiceDetailView.as_view(), name='service-detail'),
    path('services/<int:pk>/update/', ServiceUpdateView.as_view(), name='service-update'),
    path('services/<int:pk>/delete/', ServiceDeleteView.as_view(), name='service-delete'),
]
