from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('message/', include('message.urls')),
    path('user/', include('user.urls')),
    path('', views.redirect_view, name='redirect_view'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
