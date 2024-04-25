from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from config import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', include('main.urls', namespace='mailing')),
    path('', include('main.urls'), ),   # Убрать namespace='patients'
    path('patients', include('patients.urls'), ),   # Убрать namespace='patients'
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)