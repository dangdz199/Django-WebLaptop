from django.contrib import admin
from django.urls import path
from products.views import laptop_list, laptop_detail

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', laptop_list, name='laptop_list'),  # Home page
    path('laptops/', laptop_list, name='laptop_list'),  # URL for laptop listing
    path('laptops/<int:pk>/', laptop_detail, name='laptop_detail'),  # URL for laptop detail
]
#cmn
# Serve media files in development mode
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
